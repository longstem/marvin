import re

from .. import slack_manager


@slack_manager.on('app_mention')
def reply_message_about_life(sender, event):
    if re.search(r'\blife\b', event['text'], re.I):
        text = 'Life, don\'t talk to me about life'
    else:
        text = ':robot_face:'

    sender.slack_client.api_call(
        'chat.postMessage',
        channel=event['channel'],
        thread_ts=event['ts'],
        text=text)
