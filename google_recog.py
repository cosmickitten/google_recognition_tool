#!/bin/python


#   ffmpeg -i "concat:1.mp3|2.mp3|3.mp3" -acodec copy out.mp3

#   ffmpeg -i out.mp3 1.wav 

#   ffmpeg -i 1.wav -f segment -segment_time 60 -c copy out%d.wav

from time import sleep
import speech_recognition as sr
import os


def create_dirs():
    try:
        os.mkdir(path="./input")
    except FileExistsError:
        print("Directory input Exists!")
    try:
        os.mkdir(path="./wav")
    except FileExistsError:
        print("Directory wav Exists!")
    input_dir = "./input"
    wav_dir="./wav"
    input_dirs = {"input_dir" : input_dir,"wav_dir" : wav_dir}
    return input_dirs

def get_mp3(input_dirs):
    print("Поиск ",input_dirs["input_dir"])
    mp3_list=os.listdir(path=input_dirs["input_dir"])
    print("Found : " , mp3_list)
    for i in mp3_list:
        with open('mp3_list.txt', 'a') as file:
            file.write("file " + "'" + input_dirs["input_dir"] +"/"+ f'{i}' + "'\n")
    
def get_wav():
    wav_list=os.listdir(path=input_dirs["wav_dir"])
    return wav_list

def recog(wav_list):
    r = sr.Recognizer()
        #i=12
    for i in wav_list:
        try:
            voice_track = sr.AudioFile(f'./wav/{i}')
            
            with voice_track as audio_file:
                audio_content = r.record(audio_file)
            print("Recognition of "+ f'{i}' +" из "+ str(len(wav_list)-1)) 
            speech = r.recognize_google(audio_content, language = 'ru')
            
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
input_dirs = create_dirs()
get_mp3(input_dirs)
os.system('ffmpeg -f concat  -safe 0  -i mp3_list.txt -c copy ./input/out.mp3')
os.system('ffmpeg -i ./input/out.mp3 ./input/1.wav ')
os.system('ffmpeg -i ./input/1.wav -f segment -segment_time 59 -c copy ./wav/out%d.wav')
wav_list = get_wav()
recog(wav_list) 
with open('result.txt', 'a') as file:
    file.write("\n")
    file.write("\n")