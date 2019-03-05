from .. import slack_manager
from .decorators import is_not_me


@slack_manager.on('reaction_added')
@is_not_me
async def same_reaction(sender, data, **extra):
    event = data['event']
    item = event['item']

    sender.api_call(
        'reactions.add',
        channel=item['channel'],
        timestamp=item['ts'],
        name=event['reaction'])
