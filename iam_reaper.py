import boto3
from botocore.stub import Stubber
from datetime import datetime, timezone
import argparse
import json


def get_iam_client():
    return boto3.client("iam", region_name="us-east-1")


def get_user_mfa_status(iam, username):
    try:
        response = iam.list_mfa_devices(UserName=username)
        return {"HasMFA": bool(response.get("MFADevices"))}
    except Exception as e:
        return {"HasMFA": "ERROR", "Error": str(e)}


def get_user_inline_policies(iam, username):
    try:
        response = iam.list_user_policies(UserName=username)
        policies = response.get("PolicyNames", [])
        return {
            "HasInlinePolicies": bool(policies),
            "InlinePolicyNames": policies
        }
    except Exception as e:
        return {"HasInlinePolicies": "ERROR", "Error": str(e)}


def calculate_risk(user):
    if user["HasMFA"] is False and user["HasInlinePolicies"]:
        return "HIGH"
    if user["OldUser"] or user["HasInlinePolicies"]:
        return "MEDIUM"
    return "LOW"


def run_audit(iam):
    response = iam.list_users()
    users = response.get("Users", [])
    now = datetime.now(timezone.utc)

    report = []

    for user in users:
        username = user["UserName"]
        age_days = (now - user["CreateDate"]).days

        user_report = {
            "UserName": username,
            "UserAgeDays": age_days,
            "OldUser": age_days > 90
        }

        user_report.update(get_user_mfa_status(iam, username))
        user_report.update(get_user_inline_policies(iam, username))
        user_report["RiskLevel"] = calculate_risk(user_report)

        report.append(user_report)

    return report


def parse_args():
    parser = argparse.ArgumentParser(description="IAM-Reaper IAM audit tool")
    parser.add_argument("--output", default="iam_report.json", help="Output JSON file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

