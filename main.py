import json
import praw
import time

# Initialize PRAW with your credentials
secrets = json.load("secrets.json")
reddit = praw.Reddit(
    client_id= secrets["client_id"],
    client_secret= secrets["client_secret"],
    user_agent=secrets["user_agent"],
    username=secrets["username"],
    password=secrets["password"]
)

# Fetch your submissions
submissions = reddit.user.me().submissions.new(limit=None)

# Loop through each submission
for submission in submissions:
    # Uncomment the next line to delete the post
    # submission.delete()
    
    # Uncomment the next lines to edit the post
    # submission.edit("This post has been anonymized.")

    print(f"Processed post: {submission.title}")

    # Pause to avoid hitting rate limits
    time.sleep(2)

print("Cleanup complete.")
