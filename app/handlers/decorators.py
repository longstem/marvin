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
    async def decorated_handler(sender, data, bot_id, **extra):
        if data['event'].get('bot_id', '') != bot_id:
            await f(sender, data, bot_id=bot_id, **extra)
    return decorated_handler
