
# Reddit Cleanup Script

A small Python tool to delete your own Reddit **submissions** and **comments** using the Reddit API via [PRAW](https://praw.readthedocs.io/).  
Supports date filtering, dry-run previews, and safer/iterative cleanup.

> **Important:** This script only acts on the authenticated user's content. You are responsible for complying with Reddit's API rules and your local laws. Deletions are permanent.

---

## Features

- Delete your **posts** and **comments**.
- `--older-than N` filter to only target items older than **N days**.
- `--dry-run` mode to preview what would be deleted (no changes made).
- Deduplicated comment processing across listing types.
- Sensible CLI UX: running with no args shows `--help`.
- Optional `--skip-submissions` and `--skip-comments` to scope actions.
- Summary output with creation timestamps for traceability.

---

## Installation

### 1) Python environment
- Python 3.8+ is recommended.

Using `pip`:
```bash
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install praw
```

(Alternatively, `pipenv` or `poetry` will work if you prefer.)

### 2) Reddit API credentials
Create a Reddit application to obtain credentials: https://www.reddit.com/prefs/apps

Create a `secrets.json` file next to `main.py`:
```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "user_agent": "your-user-agent",
  "username": "your-reddit-username",
  "password": "your-reddit-password"
}
```

> Tip: Use a descriptive `user_agent` string (e.g., `"reddit-cleanup by u/yourname v1.0"`).

---

## Usage

Show help (also shown if you run with no args):
```bash
python main.py --help
```

Preview deletions (no changes) for items older than **45 days**:
```bash
python main.py --older-than 45 --dry-run
```

Actually delete items older than **30 days**:
```bash
python main.py --older-than 30
```

Only process comments (skip posts), still as a dry-run:
```bash
python main.py --older-than 90 --dry-run --skip-submissions
```

Only process posts (skip comments):
```bash
python main.py --older-than 365 --skip-comments
```

### Flags

- `--older-than N` — Only delete items older than **N** days (default: `0`, i.e., no age filter).
- `--dry-run` — Print what would be deleted without performing deletions.
- `--skip-submissions` — Do not process posts.
- `--skip-comments` — Do not process comments.

---

## How it works

- The script authenticates via PRAW using your credentials in `secrets.json`.
- It iterates your posts (`user.submissions.new(limit=None)`) and your comments from multiple listings, **deduplicating** them by ID to avoid re-processing the same item.
- For each item, it checks `created_utc` against the `--older-than` cutoff and deletes (unless `--dry-run`).

---

## Safety & Rate Limits

- **Dry-run first**: Always run with `--dry-run` to verify targets before deleting.
- Reddit APIs are **rate-limited**; large accounts may require multiple runs.
- Deletions are **irreversible**. Consider archiving your data first (e.g., via Reddit data export).

---

## Troubleshooting

- **`secrets.json not found`** — Ensure the file exists in the same directory as `main.py`.
- **Invalid credentials / 401** — Re-check your client ID/secret, username/password, and user_agent.
- **PRAW not installed** — `pip install praw` in your active environment.
- **Network or 429 (rate limit)** — Wait and re-run later; consider smaller date windows.

---

## Credits

- Built on [PRAW](https://praw.readthedocs.io/).
- Originally inspired by community scripts such as [JosemyDuarte/reddit-cleaner](https://github.com/JosemyDuarte/reddit-cleaner).
