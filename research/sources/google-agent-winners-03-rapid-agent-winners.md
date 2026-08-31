Source: https://www.fivetran.com/blog/meet-the-ai-agents-that-won-the-google-cloud-rapid-agent-hackathon
Title: The winners of the Google Cloud rapid agent hackathon | Blog | Fivetran
Fetched: 2026-08-31T12:15:46.653Z

Data insights

# Meet the AI agents that won the Google Cloud Rapid Agent Hackathon

July 28, 2026

![Meet the AI agents that won the Google Cloud Rapid Agent Hackathon](https://cdn.prod.website-files.com/6130fa1501794e37c21867cf/6a6374fa8c84208fd59db6ff_The%20winners%20of%20%20Google%20Cloud%20Rapid%20Agent%20Hackathon%20(2).png)

[![](https://cdn.prod.website-files.com/6130fa1501794e37c21867cf/6a08dd101f5c9921bf818d3d_628803805e4e612967dff5b3.png)\\
\\
Jalene Svrcina\\
\\
Lead Partner Marketing Manager\\
\\
,\\
\\
Fivetran](https://www.fivetran.com/people/jalene-jizdeortega)

[Anchor Link](https://www.fivetran.com/blog/meet-the-ai-agents-that-won-the-google-cloud-rapid-agent-hackathon#)

Share

[LinkedIn Share](https://www.fivetran.com/blog/meet-the-ai-agents-that-won-the-google-cloud-rapid-agent-hackathon# "LinkedIn Share")[Twitter share](https://twitter.com/intent/tweet "Twitter share")

From genomic medicine to ecommerce operations, these winning AI agents show what becomes possible when agents have access to trusted, real-time data.

What happens when you give AI agents access to trusted enterprise data?

Developers build agents that help clinicians stay ahead of evolving genetic research, prevent businesses from losing revenue because of disconnected systems, and give ecommerce operators answers without spending hours searching through dashboards.

Those were just a few of the ideas submitted during the [**Google Cloud Rapid Agent Hackathon**](https://rapid-agent.devpost.com/), where more than **14,500 developers registered** and **1,430 projects were submitted** from builders around the world. Participants were challenged to build AI agents using Google Cloud and Model Context Protocol (MCP), enabling agents to securely connect with external tools and live data rather than relying solely on static prompts.

Developers could choose from 6 partner challenges. For the **Fivetran Challenge**, participants built AI agents using either the [Fivetran MCP server](https://github.com/fivetran/fivetran-mcp) or [REST API](https://fivetran.com/docs/rest-api) to interact with enterprise data and create intelligent workflows.

Narrowing dozens of impressive submissions down to 3 winners wasn't easy. The strongest projects tackled very different problems, from healthcare to ecommerce operations, but they all shared one thing: they solved real-world challenges by giving AI agents access to reliable, continuously updated information.

\[CTA\_MODULE\]

## First place: Unravel

Genetic research is constantly evolving. A variant classified as uncertain today could become clinically significant tomorrow, but patients and clinicians don't always know when that happens. A genetic test can provide life-changing information, but only if that information reaches the people who need it.

Built by cancer geneticist Faith Ogundimu, **Unravel** tackles exactly that problem: helping ensure important genetic discoveries don't stop at research databases, but rather reach the clinicians and families most in need.

Many DNA variants are initially classified as variants of uncertain significance (VUS), meaning scientists don't yet know whether they affect a person's health. As research evolves, some of those variants are reclassified as clinically meaningful, but those updates don't always make their way back to patients and families who could benefit from knowing.

Unravel was designed to close that gap. The application uses 5 specialized [AI agents](https://www.fivetran.com/blog/how-to-power-ai-agents-with-fivetran-and-google-cloud) that continuously monitor new genomic evidence, reassess uncertain variants, and determine when changes warrant clinical review. Behind the scenes, Fivetran brings data from sources including ClinVar, gnomAD, and AlphaMissense into BigQuery, while the agents use the Fivetran MCP server to monitor data freshness, trigger targeted syncs, and manage the underlying data connections.

Together, the agents can:

- Detect meaningful changes in variant evidence
- Reconcile conflicting research and estimate the likelihood of pathogenicity
- Recommend additional testing that may help resolve uncertain findings
- Identify relatives who may also be at risk
- Draft clinician alerts, family communications, and ClinVar submissions

Because the application operates in a [clinical setting](https://www.fivetran.com/blog/5-ways-fivetran-powers-healthcare-data-integration), Unravel was intentionally designed as a decision-support system, not an autonomous diagnostic tool. Recommendations remain subject to expert review, and low-confidence findings are withheld by design.

It's a compelling example of how AI agents can augment human expertise when they're grounded in current, trustworthy data.

## Second place: TruthKeeper

Every growing SaaS company eventually runs into the same problem: the CRM says one thing, billing says another, and support is left sorting out the mess. Small inconsistencies might seem harmless at first, but over time, they can lead to missed renewals, inaccurate reporting, and frustrated customers.

**TruthKeeper** was built to find those inconsistencies before they become expensive.

Using the Fivetran MCP server, [the agent](https://www.fivetran.com/blog/how-to-build-your-first-ai-agent) connects to an organization's existing data stack, discovers connected systems, and creates a shared model of entities such as customers, subscriptions, and invoices. Once that model is approved, it continuously reconciles records across systems to surface discrepancies.

When an issue is detected, TruthKeeper doesn't simply flag it. It explains what happened, estimates the potential financial impact, and prepares a corrective action for human review.

The agent can:

- Detect conflicting customer, subscription, and billing records
- Explain why records no longer match
- Estimate the business impact of each discrepancy
- Draft corrective actions for human approval before updating source systems

Rather than replacing operational teams, TruthKeeper helps them spend less time hunting for data inconsistencies and more time resolving them.

## Third place: How Did I?

Ask any ecommerce operator how yesterday went, and chances are, they'll open 5 different dashboards before they can answer. By the time they piece together sales, inventory, advertising, and [customer data](https://www.fivetran.com/learn/customer-data-integration), the opportunity to fix the problem may already be gone.

**How Did I?** was built to replace that daily investigation with a single operational briefing.

Using data brought together through Fivetran, the agent analyzes activity across an ecommerce business to identify issues such as abandoned cart spikes, inventory shortages, payment anomalies, or advertising campaigns driving traffic to products that are nearly out of stock.

For every finding, it estimates the revenue impact, explains why it matters, and recommends next steps before the problem grows.

The platform can:

- Surface revenue leaks across sales, marketing, inventory, and support
- Estimate the financial impact of each issue
- Draft abandoned cart emails, supplier reorder requests, and support responses
- Recommend advertising changes before spend is wasted

Instead of spending hours piecing together reports from multiple systems, store owners receive a prioritized summary of the issues most likely to affect the business that day.

## More than a hackathon

What made these winning projects stand out wasn't just technical execution or creative use of AI. None of the teams set out to build a better chatbot. They built software that monitors evolving medical research, reconciles business systems before inconsistencies become costly, and helps ecommerce teams uncover revenue leaks before they impact the bottom line

Across all 3 winners, the takeaway was clear: intelligence gets the headlines, but [trusted data](https://www.fivetran.com/blog/85-of-enterprises-are-running-agentic-ai-on-a-data-foundation-that-isnt-ready) is what makes AI agents useful.

The future of AI agents won't be defined by how quickly they can generate another answer. It will be defined by whether they can help people make better decisions — whether that's a clinician understanding new research, an operations team catching a costly mistake, or a business owner knowing where to focus next.

\[CTA\_MODULE\]

See how Fivetran enables innovation in practice.

[Get a demo](https://go.fivetran.com/demo)

Ready to get started with Fivetran?

[Start a free trial](https://fivetran.com/signup)

Share

[LInkedIn share](https://www.fivetran.com/blog/meet-the-ai-agents-that-won-the-google-cloud-rapid-agent-hackathon# "LInkedIn share")[Twitter share](https://twitter.com/intent/tweet "Twitter share")

### Related blog posts

[![](https://www.fivetran.com/blog/meet-the-ai-agents-that-won-the-google-cloud-rapid-agent-hackathon)\\
\\
**Heading**](https://www.fivetran.com/blog/meet-the-ai-agents-that-won-the-google-cloud-rapid-agent-hackathon#)

## Start for free

Join the thousands of companies using Fivetran to centralize and transform their data.

Email

Thank you! Your submission has been received!

Oops! Something went wrong while submitting the form.

[Get demo](https://go.fivetran.com/demo)

![](https://cdn.prod.website-files.com/6130fa1501794ed4d11867ba/67225f8f401494dcf70bd69a_intercom.svg)![](https://cdn.prod.website-files.com/6130fa1501794ed4d11867ba/67225f8f901c34c1a4839668_asics.svg)![](https://cdn.prod.website-files.com/6130fa1501794ed4d11867ba/67225f8f537088800755a7fd_canva.svg)![](https://cdn.prod.website-files.com/6130fa1501794ed4d11867ba/69960eb3cd70d2b32ca96bf2_New%20Relic.svg)![](https://cdn.prod.website-files.com/6130fa1501794ed4d11867ba/6a68ddfd2909265ce5117ca1_disney-white.png)![](https://cdn.prod.website-files.com/6130fa1501794ed4d11867ba/67f8c9a0a3a71203bb066ef9_CondeNast-1.svg)![](https://cdn.prod.website-files.com/6130fa1501794ed4d11867ba/67225f8fc1ac43105bf5377d_the-guardian.svg)![](https://cdn.prod.website-files.com/6130fa1501794ed4d11867ba/69960eb32a5816f0b0ebb76d_Blend-white.svg)

a6262564993105920.cdn.optimizely.com

# a6262564993105920.cdn.optimizely.com is blocked

This page has been blocked by an extension

- Try disabling your extensions.

ERR\_BLOCKED\_BY\_CLIENT

Reload


This page has been blocked by an extension

![](<Base64-Image-Removed>)![](<Base64-Image-Removed>)