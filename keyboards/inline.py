import json
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api.client import GetShops

async def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            text="Товары по акции 💯", callback_data="start_products"
        ),  # 💯
        InlineKeyboardButton(
            text="Обратная связь ❓", callback_data="start_feedback"
        ),  # ❓
        InlineKeyboardButton(text="Магазины 🛒", callback_data="start_shops"),  # 🛒
    )
    return keyboard


async def get_product_keyboard(prev_url, next_url, product_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="⬅️", callback_data=f"product-{prev_url}"),
        InlineKeyboardButton(text="➡️", callback_data=f"product-{next_url}"),
        InlineKeyboardButton(text="👍", callback_data=f"product-like-{product_id}"),
    )
    return keyboard


async def get_shops_keyboard():
    response = GetShops()
    results = json.loads(
                json.dumps(response.response.json(), ensure_ascii=False)
            )
    print(results)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for object in range(0, len(results)):
        keyboard.add(
            InlineKeyboardButton(text=results[object]["name"], callback_data=f"shop_{results[object]['id']}"),
        )
    return keyboard
