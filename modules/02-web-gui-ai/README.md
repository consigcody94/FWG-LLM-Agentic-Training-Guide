<div align="center">

# Module 02: Web GUI AI Interfaces

<img src="https://img.shields.io/badge/Duration-3_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-Module_01-orange?style=for-the-badge" alt="Prerequisites"/>

</div>

---

## Learning Objectives

By the end of this module, you will be able to:

- [ ] Navigate and effectively use ChatGPT, Claude.ai, Gemini, and Copilot interfaces
- [ ] Understand the unique features and limitations of each platform
- [ ] Apply appropriate tool for specific federal use cases
- [ ] Configure workspace settings for team collaboration
- [ ] Implement security best practices for web-based AI tools

---

## Table of Contents

1. [Platform Overview](#1-platform-overview)
2. [ChatGPT Interface](#2-chatgpt-interface)
3. [Claude.ai Mastery](#3-claudeai-mastery)
4. [Google Gemini](#4-google-gemini)
5. [Microsoft Copilot](#5-microsoft-copilot)
6. [Perplexity AI](#6-perplexity-ai)
7. [Platform Comparison](#7-platform-comparison)
8. [Security Considerations](#8-security-considerations)

---

## 1. Platform Overview

### Web GUI AI Landscape

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         WEB GUI AI PLATFORMS                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │                          GENERAL PURPOSE                             │   ║
║  │                                                                       │   ║
║  │    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │   ║
║  │    │ ChatGPT │    │ Claude  │    │ Gemini  │    │ Copilot │         │   ║
║  │    │         │    │   .ai   │    │         │    │         │         │   ║
║  │    │ OpenAI  │    │Anthropic│    │ Google  │    │Microsoft│         │   ║
║  │    └─────────┘    └─────────┘    └─────────┘    └─────────┘         │   ║
║  │                                                                       │   ║
║  └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │                           SPECIALIZED                                │   ║
║  │                                                                       │   ║
║  │    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │   ║
║  │    │Perplexity│   │  Poe    │    │ You.com │    │ Phind   │         │   ║
║  │    │         │    │         │    │         │    │         │         │   ║
║  │    │ Research│    │Multi-LLM│    │  Search │    │  Code   │         │   ║
║  │    └─────────┘    └─────────┘    └─────────┘    └─────────┘         │   ║
║  │                                                                       │   ║
║  └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Quick Feature Comparison

| Feature | ChatGPT | Claude | Gemini | Copilot | Perplexity |
|:--------|:-------:|:------:|:------:|:-------:|:----------:|
| **File Upload** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Image Generation** | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Image Analysis** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Web Search** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Code Execution** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Custom GPTs/Projects** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Team Features** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Enterprise SSO** | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 2. ChatGPT Interface

### Interface Overview

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CHATGPT INTERFACE                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────┬─────────────────────────────────────────────────────┐  ║
║  │                 │                                                      │  ║
║  │  SIDEBAR        │                    CHAT AREA                         │  ║
║  │                 │                                                      │  ║
║  │  ┌───────────┐  │  ┌────────────────────────────────────────────────┐ │  ║
║  │  │ New Chat  │  │  │                                                │ │  ║
║  │  └───────────┘  │  │  Model: GPT-4o                                 │ │  ║
║  │                 │  │                                                │ │  ║
║  │  Today          │  │  ┌──────────────────────────────────────────┐ │ │  ║
║  │  ├─ Chat 1     │  │  │ User Message                              │ │ │  ║
║  │  ├─ Chat 2     │  │  └──────────────────────────────────────────┘ │ │  ║
║  │  └─ Chat 3     │  │                                                │ │  ║
║  │                 │  │  ┌──────────────────────────────────────────┐ │ │  ║
║  │  Yesterday      │  │  │ Assistant Response                       │ │ │  ║
║  │  ├─ Chat 4     │  │  │ [Copy] [Edit] [Regenerate]               │ │ │  ║
║  │  └─ Chat 5     │  │  └──────────────────────────────────────────┘ │ │  ║
║  │                 │  │                                                │ │  ║
║  │  ───────────    │  └────────────────────────────────────────────────┘ │  ║
║  │                 │                                                      │  ║
║  │  Explore GPTs   │  ┌────────────────────────────────────────────────┐ │  ║
║  │                 │  │                                                │ │  ║
║  │  ───────────    │  │  [📎] [🌐] [💻]  Message ChatGPT...    [⬆️]  │ │  ║
║  │                 │  │                                                │ │  ║
║  │  Settings       │  └────────────────────────────────────────────────┘ │  ║
║  │                 │                                                      │  ║
║  └─────────────────┴─────────────────────────────────────────────────────┘  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Key Features

#### Custom GPTs
Create specialized assistants with:
- Custom instructions
- Uploaded knowledge bases
- Connected actions (APIs)
- Specific conversation starters

#### Code Interpreter
- Execute Python code in sandbox
- Analyze data files (CSV, Excel)
- Generate visualizations
- Process documents

#### Browsing
- Real-time web search
- Citation with sources
- Current events access

### ChatGPT Tiers

| Tier | Model Access | Features | Cost |
|:-----|:-------------|:---------|:-----|
| **Free** | GPT-3.5, Limited GPT-4o | Basic chat | $0 |
| **Plus** | GPT-4o, GPT-4 | Full features, DALL-E | $20/mo |
| **Team** | Plus + Admin | Workspace, SSO | $25/user/mo |
| **Enterprise** | Full + Security | SOC 2, SSO, API | Custom |

---

## 3. Claude.ai Mastery

### Interface Overview

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           CLAUDE.AI INTERFACE                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────┬─────────────────────────────────────────────────────┐  ║
║  │                 │                                                      │  ║
║  │  SIDEBAR        │                    CHAT AREA                         │  ║
║  │                 │                                                      │  ║
║  │  ┌───────────┐  │  ┌────────────────────────────────────────────────┐ │  ║
║  │  │Start chat │  │  │                                                │ │  ║
║  │  └───────────┘  │  │  Claude 3.5 Sonnet                             │ │  ║
║  │                 │  │                                                │ │  ║
║  │  Projects       │  │  ┌──────────────────────────────────────────┐ │ │  ║
║  │  ├─ Project A  │  │  │ User Message                              │ │ │  ║
║  │  ├─ Project B  │  │  │ [📎 Attached files]                       │ │ │  ║
║  │  └─ Project C  │  │  └──────────────────────────────────────────┘ │ │  ║
║  │                 │  │                                                │ │  ║
║  │  Recents        │  │  ┌──────────────────────────────────────────┐ │ │  ║
║  │  ├─ Conv 1     │  │  │ Claude Response                           │ │ │  ║
║  │  ├─ Conv 2     │  │  │                                           │ │ │  ║
║  │  └─ Conv 3     │  │  │ [Artifacts Panel →]                       │ │ │  ║
║  │                 │  │  └──────────────────────────────────────────┘ │ │  ║
║  │  ───────────    │  │                                                │ │  ║
║  │                 │  └────────────────────────────────────────────────┘ │  ║
║  │  Starred        │                                                      │  ║
║  │                 │  ┌────────────────────────────────────────────────┐ │  ║
║  │  ───────────    │  │                                                │ │  ║
║  │                 │  │  [📎] [🔧]  Reply to Claude...          [⬆️]  │ │  ║
║  │  Settings       │  │                                                │ │  ║
║  │                 │  └────────────────────────────────────────────────┘ │  ║
║  └─────────────────┴─────────────────────────────────────────────────────┘  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Unique Features

#### Projects
- Persistent knowledge bases
- Custom instructions per project
- File storage (PDF, code, etc.)
- Team collaboration

#### Artifacts
- Interactive code previews
- React components
- SVG visualizations
- Mermaid diagrams
- HTML/CSS renders

#### Analysis Tool
- Python code execution
- Data analysis capabilities
- File processing
- Visualization generation

### Claude.ai Tiers

| Tier | Model Access | Context | Features | Cost |
|:-----|:-------------|:--------|:---------|:-----|
| **Free** | Claude 3.5 Sonnet | Standard | Basic chat | $0 |
| **Pro** | All Claude models | Extended | Projects, Priority | $20/mo |
| **Team** | Pro + Admin | Extended | Workspace, Analytics | $25/user/mo |
| **Enterprise** | Full + Security | Maximum | SSO, Audit logs | Custom |

### Federal-Specific Benefits

- **Long Context:** 200K tokens ideal for government documents
- **Safety Focus:** Constitutional AI training
- **Detailed Citations:** Source referencing for compliance
- **Artifact Previews:** Interactive document elements

---

## 4. Google Gemini

### Interface Overview

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           GEMINI INTERFACE                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────┬─────────────────────────────────────────────────────┐  ║
║  │                 │                                                      │  ║
║  │  SIDEBAR        │                    CHAT AREA                         │  ║
║  │                 │                                                      │  ║
║  │  ┌───────────┐  │  ┌────────────────────────────────────────────────┐ │  ║
║  │  │ New chat  │  │  │                                                │ │  ║
║  │  └───────────┘  │  │  Gemini Advanced                               │ │  ║
║  │                 │  │                                                │ │  ║
║  │  Gem Manager    │  │  ┌──────────────────────────────────────────┐ │ │  ║
║  │                 │  │  │ User Message                              │ │ │  ║
║  │  Recent         │  │  │ [Uploaded image/doc preview]              │ │ │  ║
║  │  ├─ Chat 1     │  │  └──────────────────────────────────────────┘ │ │  ║
║  │  ├─ Chat 2     │  │                                                │ │  ║
║  │  └─ Chat 3     │  │  ┌──────────────────────────────────────────┐ │ │  ║
║  │                 │  │  │ Gemini Response                          │ │ │  ║
║  │                 │  │  │                                           │ │ │  ║
║  │  ───────────    │  │  │ [Google Search] [Maps] [Docs]            │ │ │  ║
║  │                 │  │  │ [Share] [Export to Docs]                  │ │ │  ║
║  │  Extensions     │  │  └──────────────────────────────────────────┘ │ │  ║
║  │  ├─ Search     │  │                                                │ │  ║
║  │  ├─ Workspace  │  └────────────────────────────────────────────────┘ │  ║
║  │  └─ YouTube    │                                                      │  ║
║  │                 │  ┌────────────────────────────────────────────────┐ │  ║
║  │  ───────────    │  │                                                │ │  ║
║  │  Settings       │  │  [📎] [🎤] [📷]  Enter a prompt      [⬆️]     │ │  ║
║  │                 │  │                                                │ │  ║
║  └─────────────────┴─────────────────────────────────────────────────────┘  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Unique Features

#### Google Workspace Integration
- Direct access to Gmail, Docs, Drive
- Search across workspace
- Export responses to Docs
- Collaborative editing

#### Extensions
- Google Search with citations
- Google Maps integration
- YouTube transcript analysis
- Google Flights & Hotels

#### Gems (Custom Assistants)
- Pre-configured personas
- Specialized instructions
- Task-specific optimization

### Federal Advantages

| Feature | Federal Benefit |
|:--------|:----------------|
| **FedRAMP Authorization** | Compliant for government use |
| **1M+ Context** | Entire policy documents |
| **Workspace Integration** | Seamless with Google Workspace Gov |
| **Grounding** | Fact-checking with search |

---

## 5. Microsoft Copilot

### Interface Variants

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        MICROSOFT COPILOT ECOSYSTEM                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │                     COPILOT PRODUCTS                                 │   ║
║  │                                                                       │   ║
║  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │   ║
║  │  │    Copilot      │  │  Copilot Pro    │  │Copilot for M365 │      │   ║
║  │  │    (Free)       │  │  ($20/month)    │  │  ($30/user/mo)  │      │   ║
║  │  │                 │  │                 │  │                 │      │   ║
║  │  │ • Web chat      │  │ • Priority GPT-4│  │ • Word assist   │      │   ║
║  │  │ • Bing search   │  │ • Image create  │  │ • Excel analysis│      │   ║
║  │  │ • Basic image   │  │ • Office integr │  │ • PowerPoint gen│      │   ║
║  │  │ • Edge sidebar  │  │ • Copilot GPTs  │  │ • Outlook draft │      │   ║
║  │  └─────────────────┘  └─────────────────┘  │ • Teams summary │      │   ║
║  │                                            │ • Graph security│      │   ║
║  │                                            └─────────────────┘      │   ║
║  │                                                                       │   ║
║  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │   ║
║  │  │GitHub Copilot   │  │  Copilot        │  │   Copilot       │      │   ║
║  │  │  ($10-19/mo)    │  │  Studio         │  │   for Azure     │      │   ║
║  │  │                 │  │                 │  │                 │      │   ║
║  │  │ • Code complete │  │ • Build custom  │  │ • Infrastructure│      │   ║
║  │  │ • Chat in IDE   │  │ • Connect data  │  │ • Query assist  │      │   ║
║  │  │ • PR reviews    │  │ • Deploy agents │  │ • Cost analysis │      │   ║
║  │  └─────────────────┘  └─────────────────┘  └─────────────────┘      │   ║
║  │                                                                       │   ║
║  └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Enterprise Integration

- **Azure AD/Entra ID:** Single sign-on
- **Microsoft Graph:** Access organizational data
- **Compliance Center:** Data governance
- **Audit Logs:** Activity tracking

### GCC/GCC-High Availability

| Feature | GCC | GCC-High |
|:--------|:---:|:--------:|
| Copilot for M365 | ✅ | ✅ |
| Copilot Studio | ✅ | ✅ |
| GitHub Copilot | ⚠️ | ❌ |
| Designer | ❌ | ❌ |

---

## 6. Perplexity AI

### Research-Focused Interface

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        PERPLEXITY AI INTERFACE                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │                                                                       │   ║
║  │  ┌─────────────────────────────────────────────────────────────────┐ │   ║
║  │  │  🔍 Ask anything...                                     [Pro]   │ │   ║
║  │  │                                                                  │ │   ║
║  │  │  Focus: [All] [Academic] [Writing] [Wolfram] [YouTube] [Reddit] │ │   ║
║  │  └─────────────────────────────────────────────────────────────────┘ │   ║
║  │                                                                       │   ║
║  │  ┌─────────────────────────────────────────────────────────────────┐ │   ║
║  │  │  ANSWER                                                          │ │   ║
║  │  │  ─────────────────────────────────────────────────────────────  │ │   ║
║  │  │                                                                  │ │   ║
║  │  │  Based on multiple sources, federal AI adoption...              │ │   ║
║  │  │                                                                  │ │   ║
║  │  │  ┌─────────────────────────────────────────────────────────┐   │ │   ║
║  │  │  │  📚 SOURCES                                              │   │ │   ║
║  │  │  │  [1] whitehouse.gov - Executive Order 14110              │   │ │   ║
║  │  │  │  [2] gao.gov - AI Implementation Report                  │   │ │   ║
║  │  │  │  [3] nist.gov - AI RMF Framework                         │   │ │   ║
║  │  │  │  [4] federalnewsnetwork.com - Agency Updates             │   │ │   ║
║  │  │  └─────────────────────────────────────────────────────────┘   │ │   ║
║  │  │                                                                  │ │   ║
║  │  │  RELATED QUESTIONS                                               │ │   ║
║  │  │  • What are the key requirements of EO 14110?                   │ │   ║
║  │  │  • How are federal agencies implementing AI RMF?                │ │   ║
║  │  │  • What is the timeline for AI governance compliance?           │ │   ║
║  │  └─────────────────────────────────────────────────────────────────┘ │   ║
║  │                                                                       │   ║
║  └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Unique Value for Federal Research

| Feature | Description | Federal Use Case |
|:--------|:------------|:-----------------|
| **Academic Focus** | Scholar and journal search | Policy research |
| **Source Citations** | Inline numbered references | Report writing |
| **Collections** | Organized research threads | Project documentation |
| **Pro Search** | Multi-step research queries | Complex investigations |

---

## 7. Platform Comparison

### Feature Matrix

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    COMPREHENSIVE PLATFORM COMPARISON                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Feature              │ ChatGPT │ Claude │ Gemini │ Copilot │ Perplexity   ║
║  ─────────────────────┼─────────┼────────┼────────┼─────────┼────────────  ║
║  Context Window       │  128K   │  200K  │   1M+  │  128K   │   128K       ║
║  File Upload          │   ✅    │   ✅   │   ✅   │   ✅    │    ✅        ║
║  Code Execution       │   ✅    │   ✅   │   ✅   │   ❌    │    ❌        ║
║  Image Generation     │   ✅    │   ❌   │   ✅   │   ✅    │    ✅        ║
║  Image Analysis       │   ✅    │   ✅   │   ✅   │   ✅    │    ✅        ║
║  Web Search           │   ✅    │   ✅   │   ✅   │   ✅    │    ✅        ║
║  Custom Assistants    │   ✅    │   ✅   │   ✅   │   ✅    │    ❌        ║
║  API Access           │   ✅    │   ✅   │   ✅   │   ✅    │    ✅        ║
║  Enterprise SSO       │   ✅    │   ✅   │   ✅   │   ✅    │    ✅        ║
║  FedRAMP              │   ⏳    │   ⏳   │   ✅   │   ✅    │    ❌        ║
║  Data Residency       │  Varies │ Varies │  US    │   US    │   Varies     ║
║  Office Integration   │   ❌    │   ❌   │   ✅   │   ✅    │    ❌        ║
║  Citations/Sources    │   ✅    │   ✅   │   ✅   │   ✅    │    ✅✅      ║
║                                                                              ║
║  Best For:                                                                   ║
║  ChatGPT    → General productivity, code, custom GPTs                       ║
║  Claude     → Long documents, nuanced analysis, safety-critical             ║
║  Gemini     → Google Workspace users, multimodal, compliance                ║
║  Copilot    → Microsoft ecosystem, Office automation                        ║
║  Perplexity → Research, citations, academic work                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Use Case Recommendations

| Task | Primary | Alternative |
|:-----|:--------|:------------|
| **Policy Document Analysis** | Claude (200K context) | Gemini (1M context) |
| **Research with Citations** | Perplexity | ChatGPT + Search |
| **Code Development** | ChatGPT/Claude | GitHub Copilot |
| **Office Document Generation** | Copilot for M365 | ChatGPT + Copy |
| **Image Analysis** | Claude/Gemini | ChatGPT |
| **Compliance Review** | Gemini (FedRAMP) | Copilot (M365) |
| **Meeting Summarization** | Copilot (Teams) | Claude |

---

## 8. Security Considerations

### Data Handling Policies

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      SECURITY CONSIDERATIONS                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ⚠️  NEVER INPUT INTO PUBLIC AI INTERFACES:                                 ║
║                                                                              ║
║  • Classified information (any level)                                        ║
║  • Personally Identifiable Information (PII)                                 ║
║  • Protected Health Information (PHI)                                        ║
║  • Controlled Unclassified Information (CUI)                                 ║
║  • Export-controlled technical data (ITAR/EAR)                               ║
║  • Source code for sensitive systems                                         ║
║  • Internal security configurations                                          ║
║  • Authentication credentials                                                ║
║                                                                              ║
║  ✅  ACCEPTABLE FOR PUBLIC INTERFACES:                                       ║
║                                                                              ║
║  • Public information research                                               ║
║  • General knowledge queries                                                 ║
║  • Non-sensitive drafting assistance                                         ║
║  • Learning and training exercises                                           ║
║  • Public-facing content development                                         ║
║                                                                              ║
║  🔒  FOR SENSITIVE WORK, USE:                                                ║
║                                                                              ║
║  • FedRAMP-authorized enterprise versions                                    ║
║  • Agency-approved private instances                                         ║
║  • Local models (Ollama - see Module 03)                                     ║
║  • Air-gapped deployments                                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Enterprise Features Checklist

- [ ] SSO/SAML integration enabled
- [ ] Data retention policies configured
- [ ] Audit logging activated
- [ ] User access controls defined
- [ ] Data processing agreements signed
- [ ] Compliance certifications verified
- [ ] Training data opt-out confirmed
- [ ] Admin controls documented

---

## Exercises

### Exercise 2.1: Platform Comparison
Use all five platforms to answer the same federal policy question. Compare response quality, sources, and format.

### Exercise 2.2: Project Setup
Create a Claude Project with federal document templates and test custom instructions.

### Exercise 2.3: Research Workflow
Use Perplexity to research a federal regulation, then use Claude to summarize findings.

### Exercise 2.4: Security Audit
Review your agency's AI usage policy and map it to platform capabilities.

---

## Assessment

### Knowledge Check

1. What is the maximum context window for each major platform?
2. Which platforms have FedRAMP authorization?
3. What types of data should never be entered into public AI interfaces?
4. Compare the custom assistant features across platforms.
5. What are the key differences between free and enterprise tiers?

### Practical Assessment

Configure a Claude Project with appropriate custom instructions for a federal use case, demonstrating proper security considerations.

---

## Next Module

➡️ [Module 03: Local LLMs](../03-local-llms/README.md)

---

<div align="center">

[⬆ Back to Top](#module-02-web-gui-ai-interfaces) · [📚 Return to Curriculum](../../README.md)

</div>
