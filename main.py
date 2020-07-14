import config
import logging
import asyncio
from Habr import Habr
from BD import BD
from aiogram import Bot, Dispatcher, executor, types


# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = BD(config.BD_FILE)

# инициализируем feedparser
hr = Habr(config.LASTDATE_FILE)

# доступные команды
available_cmd = {'/help', '/subscribe', '/unsubscribe','/start','/coronavirus' }


# Проверка на правильность команды
@dp.message_handler(lambda message: message.text not in available_cmd and message.text[0] == '/')
async def error_allert(message: types.Message):
    await message.answer("Я не понимаю данную команду, набери /help для просмотра доступных команд")


# Просмотр доступных команд
@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    await message.answer('''Доступные команды:
    /subscribe - подписка на новости
    /unsubscribe - отписаться
    /help - список доступных команд
    /coronavirus - статистика по коронавирусу в Ульяновской области'''
                         )
# Приветствие
@dp.message_handler(commands=['start'])
async def greeting(message: types.Message):
    await message.answer('''Добрый день, я бот созданный для уведомлении о новых постах на habr.ru, напиши команду /help чтобы увидеть список моих доступных команд''')

# Функция просмотра статистики коронавируса
@dp.message_handler(commands=['coronavirus'])
async def coronavirus(message: types.Message):
    await message.answer("Статистика на данный момент в Ульяновской области:\n")    
    await message.  answer(Habr.ulyanovskstate())

# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    # Проверка на подписку
    if(db.subscriber_subscribired(message.from_user.id,True)):
        await message.answer("Вы уже подписаны")
    else:
        if(not db.subscriber_exists(message.from_user.id)):
            # если юзера нет в базе, добавляем его
            db.add_subscriber(message.from_user.id)
        else:
            db.update_subscription(message.from_user.id, True)
            await message.answer("Вы успешно подписались на рассылку, ожидайте новые посты!")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    # Проверка на отписку
    if(db.subscriber_subscribired(message.from_user.id,False)):
        await message.answer("Вы итак не подписаны")
    else:
        if(not db.subscriber_exists(message.from_user.id)):
            # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
            db.add_subscriber(message.from_user.id, False)
            await message.answer("Вы итак не подписаны.")
        else:
            # если он уже есть, то просто обновляем ему статус подписки
            db.update_subscription(message.from_user.id, False)
            await message.answer("Вы отписаны от рассылки.")


# проверяем наличие новых новостей и делаем рассылки
async def scheduled(wait_for):
    # проверяем наличие новых новостей
    while True:
        await asyncio.sleep(wait_for)

        new_news = hr.new_news()
        if(new_news):
            new_news.reverse()
            for nw in new_news:
                # парсим инфу о новой новости
                nfo = hr.news_info(nw)

                # получаем список подписчиков бота
                subscriptions = db.get_subscriptions()

                # отправляем всем новость
                for s in subscriptions:
                    await bot.send_message(
                        chat_id=s[1],
                        text=nfo['title'] + "\n\n" +
                        nfo['date'] + "\n\n" + nfo['link'],
                        disable_notification=True,
                    )

                # обновляем ключ
                hr.update_date(nfo['key'])


# запускаем лонг поллинг
if __name__ == '__main__':
    # пока что оставим 5 секунд (в качестве теста)
    dp.loop.create_task(scheduled(5))
    executor.start_polling(dp, skip_updates=True)
