from telegram import InlineKeyboardButton
from typing import Union, List


def build_menu(
        buttons: List[InlineKeyboardButton],
        n_cols: int,
        header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None,
        footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu


def to_offer(filters):
    res = ""
    for filter in filters:
        res += 'Offer:\n' \
               f'Details: {filter[0]}\n' \
               f'Needs to be delivered to: {filter[1]}\n' \
               f'Pays: {filter[2]}\n\n'

    return res
