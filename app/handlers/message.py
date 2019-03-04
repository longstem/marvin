from .. import slack_manager
from .decorators import is_not_me, on_channel_types


@slack_manager.on('message')
@is_not_me
@on_channel_types('im')
async def im_reply(sender, data, **extra):
    channel = data['event']['channel']
    text = 'I could calculate your chance of survival, but you won’t like it'
    sender.api_call('chat.postMessage', channel=channel, text=text)
