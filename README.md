# Reddit Cleanup Script

This Python script automates the deletion of your Reddit submissions and comments. Using the Reddit API via `PRAW` (Python Reddit API Wrapper), the script will go through all your submissions and comments, allowing you to delete or anonymize them as needed.

## Features
- Delete **all Reddit submissions (posts)** from your account.
- Delete **all Reddit comments** from your account.
- Anonymize posts instead of deleting them, if preferred.
- Avoids Reddit’s rate limit with optional pauses between deletions.
- Ensures cleanup of your submissions and comments efficiently.

## Installation

### Prerequisites
- Python 3.x
- `pipenv` for environment management (if you prefer using it, as indicated).

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### Step 2: Set Up Reddit API Credentials
You'll need a reddit 'dev app' - Go here to get your Free [API credentials](https://www.reddit.com/prefs/apps).

Create a secrets.json file in the root directory with the following structure:
```JSON
{
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "user_agent": "your-user-agent",
    "username": "your-reddit-username",
    "password": "your-reddit-password"
}
```
### Step 3: Install & Run
```bash
pipenv install
pipenv shell

python main.py
```