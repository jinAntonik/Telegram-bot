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
#         "button_text": "Î íàñ",
#         "msg_after_clicking": "Ìû êîìàíäà èíèöèàòèâíûõ ñòàðòàïåðîâ!",
#     },
#     # "bot": {
#     #
#     # },
#     "support": {
#         "button_text": "Ïîääåðæêà",
#         "msg_after_clicking": "×òîáû ïîëó÷èòü ïîìîùü, ïåðåéäèòå ïî",
#     },
#     "services": {
#         "button_text": "Óñëóãè",
#         "msg_after_clicking": "Íàøè óñëóãè íîñÿò ðàçíîîáðàçíûé õàðàêòåð",
#     },
#     "refund": {
#         "button_text": "Âîçâðàò",
#         "msg_after_clicking": "×òîáû âåðíóòü òîâàð, ïðèõîäèòå íà óãîë óëèöû Ïóøêèíà, äîì Êîëîòóøêèíà",
#     },
#     "buying": {
#         "button_text": "Êóïèòü",
#         "msg_after_clicking": "Âûáåðèòå ïðîäóêò",
#         "leads_to": {
#             "1 product": {
#                 "button_text": "Ïåðâûé ïðîäóêò",
#                 "msg_after_clicking": "Âûáåðèòå ëîêàöèþ",
#                 "leads_to": {
#                     "1 location": {
#                         "button_text": "Ñàíêò-Ïåòåðáóðã, óë.Ñòðîèòåëåé, ä.28",
#                         "msg_after_clicking": "Âûáåðèòå òèï",
#                         "leads_to": {
#                             "1 type": {
#                                 "button_text": "Òèï ¹1",
#                                 "msg_after_clicking": "Âñ¸ âåðíî?",  # * âûäàâàòü ñîîáùåíèå èç çàïîëíåííîé èíôû
#                                 "leads_to": {
#                                     "summary": {
#                                         "confirm": {
#                                             "button_text": "Äà",
#                                             "msg_after_clicking": "Âûáåðèòå ñïîñîá îïëàòû",
#                                             "leads_to": {
#                                                 "way_to_pay": {
#                                                     "1 way": {
#                                                         "button_text": "Ïåðåâîä ïî êàðòå",
#                                                         "msg_after_clicking": "À ÷òî äàëüøå õç",
#                                                     },
#                                                     "2 way": {
#                                                         "button_text": "×åðåç áèòêîèíû",
#                                                         "msg_after_clicking": "À ÷òî äàëüøå õç 2",
#                                                     },
#                                                 }
#                                             },
#                                         },
#                                         "refuse": {
#                                             "button_text": "Íåò",
#                                             "msg_after_clicking": "Âû âåðíóëèñü â ìåíþ",
#                                             "leads_to": {},  # to "buying" branch
#                                         },
#                                     }
#                                 },
#                             },
#                             "2 type": {
#                                 "button_text": "Òèï ¹2",
#                                 # "msg_after_clicking": {}  # same as for 1 type
#                                 # "leads_to": {}  # same as for 1 type
#                             },
#                         },
#                     },
#                     "2 location": {
#                         "button_text": "Ìîñêâà, ïë.Ìèðà, ä.1",
#                         # "leads_to":{}  # same as for 1 location
#                     },
#                     "3 location": {
#                         "button_text": "Ðÿçàíü, ïð.Ëåíèíà, 76",
#                         # "leads_to":{}  # same as for 1 location
#                     },
#                 },
#             },
#             "2 product": {
#                 "button_text": "Âòîðîé ïðîäóêò"
#             },  # same as for 1 product
#             "3 product": {
#                 "button_text": "Òðåòèé ïðîäóêò"
#             },  # same as for 1 product
#         },
#     },
#     "menu": {
#         "button_text": "Â ìåíþ",
#         "msg_after_clicking": "Âû âåðíóëèñü â ìåíþ",
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
        input_field_placeholder="Âûáåðèòå äåéñòâèå",
    )
    keyboard.add(*start_buttons)

    msg = text(
        hbold("Çäðàâñòâóéòå!"),
        'Ðàäû ïðèâåòñòâîâàòü âàñ â íàøåì ñåðâèñå "Êðóòîé áîò".',
        "\nÄîñòóïíûå êîìàíäû:",
        "/start - íà÷àòü ðàáîòó ñ áîòîì",
        "/support - ïîëó÷èòü ïîìîùü",
        "/photo - *çàðÿäèòüñÿ ýíåðãèåé",
        "/album - *çàðÿäèòüñÿ ýíåðãèåé 2x",
        "\nÊîíòàêòû:",
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
            title="ññûëêå",
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
        resize_keyboard=True, input_field_placeholder="Âûáåðèòå ïðîäóêò"
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
        input_field_placeholder="Âûáåðèòå ëîêàöèþ",
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
        resize_keyboard=True, input_field_placeholder="Âûáåðèòå òèï"
    )
    keyboard.add(*buttons)

    # msg = text(
    #     commands["1 product"]["leads_to"]["buy"]["msg_after_clicking"],
    #     hlink(title="ññûëêå", url="http://t.me/danya_support_bot"),
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
        input_field_placeholder="Ïîäòâåðäèòå çàêàç",
    )
    keyboard.add(*buttons)

    msg = text(
        hbold("Âàø çàêàç:"),
        f'{hitalic("Ïðîäóêò:")} {confirm_dict[user_key]["product"]}',
        f'{hitalic("Àäðåñ:")} {confirm_dict[user_key]["location"]}',
        f'{hitalic("Òèï:")} {confirm_dict[user_key]["type"]}\n',
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
        input_field_placeholder="Âûáåðèòå ñïîñîá îïëàòû",
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
        input_field_placeholder="Âûáåðèòå äåéñòâèå",
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
        "Äëÿ îïëàòû ïåðåõîäèòå â íàø",
        hlink(
            title="÷àò-áîò ñîïðîâîæäåíèÿ",
            url="http://t.me/danya_support_bot",
        ),
    )
    await message.answer(msg)
    await save_info(message)


# ============================================================

# back to menu
@dp.message_handler(
    Text(equals=commands["menu"]["button_text"])
)  #! ñäåëàòü ìíîãî âîçâðàòîâ â ìåíþ equals=ñïèñîê
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
        chat_id=chat_id, photo=photo_bytes, caption=text(emojize("Äåðæè! :fire:"))
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
        caption=text(emojize("Êàêèå îíè... :broken_heart:")),
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
            "Ìèëîðä, ðàññûëêà ïðîøëà óñïåøíî"
        )
        await save_info(message)
    else:  # block not-admins and save info
        await message.answer(f'Êîìàíäà "{message.text}" íå íàéäåíà')
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
            f'Âû îòïðàâèëè ñîîáùåíèå "{text_to_send}" ïîëüçîâàòåëþ {id}'
        )
        await save_info(message)

    else:  # block not-admins and save info
        await message.answer(f'Êîìàíäà "{message.text}" íå íàéäåíà')
        await save_info(message)


# ============================================================

# if non-available text
@dp.message_handler()
async def command_error(message: types.Message):

    await message.answer(f'Êîìàíäà "{message.text}" íå íàéäåíà')
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
        "Îïåðàòîð íå ìîæåò ïðîñëóøàòü âàøå ñîîáùåíèå. Íàïèøèòå, ïîæàëóéñòà, òåêñòîì"
    )


# ============================================================

# answer for video
@dp.message_handler(content_types=[types.ContentType.VIDEO])
async def save_photo(message: types.Message):
    await message.answer(
        "Îïåðàòîð íå ìîæåò ïîñìîòðåòü âàøå âèäåî. Ïðèøëèòå, ïîæàëóéñòà, ôîòî"
    )


# ============================================================

# answer for sticker
@dp.message_handler(content_types=[types.ContentType.STICKER])
async def save_photo(message: types.Message):
    await message.answer(
        "Áîò ïëîõî âîñïðèíèìàåò èíôîðìàöèþ ÷åðåç ñòèêåðû. Íàïèøèòå, ïîæàëóéñòà, òåêñòîì"
    )


# ============================================================

print("Bot is running")  # output in console


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
