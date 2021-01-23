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


def last_chars(x):
    return (x[3:3:])


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


def get_mp3_files(DIR):
    files = sorted(os.listdir(path=DIR), key=first_chars)
    return files


def get_wav_files(DIR):
    files = sorted(os.listdir(path=DIR), key=last_chars)
    return files

def get_mp3(INPUTDIR):

    mp3_list = get_mp3_files(INPUTDIR)

    return mp3_list


def create_mp3_list_file(mp3_list):
    print(type(mp3_list))
    if type(mp3_list) == list:
        for i in mp3_list:
            with open('mp3_list.txt', 'a') as file:
                file.write("file " + "'" +
                           os.path.join(INPUTDIR, i) + "'\n")


def get_wav(WAVDIR):
    wav_list = get_wav_files(WAVDIR)
    return wav_list


#def recog(wav_list):
#    r = sr.Recognizer()
#    # i=12
#    for i in wav_list:
#        try:
#            voice_track = sr.AudioFile(os.path.join(WAVDIR, i))#
#
 #           with voice_track as audio_file:
#                audio_content = r.record(audio_file)
#            print("Recognition  " + f'{i}' + " of " + str(len(wav_list) - 1))
#            speech = r.recognize_google(audio_content, language='ru')
#
#            with open('result.txt', 'a') as file:
#                file.write(speech)
#        except sr.UnknownValueError:
#            print(f"{i} -- Recognition error  ")
#            with open('result.txt', 'a') as file:
#                file.write("\n")
#                file.write("\n")
#                file.write(f"{i} -- Recognition error \n")
#                file.write("\n")
#
#        sleep(3)



def recog(wav_file):
    retry = 5
    r = sr.Recognizer()
    while retry > 0:
        try:
            voice_track = sr.AudioFile(os.path.join(WAVDIR, wav_file))

            with voice_track as audio_file:
                audio_content = r.record(audio_file)
            print("Recognition  " + f'{wav_file}' + " of " + str(len(wav_list) - 1))
            speech = r.recognize_google(audio_content, language='ru')
            retry = 0

            with open('result.txt', 'a') as file:
                file.write(speech)
        except sr.UnknownValueError:
            print(f"{wav_file} -- Recognition error! Retry... "+ str(retry))
            if retry == 0:
                with open('result.txt', 'a') as file:
                    file.write("\n")
                    file.write("\n")
                    file.write(f"{wav_file} -- Recognition error \n")
                    file.write("\n")
            else:
                 retry = retry -1



def clear():
    print('Clearing generates:\n')
    for file in generates:
        try:
            os.remove(file)
            print(f'{file} removed')
        except FileNotFoundError:
            print(f'{file} not found')
            pass


generates = ['result.txt', 'mp3_list.txt', os.path.join(
    INPUTDIR, '1.wav'), os.path.join(INPUTDIR, 'out.mp3')]
wav_list = get_wav(WAVDIR)
for wav in wav_list:
    generates.append(os.path.join(WAVDIR, wav))


clear()
create_dirs()
mp3_list = get_mp3(INPUTDIR)
create_mp3_list_file(mp3_list)
os.system('ffmpeg -f concat  -safe 0 -i mp3_list.txt -c copy ./input/out.mp3')
os.system('ffmpeg -i ./input/out.mp3 ./input/1.wav ')
os.system(
    'ffmpeg -i ./input/1.wav -f segment -segment_time 59 -c copy ./wav/out%3d.wav'
)
wav_list = get_wav(WAVDIR)
for wav in wav_list:
    recog(wav)
    sleep (1)

with open('result.txt', 'a') as file:
    file.write("\n")
    file.write("\n")
