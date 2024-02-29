import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, WebAppInfo
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import *
from database import Database
from function import *
import validators
from crypt_1 import *
import random

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()

class Form(StatesGroup):
	add_op_id = State() 
	add_op_name = State()
	add_op_link = State()
	add_op_count = State()
	get_link = State()

gen_key()


@dp.message_handler(commands=['start'])
async def start_handler(message,  state: FSMContext):
	req = db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.from_user.is_premium, message.from_user.language_code)
	print(req)
	unique_code = extract_unique_code(message.text)
	if unique_code:
		try:
			link = db.get_link(unique_code)
		except:
			link = 0
		async with state.proxy() as data:
			data['link'] = link
		op = db.get_op()
		print(op)
		op_kb = InlineKeyboardMarkup()
		result_op = []
		orders_id = ''
		for i in op:
			user_channel_status = await bot.get_chat_member(chat_id=i['channel_id'], user_id=message.from_user.id)
			if user_channel_status["status"] != 'left':
				print(i['channel_id'] + ' Подписан')
			else:
				result_op.append(i)
				#orders_id += i['channel_id']
				#op_kb.add(InlineKeyboardButton(i['name'], url=i['link']))
		print(len(result_op))
		if len(result_op) > 1:
			op_list = random.sample(result_op, 2)
			for j in op_list:
				orders_id += "-" + str(j['id'])
				op_kb.add(InlineKeyboardButton(j['name'], url=j['link']))
		elif len(result_op) == 1:
			op_list = random.sample(result_op, 2)
			for j in op_list:
				orders_id += "-" + str(j['id'])
				op_kb.add(InlineKeyboardButton(j['name'], url=j['link']))
			# orders_id += '-test'
			# op_kb.add(InlineKeyboardButton('test', url='https://t.me/LinkerTgBot'))
		else:
			pass

		async with state.proxy() as data:
			data['channel_ids'] = result_op
		op_kb.add(InlineKeyboardButton('Проверить подписку✅', callback_data=f"check{orders_id}"))

		await bot.send_message(message.chat.id, f'<b>Для продолжения необходимо подписаться на каналы:</b>', reply_markup=op_kb)
		await Form.get_link.set()
	else:
		await bot.send_message(message.from_user.id, texts['start'], reply_markup=render_reply_kb(keyboards['menu'], message.from_user.id))

@dp.message_handler(state=Form.get_link)
async def get_link_of_op(message, state: FSMContext):
	await bot.send_message(message.chat.id, '<b>Для продолжения необходимо подписаться на каналы❌</b>')

@dp.callback_query_handler(text_startswith="check", state=Form.get_link)
async def check_subs(callback: types.CallbackQuery,  state: FSMContext):
	channels = callback.data.split('-')
	print(callback.data)
	channels.pop(0)
	succes = 0
	no_succes = 0
	for i in channels:
		channel_id = db.get_channel_from_order(i)
		user_channel_status = await bot.get_chat_member(chat_id=channel_id, user_id=callback.from_user.id)
		if user_channel_status["status"] != 'left':
			db.buy_op(i)
			succes +=1
		else:
			no_succes +=1
	if no_succes == 0:
		async with state.proxy() as data:
			try:
				await bot.send_message(callback.from_user.id, 'Ваша ссылка готова', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Ссылка', url=data['link'])))
			except Exception as ex:
				print('НИХУЯ СЕБЕ ОШИБКА', ex)
			await callback.message.delete()
		await state.finish()
	else:
		await bot.send_message(callback.from_user.id, '<b>Для продолжения необходимо подписаться на каналы❌</b>')


###########################################
@dp.message_handler(text=keyboards['menu']['cut'])
async def cut_link_menu(message):
	await message.delete()
	await bot.send_message(message.from_user.id, texts['cut'])

@dp.message_handler(text=keyboards['menu']['profile'])
async def cut_link_menu(message):
	await message.delete()
	user = db.get_user(message.from_user.id)
	await bot.send_message(message.from_user.id, f'<b>Профиль \nБаланс: <code>{user["balance"]}</code>\n</b>', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Список моих заказов📊', web_app=WebAppInfo(url = f'{server}/buy-op?user_id={crypt(str(message.from_user.id))}'))))
############################################




############################################
@dp.message_handler(text=keyboards['menu']['buy'])
async def buy(message, state: FSMContext):
	info = await bot.get_me()
	await bot.send_message(message.from_user.id, f'<b>🛒Покупка обязательной подписки</b>\n\n1. Добавьте @{info.username} в админы канала\n2. Перешлите любое сообщение из канала в этот чат')
	await Form.add_op_id.set()

@dp.message_handler(state=Form.add_op_id)
async def buy2(message, state: FSMContext):
	if message.forward_from_chat:
		async with state.proxy() as data:
			data['channel_id'] = message.forward_from_chat.id
		await message.reply('Отправьте название канала <b>(будет отображаться на кнопке)</b>')
		await Form.add_op_name.set()
	else:
		await message.reply('Перешлите сообщение из канала!')
@dp.message_handler(state=Form.add_op_name)
async def buy3(message, state: FSMContext):
	if len(message.text) <= 30:
		async with state.proxy() as data:
			data['name'] = message.text
		await message.reply('<b>Отправьте ссылку, на которую будет вести кнопка</b>')
		await Form.add_op_link.set()
	else:
		await message.reply('<b>Длина текста не может быть больше 30 символов</b>')
@dp.message_handler(state=Form.add_op_link)
async def buy4(message, state: FSMContext):
	if validators.url(message.text):
		async with state.proxy() as data:
			data['link'] = message.text
		await bot.send_message(message.chat.id, '<b>Отлично! Теперь отправьте количество подписок, которое вам нужно.</b>')
		await Form.add_op_count.set()
	else:
		await message.reply('Отправьте ссылку в формате <code>https://t.me/LinkerTgBot</code>')
@dp.message_handler(state=Form.add_op_count)
async def buy5(message, state: FSMContext):
	#orders?user_id={crypt(str(message.from_user.id))}
	try: 
		int(message.text)
		async with state.proxy() as data:
			db.add_order(data['channel_id'], data['name'], data['link'], message.text, message.from_user.id)
		await bot.send_message(message.chat.id, f'Ваш заказ на {message.text} подписок успешно создан!', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Список моих заказов📊', web_app=WebAppInfo(url = f'{server}/buy-op?user_id={crypt(str(message.from_user.id))}'))))
		await state.finish()
	except Exception as e:
		print(e)
		await message.reply('<b>Отправьте корректное число!</b>')

#############################################



@dp.message_handler(content_types=['text'])
async def cut_links(message):
	link_id = db.cut_link(message.from_user.id, message.text)
	info = await bot.get_me()
	await bot.send_message(message.from_user.id, f"Вот ваша ссылка: https://t.me/{info.username}?start={link_id}")
	
	
if __name__ == '__main__':
	executor.start_polling(dp)