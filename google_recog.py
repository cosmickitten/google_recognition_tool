#!/bin/python


#   ffmpeg -i "concat:1.mp3|2.mp3|3.mp3" -acodec copy out.mp3

#   ffmpeg -i out.mp3 1.wav

#   ffmpeg -i 1.wav -f segment -segment_time 59 -c copy out%d.wav

from time import sleep
import speech_recognition as sr
import os

PATH = os.path.realpath(os.curdir)

INPUTDIR = os.path.join(PATH, "input")

WAVDIR = os.path.join(PATH, "wav")


def first_chars(x):
    return (x[:2:])


def create_dirs():
    try:
        os.mkdir(path=INPUTDIR)
    except FileExistsError:
        print("Directory input exists!\n")
    try:
        os.mkdir(path=WAVDIR)
    except FileExistsError:
        print("Directory wav exists!\n")
    print("Directory sucsessfully created!\n")


def get_files(DIR):
    files = sorted(os.listdir(path=DIR), key=first_chars)
    return files

def get_mp3(INPUTDIR):
    
    mp3_list = get_files(INPUTDIR)
    
    return mp3_list

def create_mp3_list_file(mp3_list):
    print(type(mp3_list))
    if type(mp3_list) == list:
        for i in mp3_list:
            with open('mp3_list.txt', 'a') as file:
                file.write("file " + "'" +
                           os.path.join(INPUTDIR, i) + "'\n")



def get_wav(WAVDIR):
    wav_list = get_files(WAVDIR)
    return wav_list


def recog(wav_list):
    r=sr.Recognizer()
    # i=12
    for i in wav_list:
        try:
            voice_track=sr.AudioFile(f'./wav/{i}')

            with voice_track as audio_file:
                audio_content=r.record(audio_file)
            print("Recognition  " + f'{i}' + " of " + str(len(wav_list) - 1))
            speech=r.recognize_google(audio_content, language='ru')

            with open('result.txt', 'a') as file:
                file.write(speech)
        except sr.UnknownValueError:
            print(f"{i} -- Recognition error  ")
            with open('result.txt', 'a') as file:
                file.write("\n")
                file.write("\n")
                file.write(f"{i} -- Recognition error \n")
                file.write("\n")

        sleep(3)


os.system('rm result.txt')
os.system('rm mp3_list.txt')
os.system('rm  ./input/1.wav')
os.system('rm  ./input/out.mp3')
os.system('rm  ./wav/*')
create_dirs()
mp3_list=get_mp3(INPUTDIR)
create_mp3_list_file(mp3_list)
os.system('ffmpeg -f concat  -safe 0  -i mp3_list.txt -c copy ./input/out.mp3')
os.system('ffmpeg -i ./input/out.mp3 ./input/1.wav ')
os.system(
    'ffmpeg -i ./input/1.wav -f segment -segment_time 59 -c copy ./wav/out%d.wav'
)
wav_list=get_wav(WAVDIR)
print(wav_list)
#recog(wav_list)
#with open('result.txt', 'a') as file:
#    file.write("\n")
#    file.write("\n")
