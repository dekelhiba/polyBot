from telegram.ext import Updater, MessageHandler, Filters
from utils import search_download_youtube_video
from loguru import logger

class Bot:

    def __init__(self, token):
        # create frontend object to the bot programmer
        self.updater = Updater(token, use_context=True)

        # add _message_handler as main internal msg handler
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self._message_handler))

    def start(self):
        """Start polling msgs from users, this function never returns"""
        self.updater.start_polling()
        logger.info(f'{self.__class__.__name__} is up and listening to new messages....')
        self.updater.idle()

    def _message_handler(self, update, context):
        """Main messages handler"""
        self.send_text(update, f'Your original message: {update.message.text}')

    def send_video(self, update, context, file_path):
        """Sends video to a chat"""
        context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'), supports_streaming=True)

    def send_text(self, update,  text, quote=False):
        """Sends text to a chat"""
        # retry https://github.com/python-telegram-bot/python-telegram-bot/issues/1124
        update.message.reply_text(text, quote=quote)


class QuoteBot(Bot):
    def _message_handler(self, update, context):
        to_quote = True

        if update.message.text == 'Don\'t quote me please':
            to_quote = False

        self.send_text(update, f'Your original message: {update.message.text}', quote=to_quote)


class YoutubeBot(Bot):
    def _message_handler(self, update, context):
        user_message = update.message.text

        # Check if the message is a valid YouTube video name
        #if 'youtube.com/' in user_message or 'youtu.be/' in user_message:
        # Directly download the video if a valid URL is provided
            #with YoutubeDL() as ydl:
                #video_file = ydl.extract_info(user_message, download=True)
                #video_path = ydl.prepare_filename(video_file)
        #else:
        # Otherwise, search for the video on YouTube using the search_download_youtube_video() function
        videos = search_download_youtube_video(user_message)
        video_path = videos[0]  # Download the first video returned by the search

        # Send the video to the user

        self.send_video(update, context, video_path)


if __name__ == '__main__':
    with open('.telegramToken') as f:
        _token = f.read()

    my_bot = Bot(_token)
    my_bot.start()

