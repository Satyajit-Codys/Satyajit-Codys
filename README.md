<a href="https://www.monkdevelopers.com">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/banner-light.svg">
    <img alt="Satyajit Debnath, Founder of Monkdevelopers. End-to-end product engineering for fintech, commerce and operations." src="./assets/banner-light.svg" width="100%">
  </picture>
</a>

<p align="center">
  I build software products end-to-end — fintech, commerce, and internal operations. Concept to launch, and beyond.
</p>

<div align="center">

| **150+** | **98%** | **5+** | **12+** |
| :---: | :---: | :---: | :---: |
| projects delivered | client satisfaction | years shipping products | countries with clients |

</div>

<p align="center">
  <a href="mailto:satyajit@monkdevelopers.com"><img src="https://img.shields.io/badge/Start%20a%20project-2563EB?style=flat-square&labelColor=2563EB&color=2563EB" height="30" alt="Start a software project with Satyajit Debnath"></a>
  <a href="https://www.monkdevelopers.com"><img src="https://img.shields.io/badge/monkdevelopers.com-0F172A?style=flat-square&labelColor=0F172A&color=0F172A" height="30" alt="Monkdevelopers software development agency website"></a>
  <a href="https://www.linkedin.com/in/dsatyajit"><img src="https://img.shields.io/badge/LinkedIn-1E293B?style=flat-square&labelColor=1E293B&color=1E293B" height="30" alt="Satyajit Debnath on LinkedIn"></a>
</p>

---

### What I do

I lead a team that takes products from a blank page to production — architecture, build, launch, and the unglamorous work of keeping them running afterward.

Most of my time goes to **regulated and operationally heavy products**: platforms that move money, manage compliance, or run a business's internal workflow. The kind where correctness matters more than novelty.

- **Product engineering** — web, mobile, and backend as one system, not three handoffs
- **Platform architecture** — multi-surface products sharing a backend, built to survive their own growth
- **Operations software** — CRMs, ERPs, and internal tooling that replace spreadsheets
- **Idea to launch** — scoping, technical direction, and delivery for founders without an in-house team

---

### How I build

Almost everything I ship has the same shape: several surfaces for different people, one backend that owns the rules, and the data and integrations behind it.

```mermaid
flowchart LR
    subgraph Surfaces
        W["Customer web app<br/><i>TypeScript · React</i>"]
        O["Operations console<br/><i>TypeScript</i>"]
        M["Mobile app<br/><i>Flutter</i>"]
    end

    subgraph Core["Shared backend"]
        API["API layer<br/><i>Python · Node.js · Java</i>"]
        SVC["Domain services<br/><i>accounts · payments · workflows</i>"]
    end

    subgraph Data["Data & infrastructure"]
        DB[("PostgreSQL / MongoDB")]
        Q[("Redis")]
    end

    EXT["Third-party integrations<br/><i>payment gateways · partner APIs</i>"]

    W & O & M --> API
    API --> SVC
    SVC --> DB & Q
    SVC <--> EXT
```

**One backend, many surfaces.** Customer app, ops console and mobile client all run on the same rules. Business logic lives in one place.<br/>
**Correctness over novelty.** In money-moving systems the boring path — explicit state, audit trails, reconciliation — is the right one.<br/>
**Own it after launch.** Monitoring, fixes and iteration are part of the product, not a follow-up contract.

---

### Team activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Satyajit-Codys/Satyajit-Codys/output/stats-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Satyajit-Codys/Satyajit-Codys/output/stats-light.svg">
  <img alt="Monkdevelopers team engineering activity over the last 12 months: commits, contributors, active repositories, languages and commits per week. Refreshed daily." src="https://raw.githubusercontent.com/Satyajit-Codys/Satyajit-Codys/output/stats-light.svg" width="100%">
</picture>

<sub>And my own contribution graph:</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Satyajit-Codys/Satyajit-Codys/output/contrib-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Satyajit-Codys/Satyajit-Codys/output/contrib-light.svg">
  <img alt="Animated personal contribution graph for the last twelve months" src="https://raw.githubusercontent.com/Satyajit-Codys/Satyajit-Codys/output/contrib-light.svg" width="100%">
</picture>

<sub>Generated daily by a <a href="./.github/workflows/profile-assets.yml">GitHub Actions workflow</a> straight from the GitHub API. Client work is under NDA, so only aggregate numbers are shown — no repository names.</sub>

---

### Founders' Grant

> [!TIP]
> **One project a month. Completely free.**

Every month, my team at Monkdevelopers builds one website or app at no cost — start to finish — for someone who needs it but can't afford agency rates. Same engineers, same process as our client work.

It's for you if:

- You're a small business, a non-profit, or an early founder with a real need
- A website or app would meaningfully move your work forward
- Paying agency rates right now genuinely isn't an option
- You can tell us what you need and why it matters

Applications take about five minutes. Every one gets read by the team — we're looking for real impact and genuine need, not polish. We pick one project each month, and applications we don't select stay on file.

**[Apply for the Founders' Grant →](https://www.monkdevelopers.com/founders-grant)**

---

### Stack

<p align="center">
  <img src="https://cdn.simpleicons.org/typescript/3178C6" height="38" alt="TypeScript" title="TypeScript" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/python/3776AB" height="38" alt="Python" title="Python" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/flutter/02569B" height="38" alt="Flutter" title="Flutter" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/react/61DAFB" height="38" alt="React" title="React" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/nodedotjs/5FA04E" height="38" alt="Node.js" title="Node.js" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/openjdk/ED8B00" height="38" alt="Java" title="Java" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/django/44B78B" height="38" alt="Django" title="Django" />
</p>

<p align="center">
  <img src="https://cdn.simpleicons.org/postgresql/4169E1" height="38" alt="PostgreSQL" title="PostgreSQL" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/mongodb/47A248" height="38" alt="MongoDB" title="MongoDB" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/redis/FF4438" height="38" alt="Redis" title="Redis" />&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/solidity/8A8F98" height="38" alt="Solidity" title="Solidity" />&nbsp;&nbsp;&nbsp;&nbsp;
  <picture><source media="(prefers-color-scheme: dark)" srcset="./assets/aws-dark.svg"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg" height="38" alt="Amazon Web Services" title="Amazon Web Services" /></picture>&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.simpleicons.org/googlecloud/4285F4" height="38" alt="Google Cloud" title="Google Cloud" />
</p>

---

### Let's talk

**Currently taking on new projects at Monkdevelopers.**

Reach out if you're building something in fintech, commerce, or operations — or if you have a product that needs a team to carry it from idea to launch. I'm also happy to talk architecture with other founders and engineers, no pitch involved.

<p align="center">
  <a href="mailto:satyajit@monkdevelopers.com"><img src="https://cdn.simpleicons.org/maildotru/2563EB" height="30" alt="Email satyajit@monkdevelopers.com"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.linkedin.com/in/dsatyajit"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" height="30" alt="Satyajit Debnath on LinkedIn"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.instagram.com/satyajitdebnath_"><img src="https://cdn.simpleicons.org/instagram/E4405F" height="30" alt="Satyajit Debnath on Instagram"></a>
</p>
