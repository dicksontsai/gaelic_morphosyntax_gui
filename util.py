def bind(widget, event):
    def decorator(func):
        widget.bind(event, func)
        return func

    return decorator

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
CONTENT_MIDDLE_X = 50
CONTENT_MIDDLE_Y = 50
SENTENCE_METADATA = ("sentence", "translation", "metatags")
#red_cross = Image.open("redx.png")
