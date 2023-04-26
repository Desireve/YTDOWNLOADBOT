from pytube import YouTube as yt
import youtube_dl


def replSlash(text):
    repltext = text.replace("/", '')
    repltext = repltext.replace("\\", '')
    repltext = repltext.replace(":", '')
    return repltext

def replace_to_text(text:str):
    repltext = ''.join([a for a in text if a.isalpha() or a.isalnum() or a in '_. '])
    return repltext


def getNameFromLink(link):
    name = f'{yt(link).streams[0].title}.mp3'
    name = replace_to_text(name)
    #name = link.replace("https://youtu.be/", '')+ '.mp3'
    return name


def downloadAudioFromLink(link):
    mus = yt(link)
    name = f'{mus.streams[0].title}.mp3'
    name = replace_to_text(name)
    #name = link.replace("https://youtu.be/", '')+ '.mp3'
    mus.streams.filter(only_audio=True).first().download(filename=name)


def downloadAudioFromLinkDLVERSION(link):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = link,download=False
    )
    filename = f"{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'restrictfilenames': True,
        'keepvideo':False,
        'outtmpl':filename,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))


def getNameFromLinkDL(link):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = link,download=False
    )
    name = f"{video_info['title']}.mp3"
    name = replace_to_text(name)
    #name = link.replace("https://youtu.be/", '')+ '.mp3'
    return name