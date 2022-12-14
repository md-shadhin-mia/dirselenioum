
import json
import math
import os
from operator import sub
from random import randint
import subprocess
from subprocess import Popen
import http.client

import requests

def convDi(value, digit=2):
    valstr = str(value)
    vallen = len(valstr)
    return '0'*(digit-vallen)+valstr

def getDuration(filename):
    args=("ffprobe","-show_entries", "format=duration","-i",filename)
    outer = Popen(args, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
    outer.wait()
    output = outer.stdout.read()
    return float(str(output, encoding="utf-8").split("FORMAT]")[1].split("=")[1].split("\n")[0])

def getFormate(milisec):
    extra = milisec %  1000
    milisec = milisec - extra
    sec = int(milisec / 1000)
    xsec = sec % 60
    sec = sec-xsec
    minit = int(sec / 60)
    sec = xsec
    xmin = minit % 60
    minit = minit - xmin
    hour = int(minit / 60)
    minit = xmin
    return convDi(hour)+":"+convDi(minit)+":"+convDi(sec)+","+str(int(extra))

class AudioVideoStream:
    def __init__(self, index):
      self.videoStream = None
      self.audioStream = None
      self.complited = False
    def setAudioStream(self, stream):
      self.audioStream = stream
    def setVideoStream(self, stream):
      self.videoStream = stream
    def complite(self):
      self.complited = True


class RenderInit:
    def __init__(self):
        self.subtitlecount = 1
        self.starttilme = 0
        self.totalduraton = 0
        self.streamArray = []
        self.conn = http.client.HTTPSConnection("api.quran.com")
        self.payload = "{}"
        self.serverStarting()
        self.userInput()
        self.suraInfoInit()
        self.InitVideoAudioWriter()
        for index in range(self.rag+1):
            self.render(index)
            self.writeSteam()

        self.finishVideoAudioWrite()
        
    def serverStarting(self):
        data = os.popen("cd npm_server/ \nnode index.js").read(6)
        print(data)

    def userInput(self):
        self.apre = input("Enter audio pre: ")
        self.suraid = int(input("Enter Sura Id: "))

    def suraInfoInit(self):
        self.conn.request("GET",  "/api/v4/chapters/"+str(self.suraid)+"?language=bn", self.payload)
        res = self.conn.getresponse()
        surainfo = json.loads(res.read().decode("utf-8"))
        self.rag = int(surainfo["chapter"]["verses_count"])
        self.nameing =str(self.suraid)+". "+ surainfo["chapter"]["name_simple"]+" ("+surainfo["chapter"]["translated_name"]["name"]+") "

    def InitVideoAudioWriter(self):
        self.audiofn = "audio-"+str(self.suraid)+".mp3"
        self.videofn = "video-"+str(self.suraid)+".mp4"
        self.audioout = Popen(["ffmpeg","-f", "mp3", "-i", "-", "-c:a", "copy", self.audiofn], stdin=subprocess.PIPE)
        self.videoout = Popen(["ffmpeg","-f","h264","-i", "-", "-r", "25","-c:v", "copy", self.videofn], stdin=subprocess.PIPE)
        self.subtitle = open("audio/video/subtitle-"+str(self.suraid)+".srt", "wb")

    def finishVideoAudioWrite(self):
        self.videoout.stdin.close()
        self.audioout.stdin.close()
        #vido close audio
        self.subtitle.close()
        print("wait for ending ")
        self.audioout.wait()
        self.videoout.wait()
        print("final build")

    def render(self, index):
        if(index==0):
            if self.suraid == 1:
                return
            self.conn.request("GET",  "/api/v4/verses/by_key/1:1?fields=text_uthmani&translations=163,131&language=en", self.payload)
        else:
            self.conn.request("GET",  "/api/v4/verses/by_key/"+str(self.suraid)+":"+str(index)+"?fields=text_uthmani&translations=163,131&language=en", self.payload)
        res = self.conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        # data = "Sura fatiha: "+str(index)
        # request to canvas for genarate image
        datajs = [data["verse"]["text_uthmani"], data["verse"]["translations"][1]['text'], data["verse"]["verse_key"], self.nameing]
        # driver.execute_script("setarray(arguments[0]);", datajs)
        # driver.execute_script("setarray(\""+data+"\");")

        imgRes = requests.post("http://localhost:8000", json=datajs)
        if(index==0):
            localfilename = "audio/bnbismillah.mp3"
        else:
            localfilename = self.apre+str(index)+".mp3"
        if(self.suraid == 1 and index == 1):
            dymeflename = "audio/bismillah.mp3"
        else:  
            dymeflename = "https://everyayah.com/data/khalefa_al_tunaiji_64kbps/"+convDi(self.suraid,3)+convDi(index,3)+".mp3"
        
        if index == 0:
            dymeflename = "audio/bismillah.mp3"
        # calculate total durations
        starttilme += totalduraton
        totalduraton = getDuration(localfilename)+getDuration(dymeflename)
        self.subtitle.write((str(index)+"\n").encode("utf-8"))
        self.subtitle.write((getFormate(starttilme*1000)+" --> "+getFormate((starttilme+totalduraton)*1000)+"\n").encode("utf-8"))
        self.subtitle.write((data["verse"]["translations"][0]['text']+"\n\n").encode("utf-8"))
        # totalduraton = getDuration(localfilename)
        norduration = round(totalduraton,2)
        extraduration = round(totalduraton-norduration, 4)
        totalduraton = norduration
        ad_vd_stream = AudioVideoStream(index)
        self.streamArray.append(ad_vd_stream)
        # with open(localfilename, "rb") as audio:
        audioProcess = Popen(["ffmpeg", "-i", dymeflename, "-ss", str(extraduration), "-i", localfilename,"-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1,loudnorm=I=-6" ,"-f", "mp3", "-"], stdout=subprocess.PIPE)
        ad_vd_stream.setAudioStream(audioProcess.stdout.read())

        # write to video file
        # output = driver.execute_script("return getArray();")
        
        print(index, "out of", self.rag)
        tempfilename = "temp-"+str(randint(10000, 99999))+".png"
        # for out in output:
        with open(tempfilename, "wb") as temp:
            temp.write(imgRes.content);
        
        videoProcess = Popen(["ffmpeg", "-loop", "1", "-t", str(totalduraton), "-r", "25", "-i", tempfilename, "-vf", "fade=t=in:st=0:d=0.3,fade=t=out:st="+str(totalduraton-0.3)+":d=0.3", "-t", str(totalduraton), "-preset","veryfast", "-f", "h264", "-"],stdout=subprocess.PIPE)
        ad_vd_stream.setVideoStream(videoProcess.stdout.read())
        os.remove(tempfilename)
        ad_vd_stream.complite()
        
    def writeSteam(self):
        if len(self.streamArray) > 0:
            streams = self.streamArray.pop(0)
            self.audioout.stdin.write(streams.audioStream)
            self.videoout.stdin.write(streams.videoStream)
    def clearUp(self):
        videoOudio = Popen(["ffmpeg", "-r", "25","-i", self.videofn,"-i", self.audiofn, "-c:v", "copy", "audio/video/video-audio-"+str(self.suraid)+".mp4"])
        videoOudio.wait()
        os.remove(self.videofn)
        os.remove(self.audiofn)


RenderInit()



