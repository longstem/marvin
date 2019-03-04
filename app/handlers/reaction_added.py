import random

from .. import slack_manager


@slack_manager.on('reaction_added')
def sometimes_same_reaction(sender, event):
    if random.choice([True, False]):
        item = event['item']

        sender.slack_client.api_call(
            'reactions.add',
            channel=item['channel'],
            timestamp=item['ts'],
            name=event['reaction'])
