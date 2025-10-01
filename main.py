import argparse
import json
import sys
import time
from datetime import datetime
import praw

def human_utc(ts: float) -> str:
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S UTC")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="main.py",
        description=(
            "Delete your own Reddit submissions and comments using PRAW.\n"
            "Requires a secrets.json in the working directory with:\n"
            '{ "client_id": "...", "client_secret": "...", "user_agent": "...", "username": "...", "password": "..." }'
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--older-than",
        type=int,
        default=0,
        help="Only delete items older than N days (0 = no age filter).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting.",
    )
    p.add_argument(
        "--skip-submissions",
        action="store_true",
        help="Skip deleting submissions (posts).",
    )
    p.add_argument(
        "--skip-comments",
        action="store_true",
        help="Skip deleting comments.",
    )
    return p

def main(argv=None) -> int:
    parser = build_parser()

    # If no arguments supplied, print help and exit 0
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) == 0:
        parser.print_help(sys.stdout)
        return 0

    args = parser.parse_args(argv)
    cutoff_time = time.time() - (args.older_than * 86400)

    # --- reddit login ---
    try:
        with open("secrets.json", "r", encoding="utf-8") as f:
            secrets = json.load(f)
    except FileNotFoundError:
        print("ERROR: secrets.json not found in the current directory.", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"ERROR: secrets.json is not valid JSON: {e}", file=sys.stderr)
        return 2

    reddit = praw.Reddit(
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        user_agent=secrets["user_agent"],
        username=secrets["username"],
        password=secrets["password"],
    )

    user = reddit.user.me()
    dry = args.dry_run
    prefix = "[DRY-RUN] " if dry else ""

    deleted_posts = 0
    processed_posts = 0

    # --- submissions ---
    if not args.skip_submissions:
        for submission in user.submissions.new(limit=None):
            processed_posts += 1
            if submission.created_utc < cutoff_time:
                print(
                    f"{prefix}Post: {submission.title} "
                    f"(created {human_utc(submission.created_utc)})"
                )
                if not dry:
                    submission.delete()
                    deleted_posts += 1

    # --- comments (deduplicated across .new() and .top()) ---
    seen_comment_ids = set()
    deleted_comments = 0
    processed_comments = 0

    def maybe_delete_comment(comment):
        nonlocal deleted_comments, processed_comments
        cid = comment.id
        if cid in seen_comment_ids:
            return
        seen_comment_ids.add(cid)
        processed_comments += 1
        if comment.created_utc < cutoff_time:
            snippet = (comment.body or "").replace("\n", " ")
            if len(snippet) > 60:
                snippet = snippet[:57] + "..."
            print(
                f"{prefix}Comment {cid}: {snippet} "
                f"(created {human_utc(comment.created_utc)})"
            )
            if not dry:
                comment.delete()
                deleted_comments += 1

    if not args.skip_comments:
        for c in user.comments.new(limit=None):
            maybe_delete_comment(c)
        for c in user.comments.top(limit=None):
            maybe_delete_comment(c)

    print("\nSummary")
    print("-------")
    print(f"Processed posts:    {processed_posts}")
    print(f"Deleted posts:      {deleted_posts}{' (simulated)' if dry else ''}")
    print(f"Processed comments: {processed_comments}")
    print(f"Deleted comments:   {deleted_comments}{' (simulated)' if dry else ''}")
    print(
        "\nNotes:\n"
        "- Use --older-than N to avoid deleting recent content.\n"
        "- --dry-run shows what would be deleted without performing deletions.\n"
        "- Private messages must be deleted manually in the inbox.\n"
        "- Reddit APIs are rate-limited; very large accounts may require multiple runs."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
