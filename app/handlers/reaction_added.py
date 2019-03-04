from .. import slack_manager


@slack_manager.on('reaction_added')
async def sometimes_same_reaction(sender, data, **extra):
    event = data['event']
    item = event['item']

    sender.api_call(
        'reactions.add',
        channel=item['channel'],
        timestamp=item['ts'],
        name=event['reaction'])
