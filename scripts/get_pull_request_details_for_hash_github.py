import requests
import argparse
import json
import re
import sys
from datetime import datetime

def format_timestamp(dt_string: str) -> str:
    # Convert to datetime object
    dt_object = datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%SZ')
    # Format datetime object as string
    formatted_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_string

def pr_title_error():
    print("PR Title does not match the required format. Please ensure the PR title follows the format: '<Something something ..> - IT Change #<number>'")
    sys.exit(1)

def get_pull_request_details(commit_hash, github_token, repo):
    """
    Retrieve pull request details for a given commit hash from a GitHub repository.

    Parameters:
    - commit_hash: The hash of the commit to find the associated pull request.
    - github_token: Personal GitHub token for authentication.
    - repo: Repository name with owner (e.g., "octocat/Hello-World").

    Returns:
    A dictionary with pull request details or a message indicating no pull request found.
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    url = f"https://api.github.com/repos/{repo}/commits/{commit_hash}/pulls"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pull_requests = response.json()
        if pull_requests:
            pr = pull_requests[0]
            print("Pull request found for the given commit. Here are the details:")
            payload = json.dumps({
                "id": pr["id"],
                "number": pr["number"],
                "state": pr["state"],
                "url": pr["html_url"],
                "title": pr["title"]
            })
            print("")
            print("Here is the returned payload")
            print("")
            print(payload)
            re.match(' - IT Change #[0-9]+$',  pr["title"]) or pr_title_error()
            print("")
            print("PR Title matches the required format.") 
        else:
            return "No pull request found for the given commit."
    else:
        return f"Failed to retrieve data. HTTP Status Code: {response.status_code}. Error: {response.text}"

def main():
    parser = argparse.ArgumentParser(description="Get pull request details for a given commit hash from GitHub.")
    parser.add_argument("--commit", required=True, help="Commit hash")
    parser.add_argument("--token", required=True, help="GitHub Personal Access Token")
    parser.add_argument("--repo", required=True, help="Repository name with owner (e.g., octocat/Hello-World)")

    args = parser.parse_args()

    pr_details = get_pull_request_details(args.commit, args.token, args.repo)
    print(pr_details)

if __name__ == "__main__":
    main()
