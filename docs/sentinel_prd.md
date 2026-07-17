# Sentinel Demo PRD v1.0

**Document Type:** Product Requirements Document (Demo Version)

**Product Name:** Sentinel

**Version:** 1.0

**Status:** Draft

**Author:** OpenAI × Project Owner

**Target Audience:** Police Cyber Crime Units, Digital Forensics Investigators, Academic Evaluators

---

# Document History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | YYYY-MM-DD | Initial Demo PRD |

---

# Table of Contents

1. Introduction
2. Vision
3. Problem Statement
4. Project Goals
5. Success Metrics
6. Demo Scope
7. Out of Scope
8. User Personas
9. User Stories
10. Functional Overview
11. End-to-End Workflow
12. Product Architecture
13. Technology Stack
14. Module Overview
15. User Interface Overview
16. Dashboard Specification
17. Upload Module
18. Static Analysis Module
19. IOC Extraction Module
20. Threat Intelligence Module
21. Risk Scoring Module
22. MITRE ATT&CK Module
23. AI Investigation Module
24. Report Generation Module
25. Database Design
26. REST API Design
27. Folder Structure
28. Development Roadmap
29. Acceptance Criteria
30. Future Scope

---

# 1. Introduction

## Purpose

Sentinel is an AI-assisted malware investigation platform designed specifically for police officers and digital forensic investigators.

The objective is not to replace commercial malware sandboxes or antivirus engines but to consolidate analysis results into a single, easy-to-understand investigation interface.

The platform emphasizes explainability over complexity. Every detection must be accompanied by supporting evidence and a clear explanation.

The demo version focuses on delivering a complete investigative workflow while keeping implementation manageable.

---

# 2. Vision

Create an investigation platform that enables investigators with limited cybersecurity expertise to upload a suspicious file and receive a structured investigation report within minutes.

Rather than displaying hundreds of technical indicators, Sentinel explains:

- What the file is.
- Why it is suspicious.
- What evidence supports the conclusion.
- Which attacker techniques were observed.
- What actions should be taken next.

---

# 3. Problem Statement

Existing malware analysis platforms are designed primarily for malware researchers and security professionals.

Their reports contain extensive technical information that can overwhelm investigators without specialized training.

Police investigators often need:

- A quick understanding of malicious behavior.
- Reliable evidence.
- Standardized reporting.
- Easy-to-read summaries.

Sentinel addresses these requirements through automated analysis, external threat intelligence, and AI-assisted explanation.

---

# 4. Project Goals

The demo version shall:

- Accept multiple suspicious file formats.
- Perform automated static analysis.
- Extract indicators of compromise.
- Query external threat intelligence services.
- Assign an explainable risk score.
- Map observed behavior to MITRE ATT&CK.
- Generate an AI-assisted investigation summary.
- Export reports in multiple formats.

---

# 5. Success Metrics

The demo shall be considered successful when it can:

- Analyze a supported file from upload to report without manual intervention.
- Display meaningful investigation results within five minutes.
- Generate downloadable reports.
- Provide understandable explanations suitable for non-technical investigators.
- Successfully query VirusTotal and MalwareBazaar when internet connectivity is available.

---

# 6. Demo Scope

## Included

The demo shall support:

- Windows PE Executables (.exe)
- DLL files
- Android APKs
- PDF documents
- Microsoft Office documents
- ZIP archives
- JavaScript
- PowerShell
- Python scripts
- Batch files

Core features include:

- File upload
- Hash generation
- Static analysis
- IOC extraction
- Threat intelligence lookup
- Risk scoring
- MITRE ATT&CK mapping
- AI-generated investigation summary
- PDF, HTML, CSV and JSON reports

---

# 7. Out of Scope

The following features are intentionally excluded from the demo:

- User authentication
- Role-based access control
- Multi-user collaboration
- Live malware execution
- Memory forensics
- Kubernetes deployment
- Background workers
- Distributed analysis
- Email notifications
- Audit compliance
- Plugin marketplace

These features are reserved for future versions.

---

# 8. User Personas

## Persona 1 – Police Investigator

Experience:
Basic computer knowledge with limited cybersecurity expertise.

Goals:

- Determine whether a suspicious file is malicious.
- Generate a report suitable for evidence documentation.
- Understand findings without reading technical manuals.

Pain Points:

- Existing malware reports are difficult to interpret.
- Multiple security tools require separate investigation.

---

## Persona 2 – Cyber Crime Officer

Experience:
Intermediate cybersecurity knowledge.

Goals:

- Correlate investigation findings.
- Review indicators of compromise.
- Identify malware families.

---

## Persona 3 – Digital Forensics Student

Experience:
Learning malware analysis.

Goals:

- Understand malware behavior.
- Learn investigation workflows.
- Practice digital forensic analysis.

---

# 9. User Stories

## Story 1

As a police investigator,

I want to upload a suspicious file,

So that Sentinel automatically analyzes it.

---

## Story 2

As an investigator,

I want the system to explain why the file is suspicious,

So that I can understand the findings without advanced malware expertise.

---

## Story 3

As an investigator,

I want external threat intelligence,

So that I know whether the malware has already been observed in the wild.

---

## Story 4

As an investigator,

I want downloadable reports,

So that they can be attached to investigation records.

---

# 10. Functional Overview

The Sentinel demo consists of eight major modules.

1. Upload Module
2. Static Analysis
3. IOC Extraction
4. Threat Intelligence
5. Risk Scoring
6. MITRE ATT&CK Mapping
7. AI Investigation Summary
8. Report Generator

Each module operates independently while contributing to the final investigation report.

---

# 11. End-to-End Workflow

User uploads file

↓

File validation

↓

Hash calculation

↓

Static analysis

↓

IOC extraction

↓

Threat intelligence lookup

↓

Risk scoring

↓

MITRE ATT&CK mapping

↓

AI investigation summary

↓

Report generation

↓

Download report

---

# 12. Product Architecture

```

+------------------------------------------------------+
\|                  Sentinel Web Client                 |
+--------------------------+---------------------------+
|
v
+------------------------------------------------------+
\|                  FastAPI Backend                     |
+--------------------------+---------------------------+
|
+----------------+-------------------+-----------------+
| | | |
v v v
Upload Static IOC
Service Analysis Extraction

| | |
+--------+-----------+
|
v
Threat Intelligence

|
v
Risk Engine

|
v
MITRE Mapping

|
v
Gemini AI

|
v
Report Generator

|
v

SQLite Database

```

---

# 13. Technology Stack

## Frontend

React

TypeScript

Tailwind CSS

ShadCN UI

Axios

## Backend

FastAPI

Python 3.12

SQLAlchemy

Pydantic

## Database

SQLite (Demo)

## Threat Intelligence

VirusTotal API

MalwareBazaar API

## AI

Gemini API

## Static Analysis Libraries

Androguard

pefile

oletools

LIEF

YARA

python-magic

---

# 14. Module Overview

The platform is divided into modular services.

Each service performs one responsibility only.

| Module | Responsibility |
|----------|---------------|
| Upload | File ingestion |
| Static Analysis | File inspection |
| IOC Extraction | Extract indicators |
| Threat Intelligence | External enrichment |
| Risk Engine | Rule-based scoring |
| MITRE | ATT&CK mapping |
| AI | Human-readable explanation |
| Reports | Export investigation |

---
# 15. User Interface Specification

## 15.1 Design Philosophy

The Sentinel interface shall prioritize clarity, simplicity, and investigator productivity over technical complexity.

The primary users are police investigators rather than malware researchers. Therefore, the interface must minimize cognitive load while still presenting all necessary evidence.

The application shall follow these principles:

- Minimal clicks
- Clean navigation
- Consistent layouts
- Evidence-first presentation
- Explain before technical details

---

## 15.2 Color Palette

| Purpose | Color |
|----------|--------|
| Primary | Blue |
| Success | Green |
| Warning | Orange |
| Critical | Red |
| Background | White |
| Secondary Background | Light Gray |

---

## 15.3 Layout

The application uses a persistent sidebar.

```

+-----------------------------------------------------------+
| Sidebar | Main Content |
| | |
| Dashboard | |
| Upload | |
| Investigations | |
| Reports | |
| Settings | |
| | |
+-----------------------------------------------------------+

```

---

## 15.4 Dashboard

The Dashboard is the first screen shown after opening Sentinel.

Its objective is to provide investigators with an overview of all investigations.

### Dashboard Widgets

• Total Investigations

• Files Uploaded Today

• High Risk Samples

• Critical Alerts

• Recent Reports

• Threat Intelligence Status

• Recent Activity

---

### Dashboard Wireframe

```

-------------------------------------------------------

Sentinel Dashboard

-------------------------------------------------------

Investigations Today 18

High Risk Samples 5

Reports Generated 12

Threat Intelligence Online ✓

-------------------------------------------------------

Recent Uploads

-------------------------------------------------------

invoice.exe

High

today

-------------------------------------------------------

document.pdf

Medium

today

-------------------------------------------------------

agent.apk

Critical

today

-------------------------------------------------------

```

---

# 16. Upload Module

## 16.1 Purpose

The Upload Module is responsible for receiving suspicious files and initiating the investigation workflow.

Every investigation begins here.

---

## 16.2 Functional Requirements

### FR-001

The system shall support drag-and-drop uploads.

---

### FR-002

The system shall allow selecting files through a file picker.

---

### FR-003

The system shall support multiple file uploads.

---

### FR-004

The system shall calculate hashes immediately after upload.

---

### FR-005

The upload progress shall be displayed in real time.

---

### FR-006

The system shall reject unsupported files.

---

### Supported File Types

Windows

- EXE
- DLL

Android

- APK

Documents

- PDF
- DOC
- DOCX
- XLS
- XLSX
- PPT
- PPTX

Scripts

- JS
- VBS
- BAT
- PS1
- PY

Archives

- ZIP
- RAR
- 7Z

---

### Upload Validation

The following checks shall occur before analysis.

- File Size
- MIME Type
- Extension
- Magic Bytes
- Duplicate SHA256

---

### Upload Workflow

```

Choose File

↓

Upload

↓

Validate File

↓

Calculate Hashes

↓

Create Investigation

↓

Start Static Analysis

```

---

### Upload Screen Wireframe

```

---------------------------------------------------------

Upload Suspicious File

---------------------------------------------------------

+-----------------------------------------------+

|

Drop File Here

|

|

or

|

|

Choose File

|

+-----------------------------------------------+

Supported Formats

EXE DLL APK PDF Office ZIP JS BAT PS1 PY

---------------------------------------------------------

```

---

# 17. File Identification Module

## Purpose

Before analysis begins Sentinel must identify exactly what kind of file has been uploaded.

This determines which analysis engine will process the sample.

---

## File Classification

The following information shall be extracted.

- Filename
- Extension
- MIME Type
- File Size
- Entropy
- Magic Bytes
- Architecture
- Platform

---

### Hash Calculation

Immediately after upload the system shall generate

MD5

SHA1

SHA256

SHA512

These values become the permanent identifiers of the evidence.

---

### Example

Filename

invoice.exe

File Type

PE32 Executable

Architecture

x64

SHA256

9A8E2F......

---

# 18. Static Analysis Module

## Overview

Static Analysis inspects the uploaded file without executing it.

This is the primary analysis stage of the demo.

---

## Objectives

The module shall

- Extract metadata
- Inspect structure
- Identify suspicious characteristics
- Produce evidence

---

## Supported File Types

### Windows Executables

Using

pefile

LIEF

Extract

- PE Header
- Sections
- Imports
- Exports
- Digital Signature
- Compilation Timestamp
- Entry Point

---

### Android APK

Using

Androguard

Extract

- Package Name
- Activities
- Services
- Broadcast Receivers
- Permissions
- Exported Components
- SDK Version
- Certificate

---

### PDF

Extract

- Embedded JavaScript
- Embedded Files
- Metadata
- Launch Actions
- URLs

---

### Microsoft Office

Using

oletools

Extract

- Macros
- VBA
- OLE Objects
- Metadata

---

### Scripts

Extract

- URLs
- Encoded Commands
- PowerShell Functions
- Suspicious Keywords

---

### Static Analysis Workflow

```

Uploaded File

↓

Determine File Type

↓

Select Analyzer

↓

Extract Metadata

↓

Extract Structure

↓

Run Detection Rules

↓

Generate Findings

```

---

## Findings

Every finding shall include

Severity

Description

Evidence

Recommendation

Example

```

Severity

High

Finding

Executable is packed.

Evidence

High entropy detected in .text section.

Recommendation

Run dynamic analysis.

```

---

## Static Analysis Screen

```

-------------------------------------------------------

Static Analysis

-------------------------------------------------------

Metadata

Sections

Imports

Strings

Certificate

Entropy

Compiler

Security Findings

-------------------------------------------------------

```

---

## Security Findings

Examples

Unsigned executable

Packed executable

Suspicious imports

Embedded executable

Macro enabled document

Dangerous Android permissions

Hidden JavaScript

Obfuscated PowerShell

Each finding shall include supporting evidence.

---

# 19. IOC Extraction Module

## Purpose

Indicators of Compromise are extracted automatically from every uploaded file.

These indicators assist investigators in identifying malicious infrastructure.

---

## IOC Types

Sentinel shall detect

- IPv4
- IPv6
- Domains
- URLs
- Email Addresses
- SHA1
- SHA256
- MD5
- File Paths
- Registry Keys
- Mutexes
- User Agents
- Cryptocurrency Wallets

---

## Extraction Workflow

```

Static Analysis

↓

Strings

↓

Regex Detection

↓

Normalize

↓

Remove Duplicates

↓

Store Database

↓

Display

```

---

## IOC Confidence

Every IOC shall receive a confidence level.

High

Medium

Low

Confidence is based upon

- Detection Source
- Validation
- Context

---

## IOC Table

| IOC | Type | Confidence |
|------|------|------------|
| evil.com | Domain | High |
| 45.xxx.xxx.xxx | IP | High |
| powershell.exe | Process | Medium |
| HKCU\Software\Run | Registry | High |

---

## IOC Screen

```

------------------------------------------------------

Extracted Indicators

------------------------------------------------------

Domains

IPs

URLs

Registry

Hashes

Email

Wallets

------------------------------------------------------

```

---

## IOC Export

Investigators may export IOC data as

- CSV
- JSON

This allows importing into external forensic platforms.

---
# 20. Threat Intelligence Module

## 20.1 Overview

The Threat Intelligence Module enriches locally extracted evidence by querying trusted external threat intelligence platforms.

Unlike the Static Analysis module, which only inspects the uploaded file, the Threat Intelligence Module answers an equally important question:

> **"Has this file, hash, IP address, domain, or URL been observed before by the global cybersecurity community?"**

This module provides investigators with additional context such as malware family, first seen date, detection ratios, threat reputation, malicious infrastructure, and associated tags.

The Threat Intelligence Module is an enrichment service. It does not determine whether a sample is malicious; instead, it provides external evidence that supports the overall investigation.

---

# 20.2 Objectives

The module shall:

- Query external reputation services.
- Enrich extracted indicators.
- Identify known malware families.
- Retrieve malware tags.
- Provide first seen timestamps.
- Display external detection statistics.
- Improve investigator confidence.
- Continue functioning even if one provider becomes unavailable.

---

# 20.3 Supported Threat Intelligence Providers

Version 1.0 of Sentinel Demo shall integrate the following providers.

| Provider | Purpose |
|----------|---------|
| VirusTotal | File reputation and antivirus detections |
| MalwareBazaar | Malware family information |
| ThreatFox | IOC reputation (Future Ready) |
| AlienVault OTX | Threat Intelligence (Future Ready) |
| URLhaus | Malicious URL Detection (Future Ready) |
| AbuseIPDB | Malicious IP Reputation (Future Ready) |

Only VirusTotal and MalwareBazaar are mandatory for the demo implementation.

---

# 20.4 Threat Intelligence Workflow

```

Static Analysis

↓

SHA256 Generated

↓

IOC Extraction

↓

Threat Intelligence Module

↓

VirusTotal Lookup

↓

MalwareBazaar Lookup

↓

Merge Results

↓

Normalize Data

↓

Store Database

↓

Display Results

```

---

# 20.5 Query Order

To reduce unnecessary API requests, Sentinel shall follow the following lookup sequence.

### Step 1

Query SHA256 hash.

If results exist:

Continue enrichment.

If not:

Proceed to IOC lookup.

---

### Step 2

Lookup extracted Domains.

---

### Step 3

Lookup extracted IP Addresses.

---

### Step 4

Lookup extracted URLs.

---

### Step 5

Merge all available results into one investigation object.

---

# 20.6 VirusTotal Integration

## Purpose

VirusTotal provides reputation information collected from dozens of antivirus engines.

Sentinel uses VirusTotal to enrich investigations.

---

## Data Retrieved

The following information shall be collected.

Detection Ratio

Example

```
58 / 72
```

---

Malware Family

Example

```
RedLine
```

---

Threat Labels

Example

```
Trojan

Stealer

Loader
```

---

Popular Threat Classification

Example

```
Credential Stealer
```

---

File Reputation

Malicious

Suspicious

Harmless

Unknown

---

Last Analysis Date

---

File Type

---

Community Votes

---

# 20.7 VirusTotal Workflow

```

SHA256

↓

VirusTotal API

↓

Receive JSON

↓

Normalize Response

↓

Save Database

↓

Display Results

```

---

# 20.8 VirusTotal Failure Handling

If VirusTotal becomes unavailable

↓

Display

```
VirusTotal

Unavailable
```

↓

Continue Investigation

No other module shall fail because VirusTotal is unavailable.

---

# 20.9 MalwareBazaar Integration

## Purpose

MalwareBazaar provides malware family information and malware samples shared by researchers.

Unlike VirusTotal, MalwareBazaar focuses specifically on malware.

---

## Retrieved Information

Malware Family

First Seen

Last Seen

Tags

File Type

Uploader

Threat Category

SHA256

Download Availability

---

Example

```

Family

RedLine

Tags

Stealer

Credential Theft

Windows

```

---

# 20.10 MalwareBazaar Workflow

```

SHA256

↓

MalwareBazaar API

↓

Receive JSON

↓

Normalize

↓

Store Database

↓

Display

```

---

# 20.11 Future Integrations

The architecture shall allow additional providers without changing existing modules.

Supported future providers include

ThreatFox

AlienVault OTX

URLhaus

AbuseIPDB

MISP

OpenCTI

Each provider shall implement the same interface.

```

lookup_hash()

lookup_ip()

lookup_domain()

lookup_url()

```

This abstraction allows adding providers without modifying other services.

---

# 20.12 Threat Intelligence Normalization

Every provider returns different JSON formats.

Sentinel shall convert all provider responses into one internal model.

```

ThreatResult

Provider

Indicator

IndicatorType

Reputation

Confidence

MalwareFamily

Tags

FirstSeen

LastSeen

RawJSON

```

This prevents UI and reporting modules from depending on provider-specific APIs.

---

# 20.13 Caching

Repeated requests waste API quotas.

The Threat Intelligence Module shall cache responses.

Default cache duration

24 Hours

If the same SHA256 is investigated again

↓

Use cached result

↓

Skip API request

---

# 20.14 API Rate Limiting

Free API plans have request limits.

The module shall

Queue requests

Retry after timeout

Respect provider limits

Log quota exhaustion

Display warning when limits are exceeded.

---

# 20.15 Threat Intelligence Screen

```

---------------------------------------------------------

Threat Intelligence

---------------------------------------------------------

VirusTotal

58 / 72

Malicious

---------------------------------------------------------

MalwareBazaar

Family

RedLine

First Seen

2026-01-18

---------------------------------------------------------

Threat Tags

Stealer

Credential Theft

Loader

---------------------------------------------------------

```

---

# 20.16 Threat Intelligence Summary

At the bottom of the page Sentinel shall display a concise summary.

Example

```

Threat Intelligence Summary

The uploaded sample is known to the global cybersecurity community.

VirusTotal reports detection by 58 security vendors.

MalwareBazaar identifies the malware family as RedLine.

The sample has been associated with credential theft campaigns.

```

---

# 20.17 Functional Requirements

### FR-020

The system shall query VirusTotal using the calculated SHA256.

---

### FR-021

The system shall query MalwareBazaar using the calculated SHA256.

---

### FR-022

The system shall normalize provider responses into a unified format.

---

### FR-023

The system shall cache threat intelligence results.

---

### FR-024

The system shall continue analysis even if external APIs are unavailable.

---

### FR-025

The system shall display provider-specific information separately.

---

### FR-026

The system shall include threat intelligence in generated reports.

---

### FR-027

The system shall log all failed API requests.

---

### FR-028

The system shall support adding new providers through a modular interface.

---

# 20.18 Error Handling

Possible errors include

- API timeout
- Invalid API key
- Daily quota exceeded
- Internet unavailable
- Provider maintenance

None of these errors shall stop the investigation.

Instead Sentinel shall display

```

Threat Intelligence

Unavailable

Reason

API Timeout

```

and continue generating the investigation report using locally available evidence.

---

# 20.19 Design Decision

Threat Intelligence is classified as an **Optional Enrichment Module**.

Core investigation features

- Upload
- Static Analysis
- IOC Extraction
- Risk Scoring
- MITRE Mapping
- Report Generation

must continue to function without internet connectivity.

External threat intelligence enhances investigations but shall never become a mandatory dependency.

# 21. Risk Scoring Engine

## 21.1 Overview

The Risk Scoring Engine is responsible for assigning an overall threat score to every uploaded sample.

Unlike machine learning-based scoring systems, Sentinel uses a deterministic, evidence-driven rule engine. Every point added to the final score must be traceable to observed evidence.

The objective is to ensure that investigators understand **why** a sample received a particular risk score.

The AI module does **not** calculate the score. AI only explains it.

---

# 21.2 Objectives

The Risk Scoring Engine shall:

- Produce a consistent score for identical evidence.
- Be transparent and explainable.
- Avoid AI hallucinations.
- Support future rule additions.
- Assign severity levels.
- Generate confidence values.
- Provide evidence for every score.

---

# 21.3 Risk Scale

Every investigation receives a score between **0 and 100**.

| Score | Severity |
|--------|----------|
| 0–20 | Informational |
| 21–40 | Low |
| 41–60 | Medium |
| 61–80 | High |
| 81–100 | Critical |

---

# 21.4 Risk Categories

Evidence is grouped into five categories.

## Category 1 – File Characteristics

Examples

- Packed executable
- High entropy
- Invalid signature
- Embedded executable
- Obfuscated script

---

## Category 2 – Static Indicators

Examples

- Dangerous imports
- Dangerous permissions
- Embedded JavaScript
- Office macros
- Suspicious strings

---

## Category 3 – Threat Intelligence

Examples

- VirusTotal detections
- MalwareBazaar match
- Malware family identified
- Malicious reputation
- Known campaign

---

## Category 4 – IOC Reputation

Examples

- Known malicious domain
- Known malicious IP
- URLhaus match
- ThreatFox IOC
- AbuseIPDB reputation

---

## Category 5 – Behavioral Indicators

(Reserved for future CAPE Sandbox integration.)

Examples

- Process Injection
- Registry Persistence
- Service Creation
- Network Beaconing
- Payload Download

---

# 21.5 Rule Table

Every rule contributes predefined points.

## File Rules

| Rule | Score |
|------|------:|
| Packed Executable | +12 |
| High Entropy | +8 |
| Unsigned Executable | +10 |
| Embedded Executable | +15 |
| Multiple Resources | +5 |

---

## Windows Rules

| Rule | Score |
|------|------:|
| CreateRemoteThread Import | +12 |
| WriteProcessMemory Import | +10 |
| VirtualAlloc Import | +8 |
| WinExec Import | +6 |
| URLDownloadToFile Import | +12 |

---

## Android Rules

| Rule | Score |
|------|------:|
| SEND_SMS Permission | +12 |
| READ_SMS Permission | +10 |
| RECEIVE_BOOT_COMPLETED | +8 |
| SYSTEM_ALERT_WINDOW | +12 |
| REQUEST_INSTALL_PACKAGES | +10 |

---

## Office Rules

| Rule | Score |
|------|------:|
| VBA Macro | +20 |
| AutoOpen Macro | +18 |
| PowerShell Execution | +15 |
| Embedded EXE | +20 |

---

## PDF Rules

| Rule | Score |
|------|------:|
| Embedded JavaScript | +12 |
| Launch Action | +18 |
| Embedded File | +10 |
| OpenAction | +8 |

---

## Threat Intelligence Rules

| Rule | Score |
|------|------:|
| VirusTotal > 30 detections | +20 |
| VirusTotal > 50 detections | +25 |
| MalwareBazaar Match | +20 |
| Malware Family Identified | +15 |
| Known Malware Campaign | +15 |

---

## IOC Rules

| Rule | Score |
|------|------:|
| Malicious Domain | +10 |
| Malicious IP | +10 |
| Known C2 Server | +15 |
| URLhaus Match | +15 |

---

# 21.6 Maximum Score

The calculated score may exceed 100 internally.

However, the displayed score shall never exceed **100**.

Example

Calculated Score

114

↓

Displayed Score

100

---

# 21.7 Confidence Score

Sentinel also produces a confidence value.

Confidence indicates the reliability of the assessment.

Factors include

- Number of supporting indicators
- Threat intelligence agreement
- Rule consistency
- Data completeness

Example

```
Risk Score

87

Confidence

95%
```

---

# 21.8 Explainability

Every score must include justification.

Example

```
Final Risk Score

87

Reason

✔ Packed executable

✔ High entropy

✔ VirusTotal detection

✔ MalwareBazaar match

✔ Dangerous imports

✔ Known malware family
```

The investigator should never wonder where the score came from.

---

# 21.9 Risk Calculation Example

Sample

invoice.exe

Evidence

Packed Executable

+12

Unsigned

+10

High Entropy

+8

CreateRemoteThread

+12

VirusTotal 58/72

+25

MalwareBazaar Match

+20

Total

87

Severity

Critical

---

# 21.10 Risk Gauge

The investigation page shall include a visual gauge.

```
0-------------------------------100

███████████████████████

87

CRITICAL
```

The gauge provides investigators with an immediate understanding of severity.

---

# 21.11 Functional Requirements

### FR-029

The system shall calculate a rule-based risk score.

---

### FR-030

The score shall range from 0 to 100.

---

### FR-031

Every point shall be traceable to supporting evidence.

---

### FR-032

The system shall calculate a confidence value.

---

### FR-033

The UI shall display both score and severity.

---

### FR-034

The AI module shall not modify the calculated score.

---

### FR-035

The report shall include the score explanation.

---

# 22. MITRE ATT&CK Mapping

## 22.1 Overview

MITRE ATT&CK is the industry-standard framework for describing attacker behavior.

Sentinel maps observed malware characteristics to ATT&CK tactics and techniques, helping investigators understand **how** a sample behaves instead of only **what** it contains.

This mapping is entirely rule-based.

---

# 22.2 Objectives

The MITRE module shall

- Standardize behavioral descriptions.
- Improve report quality.
- Align investigations with industry terminology.
- Support intelligence sharing.

---

# 22.3 Mapping Workflow

```
Static Analysis

↓

Rule Engine

↓

Observed Behavior

↓

Technique Matching

↓

MITRE Technique

↓

Display

↓

Report
```

---

# 22.4 Mapping Rules

Example mappings include:

| Observation | MITRE Technique |
|-------------|-----------------|
| Process Injection APIs | T1055 |
| PowerShell Execution | T1059.001 |
| Command Shell Usage | T1059.003 |
| Registry Run Keys | T1547 |
| Scheduled Task | T1053 |
| DLL Side Loading | T1574 |
| Credential Dumping | T1003 |
| Masquerading | T1036 |
| Obfuscated Files | T1027 |

---

# 22.5 Technique Details

Each technique card shall include:

- Technique ID
- Technique Name
- Description
- Evidence
- Confidence

Example

```
Technique

T1027

Name

Obfuscated Files or Information

Description

The malware uses obfuscation to evade analysis.

Evidence

High entropy

Packed executable

Confidence

94%
```

---

# 22.6 ATT&CK Tactics

Sentinel groups techniques into tactics.

Examples

- Initial Access
- Execution
- Persistence
- Privilege Escalation
- Defense Evasion
- Credential Access
- Discovery
- Lateral Movement
- Collection
- Command and Control
- Exfiltration
- Impact

---

# 22.7 MITRE Timeline

Investigators shall view techniques in attack order.

```
Execution

↓

Persistence

↓

Defense Evasion

↓

Credential Access

↓

Command & Control
```

This helps investigators visualize attacker progression.

---

# 22.8 Investigation Screen

```
---------------------------------------------------

MITRE ATT&CK

---------------------------------------------------

T1027

Obfuscated Files

High Confidence

-----------------------------------------

T1055

Process Injection

Medium Confidence

-----------------------------------------

T1547

Registry Run Keys

High Confidence

---------------------------------------------------
```

---

# 22.9 Functional Requirements

### FR-036

The system shall automatically map supported behaviors to MITRE ATT&CK techniques.

---

### FR-037

Every mapping shall include supporting evidence.

---

### FR-038

The report shall include an ATT&CK section.

---

### FR-039

Mappings shall be deterministic and rule-based.

---

### FR-040

The UI shall display techniques grouped by ATT&CK tactic.

---
# 23. AI Investigation Engine (Gemini)

## 23.1 Overview

The AI Investigation Engine transforms technical malware analysis into investigator-friendly language.

Unlike traditional malware analysis platforms that display raw technical data, Sentinel uses Google's Gemini API to generate concise, evidence-based investigation summaries.

The AI **does not perform malware analysis**.

Instead, it explains the results generated by the previous modules.

This distinction is critical.

Sentinel's AI is an explanation engine, not a decision engine.

---

# 23.2 Objectives

The AI module shall

- Explain technical findings in simple language.
- Summarize the investigation.
- Highlight important evidence.
- Recommend next investigation steps.
- Avoid speculation.
- Never invent evidence.
- Never override the Risk Engine.

---

# 23.3 AI Input

The AI only receives structured data produced by Sentinel.

Example Input

```json
{
  "filename":"invoice.exe",
  "sha256":"ABC123...",
  "risk_score":87,
  "severity":"Critical",
  "malware_family":"RedLine",
  "virustotal":"58/72",
  "permissions":[...],
  "imports":[...],
  "iocs":[...],
  "mitre":[...]
}
```

The AI never receives the uploaded file itself.

---

# 23.4 AI Output

Gemini generates

- Investigation Summary
- Executive Summary
- Technical Explanation
- Threat Assessment
- Evidence Summary
- Recommended Actions

---

# 23.5 Investigation Summary

Example

> The uploaded executable demonstrates several characteristics commonly associated with credential-stealing malware.

> Static analysis identified process injection APIs and high entropy, suggesting packing or obfuscation.

> External threat intelligence confirms that the sample has previously been observed and identified as the RedLine malware family.

> Based on the available evidence, the sample presents a Critical risk to affected systems.

---

# 23.6 Executive Summary

This section is intended for senior officers.

Maximum length

150 words

Contents

- Overall conclusion
- Risk level
- Recommended action

---

Example

> Sentinel classifies this sample as **Critical Risk**.

> The executable shares characteristics with known credential-stealing malware and has been identified by multiple threat intelligence providers.

> Immediate isolation and forensic preservation are recommended.

---

# 23.7 Technical Explanation

This section explains

Why Sentinel assigned the score.

Example

The executable

• is packed

• contains suspicious imports

• lacks a digital signature

• was detected by 58 antivirus engines

• matches the RedLine malware family

These findings collectively produced a Critical Risk score.

---

# 23.8 Threat Assessment

The AI summarizes

Potential objective

Possible capabilities

Observed behaviors

Confidence

Example

Potential Objective

Credential Theft

Capabilities

Credential harvesting

Persistence

Command and Control

Confidence

High

---

# 23.9 Evidence Summary

The AI shall summarize evidence.

Example

Evidence Identified

✓ Packed executable

✓ High entropy

✓ Process injection APIs

✓ VirusTotal detection

✓ MalwareBazaar match

✓ Credential theft indicators

---

# 23.10 Recommendations

Recommendations are generated from predefined templates.

The AI selects applicable recommendations.

Example

Immediate Actions

• Isolate affected system

• Preserve evidence

• Block malicious domains

• Monitor network traffic

• Scan similar endpoints

---

# 23.11 Prompt Design

System Prompt

```
You are a malware investigation assistant.

Only explain the supplied evidence.

Never fabricate information.

Never invent malware behavior.

If evidence is unavailable, explicitly state that the information could not be determined.

Write in language suitable for police investigators.
```

---

User Prompt

```
Generate an investigation report using the supplied JSON.

Explain findings.

Summarize evidence.

Describe overall risk.

Recommend next investigation steps.

Avoid speculation.
```

---

# 23.12 AI Safety Rules

Gemini shall never

- Invent malware names.
- Guess malware capabilities.
- Create fake IOCs.
- Override calculated scores.
- Modify MITRE mappings.
- Produce unsupported conclusions.

---

If evidence is insufficient

Gemini shall respond

```
Available evidence is insufficient to determine additional malware behavior.

Further dynamic analysis is recommended.
```

---

# 23.13 AI Confidence

Every AI summary includes confidence.

Example

```
AI Confidence

96%
```

Confidence depends upon

- Number of supporting findings
- Threat Intelligence agreement
- Rule Engine confidence

---

# 23.14 Investigation Screen

```
-----------------------------------------------------

AI Investigation Summary

-----------------------------------------------------

Overall Assessment

Critical

-----------------------------------------

Summary

-----------------------------------------

Threat Assessment

-----------------------------------------

Evidence Summary

-----------------------------------------

Recommendations

-----------------------------------------------------
```

---

# 23.15 Functional Requirements

### FR-041

The AI shall generate an executive summary.

---

### FR-042

The AI shall generate a technical explanation.

---

### FR-043

The AI shall summarize supporting evidence.

---

### FR-044

The AI shall recommend investigator actions.

---

### FR-045

The AI shall never fabricate evidence.

---

### FR-046

The AI shall never override Sentinel's Risk Score.

---

### FR-047

The AI shall never modify MITRE ATT&CK mappings.

---

### FR-048

The AI output shall be included in every exported report.

---

# 24. Investigation Timeline

## 24.1 Purpose

The Investigation Timeline provides investigators with a chronological view of every action performed during analysis.

This improves transparency and allows investigators to verify the sequence of events.

---

# 24.2 Timeline Events

The timeline shall include

File Uploaded

↓

Hashes Generated

↓

Static Analysis Completed

↓

IOC Extraction Completed

↓

Threat Intelligence Retrieved

↓

Risk Score Calculated

↓

MITRE Mapping Completed

↓

AI Summary Generated

↓

Report Generated

---

# 24.3 Example Timeline

```
10:15

File Uploaded

---------------------------------

10:15

SHA256 Generated

---------------------------------

10:16

Static Analysis Complete

---------------------------------

10:16

IOC Extraction Complete

---------------------------------

10:17

VirusTotal Lookup Complete

---------------------------------

10:17

MalwareBazaar Lookup Complete

---------------------------------

10:18

Risk Score Generated

---------------------------------

10:18

MITRE Mapping Complete

---------------------------------

10:19

AI Investigation Generated

---------------------------------

10:20

Report Exported
```

---

# 24.4 Investigation Evidence Panel

Every finding shall contain evidence.

Example

```
Finding

Packed Executable

Severity

High

Evidence

Section entropy 7.92

Reason

Executable appears compressed using a packer.
```

Investigators should always be able to trace findings back to observable evidence.

---

# 24.5 Investigation Status

Possible statuses

Queued

Analyzing

Waiting for Threat Intelligence

Generating Report

Completed

Failed

---

# 24.6 Functional Requirements

### FR-049

The system shall display an investigation timeline.

---

### FR-050

Every completed module shall create a timeline event.

---

### FR-051

Timeline entries shall include timestamps.

---

### FR-052

The report shall include the investigation timeline.

---
# 25. Report Generation Module

## 25.1 Overview

The Report Generation Module is the final stage of the Sentinel investigation workflow.

After all analysis modules complete successfully, Sentinel consolidates every finding into a structured investigation report suitable for police investigations, digital forensics documentation, academic demonstrations, and evidence preservation.

The report must be professional, standardized, and easy to understand by both technical and non-technical investigators.

Every report generated by Sentinel shall be reproducible from the stored investigation data.

---

# 25.2 Objectives

The Report Module shall

- Produce investigator-friendly reports.
- Include all evidence collected during analysis.
- Support multiple export formats.
- Preserve investigation integrity.
- Generate reports without requiring internet access.
- Include AI explanations alongside technical evidence.

---

# 25.3 Supported Export Formats

The demo version shall support

✓ PDF

✓ HTML

✓ CSV

✓ JSON

Future versions may additionally support

DOCX

RTF

Markdown

MISP Export

STIX 2.1

---

# 25.4 Report Structure

Every report follows the same standardized structure.

```
Cover Page

↓

Executive Summary

↓

Case Information

↓

File Identification

↓

Hash Values

↓

Static Analysis

↓

IOC Extraction

↓

Threat Intelligence

↓

Risk Assessment

↓

MITRE ATT&CK

↓

AI Investigation Summary

↓

Recommendations

↓

Appendix
```

---

# 25.5 Cover Page

Example

```
--------------------------------------------------

SENTINEL

Digital Malware Investigation Report

--------------------------------------------------

Case ID

CASE-2026-000127

Investigator

Guest Session

Generated

17 July 2026

Risk Level

CRITICAL

--------------------------------------------------
```

---

# 25.6 Executive Summary

This section should fit on one page.

Contents

- Investigation objective
- File analyzed
- Final verdict
- Overall risk
- AI summary

---

# 25.7 Case Information

Fields

Case ID

Investigation ID

Upload Time

Analysis Time

Investigator Name

Session ID

Investigation Status

---

# 25.8 File Information

Display

Filename

Extension

Size

Architecture

Platform

MIME Type

Magic Bytes

Entropy

---

# 25.9 Hash Section

Display

MD5

SHA1

SHA256

SHA512

These values shall always appear together.

---

# 25.10 Static Analysis Section

Include

Metadata

Imports

Exports

Sections

Resources

Permissions

Certificate

Compiler

Security Findings

---

# 25.11 IOC Section

Include

Domains

IP Addresses

URLs

Email Addresses

Registry Keys

Mutexes

File Paths

Wallet Addresses

Each IOC shall include

Confidence

Evidence

Source

---

# 25.12 Threat Intelligence

Display

VirusTotal

MalwareBazaar

Detection Ratio

Malware Family

Threat Tags

First Seen

Last Seen

Provider Status

---

# 25.13 Risk Assessment

Display

Overall Score

Severity

Confidence

Score Breakdown

Example

```
Risk Score

87

Critical

Confidence

95%

Reason

Packed Executable

Unsigned Binary

Known Malware

Dangerous Imports

Malicious Reputation
```

---

# 25.14 MITRE ATT&CK

Display

Technique ID

Technique Name

Confidence

Evidence

Description

---

# 25.15 AI Summary

Include

Executive Summary

Technical Summary

Threat Assessment

Recommendations

Confidence

---

# 25.16 Recommendations

Example

Immediate Actions

• Isolate affected machine

• Preserve forensic evidence

• Block malicious domains

• Scan similar endpoints

• Review firewall logs

---

# 25.17 Investigation Timeline

Display chronological events.

```
10:12 Upload

↓

10:13 Static Analysis

↓

10:14 IOC Extraction

↓

10:15 VirusTotal

↓

10:15 MalwareBazaar

↓

10:16 Risk Engine

↓

10:17 MITRE

↓

10:18 AI

↓

10:19 Report
```

---

# 25.18 Appendix

Include

Raw JSON

Complete IOC List

Complete Imports

Complete Permissions

Complete MITRE List

Raw Threat Intelligence Response

---

# 25.19 Functional Requirements

### FR-053

The system shall generate PDF reports.

---

### FR-054

The system shall generate HTML reports.

---

### FR-055

The system shall generate CSV reports.

---

### FR-056

The system shall generate JSON reports.

---

### FR-057

Reports shall include every completed module.

---

### FR-058

Reports shall include AI summaries.

---

### FR-059

Reports shall include timestamps.

---

### FR-060

Reports shall include evidence supporting every conclusion.

---

# 26. Database Design

## 26.1 Overview

The Sentinel Demo uses SQLite.

SQLite is selected because

- Zero configuration
- Easy deployment
- Suitable for demonstrations
- Fast enough for single-user investigations

Future versions may migrate to PostgreSQL.

---

# 26.2 Entity Relationship Diagram

```
Cases

│

├──────── Evidence

│

├──────── Investigations

│

├──────── StaticAnalysis

│

├──────── IOCs

│

├──────── ThreatIntel

│

├──────── RiskScores

│

├──────── MITREMappings

│

└──────── Reports
```

---

# 26.3 Cases Table

| Column | Type |
|----------|---------|
| id | INTEGER |
| case_number | TEXT |
| created_at | DATETIME |
| investigator | TEXT |
| status | TEXT |

---

# 26.4 Evidence Table

| Column | Type |
|----------|---------|
| id | INTEGER |
| case_id | INTEGER |
| filename | TEXT |
| sha256 | TEXT |
| size | INTEGER |
| mime | TEXT |

---

# 26.5 Static Analysis Table

Contains

Metadata

Sections

Imports

Resources

Permissions

Certificate

Entropy

Compiler

---

# 26.6 IOC Table

Contains

Type

Value

Confidence

Source

---

# 26.7 Threat Intelligence Table

Contains

Provider

Family

Detection Ratio

Tags

Confidence

Raw JSON

---

# 26.8 Risk Score Table

Contains

Score

Severity

Confidence

Reason

---

# 26.9 MITRE Table

Contains

Technique

Description

Evidence

Confidence

---

# 26.10 Reports Table

Contains

Format

Location

Generated Time

Status

---

# 27. REST API Specification

## Overview

Sentinel exposes REST APIs consumed by the React frontend.

Base URL

```
/api/v1
```

---

## Upload

POST

```
/upload
```

Response

```json
{
  "investigation_id":12,
  "status":"uploaded"
}
```

---

## Investigation

GET

```
/investigations/{id}
```

---

## Static Analysis

GET

```
/investigations/{id}/static
```

---

## IOC

GET

```
/investigations/{id}/iocs
```

---

## Threat Intelligence

GET

```
/investigations/{id}/threat-intelligence
```

---

## Risk Score

GET

```
/investigations/{id}/risk
```

---

## MITRE

GET

```
/investigations/{id}/mitre
```

---

## AI Summary

GET

```
/investigations/{id}/summary
```

---

## Reports

POST

```
/reports/{id}/generate
```

---

GET

```
/reports/{id}/download
```

---

## Health Check

GET

```
/health
```

Returns

```json
{
  "status":"healthy"
}
```

---

# 28. Error Handling

The API shall return standardized error responses.

Example

```json
{
  "success":false,
  "error":"VirusTotal quota exceeded",
  "code":"VT_QUOTA_EXCEEDED"
}
```

No internal stack traces shall be exposed to the frontend.

---

# 29. Logging

Sentinel shall maintain logs for

Application Events

API Requests

Analysis Results

Threat Intelligence Calls

Errors

Report Generation

Log levels

INFO

WARNING

ERROR

CRITICAL

---

# 30. Project Folder Structure

```
Sentinel/

│

├── backend/

│ ├── api/

│ ├── models/

│ ├── services/

│ ├── static_analysis/

│ ├── ioc/

│ ├── threat_intel/

│ ├── risk_engine/

│ ├── mitre/

│ ├── ai/

│ ├── reports/

│ ├── database/

│ ├── utils/

│ └── config/

│

├── frontend/

│ ├── src/

│ ├── pages/

│ ├── components/

│ ├── hooks/

│ ├── assets/

│ └── services/

│

├── uploads/

├── reports/

├── logs/

├── tests/

├── docs/

└── README.md
```

---
# 31. Non-Functional Requirements (NFR)

## 31.1 Overview

While the Functional Requirements define **what Sentinel should do**, the Non-Functional Requirements define **how well Sentinel should perform**.

The goal is to ensure the application remains responsive, reliable, maintainable, and suitable for demonstration in front of evaluators and police investigators.

---

# 31.2 Performance Requirements

### NFR-001

The application shall load the dashboard within **3 seconds** under normal conditions.

---

### NFR-002

A file upload shall begin processing within **2 seconds** after successful upload.

---

### NFR-003

Static analysis of a normal executable (<50 MB) shall complete within **30 seconds**.

---

### NFR-004

Threat Intelligence lookups shall timeout after **15 seconds** if an external provider is unavailable.

---

### NFR-005

Report generation shall complete within **10 seconds** after analysis finishes.

---

### NFR-006

The frontend shall remain responsive while analysis is running.

A progress indicator must be displayed.

---

# 31.3 Reliability

### NFR-007

The application shall never terminate unexpectedly because an external API failed.

---

### NFR-008

Every investigation shall automatically save its progress.

---

### NFR-009

Partial investigation data shall remain accessible even if analysis stops midway.

---

### NFR-010

The Report Generator shall still work even if Threat Intelligence providers are unavailable.

---

# 31.4 Security Requirements

Although authentication is excluded from the demo, basic security practices shall still be followed.

---

### NFR-011

Uploaded files shall never be executed by the backend.

---

### NFR-012

Uploaded files shall be stored outside the web root.

---

### NFR-013

Every uploaded file shall receive a randomly generated storage name.

Example

```
uploads/

93f7b812-acde-4ab2-91a2.exe
```

instead of

```
invoice.exe
```

---

### NFR-014

Only metadata and analysis results shall be shown to users.

Raw files shall never be exposed through public URLs.

---

### NFR-015

API keys shall never be hardcoded.

Configuration shall use

```
.env
```

Example

```
VT_API_KEY=

MB_API_KEY=

GEMINI_API_KEY=
```

---

### NFR-016

The frontend shall never directly communicate with external APIs.

All requests must pass through the FastAPI backend.

---

# 31.5 Maintainability

### NFR-017

Every analysis module shall be independent.

Replacing one module must not require modifications to other modules.

---

### NFR-018

Threat Intelligence providers shall implement a common interface.

Example

```python
lookup_hash()

lookup_domain()

lookup_ip()

lookup_url()
```

---

### NFR-019

Every service shall contain a single responsibility.

Examples

```
StaticAnalysisService

RiskEngine

ThreatIntelService

MITREMapper

GeminiService
```

---

### NFR-020

Business logic shall never exist inside frontend components.

---

# 31.6 Scalability

The architecture should allow future expansion.

Future versions may include

- PostgreSQL
- Redis
- Docker
- CAPE Sandbox
- MISP
- OpenCTI
- Multi-user support

The demo architecture shall not prevent these upgrades.

---

# 31.7 Availability

If an external service becomes unavailable

VirusTotal

↓

Unavailable

↓

Continue Investigation

---

MalwareBazaar

↓

Unavailable

↓

Continue Investigation

---

Gemini

↓

Unavailable

↓

Generate Report Without AI Summary

---

The application shall always prioritize completing investigations.

---

# 31.8 Compatibility

Supported Browsers

- Chrome
- Edge
- Firefox

Operating Systems

- Windows 10
- Windows 11

Backend

- Linux compatible

---

# 31.9 Accessibility

The application shall

- Use readable fonts.
- Maintain consistent spacing.
- Support keyboard navigation.
- Display meaningful icons.
- Avoid information overload.

---

# 32. Testing Strategy

## 32.1 Overview

Testing ensures every module behaves correctly before demonstration.

Testing shall occur after every completed development phase.

---

# 32.2 Unit Testing

Each backend service shall include unit tests.

Examples

Upload Service

Hash Service

Static Analysis

IOC Extraction

Risk Engine

MITRE Mapper

Threat Intelligence

Gemini Prompt Builder

---

Expected Coverage

Minimum

80%

---

# 32.3 Integration Testing

Verify interactions between modules.

Example

```
Upload

↓

Static Analysis

↓

IOC Extraction

↓

Threat Intelligence

↓

Risk Engine
```

Expected

Data flows correctly.

---

# 32.4 API Testing

Every REST endpoint shall be tested.

Examples

POST

```
/upload
```

GET

```
/investigations/12
```

GET

```
/risk
```

POST

```
/reports/generate
```

Expected

Correct status codes.

Correct JSON.

Correct validation.

---

# 32.5 UI Testing

Verify

Buttons

Navigation

Loading indicators

Progress bars

Search

Sorting

Report downloads

---

# 32.6 Threat Intelligence Testing

Scenario 1

VirusTotal Online

Expected

Results displayed.

---

Scenario 2

VirusTotal Offline

Expected

Application continues.

---

Scenario 3

Invalid API Key

Expected

Proper warning shown.

---

Scenario 4

Daily Quota Exceeded

Expected

Threat Intelligence marked unavailable.

---

# 32.7 Report Testing

Verify all formats.

PDF

HTML

CSV

JSON

Each report should contain

✓ Static Analysis

✓ IOCs

✓ Threat Intelligence

✓ Risk Score

✓ MITRE

✓ AI Summary

---

# 32.8 Demo Testing Checklist

Before presentation verify

□ Upload works

□ Dashboard loads

□ Analysis completes

□ VirusTotal connected

□ MalwareBazaar connected

□ Gemini working

□ Reports download

□ MITRE displayed

□ Risk score visible

□ Timeline complete

---

# 33. Development Phases

Development follows an incremental approach.

---

## Phase 1

Project Setup

Deliverables

- FastAPI
- React
- SQLite
- Folder Structure
- Upload Module

---

## Phase 2

Static Analysis

Deliverables

- EXE Analysis
- APK Analysis
- PDF Analysis
- Office Analysis

---

## Phase 3

IOC Extraction

Deliverables

- Regex Engine
- IOC Database
- IOC Viewer

---

## Phase 4

Threat Intelligence

Deliverables

- VirusTotal Integration
- MalwareBazaar Integration
- Caching
- API Error Handling

---

## Phase 5

Risk Engine

Deliverables

- Rule Engine
- Confidence Score
- Risk Gauge

---

## Phase 6

MITRE ATT&CK

Deliverables

- Mapping Engine
- Technique Cards
- Timeline

---

## Phase 7

Gemini AI

Deliverables

- AI Summary
- Executive Summary
- Recommendations

---

## Phase 8

Report Generator

Deliverables

PDF

HTML

CSV

JSON

---

## Phase 9

UI Polish

Deliverables

Animations

Icons

Dashboard

Charts

Investigation Timeline

---

## Phase 10

Demo Preparation

Deliverables

Testing

Bug Fixes

Presentation

Sample Files

Final Report

---
# 34. Acceptance Criteria

## 34.1 Overview

The Sentinel Demo shall be considered complete only when every mandatory feature defined in this PRD has been implemented and successfully demonstrated.

Acceptance criteria provide measurable conditions for determining whether the project satisfies its objectives.

The demo should require **no manual intervention** during a normal investigation workflow.

---

# 34.2 Functional Acceptance

## Upload Module

### AC-001

The investigator can upload a supported file.

**Expected Result**

The upload completes successfully.

---

### AC-002

Unsupported file types are rejected.

**Expected Result**

An error message explains why the file cannot be processed.

---

### AC-003

Hashes are generated automatically.

**Expected Result**

MD5

SHA1

SHA256

SHA512

are displayed.

---

## Static Analysis

### AC-004

The correct analyzer is selected automatically.

Example

```
invoice.exe

↓

PE Analyzer
```

---

### AC-005

Static analysis produces findings.

Expected

Metadata

Security Findings

Imports

Sections

Certificate

Entropy

---

### AC-006

Evidence is attached to every finding.

Example

```
Finding

Packed Executable

Evidence

Entropy 7.93
```

---

## IOC Extraction

### AC-007

The system extracts indicators automatically.

Supported indicators

✓ Domains

✓ URLs

✓ IP Addresses

✓ Registry Keys

✓ Hashes

✓ Wallet Addresses

✓ Email Addresses

---

### AC-008

Duplicate IOCs are removed.

---

### AC-009

Confidence is assigned to every IOC.

---

## Threat Intelligence

### AC-010

VirusTotal lookup succeeds using SHA256.

---

### AC-011

MalwareBazaar lookup succeeds.

---

### AC-012

Failure of one provider does not stop the investigation.

---

### AC-013

Threat Intelligence results are cached.

---

## Risk Engine

### AC-014

Risk Score is generated.

---

### AC-015

Every score includes evidence.

---

### AC-016

Severity matches score.

Example

```
82

↓

Critical
```

---

## MITRE

### AC-017

Techniques are mapped automatically.

---

### AC-018

Each mapping includes evidence.

---

## Gemini AI

### AC-019

Executive Summary generated.

---

### AC-020

Technical Summary generated.

---

### AC-021

Recommendations generated.

---

### AC-022

AI never invents unsupported evidence.

---

## Report Generator

### AC-023

PDF report generated.

---

### AC-024

HTML report generated.

---

### AC-025

CSV report generated.

---

### AC-026

JSON report generated.

---

### AC-027

Generated reports include

✓ Static Analysis

✓ IOC Extraction

✓ Threat Intelligence

✓ Risk Score

✓ MITRE

✓ AI Summary

---

# 35. Demonstration Plan

## Purpose

The demonstration should showcase the complete investigation workflow in less than ten minutes.

The evaluator should understand the system without requiring cybersecurity expertise.

---

## Demo Dataset

Prepare the following samples before the presentation.

### Windows

Benign EXE

Malicious EXE

DLL

---

### Android

Benign APK

Malicious APK

---

### Documents

Macro-enabled DOCM

PDF containing JavaScript

---

### Scripts

PowerShell

Batch

JavaScript

---

## Demonstration Flow

### Step 1

Open Sentinel Dashboard.

Explain the objective of the platform.

Time

30 seconds

---

### Step 2

Upload a suspicious executable.

Time

20 seconds

---

### Step 3

Show automatic hash generation.

Explain digital evidence preservation.

Time

20 seconds

---

### Step 4

Open Static Analysis.

Explain

Imports

Sections

Metadata

Security Findings

Time

90 seconds

---

### Step 5

Open IOC Extraction.

Explain

Domains

IPs

URLs

Registry Keys

Time

60 seconds

---

### Step 6

Open Threat Intelligence.

Explain

VirusTotal

MalwareBazaar

Detection Ratio

Malware Family

Time

60 seconds

---

### Step 7

Open Risk Assessment.

Explain

Risk Score

Confidence

Severity

Evidence

Time

60 seconds

---

### Step 8

Open MITRE ATT&CK.

Explain

Observed attacker techniques.

Time

60 seconds

---

### Step 9

Open AI Summary.

Explain

Investigator-friendly explanation.

Time

60 seconds

---

### Step 10

Generate PDF report.

Download report.

Explain that the report can be attached to an investigation case.

Time

30 seconds

---

# 36. Future Roadmap

The demo is intentionally limited in scope.

Future versions of Sentinel should include enterprise capabilities while preserving the same modular architecture.

---

## Phase 2

### Authentication

JWT

Role-Based Access Control

Police Investigator Accounts

Admin Dashboard

---

### Case Management

Case Assignment

Evidence Chain

Notes

Tags

Search

---

### Dynamic Analysis

CAPE Sandbox

Behavioral Analysis

Network Traffic

Memory Dumps

Process Tree

Persistence Detection

---

### Threat Intelligence Expansion

ThreatFox

AlienVault OTX

AbuseIPDB

URLhaus

OpenCTI

MISP

Hybrid Analysis

ANY.RUN

---

### Correlation Engine

Case Correlation

Shared IOCs

Malware Family Correlation

Campaign Detection

Timeline Correlation

---

### Recommendation Engine

Automated containment suggestions

IOC blocking recommendations

Firewall recommendations

EDR recommendations

---

### Dashboard Improvements

Threat Heatmaps

MITRE Matrix Visualization

IOC Graph

Campaign Graph

Timeline Charts

Investigation Statistics

---

### Collaboration

Multiple Investigators

Comments

Case Sharing

Evidence Locking

Audit Logs

---

### Scalability

PostgreSQL

Redis

Docker

Kubernetes

Background Workers

Task Queue

Cloud Storage

---

### AI Improvements

Offline LLM Support

RAG Knowledge Base

Historical Case Search

Malware Similarity Search

Conversational Investigation Assistant

---

# 37. Risks and Mitigations

| Risk | Impact | Mitigation |
|-------|--------|------------|
| VirusTotal quota exhausted | Medium | Cache responses and continue analysis |
| MalwareBazaar unavailable | Low | Continue investigation without enrichment |
| Gemini unavailable | Medium | Generate report without AI summary |
| Large file upload | Medium | Enforce configurable upload size limits |
| Unsupported file format | Low | Display clear validation message |
| Corrupted file | Medium | Stop analysis gracefully and log error |

---

# 38. Appendix A – Configuration

Example `.env`

```text
DATABASE_URL=sqlite:///sentinel.db

VT_API_KEY=xxxxxxxxxxxxxxxx

MALWAREBAZAAR_API_KEY=xxxxxxxxxxxxxxxx

GEMINI_API_KEY=xxxxxxxxxxxxxxxx

UPLOAD_DIRECTORY=uploads/

REPORT_DIRECTORY=reports/

MAX_UPLOAD_SIZE=100MB
```

---

# 39. Appendix B – Recommended Project Structure

```text
Sentinel/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── hooks/
│   ├── services/
│   └── assets/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── analyzers/
│   ├── threat_intelligence/
│   ├── ai/
│   ├── reports/
│   ├── risk_engine/
│   ├── mitre/
│   ├── database/
│   └── utils/
│
├── uploads/
├── reports/
├── logs/
├── tests/
├── docs/
├── README.md
└── requirements.txt
```

---

# 40. PRD Conclusion

Sentinel is designed as an **AI-assisted malware investigation platform** focused on supporting police investigators through explainable, evidence-driven analysis.

The demo emphasizes clarity, transparency, and modularity over feature overload. Every major decision—from rule-based risk scoring to optional threat intelligence enrichment and AI-generated summaries—is intended to make malware investigations easier to understand and easier to present as evidence.

The architecture is intentionally extensible. Future integrations such as CAPE Sandbox, additional threat intelligence providers, MISP, OpenCTI, authentication, and collaborative case management can be added without redesigning the core platform.

The success of the Sentinel Demo will be measured not only by its ability to analyze files, but by its ability to **present technical findings in a form that investigators can trust, understand, and act upon.**

# 41. User Interface (UI) Specification

## 41.1 Overview

The Sentinel user interface shall be designed for **simplicity, clarity, and speed**. The primary users are police investigators who may not have extensive cybersecurity knowledge. Therefore, the interface should prioritize readability over technical complexity.

### UI Design Principles

- Clean and uncluttered layout
- Minimal number of clicks
- Consistent navigation
- Clear status indicators
- Evidence-first presentation
- Responsive design
- Accessibility friendly
- Professional appearance suitable for law enforcement

---

# 41.2 Global Layout

Every page shall follow the same layout.

```
---------------------------------------------------------
Logo                 Sentinel                User Session
---------------------------------------------------------

Dashboard
Investigations
Reports
Settings

---------------------------------------------------------

               Main Content Area

---------------------------------------------------------

Status Bar

Analysis Status
API Status
Current Investigation
```

---

# 41.3 Color Guidelines

The application shall use colors only to communicate status.

| Color | Meaning |
|---------|---------|
| Green | Safe / Completed |
| Blue | Information |
| Yellow | Warning |
| Orange | Medium Risk |
| Red | High Risk |
| Gray | Unavailable |

Color shall never be the only indicator.

Icons and labels shall also be used.

---

# 41.4 Dashboard

The dashboard is the application's home screen.

It provides investigators with a quick overview.

### Widgets

Recent Investigations

Latest Reports

Risk Distribution

System Status

Threat Intelligence Status

Storage Usage

---

Example

```
------------------------------------------------------

Sentinel Dashboard

------------------------------------------------------

Investigations Today

12

--------------------------------------

Reports Generated

11

--------------------------------------

High Risk Cases

4

--------------------------------------

Threat Intelligence

✓ Online

--------------------------------------

Upload New Evidence

[ Upload Button ]

------------------------------------------------------
```

---

# 41.5 Upload Screen

Purpose

Allow investigators to upload suspicious files.

Features

Drag & Drop

Browse Files

Upload Progress

Validation Messages

Supported Formats

Maximum File Size

---

Example

```
------------------------------------------------------

Upload Evidence

------------------------------------------------------

Drag file here

OR

[ Browse Files ]

Supported

EXE

DLL

APK

PDF

Office Documents

ZIP

Scripts

------------------------------------------------------
```

---

# 41.6 Investigation Screen

The investigation page is divided into sections.

```
-----------------------------------------------------

File Information

-------------------------------------

Risk Score

-------------------------------------

Threat Intelligence

-------------------------------------

Static Analysis

-------------------------------------

IOC Extraction

-------------------------------------

MITRE ATT&CK

-------------------------------------

AI Summary

-------------------------------------

Timeline

-----------------------------------------------------
```

---

# 41.7 File Information Card

Display

Filename

Size

Type

SHA256

Upload Time

Status

Example

```
Filename

invoice.exe

Size

2.4 MB

SHA256

8A93....

Status

Analysis Complete
```

---

# 41.8 Risk Card

Large score displayed prominently.

Example

```
Risk Score

87

Critical

Confidence

95%
```

---

# 41.9 Static Analysis Card

Display

Metadata

Imports

Sections

Entropy

Resources

Security Findings

Certificate

Every finding includes severity.

---

# 41.10 IOC Card

Each IOC displayed as an expandable table.

Columns

Type

Value

Confidence

Evidence

Status

Search and filtering shall be available.

---

# 41.11 Threat Intelligence Card

Separate provider sections.

Example

```
VirusTotal

58 / 72

Malicious

----------------------------

MalwareBazaar

Family

RedLine

----------------------------

Status

Online
```

---

# 41.12 MITRE Card

Each technique displayed as a card.

Example

```
T1027

Obfuscated Files

Confidence

94%

Evidence

Packed Executable
```

---

# 41.13 AI Summary Card

Contains

Executive Summary

Technical Summary

Recommendations

Confidence

---

# 41.14 Timeline Card

Displays chronological events.

```
Upload

↓

Static Analysis

↓

IOC Extraction

↓

Threat Intelligence

↓

Risk Score

↓

MITRE

↓

AI Summary

↓

Report
```

---

# 41.15 Report Page

Lists generated reports.

Columns

Report ID

Case ID

Generated Time

Format

Download

Example

```
------------------------------------------------

Reports

------------------------------------------------

PDF

Download

HTML

Download

CSV

Download

JSON

Download

------------------------------------------------
```

---

# 42. Navigation Flow

## Primary Navigation

```
Dashboard

↓

Upload

↓

Investigation

↓

Report

↓

Download
```

---

## Secondary Navigation

```
Investigation

↓

Static Analysis

↓

IOC

↓

Threat Intelligence

↓

Risk Score

↓

MITRE

↓

AI Summary
```

---

# 43. Logging and Audit Trail

Every action performed within Sentinel shall be logged.

## Logged Events

Application Start

File Upload

Analysis Started

Analysis Completed

Threat Intelligence Request

Threat Intelligence Response

Risk Score Generated

MITRE Mapping Completed

AI Summary Generated

Report Generated

Application Error

---

## Log Format

```
Timestamp

Level

Module

Action

Details
```

Example

```
2026-07-17 14:32:11

INFO

Threat Intelligence

VirusTotal Lookup Successful
```

---

# 44. Configuration Management

The application shall allow configuration through environment variables.

Configurable values include

Maximum Upload Size

Report Directory

Database Path

API Keys

Request Timeout

Cache Duration

Log Level

Application Name

Application Version

---

# 45. Coding Standards

The project shall follow consistent coding standards.

Backend

- Python 3.12+
- PEP8 compliant
- Type hints encouraged
- Modular architecture
- Service-oriented design

Frontend

- React 19+
- Functional components
- Hooks preferred
- TailwindCSS
- Component reuse

Documentation

- Markdown
- Docstrings
- API documentation
- Inline comments only where necessary

---

# 46. Dependencies

## Backend

FastAPI

Uvicorn

SQLAlchemy

SQLite

Pydantic

Requests

Androguard

PeFile

Oletools

PyPDF2

YARA

Google Generative AI SDK

ReportLab

Jinja2

---

## Frontend

React

Vite

TailwindCSS

React Router

Axios

Chart.js

React Icons

---

# 47. Deployment (Demo)

The demo shall be executable on a single machine.

Requirements

Windows 10/11

Python

Node.js

SQLite

Internet connection (for Threat Intelligence)

Modern web browser

The backend and frontend shall be started using separate development servers during the demonstration.

---

# 48. Success Metrics

The Sentinel Demo shall be considered successful if:

- A user can upload a supported file.
- Static analysis completes successfully.
- IOCs are extracted.
- VirusTotal and MalwareBazaar enrichment works.
- Risk score is generated.
- MITRE ATT&CK mapping is displayed.
- Gemini produces an investigation summary.
- Reports can be exported in PDF, HTML, CSV, and JSON.
- The application remains functional even if external APIs fail.
- The interface is understandable to non-technical investigators.

---

# End of Document (Revision 1.0)

**Document Title:** Sentinel – Product Requirements Document (PRD)

**Version:** 1.0

**Status:** Draft for Implementation

**Target Audience:** Final-Year Project Development Team, Academic Evaluators, Police Stakeholders

