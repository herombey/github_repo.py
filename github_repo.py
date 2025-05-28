import sys
import requests
import argparse
import os
import re

def parse_github_url(repo_arg):
    url_pattern = re.compile(r'github\.com/([\w\-_]+)/([\w\-_]+)')
    match = url_pattern.search(repo_arg)
    if match:
        owner, repo = match.groups()
    elif '/' in repo_arg:
        owner, repo = repo_arg.split('/', 1)
    else:
        raise ValueError('Invalid GitHub repo format.')
    return owner, repo

def get_github_dir_contents(owner, repo, token=None, path=''):
    api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    response = requests.get(api_url, headers=headers)
    if response.status_code == 403:
        raise Exception("GitHub API error: 403 (Forbidden). Likely rate limited. Try with a token.")
    if response.status_code != 200:
        raise Exception(f'GitHub API error: {response.status_code} for {api_url}')
    items = response.json()
    results = []
    for item in items:
        results.append(item['path'])
        if item['type'] == 'dir':
            # Recursive call for subdirectories
            results.extend(get_github_dir_contents(owner, repo, token, item['path']))
    return results

def main():
    parser = argparse.ArgumentParser(description='Create a wordlist from a GitHub repo (with full paths).')
    parser.add_argument('-i', '--input', required=True, help='GitHub repository (owner/repo or URL)')
    parser.add_argument('-o', '--output', required=True, help='Output text file')
    parser.add_argument('--dirs-only', action='store_true', help='Include only directories')
    parser.add_argument('--token', help='GitHub Personal Access Token (or set GITHUB_TOKEN env var)')
    args = parser.parse_args()

    token = args.token or os.getenv('GITHUB_TOKEN')

    owner, repo = parse_github_url(args.input)
    try:
        paths = get_github_dir_contents(owner, repo, token)
        # Optionally filter for only directories (based on API type info)
        if args.dirs_only:
            # We'll have to re-fetch to ensure only directories are listed
            def is_dir(path):
                url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
                r = requests.get(url, headers={'Authorization': f'token {token}'} if token else {})
                if r.status_code == 200:
                    data = r.json()
                    if isinstance(data, dict) and data.get('type') == 'dir':
                        return True
                return False
            paths = [p for p in paths if is_dir(p)]
        # Write output with full paths, prefixed with a slash for easy use
        with open(args.output, 'w', encoding='utf-8') as f:
            for path in paths:
                f.write(f"/{path}\n")
        print(f"Wordlist written to {args.output} ({len(paths)} entries)")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
