# IAM-Reaper

IAM-Reaper is a lightweight Python security auditing tool that inspects AWS IAM users for common identity and access risks.  
It is designed to run safely in CI/CD pipelines and produce machine-readable output for downstream security automation.

This project is intentionally **stubbed by default** so it can run in GitHub Actions **without AWS credentials**.

---

## What IAM-Reaper Does

IAM-Reaper audits IAM users and reports on:

- IAM user age (long-lived users)
- MFA enabled or disabled
- Presence of inline IAM policies
- A simple, transparent risk classification per user

### Risk Levels

- **HIGH**
  - MFA disabled **and**
  - Inline policies attached

- **MEDIUM**
  - Old user (> 90 days) **or**
  - Inline policies present

- **LOW**
  - MFA enabled
  - No inline policies
  - User age ≤ 90 days

The risk model is intentionally simple and explainable.

---

## Design Principles

- CI-safe by default (no AWS credentials required)
- Deterministic output (ideal for pipelines)
- Minimal dependencies
- Security-first assumptions
- Honest scope (no overclaiming)

IAM-Reaper is meant to be a **building block**, not a full IAM governance platform.

---

## Usage

Basic usage:

```bash
python iam_reaper.py --output iam_report.json
Verbose output (prints JSON to console):

bash
Copy code
python iam_reaper.py --output iam_report.json --verbose
Output Example
json
Copy code
[
  {
    "UserName": "test-user",
    "UserAgeDays": 400,
    "OldUser": true,
    "HasMFA": false,
    "HasInlinePolicies": true,
    "InlinePolicyNames": ["InlineAdminPolicy"],
    "RiskLevel": "HIGH"
  }
]
The JSON output is intended for:

CI artifacts

Policy pipelines

Security automation tooling

Future integration with IaC enforcement

CI / Testing
IAM-Reaper uses botocore.stub.Stubber to simulate AWS IAM API responses.

This allows the tool to:

Run in GitHub Actions

Avoid live AWS credentials

Match real AWS API schemas

Fail fast if responses are invalid

The GitHub Actions workflow:

Runs IAM-Reaper on every push

Validates report generation

Uploads iam_report.json as a build artifact

Repository Structure
text
Copy code
IAM-Reaper/
├── iam_reaper.py
├── requirements.txt
└── .github/
    └── workflows/
        └── iam-reaper.yml
Future Work (Intentionally Not Implemented)
The following are explicitly deferred:

Live AWS account execution

Access key last-used analysis

Group and managed policy evaluation

Terraform / IaC enforcement hooks

Dashboards or UI layers

These belong in a higher-level system, not this tool.

Project Status
Frozen – feature complete

IAM-Reaper is considered complete and stable.
Future work will build on top of this tool rather than modifying it.

This repository serves as a reference implementation for:

CI-safe security tooling

AWS API–accurate stubbing

Identity risk evaluation foundations
