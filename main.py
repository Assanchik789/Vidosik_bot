import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
import asyncio
import yt_dlp
import subprocess


subprocess.run(['ffmpeg', '-version'])

bot = Bot(
    token="8712815619:AAEw2ANGFKgEmI5W1KaF1UFaMCoXPztC8Ks",
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True,
    ),
    timeout=720.0,
    session_timeout=720.0,
)
dp = Dispatcher()


async def Otprav_vid(message, bot, ssilka, ChatId):
    onesoob = None
    if 'instagram' in ssilka:
        harak = {
            'cookiefile': 'instagram_cookies.txt',
            'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': 'downloads/%(title)s_%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'noplaylist': True,
        'restrictfilenames': True,
        }
    elif 'tiktok' in ssilka.lower():
        harak = {
            'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.tiktok.com/',
            'Origin': 'https://www.tiktok.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Upgrade-Insecure-Requests': '1',
        },
        'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': 'downloads/%(title)s_%(id)s.%(ext)s',
        'extractor_args': {'tiktok': {'webpage_download': True}},
        'extract_flat': False,
        'force_generic_extractor': False,
        'socket_timeout': 30,
        'retries': 10,
        'file_access_retries': 5,
        'extractor_retries': 5,
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'noplaylist': True,
        'restrictfilenames': True,
    }
    else:
        harak = {
    'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'noplaylist': True,
        'restrictfilenames': True,
    }

    try:
        with yt_dlp.YoutubeDL(harak) as ydl:#Создаю объект YoutubeDL с настройками harak (словарь с параметрами скачивания)
            info = ydl.extract_info(ssilka, download=False)#временно не скачиваю видео сразу
            file_size = info.get('filesize') or info.get('filesize_approx')#получаем размер файла до загрузки
            if file_size:
                file_size_mb = file_size / (1024 * 1024)# переводим в мегабайты
                if file_size_mb > 50: #если файл весит больше 50 мб, то не скачиваем его
                    #информируем пользователя об этом
                    await message.answer(f'Видео весит {file_size_mb:.1f} MB, что больше 50 MB. Telegram не может отправить такое видео.')
                    return
            status_msg = await message.answer("⏬ Скачиваю видео...")  # сообщение о начале скачки видео
            ydl.download([ssilka])#начинаем скачивание видео, если он прошел по вессу
            filename = ydl.prepare_filename(info)#получаю имя скаченого файла
            videof = FSInputFile(filename)#Создаю объект для отправки файла из файловой системы
            onesoob = await message.answer('Видос отправляется...')#сообщение о том что видео отправляется
            add = await message.answer('тут могла быть ваша реклама')
            await status_msg.delete()#удаление сообщения о скачивании
            # отправка видео с названием и тегами
            await bot.send_video(chat_id=ChatId, video=videof, caption=f"{info.get('title', 'Видео')}\n\n@VidosInator_bot")
            await add.delete()
            await onesoob.delete()#удаление сообщения о отправке
            await bot.send_sticker(chat_id=ChatId,#отправка стикера
                                   sticker='CAACAgIAAxkBAAEChIVpp0W_c-MVLamShu7KaPh254IdRwACrogAAox_eEh3Vac4UUDhVjoE')
            os.remove(filename)#удаляю видео с своего устройства для экономии памяти
    except:
        if onesoob:#если видео не начало отправляться мы сразу же удаляем сообщение о его отправки
            await onesoob.delete()
        #сообщаю польхователю об ошибке
        await message.answer('Видео долго отправляется. Либо возникла некая ошибка. Скорее всего файл не поддерживается')
        await bot.send_sticker(chat_id=ChatId,#стикер грустный
                               sticker='CAACAgIAAxkBAAEChHppp0PuOm70HvARuy-xvyv0VvQwBQAC940AAgeWaUh3ucs2_FDfCzoE')
        os.remove(filename)  # удаляю видео с своего устройства для экономии памяти



@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer('Привет! Скинь ссылку на видео и я пришлю его тебе, НО - бот не может скачивать и отправлять видеоролики весящие более 50мб, это ограничение телеграмма')
    await bot.send_sticker(chat_id=message.chat.id, sticker= 'CAACAgIAAxkBAAEChGBppz0v7pB2sD5HB8YZlQLwanvDwwAC940AAiRKYEgQtH6aFfJD8DoE')

@dp.message()
async def get_name(message: Message):
    ChatId = message.chat.id
    ssilka = message.text
    await Otprav_vid(message, bot, ssilka, ChatId)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
