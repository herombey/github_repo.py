# github_repo.py
A simple Python CLI tool to generate wordlists from public GitHub repositories.  
It crawls a repository’s full directory and file structure using the GitHub API and outputs every path (with relative folders and filenames), making it perfect for directory brute-forcing or reconnaissance.

## Features

- Outputs every file and directory in a GitHub repo as full relative paths (e.g. /src/routes/index.ts).
- Optionally output directories only (--dirs-only).
- Supports large repos with authentication (GitHub Personal Access Token).
- Works with both owner/repo and full GitHub URLs.

## Installation

1. Clone or download this repo.
2. Install Python dependencies (only requests):

Usage
```bash
python github_wordlist.py -i <github_repo> -o <output_file> [--dirs-only] [--token <github_token>]
```

**Arguments:**
- `-i`, `--input`: GitHub repository (either `owner/repo` or full GitHub URL)
- `-o`, `--output`: Output file for the wordlist
- `--dirs-only`: _(Optional)_ Output only directories, not files
- `--token`: _(Optional)_ GitHub Personal Access Token (to avoid rate limits)

### Examples

All files and folders:
```sh
python github_wordlist.py -i htts://github.com/something/folder/ -o wordlist.txt
```

Directories only:
```sh
python github_wordlist.py -i https://github.com/something/other -o dirlist.txt --dirs-only
```

Using a GitHub Token (recommended for large repos):
```sh
python github_wordlist.py -i htts://github.com/something/folder/ -o wordlist.txt --token ghp_yourtokenhere
```

### Notes
- **Rate Limits:** Unauthenticated requests are limited to 60 per hour. Use a [GitHub Personal Access Token](https://github.com/settings/tokens) for 5,000 requests/hour.
- **Private repos are not supported** unless you modify the script for authenticated access with additional scopes.
- The output is **one path per line**, in the format `/full/path/to/file_or_dir`.

