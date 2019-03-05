from functools import wraps


def on_channel_types(*types):
    def decorator(f):
        @wraps(f)
        async def decorated_handler(sender, data, **extra):
            if data['event']['channel_type'] in types:
                await f(sender, data, **extra)
        return decorated_handler
    return decorator


def is_not_me(f):
    @wraps(f)
    async def decorated_handler(sender, data, **extra):
        event = data['event']
        if event.get('bot_id') != extra['bot_id'] and\
                event.get('user') != extra['bot_user_id']:
            await f(sender, data, **extra)
    return decorated_handler
