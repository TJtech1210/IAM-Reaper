import boto3
from datetime import datetime, timezone
from pprint import pprint
import csv


# Initialize the IAM client
iam = boto3.client('iam')

# Get list of all IAM users
response = iam.list_users()
users = response['Users']

print("🔍 Scanning IAM users...\n")


def get_user_mfa_status(user_name):
    response = iam.list_mfa_devices(UserName=user_name)
    mfa_devices = response['MFADevices']
    if not mfa_devices:
        has_mfa = False
    else:
        has_mfa = True
    return {"UserName": user_name, "HasMFA": has_mfa}

def get_user_inline_policies(user_name):
    response = iam.list_user_policies(UserName=user_name)
    policy_names = response["PolicyNames"]
    has_inline_policies = bool(policy_names)
    return {
        "HasInlinePolicies": has_inline_policies,
        "InlinePolicyNames": policy_names
    }

user_audit_report = []

# Loop through users and check credential age
for user in users:
    username = user['UserName']
    create_date = user['CreateDate']
    now = datetime.now(timezone.utc)
    age = (now - create_date).days
    create_date_str = create_date.strftime("%Y-%m-%d %H:%M:%S %Z")

    user_report = {
        "UserName": username,
        "CreateDate": create_date_str,
        "AgeDays": age,
        "OldCredentials": age > 90
    }
    user_report.update(get_user_mfa_status(username))
    user_report.update(get_user_inline_policies(username))

    user_audit_report.append(user_report)
    

     # Optional: Print per-user status as you loop (for feedback)
    print(f"User: {username} | Created: {create_date} | Age: {age} days")

    if age > 90:
        print(f"⚠️  {username} has credentials older than 90 days!\n")
    else:
        print(f"✅  {username} credentials age is OK.\n")
# Only print the report ONCE, after the loop

pprint(user_audit_report)

# Optionally, set your CSV filename
csv_filename = "iam_audit_report.csv"

# List the fields you want in the CSV (should match your dict keys)
fieldnames = [
    "UserName",
    "CreateDate",
    "AgeDays",
    "OldCredentials",
    "HasMFA",
    "HasInlinePolicies",
    "InlinePolicyNames"
]

# Open the file and write
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for user in user_audit_report:
        writer.writerow(user)
print("✅ CSV export complete: iam_audit_report.csv")
