# google_recognition_tool
Tool just recognize russian speech  from mp3 files and write it to file.


Простая утилита для распознования  русской речи с помощью google. 

На вход подаются сколь угодно mp3 файлов неограниченного размера, скрипт преобразует их в  wav файлы длиной не более минуты (ограничение google). На выходе выдается txt документ. 

## Использование:

```
python3 voice_recog.py -h
```

```
python3 voice_recog.py -d ~/Downloads/
```
Найдет в папке Downloads все mp3  файлы и попытается их распознать как один текст. Результат распознования сохранится в текущем каталоге с именем result.txt
```
python3 voice_recog.py -f ~/Downloads/0[1-5].mp3 -o ~/Documents/лекция.txt
``````
Отправит на распознование файлы 01.mp3 02.mp3 04.mp3 05.mp3  и сохранит результат распознования в файл лекция.txt
```
python3 voice_recog.py -t /mnt/media/
```
Найдет в текущей папке все mp3 файлы, результат распознования сохранится в текущем каталоге с именем result.txt, а каталог /mnt/media/ будет использоваться для хранения промежуточных wav файлов необходимых для работы скрипта.

## Установка:

```
git clone https://github.com/cosmickitten/google_recognition_tool.git
cd google_recognition_tool
pip install -r requirements.txt
python3 voice_recog.py --help
```
