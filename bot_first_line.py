# -*- coding: cp1251 -*-
import csv
import datetime as dt
import json
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.filters import Command, Text

# from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InputFile, MediaGroup
from aiogram.utils.markdown import hbold, hitalic, hlink, text
from config import TOKEN, admin_id, new_csv_file, users
from emoji import emojize

my_path = f"{os.getcwd()}\\telegram_bot_aiogram3"
confirm_dict = {}  # dict for all users
id_set = set()  # obtained id for .txt file

# ! DO NOT open .csv using Excel while running (allowed in VS Code)
# new run -> new file(empty)
if new_csv_file:
    new_name_file = rf'{my_path}\telegram_data_{str(dt.datetime.now().time())[0:8].replace(":", "+")}.csv'
    with open(new_name_file, "w", newline="") as fp:
        writer = csv.writer(fp, delimiter="$", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(("date", "time", "user_id", "user_full_name", "message"))
else:
    with open(rf"{my_path}\telegram_data.csv", "w", newline="") as fp:
        writer = csv.writer(fp, delimiter="$", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(("date", "time", "user_id", "user_full_name", "message"))


async def save_info(message: types.Message):
    """Save info about user and their message"""

    user_date = str(dt.datetime.now().date())
    user_time = str(dt.datetime.now().time())[0:11]
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_message = message.text

    user_data = (user_date, user_time, user_id, user_full_name, user_message)

    # saving all data
    if new_csv_file:
        with open(new_name_file, "a", newline="") as fp:
            writer = csv.writer(
                fp, delimiter="$", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(user_data)
    else:
        with open(rf"{my_path}\telegram_data.csv", "a", newline="") as fp:
            writer = csv.writer(
                fp, delimiter="$", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(user_data)

    # separately saving user_id
    with open(rf"{my_path}\users_list.txt", "a") as ouf:
        if user_id not in id_set:
            ouf.write(str(user_id))
            ouf.write("\n")
            id_set.add(user_id)
        else:
            pass


token_first_bot = TOKEN
bot = Bot(token=token_first_bot, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


# commands = {
#     "about us": {
#         "button_text": "О нас",
#         "msg_after_clicking": "Мы команда инициативных стартаперов!",
#     },
#     # "bot": {
#     #
#     # },
#     "support": {
#         "button_text": "Поддержка",
#         "msg_after_clicking": "Чтобы получить помощь, перейдите по",
#     },
#     "services": {
#         "button_text": "Услуги",
#         "msg_after_clicking": "Наши услуги носят разнообразный характер",
#     },
#     "refund": {
#         "button_text": "Возврат",
#         "msg_after_clicking": "Чтобы вернуть товар, приходите на угол улицы Пушкина, дом Колотушкина",
#     },
#     "buying": {
#         "button_text": "Купить",
#         "msg_after_clicking": "Выберите продукт",
#         "leads_to": {
#             "1 product": {
#                 "button_text": "Первый продукт",
#                 "msg_after_clicking": "Выберите локацию",
#                 "leads_to": {
#                     "1 location": {
#                         "button_text": "Санкт-Петербург, ул.Строителей, д.28",
#                         "msg_after_clicking": "Выберите тип",
#                         "leads_to": {
#                             "1 type": {
#                                 "button_text": "Тип №1",
#                                 "msg_after_clicking": "Всё верно?",  # * выдавать сообщение из заполненной инфы
#                                 "leads_to": {
#                                     "summary": {
#                                         "confirm": {
#                                             "button_text": "Да",
#                                             "msg_after_clicking": "Выберите способ оплаты",
#                                             "leads_to": {
#                                                 "way_to_pay": {
#                                                     "1 way": {
#                                                         "button_text": "Перевод по карте",
#                                                         "msg_after_clicking": "А что дальше хз",
#                                                     },
#                                                     "2 way": {
#                                                         "button_text": "Через биткоины",
#                                                         "msg_after_clicking": "А что дальше хз 2",
#                                                     },
#                                                 }
#                                             },
#                                         },
#                                         "refuse": {
#                                             "button_text": "Нет",
#                                             "msg_after_clicking": "Вы вернулись в меню",
#                                             "leads_to": {},  # to "buying" branch
#                                         },
#                                     }
#                                 },
#                             },
#                             "2 type": {
#                                 "button_text": "Тип №2",
#                                 # "msg_after_clicking": {}  # same as for 1 type
#                                 # "leads_to": {}  # same as for 1 type
#                             },
#                         },
#                     },
#                     "2 location": {
#                         "button_text": "Москва, пл.Мира, д.1",
#                         # "leads_to":{}  # same as for 1 location
#                     },
#                     "3 location": {
#                         "button_text": "Рязань, пр.Ленина, 76",
#                         # "leads_to":{}  # same as for 1 location
#                     },
#                 },
#             },
#             "2 product": {
#                 "button_text": "Второй продукт"
#             },  # same as for 1 product
#             "3 product": {
#                 "button_text": "Третий продукт"
#             },  # same as for 1 product
#         },
#     },
#     "menu": {
#         "button_text": "В меню",
#         "msg_after_clicking": "Вы вернулись в меню",
#     },
# }

# # saving json
# with open(rf"{my_path}\commands_dict.json", "w") as fp:
#     json.dump(commands, fp, indent=4, sort_keys=True, ensure_ascii=False)

# loading json
with open(rf"{my_path}\commands_dict.json") as f:
    commands = json.load(f)

# ============================================================

# after /start
@dp.message_handler(commands="start")
async def start(message: types.Message):

    user_key = message.from_user.id
    if user_key not in confirm_dict.keys():
        confirm_dict[user_key] = {"product": None, "location": None, "type": None}
    else:
        pass

    start_buttons = [
        commands["about us"]["button_text"],
        commands["support"]["button_text"],
        commands["services"]["button_text"],
        commands["refund"]["button_text"],
        commands["buying"]["button_text"],
    ]
    # input_field_placeholder is visible on PC (in the background of input line)
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
    )
    keyboard.add(*start_buttons)

    msg = text(
        hbold("Здравствуйте!"),
        'Рады приветствовать вас в нашем сервисе "Крутой бот".',
        "\nДоступные команды:",
        "/start - начать работу с ботом",
        "/support - получить помощь",
        "/photo - *зарядиться энергией",
        "/album - *зарядиться энергией 2x",
        "\nКонтакты:",
        "8(800)555-35-35",
        sep="\n",
    )

    await message.answer(msg, reply_markup=keyboard)
    await save_info(message)


# ============================================================

# after /about us
@dp.message_handler(Text(equals=commands["about us"]["button_text"]))
async def start(message: types.Message):

    await message.answer(commands["about us"]["msg_after_clicking"])
    await save_info(message)


# ============================================================

# after /support
@dp.message_handler(Text(equals=commands["support"]["button_text"]))
async def start(message: types.Message):
    msg = text(
        commands["support"]["msg_after_clicking"],
        hlink(
            title="ссылке",
            url="http://t.me/danya_support_bot",
        ),
    )
    await message.answer(msg)
    await save_info(message)


# ============================================================

# after /services
@dp.message_handler(Text(equals=commands["services"]["button_text"]))
async def start(message: types.Message):

    msg = text(emojize(f'{commands["services"]["msg_after_clicking"]} :smirking_face:'))
    await message.answer(msg)
    await save_info(message)


# ============================================================

# after /refund
@dp.message_handler(Text(equals=commands["refund"]["button_text"]))
async def start(message: types.Message):

    await message.answer(commands["refund"]["msg_after_clicking"])
    await save_info(message)


# ============================================================

# after /buying
@dp.message_handler(Text(equals=commands["buying"]["button_text"]))
async def first_but(message: types.Message):
    buttons = [
        commands["buying"]["leads_to"]["1 product"]["button_text"],
        commands["buying"]["leads_to"]["2 product"]["button_text"],
        commands["buying"]["leads_to"]["3 product"]["button_text"],
        commands["menu"]["button_text"],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, input_field_placeholder="Выберите продукт"
    )
    keyboard.row(*buttons)  # buttons in one line

    await message.answer(
        commands["buying"]["msg_after_clicking"], reply_markup=keyboard
    )
    await save_info(message)


# ============================================================

# after buying-1st product
@dp.message_handler(
    Text(
        equals=[
            commands["buying"]["leads_to"]["1 product"]["button_text"],
            commands["buying"]["leads_to"]["2 product"]["button_text"],
            commands["buying"]["leads_to"]["3 product"]["button_text"],
        ]
    )
)
async def first_prod(message: types.Message):

    user_key = message.from_user.id
    confirm_dict[user_key]["product"] = message.text

    buttons = [
        [
            types.KeyboardButton(
                text=commands["buying"]["leads_to"]["1 product"]["leads_to"][
                    "1 location"
                ]["button_text"]
            )
        ],
        [
            types.KeyboardButton(
                text=commands["buying"]["leads_to"]["1 product"]["leads_to"][
                    "2 location"
                ]["button_text"]
            )
        ],
        [
            types.KeyboardButton(
                text=commands["buying"]["leads_to"]["1 product"]["leads_to"][
                    "3 location"
                ]["button_text"]
            )
        ],
        [types.KeyboardButton(text=commands["menu"]["button_text"])],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите локацию",
    )

    await message.answer(
        commands["buying"]["leads_to"]["1 product"]["msg_after_clicking"],
        reply_markup=keyboard,
    )
    await save_info(message)


# ============================================================

# after buying-1st product-1 location
@dp.message_handler(
    Text(
        equals=[
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
                "button_text"
            ],
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["2 location"][
                "button_text"
            ],
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["3 location"][
                "button_text"
            ],
        ]
    )
)
async def first_but(message: types.Message):

    user_key = message.from_user.id
    confirm_dict[user_key]["location"] = message.text

    buttons = [
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["1 type"]["button_text"],
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["2 type"]["button_text"],
        commands["menu"]["button_text"],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, input_field_placeholder="Выберите тип"
    )
    keyboard.add(*buttons)

    # msg = text(
    #     commands["1 product"]["leads_to"]["buy"]["msg_after_clicking"],
    #     hlink(title="ссылке", url="http://t.me/danya_support_bot"),
    # )

    await message.answer(
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "msg_after_clicking"
        ],
        reply_markup=keyboard,
    )
    await save_info(message)


# ============================================================

# after buying-1st product-1 location-1 type
@dp.message_handler(
    Text(
        equals=[
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
                "leads_to"
            ]["1 type"]["button_text"],
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
                "leads_to"
            ]["2 type"]["button_text"],
        ]
    )
)
async def first_but(message: types.Message):

    user_key = message.from_user.id
    confirm_dict[user_key]["type"] = message.text

    buttons = [
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["1 type"]["leads_to"]["summary"]["confirm"]["button_text"],
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["1 type"]["leads_to"]["summary"]["refuse"]["button_text"],
        commands["menu"]["button_text"],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Подтвердите заказ",
    )
    keyboard.add(*buttons)

    msg = text(
        hbold("Ваш заказ:"),
        f'{hitalic("Продукт:")} {confirm_dict[user_key]["product"]}',
        f'{hitalic("Адрес:")} {confirm_dict[user_key]["location"]}',
        f'{hitalic("Тип:")} {confirm_dict[user_key]["type"]}\n',
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["1 type"]["msg_after_clicking"],
        sep="\n",
    )

    await message.answer(
        msg,
        reply_markup=keyboard,
    )
    await save_info(message)


# ============================================================

# after buying-1st product-1 location-1 type-confirm
@dp.message_handler(
    Text(
        equals=[
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
                "leads_to"
            ]["1 type"]["leads_to"]["summary"]["confirm"]["button_text"]
        ]
    )
)
async def first_but(message: types.Message):

    buttons = [
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["1 type"]["leads_to"]["summary"]["confirm"]["leads_to"]["way_to_pay"][
            "1 way"
        ][
            "button_text"
        ],
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["1 type"]["leads_to"]["summary"]["confirm"]["leads_to"]["way_to_pay"][
            "2 way"
        ][
            "button_text"
        ],
        commands["menu"]["button_text"],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Выберите способ оплаты",
        one_time_keyboard=True,
    )
    keyboard.add(*buttons)

    msg = text(
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["1 type"]["leads_to"]["summary"]["confirm"]["msg_after_clicking"]
    )

    await message.answer(
        msg,
        reply_markup=keyboard,
    )
    await save_info(message)


# ============================================================

# after buying-1st product-1 location-1 type-refuse
@dp.message_handler(
    Text(
        equals=[
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
                "leads_to"
            ]["1 type"]["leads_to"]["summary"]["refuse"]["button_text"]
        ]
    )
)
async def first_but(message: types.Message):

    start_buttons = [
        commands["about us"]["button_text"],
        commands["support"]["button_text"],
        commands["services"]["button_text"],
        commands["refund"]["button_text"],
        commands["buying"]["button_text"],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
    )
    keyboard.add(*start_buttons)

    msg = text(
        commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
            "leads_to"
        ]["1 type"]["leads_to"]["summary"]["refuse"]["msg_after_clicking"]
    )

    await message.answer(
        msg,
        reply_markup=keyboard,
    )
    await save_info(message)


# ============================================================

# after buying-1st product-1 location-1 type-confirm-way_to_pay
@dp.message_handler(
    Text(
        equals=[
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
                "leads_to"
            ]["1 type"]["leads_to"]["summary"]["confirm"]["leads_to"]["way_to_pay"][
                "1 way"
            ][
                "button_text"
            ],
            commands["buying"]["leads_to"]["1 product"]["leads_to"]["1 location"][
                "leads_to"
            ]["1 type"]["leads_to"]["summary"]["confirm"]["leads_to"]["way_to_pay"][
                "2 way"
            ][
                "button_text"
            ],
        ]
    )
)
async def first_but(message: types.Message):
    msg = text(
        "Для оплаты переходите в наш",
        hlink(
            title="чат-бот сопровождения",
            url="http://t.me/danya_support_bot",
        ),
    )
    await message.answer(msg)
    await save_info(message)


# ============================================================

# back to menu
@dp.message_handler(
    Text(equals=commands["menu"]["button_text"])
)  #! сделать много возвратов в меню equals=список
async def first_but(message: types.Message):
    start_buttons = [
        commands["about us"]["button_text"],
        commands["support"]["button_text"],
        commands["services"]["button_text"],
        commands["refund"]["button_text"],
        commands["buying"]["button_text"],
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer(commands["menu"]["msg_after_clicking"], reply_markup=keyboard)
    await save_info(message)


# ============================================================

# to send ONE picture
@dp.message_handler(commands="photo")
async def send_photo(message: types.Message):

    chat_id = message.from_user.id  # obligatory to use
    photo_bytes = InputFile(path_or_bytesio=rf"{my_path}\picture_1.jpg")

    await dp.bot.send_photo(
        chat_id=chat_id, photo=photo_bytes, caption=text(emojize("Держи! :fire:"))
    )
    await save_info(message)


# ============================================================

# to send an album (FEW pictures or files)
@dp.message_handler(commands="album")
async def send_album(message: types.Message):

    our_album = MediaGroup()

    photo_bytes_1 = InputFile(path_or_bytesio=rf"{my_path}\dog.jpg")
    photo_bytes_2 = InputFile(path_or_bytesio=rf"{my_path}\cat.png")
    # one caption for whole album
    our_album.attach_photo(
        photo=photo_bytes_1,
        caption=text(emojize("Какие они... :broken_heart:")),
    )
    our_album.attach_photo(photo=photo_bytes_2)

    await message.answer_media_group(media=our_album)
    await save_info(message)


# ============================================================

# for mailing (all users in list)
@dp.message_handler(Command("mailing"))  # using Command is obligatory
async def start_mailing(message: types.Message):

    if message.chat.id in admin_id:
        for user in list(id_set):
            await bot.send_message(user, message.text[message.text.find(" ") + 1 :])
            # write: "/mailing <text>". Space is necessary!
        await message.answer(
            "Милорд, рассылка прошла успешно"
        )
        await save_info(message)
    else:  # block not-admins and save info
        await message.answer(f'Команда "{message.text}" не найдена')
        await save_info(message)


# ============================================================

# for sending message to particular user
@dp.message_handler(Command("personal"))  # using Command is obligatory
async def start_mailing(message: types.Message):

    if message.chat.id in admin_id:
        id = message.text.split(" ")[1]
        msg = message.text.split(" ")[2:]
        text_to_send = " ".join(msg)

        await bot.send_message(id, text_to_send)
        # write: "/personal <user_id> <text>". Spaces are necessary!
        await message.answer(
            f'Вы отправили сообщение "{text_to_send}" пользователю {id}'
        )
        await save_info(message)

    else:  # block not-admins and save info
        await message.answer(f'Команда "{message.text}" не найдена')
        await save_info(message)


# ============================================================

# if non-available text
@dp.message_handler()
async def command_error(message: types.Message):

    await message.answer(f'Команда "{message.text}" не найдена')
    await save_info(message)


# ============================================================

# saving photo
@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def save_photo(message: types.Message):
    """Save photo/file from user"""

    user_date = f"{dt.datetime.now().date():%d-%m-%Y}"
    user_time = str(dt.datetime.now().time())[0:8].replace(":", "_")
    user_fullname = message.from_user.full_name
    user_caption = message.caption

    file_photo = await bot.get_file(message.photo[-1].file_id)
    file_name_old, file_extension = os.path.splitext(file_photo.file_path)
    file_name_new = (
        f"{user_date}+{user_fullname}+{user_time}+{user_caption}{file_extension}"
    )

    await bot.download_file_by_id(
        message.photo[-1].file_id,
        destination=rf"{my_path}\photos\{file_name_new}",
    )


# ============================================================

# saving file
@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def save_file(message: types.Message):
    """Save photo/file from user"""

    user_date = f"{dt.datetime.now().date():%d-%m-%Y}"
    user_time = str(dt.datetime.now().time())[0:8].replace(":", "_")
    user_fullname = message.from_user.full_name
    user_caption = message.caption

    file_document = await bot.get_file(message.document.file_id)
    file_name_old, file_extension = os.path.splitext(file_document.file_path)
    file_name_new = (
        f"{user_date}+{user_fullname}+{user_time}+{user_caption}{file_extension}"
    )

    await bot.download_file_by_id(
        message.document.file_id,
        destination=rf"{my_path}\photos\{file_name_new}",
    )


# ============================================================

# answer for voice message
@dp.message_handler(content_types=[types.ContentType.VOICE])
async def save_photo(message: types.Message):
    await message.answer(
        "Оператор не может прослушать ваше сообщение. Напишите, пожалуйста, текстом"
    )


# ============================================================

# answer for video
@dp.message_handler(content_types=[types.ContentType.VIDEO])
async def save_photo(message: types.Message):
    await message.answer(
        "Оператор не может посмотреть ваше видео. Пришлите, пожалуйста, фото"
    )


# ============================================================

# answer for sticker
@dp.message_handler(content_types=[types.ContentType.STICKER])
async def save_photo(message: types.Message):
    await message.answer(
        "Бот плохо воспринимает информацию через стикеры. Напишите, пожалуйста, текстом"
    )


# ============================================================

print("Бот запущен")  # output in console


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


# * 1. оставить кнопки такими или сделать их под сообщением - оставить так -- ГОТОВО
# * 2. норм ли такой формат записи json -- норм
# * 3. админ должен писать челику напрямую через тг -- ГОТОВО
# * норм ли, если отдельно в файл csv будут выводиться сообщения от чела? (с пометкой имени от кого) -- ГОТОВО
# * 4. надо ли просматривать фото, присланную челом? -- можно! -- ГОТОВО
# * 5. должен ли бот слать фото? -- нет, но написать код который -- ГОТОВО (и для альбомов тоже)

# * 1. отдельно вести txt файл с id людей для рассылки -- ГОТОВО
# TODO 2. функция для рассылки должна считывать условие из другого .py файла (если там сообщение alarm,
# TODO то пользователям отправляется смс)
# 3. глянуть есть ли норм интерфейсы для админов (чтобы писать не через консоль) - мб через help_desk
# 4. глянуть опыт самоката
# * 5. добить дерево
# 6. подумать про бот поддержки
# * 7. генерировать в конце сообщение для пользователя с введенной инфой
# * 8. сделать параметр в конфиг (true в старом файле, false в новом)
# TODO 9. везде добавить кнопку в главное меню
# ! к выходным закончить
