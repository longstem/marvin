from .. import slack_manager


@slack_manager.on('team_join')
async def welcome(sender, data, **extra):
    event = data['event']
    text = f"Welcome <@{event['user']['id']}> !!"
    sender.api_call('chat.postMessage', channel=event['channel'], text=text)
