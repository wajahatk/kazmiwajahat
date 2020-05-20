from os import getenv
from subprocess import Popen, PIPE


# ---------------------------------------------------------------------------- #
# API key:
api_key = getenv("CONSUMER_KEY")
# API secret key:
api_secret = getenv("CONSUMER_SECRET")
# Access token: 
access_token = getenv("API_KEY")
# Access token secret: 
access_token_secret = getenv("API_SECRET")


# ---------------------------------------------------------------------------- #
def create_auth_json():
    #Create auth.json file for twitter-to-sqlite
    p = Popen(['twitter-to-sqlite', 'auth'], stdin=PIPE)
    p.stdin.write(f"{api_key}\n".encode())
    p.stdin.write(f"{api_secret}\n".encode())
    p.stdin.write(f"{access_token}\n".encode())
    p.stdin.write(f"{access_token_secret}\n".encode())
    p.stdin.flush()
    return


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    create_auth_json()