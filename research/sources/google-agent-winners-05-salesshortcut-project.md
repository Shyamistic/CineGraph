Source: https://devpost.com/software/salesshortcut
Title: SalesShortcut | Devpost
Fetched: 2026-08-31T12:16:04.942Z

[![SalesShortcut – screenshot 1](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/504/642/datas/gallery.jpg)](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/504/642/datas/original.jpg)
_Project architecture_

Google ADK Hackathon: SalesShortcut - Tsales automation and engagement - YouTube

Tap to unmute

[Google ADK Hackathon: SalesShortcut - Tsales automation and engagement](https://www.youtube.com/watch?v=UxP3iDqRKZ0) [Merdan Durdyyev](https://www.youtube.com/channel/UChvlVX7JxVtQJAvB_rrGTNQ)

Merdan Durdyyev8 subscribers

[Watch on](https://www.youtube.com/watch?v=UxP3iDqRKZ0)

[![SalesShortcut – screenshot 1](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/504/642/datas/gallery.jpg)](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/504/642/datas/original.jpg)
_Project architecture_

Google ADK Hackathon: SalesShortcut - Tsales automation and engagement - YouTube

Tap to unmute

[Google ADK Hackathon: SalesShortcut - Tsales automation and engagement](https://www.youtube.com/watch?v=UxP3iDqRKZ0) [Merdan Durdyyev](https://www.youtube.com/channel/UChvlVX7JxVtQJAvB_rrGTNQ)

Merdan Durdyyev8 subscribers

[Watch on](https://www.youtube.com/watch?v=UxP3iDqRKZ0)

[![SalesShortcut – screenshot 1](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/504/642/datas/gallery.jpg)](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/003/504/642/datas/original.jpg)
_Project architecture_

- 1
- 2

# 🚀 SalesShortcut Hackathon Journey

## Inspiration

The idea for SalesShortcut came from a real-world problem we witnessed firsthand. A friend of ours was working as a freelance developer, and he partnered with a sales-savvy friend to generate new business. The process was entirely manual: the salesperson would spend hours cold-calling businesses, trying to find clients who needed a new website. When he saw an interested lead, my developer friend would jump in and build the site.

It was a classic, manual grind. While their hustle was admirable, it was incredibly time-consuming and inefficient. We thought, "There has to be a better way."

This sparked the core idea behind SalesShortcut: **What if we could automate that entire process?** What if we could use the power of AI to not only find the leads but also to research them, craft personalized proposals, and even make the initial contact? We were inspired by the idea of building a system that could empower anyone, from a single developer to a small team, to create a new and significant stream of income using the incredible tools Google provides. We wanted to turn that manual hustle into a scalable, automated business engine.

## What it does

SalesShortcut is a comprehensive AI-powered Sales Development Representative (SDR) system that automates the entire sales process from lead discovery to deal closure. The system:

🔍 **Finds Leads**: Automatically discovers potential business leads in specified cities using Google Maps and location-based search, focusing on businesses without websites or with poor digital presence.

🧠 **Researches Prospects**: Conducts comprehensive business analysis to understand target business needs, pain points, competitor landscape, and opportunities through multiple specialized research agents.

📝 **Generates Proposals**: Creates personalized website development proposals based on research findings, using AI to craft compelling, tailored content that addresses specific business needs.

📞 **Makes Outreach**: Performs professional phone calls using ElevenLabs AI voice technology and sends follow-up emails with detailed proposals to interested prospects.

📋 **Manages Leads**: Tracks engagement, schedules follow-up activities, manages the sales funnel, and integrates with calendar systems for appointment scheduling.

## How we built it

SalesShortcut is not just a single application; it's a comprehensive system of **34 specialized AI agents** working in concert. We built a sophisticated multi-agent architecture using Google's cutting-edge technologies:

### 🏗️ Architecture & Scale

- **34 distinct agents** (21 LLMAgents, 7 Sequential Agents, 1 Parallel Agent, 2 Custom Agents, 1 Loop Agent)
- **5 microservices** on Cloud Run communicating via A2A protocol
- **16+ specialized tools** including agent-as-a-tool patterns
- **Advanced agentic patterns**: Review/Critique, Iterative Refinement, Parallel Fan-Out/Gather, and Human-in-the-Loop

### 🛠️ Technology Stack

- **Google Agent Development Kit (ADK)** for agent orchestration
- **Google Cloud Run** for serverless deployment
- **Vertex AI & Gemini Models** for AI capabilities
- **Google BigQuery** for data persistence
- **Google Maps, Search, Gmail, Calendar APIs** for comprehensive functionality
- **ElevenLabs API** for natural voice conversations
- **A2A Protocol** for service-to-service communication

## Challenges we ran into

Building a system this complex presented significant challenges:

### 🎯 Orchestrating 34 Agents

Managing the state and communication flow between three dozen agents was our biggest challenge. Ensuring proper coordination, avoiding conflicts, and maintaining data consistency across all agents required sophisticated state management and advanced ADK patterns.

### ⚡ Implementing True Parallelism

Designing the fan-out/gather pattern for simultaneous lead research required careful management of asynchronous tasks and data aggregation to avoid race conditions and ensure all information was correctly processed and synchronized.

### 🔧 Dynamic Tool Invocation

Allowing agents to use other agents as tools added complexity. We had to ensure that calling agents could correctly format requests and interpret responses from agent-tools, while maintaining proper execution flow and error handling.

### 🔗 Microservices Communication

Implementing reliable A2A communication patterns across 5 services while maintaining system resilience and handling network failures, timeouts, and service dependencies.

## Accomplishments that we're proud of

### 🏆 Technical Achievements

- Successfully orchestrated **34 AI agents** in a cohesive, production-ready system
- Implemented sophisticated multi-agent patterns that work seamlessly together
- Built a scalable microservices architecture using Google Cloud technologies
- Achieved true parallelism with fan-out/gather patterns for efficient lead processing

### 💼 Business Impact

- Created a system that can genuinely replace manual sales processes
- Demonstrated the power of AI automation in real-world business scenarios
- Built a solution that can scale from individual developers to small teams
- Integrated voice calling capabilities for natural prospect conversations

### 🎨 User Experience

- Developed an intuitive web dashboard with real-time WebSocket updates
- Created seamless human-in-the-loop integration for oversight and control
- Built comprehensive lead tracking and analytics capabilities

## What we learned

Starting this project was an ambitious leap for us. We decided to build it from scratch, which meant a steep but rewarding learning curve. Our journey was a deep dive into Google's powerful suite of technologies:

### 🤖 Google's Agent Development Kit (ADK)

We were new to ADK, but we were immediately impressed by its structured approach to building complex AI agents. We learned how to effectively manage agent state, which was critical for a system where multiple AI agents need to collaborate. The logical structure and powerful features like lifecycle hooks (`before_agent`, `after_agent`, `before_tool`, `after_tool`) gave us granular control over the entire execution flow.

### 🔗 App-to-App (A2A) Communication

Building a microservices-based architecture required a robust way for our services to talk to each other. We learned how to implement efficient and reliable A2A communication patterns to ensure our agents and services were always in sync across our 2 A2A clients.

### ☁️ Google Cloud Run & Vertex AI

Deploying a multi-service application can be complex, but Cloud Run was a game-changer. We learned how to containerize and deploy our services as scalable, serverless instances. Furthermore, we explored beyond the standard APIs and learned to host and query different LLMs for our agentic brains, including models on Vertex AI, giving us ultimate flexibility.

We came away from this hackathon with a profound appreciation for the power and elegance of Google's technology. It felt like we had a set of world-class building blocks that enabled us to bring our ambitious vision to life.

## What's next for SalesShortcut

### 🔮 Immediate Enhancements

- **Industry Specialization**: Expand beyond website development to target other service industries
- **Advanced Analytics**: Implement ML-powered conversion prediction and optimization
- **Multi-language Support**: Add localization for international markets
- **CRM Integration**: Connect with popular CRM systems like Salesforce and HubSpot

### 🚀 Long-term Vision

- **Vertical Expansion**: Adapt the system for different industries (legal, healthcare, consulting)
- **AI-Powered Negotiations**: Implement advanced negotiation agents for deal closing
- **Predictive Lead Scoring**: Use historical data to predict lead quality and conversion probability
- **Enterprise Features**: Add team collaboration, role-based access, and advanced reporting

### 🌟 Platform Evolution

- **Agent Marketplace**: Allow users to create and share custom agents
- **No-Code Agent Builder**: Enable non-technical users to build specialized sales agents
- **Integration Ecosystem**: Expand integrations with marketing tools, payment processors, and business systems

SalesShortcut represents just the beginning of what's possible when combining Google's powerful AI and cloud technologies with real-world business needs. We're excited to continue pushing the boundaries of AI-powered sales automation!

Update from the future - we started a startup - [https://salesshortcut.ai](https://salesshortcut.ai/)

## Bonuses

- **A contribution to the Agent Development Kit open source repository**: We make two open issues on ADK GitHub [here](https://github.com/google/adk-docs/issues/378) and [here](https://github.com/google/adk-docs/issues/379) and accepted [PR](https://github.com/google/adk-docs/pull/408)
- **A published blog post, video, or podcast**: LinkedIn [post](https://www.linkedin.com/feed/update/urn:li:activity:7342803791395680256/) and [article](https://medium.com/@sernur213/salesshortcut-building-an-autonomous-ai-sales-team-with-multi-agent-ai-architecture-using-google-e794c2c72152). Published [video](https://www.youtube.com/watch?v=UxP3iDqRKZ0&t=290s) and other LinkendIn [post here](https://www.linkedin.com/posts/merdandt_turn-google-adk-into-your-gmail-and-calendar-activity-7343032231789051905-Ej7-?utm_source=share&utm_medium=member_desktop&rcm=ACoAADV9y8UBXkHS5-iKIWwXlGSULDeCuTkO01M) and another Medium [article here](https://medium.com/@meinnps/turn-google-adk-into-your-gmail-and-calendar-assistant-8fee1b1cb05f)
- **The use of Google Cloud technology**: We used Lots of good staff from Google:
- Opened Google Admin and Workspace
- Created a Service Account and credential integration with all services
- Deployed 5 services to Cloud Run
- Integrated PubSub listener and Gmail Watcher
- Utilized Firebase Studio in our project
- Created and utilized Vertex AI

* * *

**🚀 Built with passion during the hackathon - transforming manual sales processes into AI-powered automation!**

## Built With

- a2a-sdk
- elevenlabs
- google-adk
- google-api-python-client
- google-auth
- google-auth-httplib2
- google-auth-oauthlib
- google-cloud-aiplatform
- google-cloud-pubsub
- google-generativeai
- [google-maps](https://devpost.com/software/built-with/google-maps)
- [twilio](https://devpost.com/software/built-with/twilio)
- vertexai

[Like\\
58](https://secure.devpost.com/users/register?flow%5Bdata%5D%5Bsoftware_id%5D=972284&flow%5Bname%5D=like_software&return_to=https%3A%2F%2Fdevpost.com%2Fsoftware%2Fsalesshortcut)

58 people like this:


- [![Chetan Sharma](https://lh3.googleusercontent.com/a/ACg8ocLc_LXsQ9u8KH47bacWUL8T_5-1Yzwo_parD_AdlO8VWin1lA=s96-c?type=square)](https://devpost.com/mss-chetansharma)
- [![MD. Riaz Ahmed](https://lh3.googleusercontent.com/a/ACg8ocL2nlvUEWxUe43xgOURlsLDdnL39QFvp-XeUsw-z08E_kqb-T_i=s96-c?type=square)](https://devpost.com/riazahmed2246)
- [![anshumanNitk Upadhyay](https://avatars.githubusercontent.com/u/119486460?type=square&v=4)](https://devpost.com/anshumanNitk)
- [![Nelson A.  Campos Maida](https://media.licdn.com/dms/image/v2/D4D03AQFfCmfDyhQhGw/profile-displayphoto-shrink_800_800/B4DZazvs3jHEAc-/0/1746772349355?e=1753315200&t=JGdgRcVym_c2AXQF7GAbeD2LigJIEHCmNa_Ucoq0ElI&type=square&v=beta)](https://devpost.com/nelson-maida)
- [![Pamphile GANSOU](https://lh3.googleusercontent.com/a/ACg8ocLCfLR9146NayksPNA_ilrx7dXMMmFJk053B3PVJIgPAO5KSgSr=s96-c?type=square)](https://devpost.com/gansphilos)
- [![Angela Zhen](https://lh3.googleusercontent.com/a/AEdFTp5AAJxNepXhn7Arb7uqz-loiGwCAIcL3h_gb9gdPw=s96-c?type=square)](https://devpost.com/yz6531)
- [![Peter Bodnar](https://lh3.googleusercontent.com/a/ACg8ocKqHPo_tqrinYkKdCqqBP1ThBdDsJleOttCAtCU83Ipp7vOPA=s96-c?type=square)](https://devpost.com/pb25em)
- [![Barry TANG](https://lh3.googleusercontent.com/a/ACg8ocKGQSTsXN2GhtfC67T6JRG6aBh8YmJQHGHGRQ0QfP4t_XCyMA=s96-c?type=square)](https://devpost.com/tr1173309602)
- [![George UTZYx](https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/004/172/247/datas/medium.jpeg)](https://devpost.com/g0_UTZYx)
- [![Eldar Akhmetgaliyev](https://lh3.googleusercontent.com/a/AAcHTtfYUgBLav4jv09zY78tDyFL5AfrwUe17eIcTP58unBNljA=s96-c?type=square)](https://devpost.com/eldar-373)

[\+ 48 more](https://devpost.com/software/salesshortcut/likes)

Share this project:




## Updates

[![Merdan Durdyyev](https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/003/445/586/datas/profile.jpg)](https://devpost.com/meinnps)

[Merdan Durdyyev](https://devpost.com/meinnps)
posted an update

—
[7 months ago](https://devpost.com/software/salesshortcut/updates/725491)

We launched a startup - [https://salesshortcut.ai](https://salesshortcut.ai/)

**[Log in](https://secure.devpost.com/users/login)**
or
**[sign up for Devpost](https://secure.devpost.com/users/register?flow%5Bdata%5D%5Bcommentable_id%5D=725491&flow%5Bname%5D=comment_on_software_update&return_to=https%3A%2F%2Fdevpost.com%2Fsoftware%2Fsalesshortcut)**
to join the conversation.


[![Merdan Durdyyev](https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/003/445/586/datas/profile.jpg)](https://devpost.com/meinnps)

[Merdan Durdyyev](https://devpost.com/meinnps)
started this project

—
[about a year ago](https://devpost.com/software/salesshortcut/updates/650549)

_Leave feedback in the comments!_

[View previous comments](https://devpost.com/software/salesshortcut#)

- [![danifdev](https://avatars.githubusercontent.com/u/90039480?height=180&v=4&width=180)](https://devpost.com/danifdev)





[danisultan](https://devpost.com/danifdev)
· about a year ago



well done

- [![m21rahmankhan](https://lh3.googleusercontent.com/a/ACg8ocLhlPtNjYrl_JMaUOlmoRqLtwOJ4UMupMq3NvezESsFQMmDwrAU=s96-c?height=180&width=180)](https://devpost.com/m21rahmankhan)





[Rahman Khan](https://devpost.com/m21rahmankhan)
· about a year ago



brother can we talk i am intrested in your voice agent.even i had created it .my instagram @khan\_sa1989004 do message me over here i am almost there but i am having some errors . help me with that a little bit

- ![Private user](https://devpost.com/assets/defaults/no-avatar-180-0301cf28954e6ce8ef036798be3a87b1f79306010122c2356cb9133bb10ed28d.png)









Private user



· about a year ago



that is clean mate congratulations

- [![Birendra45](https://lh3.googleusercontent.com/a-/ALV-UjXrgBEJXMt1XJlME5XFYeaDcyNt1lOWrLKi8_uYDmyOtbAy5BE0wvq2aESZWyw2aOMPHPsFM5EBJhrOlU7138QXceZIBBCaWpNKHCj576a_KI0Jj2gTTDriGsJz_X2u1agIb_2W5Ezp93lfeEmNlrh3wfT09UKk4Ixx5QCOzt3uIoQyP2x0rBO0UwyZt6IZ30JyzW2TNXKH6whD25GfQxZV0z0h0-t2s6JqUcB1B9l00NXxuDojbkM6J7T5og3B81Bc4eirRhbNSus7bSNe4AIVEmvgdFmDZHoh6nDJq0hqOuGpB5h6MF95P_8nOeEo5IHxkkBGBSs8s21dg70GSx-83oWFIN3McduuYXofoE0vYRFvG6GjSwBRvR3hfb_wPtLAELTKkmYlp2iI0LtY2A9LzxJSl-QLqE9iaesHKEX13un_TTsrrAuyHhOZUWEp0-s8RkPN7dipUlrdNat2seHCj87Up_kTEifvKnbWh3llc8W-km0vpncyPg3bPjuPl7dZPAKIwtyQHavcXovYckTH-ZzHpP0VdtXxb35qGjCiWMsZbm3v25feF-ePMx7tTnGooGOQedp9kgj53Y2N9-GYvs0NUlfsCZidXoiPokmVVljq8IanA0gA7i6wOjyzgdPuZoeBYGpzBdKq6hjjTgpoTnPsCYoW_K5fAi3VfD2a3RYuguD7rAvF5Ppwa9ZUKTFIRzawaMuGH6yXx3hxxdt9xg8NMfqAe_IAbz5YDUpfTVRyc3lRiOGRQLZOlqasVNjeJNeJVMknvsma42uJvpB1HIxd-_WRJAANkbbdiOeSnrSlihd9Mr64XFmtOPMLX9_vG0l13UkpR4Fx8bn4p1wVR16WY9bDSQ19JN4m5juj3VTyUmE7tA5wyuRih_VeATQ9h9TB9D18QY6IQvBa2zEGP0LRUMR031QnwTUGx3mowtz2gR72c7ojUqu5xM39F1fo5wKTFA0gb2i__8aq4m_DAw=s96-c?height=180&width=180)](https://devpost.com/Birendra45)





[Birendra Pratap Singh B P Singh](https://devpost.com/Birendra45)
· about a year ago



Very nice

- [![meinnps](https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/003/445/586/datas/profile.jpg)](https://devpost.com/meinnps)





[Merdan Durdyyev](https://devpost.com/meinnps)
· 12 months ago



Sorry, Rahman did not notice your message. Have you done it?


**[Log in](https://secure.devpost.com/users/login)**
or
**[sign up for Devpost](https://secure.devpost.com/users/register?flow%5Bdata%5D%5Bcommentable_id%5D=650549&flow%5Bname%5D=comment_on_software_update&return_to=https%3A%2F%2Fdevpost.com%2Fsoftware%2Fsalesshortcut)**
to join the conversation.


![](<Base64-Image-Removed>)

[Previous image](https://devpost.com/software/salesshortcut)[Next image](https://devpost.com/software/salesshortcut)