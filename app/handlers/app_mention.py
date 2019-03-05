import re

from .. import slack_manager


@slack_manager.on('app_mention')
async def reply_message(sender, data, **extra):
    event = data['event']

    if re.search(r'\blife\b', event['text'], re.I):
        text = 'Life, don\'t talk to me about life'
    else:
        text = f":robot_face: knock, knock, knock, <@{event['user']}>"

    sender.api_call(
        'chat.postMessage',
        channel=event['channel'],
        thread_ts=event['ts'],
        text=text)
