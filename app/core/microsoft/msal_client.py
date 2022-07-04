from app.core.logger import log
from app.core.settings import authority_endpoint, proxies, client_id, user_name, user_ps, scope
from app.core.rest_request import get_http_client
import msal

class MSALClient:
    def __init__(self) -> None:
        self.msal_client = None
        self.result = None
        self.account_cache = None
        self._init_msal_application()

    def _init_msal_application(self):
        self.msal_client = msal.PublicClientApplication(
            client_id,
            authority=authority_endpoint,
            http_client = self._create_http_client()
        )
    def _create_http_client(self):
        http_client = get_http_client(verify=False, proxies=proxies)
        http_client.headers.update({'User-Agent': 'linux'})
        return http_client

    def get_access_token(self):
        self.account_cache = self.msal_client.get_accounts(username=user_name)
        if self.account_cache:
            log.info("Account exists in cache, probably with token too. Let's try.")
            self.result = self.msal_client.acquire_token_silent(scope,
                            account=self.account_cache[0])
        if not self.result:
            log.info("No suitable token exists in cache. Let's get a new one from AAD.")
            self.result = self.msal_client.acquire_token_by_username_password(
                        user_name,
                        user_ps,
                        scopes=scope)
        if "access_token" in self.result:
            log.info("Return access token %s", self.result)
            return {"result": "success",
                    "access_token": self.result["access_token"]}
        else:
            log.error(self.result)
            # print(result.get("error"))
            # print(result.get("error_description"))
            # print(result.get("correlation_id"))  # You may need this when reporting a bug
            # if 65001 in result.get("error_codes", []):  # Not mean to be coded programatically, but...
            #     # AAD requires user consent for U/P flow
            #     print("Visit this to consent:", app.get_authorization_request_url(config["scope"]))
        return {"result": "fail", "msg": self.result.get("error"), "detail": self.result.get("error_description")}
