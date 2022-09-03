
import http.client
import json
import subprocess

conn = http.client.HTTPSConnection("api.qurancdn.com")
payload = "{}"

def str2dig(sec):
    if len(str(sec)) == 1:
        return "0"+str(sec)
    else:
        return str(sec)

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
    return str2dig(hour)+":"+str2dig(minit)+":"+str2dig(sec)+"."+str(extra)

conn.request("GET", "/api/v4/chapter_recitations/7/1?segments=true", payload)
res = conn.getresponse()
sura = json.loads(res.read().decode("utf-8"))
print
datas = sura['audio_file']
print(datas["audio_url"])
i = 0
for times in datas["timestamps"]:
    print(getFormate(times["timestamp_from"]), getFormate(times["duration"]))
    process = subprocess.Popen(["ffmpeg", "-i", datas["audio_url"], "-ss", getFormate(times["timestamp_from"]), "-t", getFormate(times["duration"]), "splited/"+str2dig(i)+".mp3"])
    i+=1
    process.wait()