def bind(widget, event):
    def decorator(func):
        widget.bind(event, func)
        return func

    return decorator
