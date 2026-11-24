#!/usr/bin/env python3
"""Generate the team activity card (dark + light SVG) from the GitHub GraphQL API.

Counts every author's commits on the default branch of every non-fork repository
the account owns, over the last 12 months. Only aggregates are rendered: no
repository names, commit messages or author identities leave this script, so
the card is safe for NDA-covered client work.

Stdlib only, so the workflow needs no install step.

Env:
  GH_TOKEN   token owned by GH_LOGIN that can read its private repositories
             (the PROFILE_TOKEN secret). The default Actions GITHUB_TOKEN only
             sees public repos, which would undercount badly, so it is refused.
  GH_LOGIN   account whose repositories are measured (default: Satyajit-Codys)
  OUT_DIR    where to write the SVGs (default: dist)
"""

import html
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone

LOGIN = os.environ.get("GH_LOGIN", "Satyajit-Codys")
TOKEN = os.environ.get("GH_TOKEN")
OUT_DIR = os.environ.get("OUT_DIR", "dist")

NOW = datetime.now(timezone.utc)
SINCE = NOW - timedelta(days=365)
SINCE_ISO = SINCE.strftime("%Y-%m-%dT%H:%M:%SZ")

# Markup/styling languages inflate byte counts without saying much about the work.
SKIP_LANGS = {"HTML", "CSS", "SCSS", "Less", "Sass", "Jupyter Notebook"}

REPOS_QUERY = """
query($login: String!, $cursor: String, $since: GitTimestamp!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, first: 50, after: $cursor) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        id
        isPrivate
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
        defaultBranchRef { target { ... on Commit { history(since: $since) { totalCount } } } }
      }
    }
  }
}
"""

HISTORY_QUERY = """
query($id: ID!, $cursor: String, $since: GitTimestamp!) {
  node(id: $id) {
    ... on Repository {
      defaultBranchRef { target { ... on Commit {
        history(since: $since, first: 100, after: $cursor) {
          pageInfo { hasNextPage endCursor }
          nodes { committedDate author { email user { login } } }
        }
      } } }
    }
  }
}
"""

THEMES = {
    "dark": {
        "bg": "#0D1117", "border": "#30363D", "title": "#E6EDF3",
        "label": "#8B949E", "value": "#E6EDF3", "accent": "#2F81F7", "track": "#21262D",
    },
    "light": {
        "bg": "#FFFFFF", "border": "#D0D7DE", "title": "#1F2328",
        "label": "#656D76", "value": "#1F2328", "accent": "#0969DA", "track": "#EAEEF2",
    },
}

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def gql(query, variables, attempts=4):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.load(resp)
            if body.get("errors"):
                sys.exit(f"GraphQL error: {body['errors']}")
            return body["data"]
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == attempts - 1:
                raise
        time.sleep(2 ** i)


def list_repos():
    cursor, repos, total = None, [], 0
    while True:
        page = gql(REPOS_QUERY, {"login": LOGIN, "cursor": cursor, "since": SINCE_ISO})["user"]["repositories"]
        total = page["totalCount"]
        repos.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            return repos, total
        cursor = page["pageInfo"]["endCursor"]


def commits_for(repo_id):
    cursor = None
    while True:
        node = gql(HISTORY_QUERY, {"id": repo_id, "cursor": cursor, "since": SINCE_ISO})["node"]
        hist = node["defaultBranchRef"]["target"]["history"]
        yield from hist["nodes"]
        if not hist["pageInfo"]["hasNextPage"]:
            return
        cursor = hist["pageInfo"]["endCursor"]


def count_people(pairs):
    """Distinct humans from (login, email) pairs, merging an email into a login
    whenever both appear on the same commit, and dropping bots."""
    email_to_login, people = {}, set()
    for login, email in pairs:
        if login and email:
            email_to_login[email] = login
    for login, email in pairs:
        who = login or email_to_login.get(email) or email
        if not who or who.endswith("[bot]") or "[bot]@" in who:
            continue
        people.add(who)
    return len(people)


def history_count(repo):
    ref = repo.get("defaultBranchRef") or {}
    return ((ref.get("target") or {}).get("history") or {}).get("totalCount", 0)


def collect():
    repos, total_repos = list_repos()
    if not any(r["isPrivate"] for r in repos):
        sys.exit(
            "No private repositories visible. Set the PROFILE_TOKEN secret to a token owned by "
            f"{LOGIN} with read access to its private repos; public-only numbers would undercount."
        )

    langs = {}
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name in SKIP_LANGS:
                continue
            entry = langs.setdefault(name, {"size": 0, "color": edge["node"]["color"] or "#8B949E"})
            entry["size"] += edge["size"]
    lang_total = sum(l["size"] for l in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: kv[1]["size"], reverse=True)[:6]

    active = [r for r in repos if history_count(r)]
    pairs, per_day, commits = set(), Counter(), 0
    for repo in active:
        for c in commits_for(repo["id"]):
            commits += 1
            author = c["author"] or {}
            login = ((author.get("user") or {}).get("login") or "").lower()
            pairs.add((login, (author.get("email") or "").lower()))
            per_day[c["committedDate"][:10]] += 1

    # Daily series over the window, oldest first.
    start = SINCE.date()
    days = [(start + timedelta(days=i)) for i in range((NOW.date() - start).days + 1)]
    series = [per_day.get(d.isoformat(), 0) for d in days]

    longest = run = 0
    for c in series:
        run = run + 1 if c else 0
        longest = max(longest, run)

    # 52 weekly buckets ending today.
    weekly = [sum(series[max(0, len(series) - 7 * (52 - w)):len(series) - 7 * (51 - w)]) for w in range(52)]

    return {
        "stats": [
            ("Commits", commits),
            ("Contributors", count_people(pairs)),
            ("Active repositories", len(active)),
            ("Active days", sum(1 for c in series if c)),
            ("Longest daily streak", longest),
            ("Repositories, all time", total_repos),
        ],
        "languages": [(n, l["color"], l["size"] / lang_total) for n, l in top],
        "weekly": weekly,
    }


def fmt(n):
    return f"{n/1000:.1f}k" if n >= 10000 else f"{n:,}"


def render(data, t):
    w, h = 840, 344
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="Team engineering activity over the last 12 months">',
        "<style>"
        f".t{{font:600 15px {FONT};fill:{t['title']}}}"
        f".s{{font:400 12px {FONT};fill:{t['label']}}}"
        f".l{{font:400 12.5px {FONT};fill:{t['label']}}}"
        f".v{{font:600 20px {FONT};fill:{t['value']}}}"
        f".lg{{font:400 12px {FONT};fill:{t['label']}}}"
        ".f{opacity:0;animation:in .6s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}"
        ".bar{transform-box:fill-box;transform-origin:left;animation:grow 1.1s cubic-bezier(.2,.8,.2,1) forwards;transform:scaleX(0)}"
        "@keyframes grow{to{transform:scaleX(1)}}"
        ".wk{transform-box:fill-box;transform-origin:bottom;animation:up .7s cubic-bezier(.2,.8,.2,1) forwards;transform:scaleY(0)}"
        "@keyframes up{to{transform:scaleY(1)}}"
        "@media (prefers-reduced-motion:reduce){.f,.bar,.wk{animation:none;opacity:1;transform:none}}"
        "</style>",
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<text x="28" y="40" class="t">Team engineering</text>',
        f'<text x="28" y="58" class="s">Monkdevelopers · last 12 months · all repositories, all authors</text>',
        f'<text x="472" y="40" class="t">Languages</text>',
        f'<text x="472" y="58" class="s">by code volume across repositories</text>',
        f'<line x1="444" y1="28" x2="444" y2="200" stroke="{t["border"]}"/>',
    ]

    for i, (label, value) in enumerate(data["stats"]):
        col, row = i % 2, i // 2
        x, y = 28 + col * 200, 96 + row * 46
        out.append(
            f'<g class="f" style="animation-delay:{i*90}ms">'
            f'<text x="{x}" y="{y}" class="v">{fmt(value)}</text>'
            f'<text x="{x}" y="{y+18}" class="l">{html.escape(label)}</text></g>'
        )

    bx, by, bw = 472, 80, 340
    out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="10" rx="5" fill="{t["track"]}"/>')
    out.append(f'<clipPath id="c"><rect x="{bx}" y="{by}" width="{bw}" height="10" rx="5"/></clipPath>')
    out.append('<g clip-path="url(#c)"><g class="bar">')
    x = bx
    shown = sum(p for _, _, p in data["languages"]) or 1
    for _, color, pct in data["languages"]:
        seg = bw * pct / shown
        out.append(f'<rect x="{x:.2f}" y="{by}" width="{seg+0.5:.2f}" height="10" fill="{color}"/>')
        x += seg
    out.append("</g></g>")
    for i, (name, color, pct) in enumerate(data["languages"]):
        col, row = i % 2, i // 2
        lx, ly = bx + col * 175, by + 42 + row * 30
        out.append(
            f'<g class="f" style="animation-delay:{300+i*90}ms">'
            f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{color}"/>'
            f'<text x="{lx+18}" y="{ly}" class="lg">{html.escape(name)} '
            f'<tspan fill="{t["value"]}" font-weight="600">{pct*100:.1f}%</tspan></text></g>'
        )

    # Weekly commits chart
    cx, cy, cw, ch = 28, 252, w - 56, 54
    out.append(f'<line x1="{cx}" y1="228" x2="{w-28}" y2="228" stroke="{t["border"]}"/>')
    out.append(f'<text x="{cx}" y="{cy-6}" class="s">Commits per week</text>')
    peak = max(data["weekly"]) or 1
    out.append(f'<text x="{w-28}" y="{cy-6}" class="s" text-anchor="end">peak {fmt(peak)}</text>')
    n = len(data["weekly"])
    gap = 3
    bwk = (cw - gap * (n - 1)) / n
    base = cy + 8 + ch
    for i, v in enumerate(data["weekly"]):
        bh = max(2, ch * v / peak) if v else 2
        fill = t["accent"] if v else t["track"]
        out.append(
            f'<rect class="wk" style="animation-delay:{500+i*12}ms" x="{cx + i*(bwk+gap):.2f}" '
            f'y="{base-bh:.2f}" width="{bwk:.2f}" height="{bh:.2f}" rx="1.5" fill="{fill}"/>'
        )

    stamp = NOW.strftime("%d %b %Y")
    out.append(f'<text x="{w-28}" y="{h-10}" class="lg" text-anchor="end" font-size="10.5">Updated {stamp} · auto-generated</text>')
    out.append("</svg>")
    return "\n".join(out)


def main():
    if not TOKEN:
        sys.exit("GH_TOKEN is not set")
    data = collect()
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, theme in THEMES.items():
        path = os.path.join(OUT_DIR, f"stats-{name}.svg")
        with open(path, "w") as f:
            f.write(render(data, theme))
        print(f"wrote {path}")
    print("stats:", ", ".join(f"{k}={v}" for k, v in data["stats"]))


if __name__ == "__main__":
    main()
