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

def get_git_username():
    try:
        name = subprocess.run(["git", "config", "user.name"],
                              text=True, capture_output=True, check=True).stdout.strip()
        if name:
            return name
    except Exception:
        pass
    try:
        import pwd
        return pwd.getpwuid(os.getuid()).pw_gecos or pwd.getpwuid(os.getuid()).pw_name
    except Exception:
        return os.getenv("USER") or "unknown"

def get_github_username():
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"],
                             text=True, capture_output=True, check=True).stdout.strip()
        if "github.com" in url:
            m = re.search(r"github\.com[:/](?P<user>[^/]+)/", url)
            if m:
                return m.group("user")
    except Exception:
        pass
    try:
        user = subprocess.run(["git", "config", "github.user"],
                              text=True, capture_output=True, check=True).stdout.strip()
        if user:
            return user
    except Exception:
        pass
    return get_git_username()

def detect_license_type(lic_text: str) -> str:
    text = lic_text.lower()
    if 'mit license' in text:
        return 'MIT'
    if 'gnu general public license' in text or 'gpl' in text:
        return 'GPL-3.0'
    if 'apache license' in text:
        return 'Apache-2.0'
    if 'bsd' in text:
        return 'BSD-3-Clause'
    return 'Custom'
