import argparse
import pathlib
import os
import sys
import subprocess
import shutil
import speech_recognition as sr
from progress.bar import IncrementalBar


parser = argparse.ArgumentParser()
input_extentions = ['mp3']
process_extentions = ['wav']
txt_extensions = ['txt']
file_for_ffmpeg = '/tmp/mp3_list.txt'
#tmp_dir = '/tmp/voice_recog'


def recog(wav_file):
    retry = 1
    r = sr.Recognizer()
    resultfile = (str(wav_file) + '.txt')
    while retry < 6:
        try:
            voice_track = sr.AudioFile(wav_file)

            with voice_track as audio_file:
                audio_content = r.record(audio_file)
            # print("Recognition  " + f'{wav_file}' +
            #      " of " + str(len(wav_list) - 1))
            speech = r.recognize_google(audio_content, language='ru')
            retry = 6

            with open(resultfile, 'a') as file:
                file.write(speech)
            #print(f"Writed in {resultfile}")
        except sr.UnknownValueError:
            #print(f"{wav_file} -- Recognition error! Retry... " + str(retry))
            with open(resultfile, 'a') as file:
                file.write("\n")
                file.write("\n")
                file.write(f"{wav_file} -- Recognition error \n")
                file.write("\n")

            retry = retry + 1


# def concat_audio(file_for_ffmpeg, tmp_dir):
#    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i',
#                    file_for_ffmpeg, '-c', 'copy', os.path.join(tmp_dir, 'out.mp3')])


def segment_file(inputfile, tmp_dir):
    subprocess.run([f'ffmpeg', '-i', inputfile, '-f', 'segment',
                    '-segment_time', '59', '-c', 'copy', os.path.join(tmp_dir, ((inputfile.split('/')[-1]).split('.')[0]) + '%3d.mp3')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_wav_order(list, tmp_dir):
    bar = IncrementalBar('Getting WAV order  \t', max=len(list))

    for file in list:

        duration = get_track_duration(file)
        if duration > 59:
            segment_file(file, tmp_dir)
        else:
            wavfile = os.path.join(
                tmp_dir, ((file.split('/')[-1]).split('.')[0]) + '000.wav')
        bar.next()
    bar.finish()


def rm_dir(directory):
    try:
        shutil.rmtree(directory)
    except OSError as e:
        print("Error: %s : %s" % (directory, e.strerror))


def get_track_duration(input_filename):
    #   ffprobe -i <file> -show_entries format=duration -v quiet -of csv="p=0"
    input_filename = input_filename.replace(' ', '\ ')
    cmd = f'ffprobe -i {input_filename} -show_entries format=duration -v quiet -of csv="p=0"'
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    #output = p.stdout.read()
    stdout, stderr = p.communicate()
    output = int(float(stdout))
    return output


def mp3_to_wav(mp3file, wavfile):
    subprocess.run(['ffmpeg', '-i', mp3file, wavfile],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def create_dirs(tmp_dir):
    try:
        os.mkdir(path=tmp_dir)
        print(f"Directory {tmp_dir} sucsessfully created!\n")
    except FileExistsError:
        print(f"Directory {tmp_dir} exists!\n")


def create_file_with_input_path(filelist, file_for_ffmpeg):
    for filepath in filelist:
        print(filepath)
        with open(file_for_ffmpeg, 'a') as file:
            file.write("file " + "'" + str(filepath) + "'\n")


def get_input_file_list(filelist):
    input_file_list = []
    for file in filelist:
        if file.split('.')[-1] in input_extentions:
            input_file_list.append(file)
    return input_file_list


def get_file_list(tmp_dir, list_of_extentions):
    file_list = []
    lf = os.listdir(path=tmp_dir)
    for file in lf:
        if file.split('.')[-1] in list_of_extentions:
            file_list.append(os.path.join(tmp_dir, file))
    return file_list


def dir_checker(directory):
    print("Checking directory")
    if os.path.isdir(directory):
        print("Directory: ")
        print(directory)
        print("Checking directory:\t OK")
    else:
        print("Directory: ", directory, "doesn't exists!")
        parser.print_help()
        sys.exit(2)
    return directory


def args_to_file_list(raw_file_list):
    file_list = []
    try:
        for file in raw_file_list:
            f = os.path.realpath(file.name)
            file_list.append(f)
    except TypeError:
        pass
    return file_list

def cli_parser():

    parser.add_argument("-d", "--directory",
                        type=pathlib.Path,
                        default=os.path.realpath(os.curdir),
                        help='set files directory , default current directory')

    parser.add_argument("-f", "--files",
                        type=argparse.FileType('r'),
                        nargs='*',
                        help='work with only given mp3 file list')

    parser.add_argument("-o", "--outputfile",
                        type=argparse.FileType('w'),
                        default=os.path.join(
                            os.path.realpath(os.curdir), 'result.txt'),
                        help='set outputfile')
    parser.add_argument("-tmp", "--tempdir",
                        type=pathlib.Path,
                        default='/tmp/voice_recog',
                        help='set temp dir')
    args = parser.parse_args()

    directory = os.path.realpath(args.directory)
    outputfile = args.outputfile.name
    tmp_dir = args.tempdir
    print("outputfile :", outputfile)

    return directory, args.files, outputfile, tmp_dir


directory, raw_file_list, outputfile, tmp_dir = cli_parser()
outputfile = outputfile.replace(' ', '\ ')
create_dirs(tmp_dir)

wdir = dir_checker(directory)
fl = args_to_file_list(raw_file_list)
if len(fl) == 0:
    fl = os.listdir(path=wdir)
input_files = get_input_file_list(fl)

create_file_with_input_path(input_files, file_for_ffmpeg)
get_wav_order(input_files, tmp_dir)
mp3_list = get_file_list(tmp_dir, input_extentions)
bar = IncrementalBar('Mp3 to WAV \t \t', max=len(mp3_list))
for mp3 in mp3_list:
    wavfile = (mp3.split('.')[0] + '.wav')
    mp3_to_wav(mp3, wavfile)
    bar.next()
bar.finish()
wav_list = get_file_list(tmp_dir, process_extentions)

bar = IncrementalBar('Recognition \t \t', max=len(wav_list))
for file in wav_list:
    bar.next()
    recog(file)
bar.finish()
# rm_dir(tmp_dir)
txt = get_file_list(tmp_dir, txt_extensions)

with open(outputfile, 'w') as outfile:
    for fname in txt:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
print('Result writed in: \n', outputfile)
rm_dir(tmp_dir)
