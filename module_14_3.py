from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import  FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = "7715838785:AAHWFuxFItqRsoetC_dgSd60OW9ke6lK_c8"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
bottom = KeyboardButton(text='Рассчитать')
bottom2 = KeyboardButton(text='Информация')
bottom3 = KeyboardButton(text= 'Купить')

kb.row(bottom, bottom2, bottom3)

inline_kb = InlineKeyboardMarkup()
inline_bottom1 = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
inline_bottom2 = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_kb.row(inline_bottom1, inline_bottom2 )
inline_kb2 = InlineKeyboardMarkup()
inline_bottom3 = InlineKeyboardButton('Мужчина', callback_data='formulas_M')
inline_bottom4 = InlineKeyboardButton('Женщина', callback_data='formulas_W')
inline_kb2.row(inline_bottom3, inline_bottom4)
inline_kb3 = InlineKeyboardMarkup()
inline_bottom5 = InlineKeyboardButton('Product1', callback_data='product_buying')
inline_bottom6 = InlineKeyboardButton('Product2', callback_data='product_buying')
inline_bottom7 = InlineKeyboardButton('Product3', callback_data='product_buying')
inline_bottom8 = InlineKeyboardButton('Product4', callback_data='product_buying')
inline_kb3.row(inline_bottom5, inline_bottom6, inline_bottom7, inline_bottom8)

list_photo = ['foto/banka_1.png', 'foto/banka_2.png', 'foto/banka_3.png', 'foto/banka_4.png']
captions = [
    'Название: Product 1 | Описание: описание 1 | Цена: 500',
    'Название: Product 2 | Описание: описание 2 | Цена: 700',
    'Название: Product 3 | Описание: описание 3 | Цена: 900',
    'Название: Product 4 | Описание: описание 4 | Цена: 1500'
]


class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()
    gender = State()
    result = State()




@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет', reply_markup=kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f"Product{i} | Описание: описание {i} | Цена: {i * 100}")
        await bot.send_photo(message.from_user.id, photo=open(f'banka_{i}.png', 'rb'))
    await  message.answer('Выберите продукт для покупки: ', reply_markup=inline_kb3)

@dp.callback_query_handler(text= ['product_buying'])
async def send_confirm_message(call):
    await  call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              '\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
     await call.message.answer('Введите свой возраст:')
     await UserState.age.set()
     await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def get_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Определить пол:', reply_markup=inline_kb2)
    await UserState.gender.set()

@dp.callback_query_handler(lambda c: c.data in ['formulas_M', 'formulas_W'], state=UserState.gender)
async def calculate_calories(call: types.CallbackQuery, state: FSMContext):
    # Получаем данные пользователя
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])


    if call.data == 'formulas_M':
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
        await call.message.answer(f'Ваша норма калорий (Мужчина): {calories} ккал')
    elif call.data == 'formulas_W':
        calories = 10 * weight + 6.25 * growth - 5 * age - 161
        await call.message.answer(f'Ваша норма калорий (Женщина): {calories} ккал')


    await state.finish()
    await call.answer()


@dp.message_handler()
async def all_message(message):
     await message.answer('Введите команду /start, чтобы начать.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
