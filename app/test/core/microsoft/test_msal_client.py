# from app.core.microsoft import graph_client, msal_client
from app.core.microsoft.msal_client import MSALClient
from unittest.mock import Mock, patch
from unittest import mock

class TestMSALClient:

    # @patch.object(MSALClient, '_init_msal_application')
    # def setUp(self):
        # mock_get_access_token.return_value = {"result":"success"}
        # self.msal_app = MSALClient()

    
    # @pytest.mark.asyncio
    # @mock.patch("app.core.microsoft.msal_client.MSALClient")
    # def test_get_msal_access_token(self):
    #     mock_response = mock.Mock(return_value={"result":"success", "access_token":"test_token"})
    #     msal_app = msal_client.MSALClient()
    #     msal_app.get_access_token = mock_response.return_value
    #     result = msal_app.get_ip
    #     assert result == "192.168.1.1"

    # @patch.object(MSALClient, 'get_access_token')
    # def test_get_access_token(self, mock_get_access_token):
    #     mock_get_access_token.return_value = {"result":"success"}
    #     msal_app = MSALClient()
    #     result = msal_app.get_access_token() 
    #     assert result["result"] == "success"

    # @patch("app.core.microsoft.msal_client.MSALClient")
    # def test_get_access_token(self, mock_MSALClient):
    #     b = mock_MSALClient.return_value
    #     b.msal_client.return_value = "123"
    #     msal_app = MSALClient()
    #     result = msal_app._init_msal_application() 
    #     assert b.msal_client.return_value == "123"
    
    # @patch.object(MSALClient, 'get_ip')
    # def test_get_ip(self, mock_get_ip):
    #     mock_get_ip.return_value = "192.168.1.1"
    #     msal_app = MSALClient()
    #     result = msal_app.get_ip() 
    #     assert result == "192.168.1.1"

    @patch.object(MSALClient, '_init_msal_application')
    def test_get_access_token_success(self, mock_init_msal_application):
        # mock_get_ip.return_value = "192.168.1.1"
        # msal_app = MSALClient()
        # result = msal_app.get_ip() 
        # assert result == "192.168.1.1"
        # mock_response = mock.Mock(return_value="192.168.1.1")
        msal_app = MSALClient()
        msal_app.get_access_token = Mock(return_value={"result":"success", "access_token": "token"})
        result = msal_app.get_access_token()
        assert result["result"] == "success"
        assert "access_token" in result

    @patch.object(MSALClient, '_init_msal_application')
    def test_get_access_token_fail(self, mock_init_msal_application):
        # mock_get_ip.return_value = "192.168.1.1"
        # msal_app = MSALClient()
        # result = msal_app.get_ip() 
        # assert result == "192.168.1.1"
        # mock_response = mock.Mock(return_value="192.168.1.1")
        msal_app = MSALClient()
        msal_app.get_access_token = Mock(return_value={"result":"fail", "msg": "error_message", "detail": "error_description"})
        result = msal_app.get_access_token()
        assert result["result"] == "fail"
        assert "msg" in result
        assert "detail" in result