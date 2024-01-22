import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import psycopg2
import asyncio

con = psycopg2.connect(
database="bot",
user="postgres",
password="Toirjonov2006",
host="localhost",
port= '5432'
)

API_TOKEN = '6922773532:AAE4B9FXftq9clKEjXfmNIv_YM9busKA-TE'

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


#### USER REGISTARTION
class User_registration(StatesGroup):
    wait_for_fullname = State()

####### MENU
menu_markup = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    KeyboardButton(text='Idish yuvish'),
    KeyboardButton(text='Musr tashlab kelish'),
    KeyboardButton(text='Uy tozalash'),
    KeyboardButton(text='Vanna yuvish')
]
menu_markup.add(*buttons)
ortga = KeyboardButton(text="Ortga")
button1_idish = KeyboardButton(text="Idish yuvishga qo'shilish")
buttun2_idish = KeyboardButton(text="Idish yuvishdan chiqish")
menu1_idish = ReplyKeyboardMarkup(resize_keyboard=True)
menu2_idish = ReplyKeyboardMarkup(resize_keyboard=True)
menu1_idish.add(button1_idish)
menu2_idish.add(buttun2_idish)
menu1_idish.add(ortga)
menu2_idish.add(ortga)

button1_non = KeyboardButton(text="Musr tashlab kelishga qo'shilish")
buttun2_non = KeyboardButton(text="Musr tashlab kelishdan chiqish")
menu1_non = ReplyKeyboardMarkup(resize_keyboard=True)
menu2_non = ReplyKeyboardMarkup(resize_keyboard=True)
menu1_non.add(button1_non)
menu2_non.add(buttun2_non)
menu1_non.add(ortga)
menu2_non.add(ortga)

button1_uy = KeyboardButton(text="Uy tozalashga qo'shilish")
buttun2_uy = KeyboardButton(text="Uy tozalashdan chiqish")
menu1_uy = ReplyKeyboardMarkup(resize_keyboard=True)
menu2_uy = ReplyKeyboardMarkup(resize_keyboard=True)
menu1_uy.add(button1_uy)
menu2_uy.add(buttun2_uy)
menu1_uy.add(ortga)
menu2_uy.add(ortga)

button1_vanna = KeyboardButton(text="Vanna yuvishga qo'shilish")
buttun2_vanna = KeyboardButton(text="Vanna yuvishdan chiqish")
menu1_vanna = ReplyKeyboardMarkup(resize_keyboard=True)
menu2_vanna = ReplyKeyboardMarkup(resize_keyboard=True)
menu1_vanna.add(button1_vanna)
menu2_vanna.add(buttun2_vanna)
menu1_vanna.add(ortga)
menu2_vanna.add(ortga)


async def idish_task(chat_id):
    with con:
        with con.cursor() as curs_obj:
            today = datetime.today()
            curs_obj.execute('select tel_id, date from idish where date = date %s', (datetime(today.year, today.month, today.day),))
            res = curs_obj.fetchall()
            name = []
            for user_id, _ in res:
                curs_obj.execute('select date from idish where tel_id in (select tel_id from users where "group" in (select "group" from users where tel_id = %s)) order by date desc limit 1 ', (user_id,))
                last_que = curs_obj.fetchone()
                curs_obj.execute("insert into idish(tel_id, date) values (%s, date %s + interval '1 day')", (user_id, last_que[0],))
                curs_obj.execute('select name from users where tel_id = %s', (user_id,))
                name.append(curs_obj.fetchone()[0])
            curs_obj.execute('select name from users where tel_id = (select tel_id from idish where date = date %s)', ((datetime(today.year, today.month, today.day) + timedelta(days=1)),))
            nextname = curs_obj.fetchall()
    if name:
        for i in name:
            await bot.send_message(chat_id, f"{i} bugun sizning IDISH YUVISH navbatingiz!")
    await asyncio.sleep(36000)
    if name:
        for i in name:
            await bot.send_message(chat_id, f"{i} bugun sizning IDISH YUVISH navbatingiz!")
    if nextname:
        for i in nextname:
            await bot.send_message(chat_id, f"{i[0]} ertaga sizning IDISH YUVISH navbatingiz!")


async def non_task(chat_id):
    print(2)
    with con:
        with con.cursor() as curs_obj:
            today = datetime.today()
            curs_obj.execute('select tel_id from non where date = date %s', (datetime(today.year, today.month, today.day),))
            res = curs_obj.fetchone()
            curs_obj.execute('select date from non order by date desc limit 1 ')
            last_que = curs_obj.fetchone()
            if res:
                curs_obj.execute("insert into non(tel_id, date) values (%s, date %s + interval '3 day')", (res[0], last_que[0],))
                curs_obj.execute('select name from users where tel_id = %s', (res[0],))
                name = curs_obj.fetchone()
            curs_obj.execute('select name from users where tel_id = (select tel_id from non where date = date %s)', ((datetime(today.year, today.month, today.day) + timedelta(days=3)),))
            nextname = curs_obj.fetchone()
    if res and name:
        await bot.send_message(chat_id, f"{name[0]} bugun sizning MUSRLARNI TASHLAB KELISH VA ESHIK OLDIDAGI KLYONKANI TOZALASH navbatingiz!")
    await asyncio.sleep(36000)
    if res and name:
        await bot.send_message(chat_id, f"{name[0]} bugun sizning MUSRLARNI TASHLAB KELISH VA ESHIK OLDIDAGI KLYONKANI TOZALASH navbatingiz!")
    if nextname:      
        await bot.send_message(chat_id, f"{nextname[0]} 3 KUNDAN KEYIN sizning MUSRLARNI TASHLAB KELISH VA ESHIK OLDIDAGI KLYONKANI TOZALASH navbatingiz!")


async def uy_task(chat_id):
    with con:
        with con.cursor() as curs_obj:
            today = datetime.today()
            curs_obj.execute('select tel_id from uy where date = date %s', (datetime(today.year, today.month, today.day),))
            res = curs_obj.fetchone()
            curs_obj.execute('select date from uy order by date desc limit 1 ')
            last_que = curs_obj.fetchone()
            if res:
                curs_obj.execute("insert into uy(tel_id, date) values (%s, date %s + interval '7 day')", (res[0], last_que[0],))
                curs_obj.execute('select name from users where tel_id = %s', (res[0],))
                name = curs_obj.fetchone()
            curs_obj.execute('select name from users where tel_id = (select tel_id from uy where date = date %s)', ((datetime(today.year, today.month, today.day) + timedelta(days=7)),))
            nextname = curs_obj.fetchone()
    if res and name:
        await bot.send_message(chat_id, f"{name[0]} bugun sizning UY TOZALASH navbatingiz!(BOZORLIK QILISH HAM KERAK)")
    await asyncio.sleep(36000)
    if res and name:
        await bot.send_message(chat_id, f"{name[0]} bugun sizning UY TOZALASH navbatingiz!")
    if nextname:       
        await bot.send_message(chat_id, f"{nextname[0]} 7 kundan keyin sizning UY TOZALASH navbatingiz!")


async def vanna_task(chat_id):
    with con:
        with con.cursor() as curs_obj:
            today = datetime.today()
            curs_obj.execute('select tel_id from vanna where date = date %s', (datetime(today.year, today.month, today.day),))
            res = curs_obj.fetchone()
            curs_obj.execute('select date from vanna order by date desc limit 1 ')
            last_que = curs_obj.fetchone()
            if res:
                curs_obj.execute("insert into vanna(tel_id, date) values (%s, date %s + interval '14 day')", (res[0], last_que[0],))
                curs_obj.execute('select name from users where tel_id = %s', (res[0],))
                name = curs_obj.fetchone()
            curs_obj.execute('select name from users where tel_id = (select tel_id from vanna where date = date %s)', ((datetime(today.year, today.month, today.day) + timedelta(days=14)),))
            nextname = curs_obj.fetchone()
    if res and name:
        await bot.send_message(chat_id, f"{name[0]} bugun sizning VANNA VA HOJATXONA YUVISH navbatingiz!")
    await asyncio.sleep(36000)
    if res and name:
        await bot.send_message(chat_id, f"{name[0]} bugun sizning VANNA VA HOJATXONA YUVISH navbatingiz!")
    if nextname:     
        await bot.send_message(chat_id, f"{nextname[0]} 14 kundan keyin sizning VANNA VA HOJATXONA YUVISH navbatingiz!")



#### START
@dp.message_handler(commands=['start'])
async def registration(message: types.Message, state: FSMContext):
    tel_id = message.from_user.id
    
    with con:
        with con.cursor() as curs_obj:
            curs_obj.execute("SELECT * FROM users WHERE tel_id = %s", (tel_id,))
            existing_user = curs_obj.fetchone()

    if existing_user:
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)
    else:
        await message.answer("Ism familiyangizni kiriting:")
        await User_registration.wait_for_fullname.set()



##### GET FULLNAME
@dp.message_handler(state=User_registration.wait_for_fullname)
async def get_fullname(message: types.Message, state: FSMContext):
    try:
        name, surename = (message.text.strip()).split(' ')
    except ValueError:
        await message.answer("Notogri formatda kiritdingiz!")
        return
    tel_id = message.from_user.id
    with con:
        with con.cursor() as curs_obj:
            curs_obj.execute("INSERT INTO users(tel_id, name, surename) VALUES (%s, %s, %s)", (tel_id, name, surename))

    await message.answer("Muvaffaqiyatli ro'yhatdan o'tdingiz!")
    await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)
    await state.reset_state()


##### SECOND MENU
@dp.message_handler()
async def idish_yuvish(message: types.Message):
    user_id = message.from_user.id
    if message.text == 'Idish yuvish':
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('select idish from users where tel_id = %s', (user_id,))
                res = curs_obj.fetchone()
        if res[0] == True:
            await bot.send_message(message.chat.id, "Idish Yuvish", reply_markup=menu2_idish)
        if res[0] == False:
            await bot.send_message(message.chat.id, "Idish Yuvish", reply_markup=menu1_idish)
    elif message.text == 'Musr tashlab kelish':
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('select non from users where tel_id = %s', (user_id,))
                res = curs_obj.fetchone()
        if res[0] == True:        
            await bot.send_message(message.chat.id, "Musr tashlab kelish", reply_markup=menu2_non)
        if res[0] == False:        
            await bot.send_message(message.chat.id, "Musr tashlab kelish", reply_markup=menu1_non)
    elif message.text == 'Uy tozalash':
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('select uy from users where tel_id = %s', (user_id,))
                res = curs_obj.fetchone()
        if res[0] == True:
            await bot.send_message(message.chat.id, "Uy tozalash", reply_markup=menu2_uy) 
        if res[0] == False:
            await bot.send_message(message.chat.id, "Uy tozalash", reply_markup=menu1_uy)     
    elif message.text == 'Vanna yuvish':
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('select vanna from users where tel_id = %s', (user_id,))
                res = curs_obj.fetchone()
        if res[0] == True:        
            await bot.send_message(message.chat.id, "Vanna Yuvish", reply_markup=menu2_vanna)
        if res[0] == False:        
            await bot.send_message(message.chat.id, "Vanna Yuvish", reply_markup=menu1_vanna)

    if message.text == "Idish yuvishga qo'shilish":
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('update users set idish = TRUE where tel_id = %s', (user_id,))
                curs_obj.execute('select "group" from users where tel_id = %s', (user_id,))
                group = curs_obj.fetchone()
                curs_obj.execute('select date from idish where tel_id in (select tel_id from users where "group" = %s) order by date desc limit 1 ', (group,))
                last_que = curs_obj.fetchone()
                # print(last_que)
                if last_que:
                    curs_obj.execute("insert into idish(tel_id, date) values (%s, date %s + interval '1 day')", (user_id, last_que,))
                else:
                    today = datetime.today()
                    curs_obj.execute('insert into idish(tel_id, date) values (%s, %s)', (user_id, (datetime(today.year, today.month, today.day) + timedelta(days=1)),))
        await message.answer("Idish yuvishga muvaffaqiyatli qo'shildingiz!")
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)
    elif message.text == "Idish yuvishdan chiqish":
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('update users set idish = False where tel_id = %s', (user_id,))
                today = datetime.today()
                curs_obj.execute('select date from idish where tel_id = %s and date >= date %s', (user_id, datetime(today.year, today.month, today.day),))
                datem = curs_obj.fetchone()
                curs_obj.execute('delete from idish where tel_id = %s and date >= date %s', (user_id, datetime(today.year, today.month, today.day),))
                curs_obj.execute("""update idish set date = date - interval '1 day' where date > date %s and tel_id in (select tel_id from users where "group" in (select "group" from users where tel_id = %s))""", (datem, user_id))
        await message.answer("Idish yuvishdan chiqdingiz!")
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)

    if message.text == "Musr tashlab kelishga qo'shilish":
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('update users set non = TRUE where tel_id = %s', (user_id,))
                curs_obj.execute('select date from non order by date desc limit 1')
                last_que = curs_obj.fetchone()
                # print(last_que)
                if last_que:
                    curs_obj.execute("insert into non(tel_id, date) values (%s, date %s + interval '3 days')", (user_id, last_que,))
                else:
                    today = datetime.today()
                    curs_obj.execute('insert into non(tel_id, date) values (%s, %s)', (user_id, (datetime(today.year, today.month, today.day) + timedelta(days=3)),))
        await message.answer("Musr tashlab kelishga qo'shildingiz!")
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)
    elif message.text == "Musr tashlab kelishdan chiqish":
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('update users set non = False where tel_id = %s', (user_id,))
                today = datetime.today()
                curs_obj.execute('select date from non where tel_id = %s and date >= date %s', (user_id, datetime(today.year, today.month, today.day),))
                datem = curs_obj.fetchone()
                curs_obj.execute('delete from non where tel_id = %s and date >= date %s', (user_id, datetime(today.year, today.month, today.day),))
                curs_obj.execute("update non set date = date - interval '3 days' where date > date %s", (datem,))
        await message.answer("Musr tashlab kelishdan chiqdingiz!")
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)   

    if message.text == "Uy tozalashga qo'shilish":
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('update users set uy = TRUE where tel_id = %s', (user_id,))
                curs_obj.execute('select date from uy order by date desc limit 1')
                last_que = curs_obj.fetchone()
                # print(last_que)
                if last_que:
                    curs_obj.execute("insert into uy(tel_id, date) values (%s, date %s + interval '7 days')", (user_id, last_que,))
                else:
                    today = datetime.today()
                    curs_obj.execute('insert into uy(tel_id, date) values (%s, %s)', (user_id, (datetime(today.year, today.month, today.day) + timedelta(days=7)),))
        await message.answer("Uy tozalashga muvaffaqiyatli qo'shildingiz!")
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)
    elif message.text == "Uy tozalashdan chiqish":
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('update users set uy = False where tel_id = %s', (user_id,))
                today = datetime.today()
                curs_obj.execute('select date from uy where tel_id = %s and date >= date %s', (user_id, datetime(today.year, today.month, today.day),))
                datem = curs_obj.fetchone()
                curs_obj.execute('delete from uy where tel_id = %s and date >= date %s', (user_id, datetime(today.year, today.month, today.day),))
                curs_obj.execute("update uy set date = date - interval '7 days' where date > date %s", (datem,))
        await message.answer("Uy tozalashdan chiqdingiz!")
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)

    if message.text == "Vanna yuvishga qo'shilish":
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('update users set vanna = TRUE where tel_id = %s', (user_id,))
                curs_obj.execute('select date from vanna order by date desc limit 1')
                last_que = curs_obj.fetchone()
                # print(last_que)
                if last_que:
                    curs_obj.execute("insert into vanna(tel_id, date) values (%s, date %s + interval '14 days')", (user_id, last_que,))
                else:
                    today = datetime.today()
                    curs_obj.execute('insert into vanna(tel_id, date) values (%s, %s)', (user_id, (datetime(today.year, today.month, today.day) + timedelta(days=14)),))
        await message.answer("Vanna yuvishga muvaffaqiyatli qo'shildingiz!")
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)
    elif message.text == "Vanna yuvishdan chiqish":
        with con:
            with con.cursor() as curs_obj:
                curs_obj.execute('update users set vanna = False where tel_id = %s', (user_id,))
                today = datetime.today()
                curs_obj.execute('select date from vanna where tel_id = %s and date >= date %s', (user_id, datetime(today.year, today.month, today.day),))
                datem = curs_obj.fetchone()
                curs_obj.execute('delete from vanna where tel_id = %s and date >= date %s', (user_id, datetime(today.year, today.month, today.day),))
                curs_obj.execute("update vanna set date = date - interval '14 days' where date > date %s", (datem,))
        await message.answer("Vanna yuvishdan chiqdingiz!")
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)

    if message.text == 'Ortga':
        await message.answer("Ishlar ro'yhati: ", reply_markup=menu_markup)
    


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(idish_task, 'cron', hour=9, minute=0, args=[-1002010267678])
    scheduler.add_job(non_task, 'cron', hour=17, minute=36, args=[-1002010267678])
    scheduler.add_job(uy_task, 'cron', hour=9, minute=0, args=[-1002010267678])
    scheduler.add_job(vanna_task, 'cron', hour=9, minute=0, args=[-1002010267678])
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
