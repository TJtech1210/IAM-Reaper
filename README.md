# IAM-Reaper

IAM-Reaper is a lightweight Python security tool that audits AWS IAM users for common misconfigurations and risk indicators.  
It is designed to run safely in CI/CD pipelines and produce machine-readable output for downstream security tooling.

This project is intentionally **stubbed by default** to enable testing in GitHub Actions without AWS credentials.

---

## 🔍 What IAM-Reaper Checks

- IAM user age (identifies long-lived users)
- MFA enabled / disabled
- Inline IAM policies attached
- Basic risk classification per user

Risk levels:
- **HIGH** – No MFA and inline policies present
- **MEDIUM** – Old users or inline policies present
- **LOW** – MFA enabled and no inline policies

---

## 🧱 Design Principles

- CI-safe (no AWS credentials required)
- Deterministic output for pipelines
- Minimal dependencies
- Security-first assumptions

IAM-Reaper is intended as a **building block** for larger secure-infrastructure pipelines.

---

## ▶️ Usage

```bash
python iam_reaper.py --output iam_report.json

Optional:

python iam_reaper.py --output iam_report.json --verbose


📄 Output Example
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
