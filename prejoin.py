from asyncio import subprocess
from subprocess import Popen


def convDi(value, digit=2):
    valstr = str(value)
    vallen = len(valstr)
    return '0'*(digit-vallen)+valstr

apre = input("Enter audio pre: ")
rag = int(input("Enter Range: ")) 
suraid = int(input("Enter Sura Id: ")) 
process = Popen(["ffmpeg","-f", "mp3", "-i", "-", "sura-"+str(suraid)+".mp3"], stdin=subprocess.PIPE)
fin = process.stdin
for i in range(1, rag+1):
    with open(apre+str(i)+".mp3", "rb") as audio:
        quran = Popen(["ffmpeg","-f", "mp3", "-i", "https://download.quranicaudio.com/verses/Alafasy/mp3/"+convDi(suraid,3)+convDi(i,3)+".mp3", "-f", "mp3","-c:a", "copy", "-"], stdout=subprocess.PIPE)
        fin.write(quran.stdout.read())
        fin.write(audio.read())
fin.flush()
