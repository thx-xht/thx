import os
from atproto import Client

POSTS_FILE = 'tweets.txt'
INDEX_FILE = '.bot/index.txt'

def main():
    # Login using GitHub Secrets
    client = Client()
    client.login(
        os.environ['BSKY_HANDLE'],
        os.environ['BSKY_APP_PASSWORD']
    )
    
    # Load posts
    with open(POSTS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    posts = [p.strip() for p in content.split('---') if p.strip()]
    
    if not posts:
        print("No posts found!")
        return
    
    # Load current index
    try:
        with open(INDEX_FILE, 'r') as f:
            index = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        print("Index file not found or invalid, starting from 0")
        index = 0
    
    # Ensure index is within bounds
    index = index % len(posts)
    
    # Post
    post_text = posts[index]
    print(f"Posting (index {index}): {post_text[:50]}...")
    
    try:
        client.send_post(post_text)
        print("Post sent successfully!")
    except Exception as e:
        print(f"Error sending post: {e}")
        raise
    
    # Save updated index
    new_index = (index + 1) % len(posts)
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, 'w') as f:
        f.write(str(new_index))
    
    print(f"Updated index to {new_index}")

if __name__ == "__main__":
    main()
