import os
from linebot import (
    LineBotApi
)
from linebot.models import (
    RichMenu, RichMenuArea, RichMenuSize, RichMenuBounds,
    MessageAction, URIAction
)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)


def create_rich_menu():
    result = False
    try:
        # define a new rich menu
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=1200, height=405),
            selected=True,
            name='RichMenu for j-bot',
            chat_bar_text='TAP HERE',
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=500, height=405),
                    action=URIAction(label='Open Google Map', uri='https://www.google.co.jp/maps/?hl=ja')
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=480, y=0, width=700, height=405),
                    action=MessageAction(text='Menu 2')
                )
            ]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        # upload an image for rich menu
        path = '../static/rich_menu/rich_menu_sample.png'
        with open(path, 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)
        # set the default rich menu
        line_bot_api.set_default_rich_menu(rich_menu_id)
        result = True
    except Exception:
        result = False
    return result
