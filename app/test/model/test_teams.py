from app.model.teams import Teams
from unittest.mock import patch
from unittest import mock
class TestTeams:

    @patch.object(Teams, 'send_channel_message')
    def test_send_channel_message_fail(self, mock_init_msal_application):
        # mock_init_msal_application.side_effect = Exception("It's can not get access token from msal client.")
        # teams_app = Teams("team_id", "channel_id")
        # with pytest.raises(Exception) as context:
        #     assert teams_app.send_channel_message("msg")
        # assert context.type == Exception
        # assert "It's can not get access token from msal client." in str(context.value)
        mock_init_msal_application.side_effect = mock.Mock(return_value=False)
        teams_app = Teams("team_id", "channel_id")
        assert teams_app.send_channel_message("msg") == False

    @patch.object(Teams, 'send_channel_message')
    def test_send_channel_message_success(self, mock_init_msal_application):
        mock_init_msal_application.side_effect = mock.Mock(return_value=True)
        teams_app = Teams("team_id", "channel_id")
        assert teams_app.send_channel_message("msg") == True
