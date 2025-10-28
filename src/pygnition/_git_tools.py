import re
import subprocess

def get_upstream_url():
    try:
        # This gets the URL of the 'origin' remote
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            check=True,
            capture_output=True,
            text=True
        )
        url = result.stdout.strip()

        # Convert a ssh link to a http link
        if url.startswith('git@'):
            url = 'https://' + re.sub(':', '/', url.partition('@')[-1])
        
        return url if url else None
    except subprocess.CalledProcessError:
        return None

# url = get_upstream_url()
# print(url)

