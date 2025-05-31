IAM Reaper

A Python-powered AWS IAM audit tool to check IAM users for risky security posture and export findings to CSV.

---

🚀 What It Does

- Lists all IAM users in your AWS account
- Checks which users have MFA enabled or disabled
- Detects users with risky inline policies
- Flags users with “old” credentials (over 90 days by default)
- Outputs a detailed report to a CSV file, ready for security review or Excel


⚙️ How To Run

1. Clone the repo:
  
   git clone https://github.com/TJtech1210/IAM-Reaper.git
   cd IAM-Reaper


2. Set up your Python environment (optional but recommended):

 
   python3 -m venv venv
   source venv/bin/activate
   pip install boto3
   

3. Configure AWS credentials:

   * Use `aws configure` or set your credentials in environment variables.
   * Make sure you have permission to list users and policies.

4. Run the script:

   
   python reaper.py
   

5. Check the output:

Review `iam_audit_report.csv` for your audit results.


📝 Example Output

User: reaper_user | Created: 2025-05-29 05:37:19 UTC | Age: 1 days
✅  reaper_user credentials age is OK.

---

CSV Example:
UserName,CreateDate,AgeDays,OldCredentials,HasMFA,HasInlinePolicies,InlinePolicyNames
reaper_user,2025-05-29 05:37:19 UTC,1,False,False,False,[]

---

🔒 What’s Next (Planned Improvements)

* Export report to JSON
* Add CLI options for output format and credential age threshold (`argparse`)
* Add error handling/logging for failed AWS calls
* Check last login, access key age, and permissions summary
* (Optional) Upload report to S3

---

👤 Author

[TJtech1210](https://github.com/TJtech1210)

---

🤝 Contributing

PRs welcome! If you want to practice Python/AWS/Boto3, feel free to fork and improve!*

---

🏷️ License

MIT 


