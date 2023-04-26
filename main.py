import telebot
from properties import token


#my_file
import audio_download

#end

from os import listdir
from os.path import isfile, join
import os

#@WeatherWeatherBotBot
bot = telebot.TeleBot(token)


def getContentList():
    mypath = "content/"
    contentList = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #print(contentList)
    return contentList

def clearContentFolder():
    contentfolder = 'content'
    for filename in os.listdir(contentfolder):
        file_path = os.path.join(contentfolder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) # удалить файл или символическую ссылку
            elif os.path.isdir(file_path):
                os.rmdir(file_path) # удалить пустую папку
        except Exception as e:
            print('Не удалось удалить %s. Причина: %s' % (file_path, e))


def moveFileToContentFolder(name):
    os.system('move "' +name + '" content/')


def ifHaveInContent(name):
    cntlist = getContentList()
    if name in cntlist:
        return True
    else:
        return False

def ifYoutubeLink(link):
    if "youtube.com" in link:
        return True



print("###BOT STARTED###\n")

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    print(message.text)
    url = message.text
    if url == "cls":
        clearContentFolder()
        bot.send_message(message.from_user.id, "Файлы очищенны")
    else:
        print("username: ", str(message.from_user.username), "| link: ", url)
        
        
        
        

        #try:
        if 'https://youtu.be/' in url:
            try:
                filename = audio_download.getNameFromLink(url)
                bot.send_message(message.from_user.id, "Ожидайте")
                print(filename)
                if ifHaveInContent(filename):
                    linktofile = f"content/{filename}"
                    audio = open(linktofile, 'rb')
                    bot.send_audio(message.from_user.id, audio)
                    audio.close()
                    print("Файл уже в библиотеке")
                else:
                    #try:
                    audio_download.downloadAudioFromLink(url)
                    moveFileToContentFolder(f"{filename}")
                    with open(f"content/{filename}", 'rb') as openned_audio:
                        bot.send_audio(message.from_user.id, openned_audio)
                    print("файл скачан в библиотеку")
            except Exception as e:
                bot.send_message(message.from_user.id, "Вы уверенны что это правильная ссылка на видео с Youtube?")
                print(e)
            
        else:
            bot.send_message(message.from_user.id, "Вы уверенны что это ссылка на видео с Youtube?")

CONTENT_TYPES = ["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]
@bot.message_handler(content_types=CONTENT_TYPES)
def get_none_text_message(message):
    bot.send_message(message.from_user.id, "Вы уверенны что отправили ссылку на видео с YouTube?")
    

bot.polling(non_stop=True, interval=0)
