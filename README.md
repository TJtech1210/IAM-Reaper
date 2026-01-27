
# IAM-Reaper

IAM-Reaper is a lightweight, CI-safe Python security tool that audits AWS IAM users for common identity and access risks.  
It is designed to run **without AWS credentials**, produce **deterministic JSON output**, and act as a **foundational building block** for secure infrastructure pipelines.

This project intentionally uses **stubbed AWS IAM responses** so it can execute safely in GitHub Actions and other CI environments.

---

## Why This Exists

Most IAM audit demos require live AWS credentials and cannot safely run in CI.  
IAM-Reaper focuses on correctness, explainability, and pipeline-first execution instead of scale or feature bloat.

This repository demonstrates:
- CI-safe cloud security tooling
- Accurate AWS API modeling
- Deterministic security analysis
- Honest, limited scope

---

## What IAM-Reaper Checks

- IAM user age (identifies long-lived users)
- Whether MFA is enabled
- Whether inline IAM policies are attached
- A transparent, rule-based risk classification

---

## Risk Model

Risk levels are intentionally simple and explainable.

**HIGH**
- MFA disabled  
- Inline policies present  

**MEDIUM**
- User older than 90 days  
- OR inline policies present  

**LOW**
- MFA enabled  
- No inline policies  
- User age ≤ 90 days  

---

## Usage

Run the tool:

```bash
python iam_reaper.py --output iam_report.json
````

Verbose mode:

```bash
python iam_reaper.py --output iam_report.json --verbose
```

---

## Output Example

```json
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
```

The output is designed for:

* CI artifacts
* Security pipelines
* Policy enforcement workflows
* Downstream infrastructure analysis

---

## CI and Testing

IAM-Reaper uses `botocore.stub.Stubber` to simulate AWS IAM API responses.

This ensures:

* No AWS credentials are required
* CI execution is deterministic
* Responses must match real AWS schemas
* Failures occur early and predictably

The GitHub Actions workflow runs IAM-Reaper on every push, validates report creation, and uploads the JSON report as a build artifact.

---

## Repository Structure

```text
IAM-Reaper/
├── iam_reaper.py
├── requirements.txt
└── .github/
    └── workflows/
        └── iam-reaper.yml
```

---

## Project Status

**Frozen – feature complete**

IAM-Reaper is intentionally stable and will not receive additional features.
Future security automation work will build on top of this tool rather than modifying it.

```
