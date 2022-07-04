import os

env_list = ["APP_CLIENT_ID", "USER_NAME", "USER_PS"]
env_list = []
proxies = {}
if "PROXY" in os.environ:
    proxies = {
        "http"  : os.getenv("PROXY"),
        "https" : os.getenv("PROXY")
    }

client_id = os.getenv("APP_CLIENT_ID")
user_name = os.getenv("USER_NAME")
user_ps = os.getenv("USER_PS")
authority_endpoint = "https://login.microsoftonline.com/organizations"
graph_endpoint = "https://graph.microsoft.com/v1.0/"
scope = ["User.Read"]