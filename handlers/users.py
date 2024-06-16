import json

from aiogram import types
from aiogram.types import InputFile, ChatActions
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from api.client import GetProducts, GetAddress, SendBestProduct
from config import bot, CHAT_FEEDBACK_ID
from db.requests import get_user, create_user, check_user_best_products, create_best_product
from keyboards.inline import get_start_keyboard, get_product_keyboard, get_shops_keyboard
from config import dp
from class_group.states import FeedBackState
from .services_user import async_worker

async def start(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id - 1
        )
    except:
        pass
    await state.finish()
    user = await get_user(user_id=message.from_user.id)
    if user is None:
        await create_user(
            user_id=message.from_user.id, username=message.from_user.username
        )

    await bot.send_message(
        chat_id=message.from_user.id,
        text="Привет! Я - твой помощник в поисках выгодных товаров и предложений! \n\n"
        "Здесь ты сможешь найти товары по скидке в известных магазинах розничной торговли.\n\n",
        reply_markup=await get_start_keyboard(),
    )


async def choose_keyboard_start(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.answer_callback_query(callback.id)
    button = callback.data.split("_")[1]
    if button == "products":
        try:
            await bot.send_message(chat_id=callback.from_user.id,
                                   text="Выберите магазин:", reply_markup=await get_shops_keyboard())
        except Exception as exp:
            print(exp)
            await state.finish()
            await bot.send_message(chat_id=callback.from_user.id,
                                   text="Произошла ошибка. Попробуйте позже", reply_markup=await get_start_keyboard())


    if button == "feedback":
        await bot.send_message(
            chat_id=callback.from_user.id,
            text="Если у вас есть вопрос или предложение по сотрудничеству, напишите его сюда. Не забудьте указать контакты для связи с вами 👇\n\n"
                 "Для того, чтобы вернуться назад - нажмите /start",
        )
        await FeedBackState.message.set()

    if button == "shops":
        try:
            response = GetAddress()
        except Exception as exp:
            print(exp)
            await bot.send_message(
                chat_id=callback.from_user.id,
                text="Что-то пошло не так. Попробуйте позже.",
                reply_markup=await get_start_keyboard(),
            )
        else:
            results = json.loads(
                json.dumps(response.response.json(), ensure_ascii=False)
            )
            if results:
                message_text = ""
                for obj in results:
                    if obj["address"]:
                        message_text += f"*{obj['name']}:*\n"
                        for address in obj["address"]:
                            message_text += f"{address['city']['name']}, {address['street']}\n"
                await bot.send_message(text=message_text,
                                       chat_id=callback.from_user.id,
                                       parse_mode="Markdown",
                                       reply_markup=await get_start_keyboard())


async def choose_shop_keyboard(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    shop_id = callback.data.split("_")[1]
    url = f"http://127.0.0.1:8000/api/products?shop_id={shop_id}"
    try:
        response = GetProducts(url=url)
    except Exception as exp:
        print(exp)
        await bot.send_message(
            chat_id=callback.from_user.id,
            text="Что-то пошло не так",
            reply_markup=await get_start_keyboard(),
        )
    else:
        results = json.loads(
            json.dumps(response.response.json(), ensure_ascii=False)
        )
        print(results)
        if results['results']:
            url = f"[фото]({results['results'][0]['img_url']})"
            name = results["results"][0]["name"]
            name = name.replace("(", "\\(")
            name = name.replace(")", "\\)")
            name = name.replace("-", "\\-")
            price = results["results"][0]["price"]
            price = price.replace(".", "\\.")
            last_price = results["results"][0]["last_price"]
            last_price = last_price.replace(".", "\\.")
            discount = results["results"][0]["discount"]
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=f"{url}\n\n"
                f"*{name}*\n\n"
                f"Новая цена: *{price}*\n\n"
                f"Старая цена: ~{last_price}~\n\n"
                f"Скидка: *{discount}%*\n\n"
                f"Для того чтобы вернуться назад \\- нажмите /start\n\n"
                f"Вы можете поставить лайк 👍 1 товару, если вам понравилась скидка на него\n\n1 👍 на 1 день",
                parse_mode="MarkdownV2",
                reply_markup=await get_product_keyboard(
                    prev_url=results["previous"], next_url=results["next"], product_id=results["results"][0]["id"]
                ),
            )
        else:
            await bot.send_message(chat_id=callback.from_user.id,
                                   text="Товаров нет :(\n\nВыберите другой магазин:", reply_markup=await get_shops_keyboard())


async def choose_product_keyboard(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    button_or_url = callback.data.split("-")[1]
    if button_or_url == "like":
        # if not await check_user_best_products(user_id=callback.from_user.id):
        #     await callback.answer(text="Ваш голос принят!", show_alert=True)
        #     await create_best_product(user_id=callback.from_user.id, message_id=callback.message.message_id)
        #     # await bot.copy_message(chat_id=callback.from_user.id, from_chat_id=callback.from_user.id, message_id=callback.message.message_id)
        # else:
        #     await callback.answer(text="Вы уже проголосовали!", show_alert=True)
        # return
        try:
            response = SendBestProduct(product_id=int(callback.data.split("-")[2]), telegram_id=int(callback.from_user.id))
        except Exception as exp:
            print(exp)
        else:
            if response.response.status_code == 201:
                await callback.answer(text="Ваш голос принят!", show_alert=True)
            elif response.response.status_code == 400:
                await callback.answer(text="Вы уже проголосовали! Позже вы сможете проголосовать опять", show_alert=True)
            else:
                await callback.answer(text="Что-то пошло не так. Попробуйте позже", show_alert=True)
        return
    await bot.answer_callback_query(callback.id)
    if button_or_url != "None":
        await bot.delete_message(
            chat_id=callback.from_user.id, message_id=callback.message.message_id
        )
        try:
            response = GetProducts(url=button_or_url)
        except Exception as exp:
            print(exp)
        else:
            results = json.loads(
                json.dumps(response.response.json(), ensure_ascii=False)
            )
            url = f"[фото]({results['results'][0]['img_url']})"
            name = results["results"][0]["name"]
            name = name.replace("(", "\\(")
            name = name.replace(")", "\\)")
            name = name.replace("-", "\\-")
            price = results["results"][0]["price"]
            price = price.replace(".", "\\.")
            last_price = results["results"][0]["last_price"]
            last_price = last_price.replace(".", "\\.")
            discount = results["results"][0]["discount"]
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=f"{url}\n\n"
                f"*{name}*\n\n"
                f"Новая цена: *{price}*\n\n"
                f"Старая цена: ~{last_price}~\n\n"
                f"Скидка: *{discount}%*\n\n"
                f"Для того чтобы вернуться назад \\- нажмите /start\n\n"
                f"Вы можете поставить лайк 👍 1 товару, если вам понравилась скидка на него\n\n1 👍 на 1 день",
                parse_mode="MarkdownV2",
                reply_markup=await get_product_keyboard(
                    prev_url=results["previous"], next_url=results["next"], product_id=results["results"][0]["id"]
                ),
            )

async def feedback_message(message: types.Message, state: FSMContext):
    if message.text == "/start":
        await start(message, state)
        return
    await bot.send_message(CHAT_FEEDBACK_ID,
                           text=f"Username: @{message.from_user.username}\n\n"
                                f"ID: {message.from_user.id}\n\n"
                                f"Сообщение: {message.text}")
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Ваше сообщение принято!",
        reply_markup=await get_start_keyboard(),
    )
    await state.finish()


def setup(dp):
    async_worker()
    dp.register_message_handler(start, commands="start", state=None)
    dp.register_callback_query_handler(
        choose_keyboard_start, Text(startswith="start_"), state=None
    )
    dp.register_callback_query_handler(
        choose_product_keyboard, Text(startswith="product-"), state=None
    )
    dp.register_callback_query_handler(
        choose_shop_keyboard, Text(startswith="shop_"), state=None
    )
    dp.register_message_handler(
        feedback_message, content_types=['text'], state=FeedBackState.message
    )
