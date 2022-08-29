from asyncio import subprocess
from subprocess import Popen


def convDi(value, digit=2):
    valstr = str(value)
    vallen = len(valstr)
    return '0'*(digit-vallen)+valstr

apre = input("Enter audio pre: ")
rag = int(input("Enter Range: ")) 
process = Popen(["ffmpeg","-f", "mp3", "-i", "-", "-c:a", "copy", "arabn.mp3"], stdin=subprocess.PIPE)
fin = process.stdin
for i in range(1, rag+1):
    with Popen(["ffmpeg","-f", "mp3", "-i", "https://download.quranicaudio.com/verses/Alafasy/mp3/"+convDi(2,3)+convDi(i,3)+".mp3", "-f", "mp3","-c:a", "copy", "-"], stdout=subprocess.PIPE) as audio:
        fin.write(audio.stdout.read())
    with open(apre+str(i)+".mp3", "rb") as audio:
        fin.write(audio.read())
fin.close()
process.terminate()