import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.client import GetAllProductsAndShop, GetDetailProduct, GetBestProduct
from db.requests import get_log_products, save_log_products, update_was_send_product, get_log_product_first, delete_log_product
from db.models import LogSendProdcut
from config import bot, CHAT_DISCOUNT_ID


scheduler = AsyncIOScheduler()


async def get_all_products_and_shop():
    try:
        response = GetAllProductsAndShop()
    except Exception as exp:
        print(exp)
        return
    else:
        results = json.loads(
            json.dumps(response.response.json(), ensure_ascii=False)
        )
        to_save_products = []
        if results:
            for obj in results:
                to_save_products.append(LogSendProdcut(product_id=obj['id'], shop_id=obj['shop']))
            await save_log_products(to_save_products)
        await interval_send_product()


async def get_product_detail(product_id):
    print(f"product_id = {product_id}")
    try:
        response = GetDetailProduct(product_id=product_id)
    except Exception as exp:
        print(exp)
        return
    else:
        results = json.loads(
            json.dumps(response.response.json(), ensure_ascii=False)
        )
        if results and results.get('id', False):
            bot_url = f"[БОТA](https://t.me/store_promotions_ru_bot)"
            url = f"[фото]({results['img_url']})"
            name = results["name"]
            name = name.replace("(", "\\(")
            name = name.replace(")", "\\)")
            name = name.replace("-", "\\-")
            price = results["price"]
            price = price.replace(".", "\\.")
            last_price = results["last_price"]
            last_price = last_price.replace(".", "\\.")
            discount = results["discount"]
            message_text = f"{url}\n\n"\
                           f"*{name}*\n\n"\
                           f"Новая цена: *{price}*\n\n"\
                           f"Старая цена: ~{last_price}~\n\n"\
                           f"Скидка: *{discount}%*\n\n" \
                           f"Чтобы найти все товары по скидке и магазины, подписывайтесь на {bot_url}"
            return message_text
        return None


async def interval_send_product():
    print("START SHEDL")
    if await get_log_products():
        product = await get_log_product_first()
        print(f"product = {product}")
        if product:
            message_text = await get_product_detail(product_id=product.product_id)
            if message_text:
                await bot.send_message(
                    chat_id=CHAT_DISCOUNT_ID,
                    text=message_text,
                    parse_mode="MarkdownV2",
                )
                await update_was_send_product(product_id=product.product_id)
            else:
                await delete_log_product()
                await get_all_products_and_shop()
        else:
            await delete_log_product()
            await get_all_products_and_shop()
    else:
        await get_all_products_and_shop()


async def send_best_product():
    try:
        response = GetBestProduct()
    except Exception as exp:
        print(exp)
        return
    else:
        results = json.loads(
            json.dumps(response.response.json(), ensure_ascii=False)
        )
        print(results)
        if response.response.status_code == 200 and results.get('id', False):
            bot_url = f"[БОТA](https://t.me/store_promotions_ru_bot)"
            url = f"[фото]({results['img_url']})"
            name = results["name"]
            name = name.replace("(", "\\(")
            name = name.replace(")", "\\)")
            name = name.replace("-", "\\-")
            price = results["price"]
            price = price.replace(".", "\\.")
            last_price = results["last_price"]
            last_price = last_price.replace(".", "\\.")
            discount = results["discount"]
            await bot.send_message(
                chat_id=CHAT_DISCOUNT_ID,
                text=f"{url}\n\n"
                     f"Лучший товар по мнению пользователей {bot_url}\n\n"
                     f"*{name}*\n\n"
                     f"Новая цена: *{price}*\n\n"
                     f"Старая цена: ~{last_price}~\n\n"
                     f"Скидка: *{discount}%*\n\n",
                parse_mode="MarkdownV2",
            )
        else:
            return



def async_worker():
    # scheduler.add_job(interval_send_product,
    #                   'interval',
    #                   hours=1)
    print("async_worker start")
    scheduler.add_job(interval_send_product,
                      'interval',
                      hours=1)
    # scheduler.add_job(send_best_product,
    #                   'interval',
    #                   seconds=20
    #                   )
    scheduler.add_job(send_best_product,
                      'cron',
                      hour=10, minute=0
                      )
    scheduler.start()
