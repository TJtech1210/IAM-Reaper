import boto3
from botocore.stub import Stubber
from datetime import datetime, timezone
import json


def get_iam_client():
    """
    Create IAM client (will be stubbed in tests / GitHub Actions)
    """
    return boto3.client("iam", region_name="us-east-1")


def get_user_mfa_status(iam, username):
    try:
        response = iam.list_mfa_devices(UserName=username)
        return {
            "HasMFA": bool(response.get("MFADevices"))
        }
    except Exception as e:
        return {
            "HasMFA": "ERROR",
            "Error": str(e)
        }


def get_user_inline_policies(iam, username):
    try:
        response = iam.list_user_policies(UserName=username)
        policies = response.get("PolicyNames", [])
        return {
            "HasInlinePolicies": bool(policies),
            "InlinePolicyNames": policies
        }
    except Exception as e:
        return {
            "HasInlinePolicies": "ERROR",
            "Error": str(e)
        }


def run_audit(iam):
    response = iam.list_users()
    users = response.get("Users", [])

    now = datetime.now(timezone.utc)
    report = []

    for user in users:
        username = user["UserName"]
        create_date = user["CreateDate"]
        age_days = (now - create_date).days

        user_report = {
            "UserName": username,
            "CreateDate": create_date.isoformat(),
            "UserAgeDays": age_days,
            "OldUser": age_days > 90
        }

        user_report.update(get_user_mfa_status(iam, username))
        user_report.update(get_user_inline_policies(iam, username))

        report.append(user_report)

    return report


if __name__ == "__main__":
    iam = get_iam_client()

    # ---- STUBBED DATA (SIMULATION MODE) ----
    stubber = Stubber(iam)

    stubber.add_response(
        "list_users",
        {
            "Users": [
                {
                    "UserName": "test-user",
                    "CreateDate": datetime(2023, 1, 1, tzinfo=timezone.utc)
                }
            ]
        }
    )

    stubber.add_response(
        "list_mfa_devices",
        {
            "MFADevices": []
        },
        {"UserName": "test-user"}
    )

    stubber.add_response(
        "list_user_policies",
        {
            "PolicyNames": ["InlineAdminPolicy"]
        },
        {"UserName": "test-user"}
    )

    stubber.activate()

    audit_results = run_audit(iam)

    print(f"Scanned {len(audit_results)} IAM users")

    with open("iam_report.json", "w") as f:
        json.dump(audit_results, f, indent=2)

    print("iam_report.json generated")

    stubber.deactivate()
