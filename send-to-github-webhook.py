#!/usr/bin/python3
"""


/home/martin/bin/send-to-github-webhook.py https://httpbin.org/post monperrus/test-repo abcdef1234567890abcdef1234567890abcdef12

/home/martin/bin/send-to-github-webhook.py  https://api.monperrus.com/github-webhook monperrus/test-repo abcdef1234567890abcdef1234567890abcdef12
"""

import sys
import json
import requests
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser(description='Send a simulated GitHub push webhook payload.')
    parser.add_argument('url', help='The URL of the webhook receiver.')
    parser.add_argument('slug', help='The repository slug (e.g., owner/repo).')
    parser.add_argument('sha', help='The commit SHA to send.')
    parser.add_argument('--event', default='push', help='The GitHub event type (default: push).')
    parser.add_argument('--ref', default='refs/heads/main', help='The git ref (default: refs/heads/main).')
    parser.add_argument('--secret', help='Webhook secret for X-Hub-Signature-256 header.')
    
    args = parser.parse_args()

    parts = args.slug.split('/')
    if len(parts) != 2:
        print("Error: slug must be in 'owner/repo' format.")
        sys.exit(1)
    owner, repo = parts

    timestamp = datetime.datetime.now().isoformat() + "Z"

    payload = {
        "ref": args.ref,
        "before": "0000000000000000000000000000000000000000",
        "after": args.sha,
        "repository": {
            "name": repo,
            "full_name": args.slug,
            "owner": {
                "login": owner,
                "name": owner,
                "email": f"{owner}@users.noreply.github.com"
            },
            "html_url": f"https://github.com/{args.slug}",
            "description": "Triggered by send-to-github-webhook.py",
            "fork": False,
            "url": f"https://github.com/{args.slug}",
            "created_at": timestamp,
            "updated_at": timestamp,
            "pushed_at": timestamp,
            "git_url": f"git://github.com/{args.slug}.git",
            "ssh_url": f"git@github.com:{args.slug}.git",
            "clone_url": f"https://github.com/{args.slug}.git",
            "svn_url": f"https://github.com/{args.slug}",
            "homepage": None,
            "size": 0,
            "stargazers_count": 0,
            "watchers_count": 0,
            "language": None,
            "has_issues": True,
            "has_projects": True,
            "has_downloads": True,
            "has_wiki": True,
            "has_pages": False,
            "forks_count": 0,
            "mirror_url": None,
            "archived": False,
            "disabled": False,
            "open_issues_count": 0,
            "license": None,
            "forks": 0,
            "open_issues": 0,
            "watchers": 0,
            "default_branch": "main",
            "stargazers": 0,
            "master_branch": "main"
        },
        "pusher": {
            "name": owner,
            "email": f"{owner}@users.noreply.github.com"
        },
        "sender": {
            "login": owner,
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": f"https://github.com/{owner}.png",
            "gravatar_id": "",
            "url": f"https://api.github.com/users/{owner}",
            "html_url": f"https://github.com/{owner}",
            "followers_url": f"https://api.github.com/users/{owner}/followers",
            "following_url": f"https://api.github.com/users/{owner}/following{{/other_user}}",
            "gists_url": f"https://api.github.com/users/{owner}/gists{{/gist_id}}",
            "starred_url": f"https://api.github.com/users/{owner}/starred{{/owner}}{{/repo}}",
            "subscriptions_url": f"https://api.github.com/users/{owner}/subscriptions",
            "organizations_url": f"https://api.github.com/users/{owner}/orgs",
            "repos_url": f"https://api.github.com/users/{owner}/repos",
            "events_url": f"https://api.github.com/users/{owner}/events{{/privacy}}",
            "received_events_url": f"https://api.github.com/users/{owner}/received_events",
            "type": "User",
            "site_admin": False
        },
        "commits": [
            {
                "id": args.sha,
                "tree_id": args.sha,
                "distinct": True,
                "message": f"Manual trigger for {args.sha}",
                "timestamp": timestamp,
                "url": f"https://github.com/{args.slug}/commit/{args.sha}",
                "author": {
                    "name": owner,
                    "email": f"{owner}@users.noreply.github.com",
                    "username": owner
                },
                "committer": {
                    "name": owner,
                    "email": f"{owner}@users.noreply.github.com",
                    "username": owner
                },
                "added": [],
                "removed": [],
                "modified": []
            }
        ],
        "head_commit": {
            "id": args.sha,
            "tree_id": args.sha,
            "distinct": True,
            "message": f"Manual trigger for {args.sha}",
            "timestamp": timestamp,
            "url": f"https://github.com/{args.slug}/commit/{args.sha}",
            "author": {
                "name": owner,
                "email": f"{owner}@users.noreply.github.com",
                "username": owner
            },
            "committer": {
                "name": owner,
                "email": f"{owner}@users.noreply.github.com",
                "username": owner
            },
            "added": [],
            "removed": [],
            "modified": []
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': args.event,
        'X-GitHub-Delivery': '12345678-1234-1234-1234-123456789012', # Dummy delivery ID
        'User-Agent': 'GitHub-Hookshot/1234567'
    }

    # Compute X-Hub-Signature-256 if secret is provided
    data = json.dumps(payload).encode('utf-8')
    if args.secret:
        import hmac
        import hashlib
        signature = hmac.new(args.secret.encode('utf-8'), data, hashlib.sha256).hexdigest()
        headers['X-Hub-Signature-256'] = f"sha256={signature}"

    print(f"Sending payload for commit {args.sha} to {args.url}...")
    try:
        response = requests.post(args.url, data=data, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
