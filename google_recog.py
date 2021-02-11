#!/bin/python


import time
import speech_recognition as sr
import os
import subprocess

PATH = os.path.realpath(os.curdir)

INPUTDIR = os.path.join(PATH, "input")

WAVDIR = os.path.join(PATH, "wav")

RESULTDIR = os.path.join(PATH, "result")


RESULTFILENAME = time.strftime("%Y-%m-%d--%H-%M-%S")


def first_chars(x):
    return (x[:2:])  # 01.mp3 02.mp3 etc..


def last_chars(x):
    return (x[3:3:])  # out002.wav


def create_dirs():
    try:
        os.mkdir(path=INPUTDIR)
        print(f"Directory {INPUTDIR} sucsessfully created!\n")
    except FileExistsError:
        print(f"Directory {INPUTDIR} exists!\n")
    try:
        os.mkdir(path=WAVDIR)
        print(f"Directory {WAVDIR} sucsessfully created!\n")
    except FileExistsError:
        print(f"Directory {WAVDIR} exists!\n")
    try:
        os.mkdir(path=RESULTDIR)
        print(f"Directory {RESULTDIR} sucsessfully created!\n")
    except FileExistsError:
        print(f"Directory {RESULTDIR} exists!\n")


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


def recog(wav_file):
    retry = 1
    r = sr.Recognizer()
    while retry < 6:
        try:
            voice_track = sr.AudioFile(os.path.join(WAVDIR, wav_file))

            with voice_track as audio_file:
                audio_content = r.record(audio_file)
            print("Recognition  " + f'{wav_file}' +
                  " of " + str(len(wav_list) - 1))
            speech = r.recognize_google(audio_content, language='ru')
            retry = 6

            with open(os.path.join(RESULTDIR, RESULTFILENAME ), 'a') as file:
                file.write(speech)
        except sr.UnknownValueError:
            print(f"{wav_file} -- Recognition error! Retry... " + str(retry))
            with open(os.path.join(RESULTDIR, RESULTFILENAME), 'a') as file:
                file.write("\n")
                file.write("\n")
                file.write(f"{wav_file} -- Recognition error \n")
                file.write("\n")

            retry = retry + 1


def clear():
    print('Clearing generates:\n')
    generates = ['result.txt', 'mp3_list.txt', os.path.join(
        INPUTDIR, '1.wav'), os.path.join(INPUTDIR, 'out.mp3')]
    wav_list = get_wav(WAVDIR)
    for wav in wav_list:
        try:
            generates.append(os.path.join(WAVDIR, wav))
        except FileNotFoundError:
            print(f'{wav} not found')
    
        for file in generates:
            try:
                os.remove(file)
                print(f'{file} removed')
            except FileNotFoundError:
                print(f'{file} not found')
                pass
    print('Done!\n')





create_dirs()
mp3_list = get_mp3(INPUTDIR)
create_mp3_list_file(mp3_list)
subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i',
                'mp3_list.txt', '-c', 'copy', os.path.join(INPUTDIR, 'out.mp3')])
subprocess.run(['ffmpeg', '-i', os.path.join(INPUTDIR,
                                             'out.mp3'), os.path.join(INPUTDIR, '1.wav')])
subprocess.run(['ffmpeg', '-i', os.path.join(INPUTDIR, '1.wav'), '-f', 'segment',
                '-segment_time', '59', '-c', 'copy', os.path.join(WAVDIR, 'out%3d.wav')])

wav_list = get_wav(WAVDIR)
for wav in wav_list:
    recog(wav)
    time.sleep(1)

with open('result.txt', 'a') as file:
    file.write("\n")
    file.write("\n")
clear()