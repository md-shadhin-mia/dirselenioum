
import json
import sys
from operator import sub
import subprocess
from subprocess import Popen
import http.client
#importing selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


conn = http.client.HTTPSConnection("api.quran.com")

payload = "{}"

def convDi(value, digit=2):
    valstr = str(value)
    vallen = len(valstr)
    return '0'*(digit-vallen)+valstr

def getDuration(filename):
    args=("ffprobe","-show_entries", "format=duration","-i",filename)
    outer = Popen(args, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    outer.wait()
    output = outer.stdout.read()
    return float(str(output, encoding="utf-8").split("FORMAT]")[1].split("=")[1].split("\r")[0])

server = Popen(["python3", "-m", "http.server", "3000"], stderr=subprocess.PIPE)
driver = webdriver.Firefox()
driver.get("http://localhost:3000/canvastest.html")

#input from your
apre = input("Enter audio pre: ")

suraid = int(input("Enter Sura Id: "))

conn.request("GET",  "/api/v4/chapters/"+str(suraid)+"?language=bn", payload)
res = conn.getresponse()
surainfo = json.loads(res.read().decode("utf-8"))
rag = int(surainfo["chapter"]["verses_count"])
nameing =str(suraid)+". "+ surainfo["chapter"]["name_simple"]+" ("+surainfo["chapter"]["translated_name"]["name"]+") "
#output audio video
audiofn = "audio-"+str(suraid)+".mp3"
videofn = "video-"+str(suraid)+".mp4"
audioout = Popen(["ffmpeg","-f", "mp3", "-i", "-", audiofn], stdin=subprocess.PIPE)
videoout = Popen(["ffmpeg","-f","h264","-i", "-", "-r", "25","-c:v", "copy", videofn], stdin=subprocess.PIPE)


for index in range(rag+1):
    if(index==0):
        if suraid == 1:
            continue
        conn.request("GET",  "/api/v4/verses/by_key/1:1?fields=text_uthmani&translations=163&language=en", payload)
    else:
        conn.request("GET",  "/api/v4/verses/by_key/"+str(suraid)+":"+str(index)+"?fields=text_uthmani&translations=163&language=en", payload)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    # data = "Sura fatiha: "+str(index)
    # request to canvas for genarate image
    datajs = json.dumps([data["verse"]["text_uthmani"], data["verse"]["translations"][0]['text'], data["verse"]["verse_key"], nameing])
    driver.execute_script("setarray(arguments[0]);", datajs)
    # driver.execute_script("setarray(\""+data+"\");")
    if(index==0):
        localfilename = "bnbismillah.mp3"
    else:
        localfilename = apre+str(index)+".mp3"
    if(suraid == 1 and index == 1):
        dymeflename = "bismillah.mp3"
    else:  
        dymeflename = "https://everyayah.com/data/khalefa_al_tunaiji_64kbps/"+convDi(suraid,3)+convDi(index,3)+".mp3"

    # calculate total durations
    totalduraton = getDuration(localfilename)+getDuration(dymeflename)
    # totalduraton = getDuration(localfilename)
    norduration = round(totalduraton,2)
    extraduration = round(totalduraton-norduration, 4)
    totalduraton = norduration

    # with open(localfilename, "rb") as audio:
    arabic = Popen(["ffmpeg","-f", "mp3", "-i", dymeflename, "-f", "mp3", "-c:a","copy", "-"], stdout=subprocess.PIPE)
    audioout.stdin.write(arabic.stdout.read())
    bangla = Popen(["ffmpeg","-f", "mp3", "-i", localfilename, "-ss", str(extraduration), "-f", "mp3","-"], stdout=subprocess.PIPE)
    audioout.stdin.write(bangla.stdout.read())

    # write to video file
    output = driver.execute_script("return getArray();")
    
    print("read image",len(output))
    for out in output:
        with open("temp.png", "wb") as temp:
            temp.write(bytearray(out))
    
    videloop = Popen(["ffmpeg", "-loop", "1", "-t", str(totalduraton), "-r", "25", "-i", "temp.png", "-vf", "fade=t=in:st=0:d=0.3,fade=t=out:st="+str(totalduraton-0.3)+":d=0.3", "-t", str(totalduraton),  "-f", "h264", "-"],stdout=subprocess.PIPE)
    videoout.stdin.write(videloop.stdout.read())

videoout.stdin.close()
audioout.stdin.close()
#vido close audio

print("wait for ending ")
audioout.wait()
videoout.wait()
print("final build")
videoOudio = Popen(["ffmpeg", "-r", "25","-i", videofn,"-i", audiofn, "-c:v", "copy", "video-audio-"+str(suraid)+".mp4"])
videoOudio.wait()

server.terminate()