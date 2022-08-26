import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
from subprocess import Popen

from os import path

import http.client

conn = http.client.HTTPSConnection("api.quran.com")

payload = "{}"

class drivetts:
    def __init__(self) :
        self.driver = webdriver.Firefox()
        self.driver.get("https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech")
        self.ssmlbtn = self.driver.find_element(By.ID, "ssmlInputTab")
        self.ssmlfild = self.driver.find_element(By.ID, "ttsssml")
        self.btnwapper = self.driver.find_element(By.ID, "playli")
        self.driver.implicitly_wait(3)
        self.driver.execute_script("document.getElementById(\"ssmlInputTab\").scrollIntoView()")
        self.driver.execute_script("document.getElementById(\"ssmlInputTab\").click()")
        while self.ssmlfild.get_attribute("value")=="":
            sleep(0.5)
        self.driver.execute_script("document.getElementById(\"ttsssml\").value =\"\"")

    def playtts(self, text):
        self.driver.execute_script("document.getElementById(\"ttsssml\").value =\'\'")
        self.ssmlfild.send_keys(text)
        self.driver.execute_script("document.getElementById(\"playbtn\").click()")
        while self.btnwapper.get_attribute("hidden")!=None:
            sleep(0.5)
        print("ending")
    def refesh(self):
        self.driver.quit()
        self.__init__()







textssl = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="en-US-JennyNeural"><prosody rate="0%" pitch="0%">
that is working!
</prosody></voice></speak>
"""
textsslbn = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="bn-BD-NabanitaNeural"><prosody rate="0%" pitch="0%">বাংলায় এটি কাজ করে</prosody></voice></speak>"""

def bangla(text):
    ssml = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="bn-BD-PradeepNeural"><prosody rate="0%" pitch="0%">"""+text+"""</prosody></voice></speak>"""
    return ssml
def engreji(text):
    ssml = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="en-US-GuyNeural"><prosody rate="0%" pitch="0%">"""+text+"""</prosody></voice></speak>"""
    return ssml

azuretts = drivetts()
for suraId in range(1, 115):
    conn.request("GET", "/api/v4/chapters/"+str(suraId)+"?language=en", payload)
    res = conn.getresponse()
    sura = json.loads(res.read().decode("utf-8"))
    totalVerse = sura["chapter"]["verses_count"]
    print(totalVerse)
    suraname = sura["chapter"]["name_simple"]
    suraname = suraname.replace(" ", "-")
    trac = 1
    for i in range(1, totalVerse+1):
        filename = "/audio/"+suraname+"-"+str(i)+".mp3"
        if not path.exists(filename):
            conn.request("GET", "/api/v4/quran/translations/162?verse_key="+str(suraId)+"%3A"+str(i), payload)
            res = conn.getresponse()
            data = json.loads(res.read().decode("utf-8"))
            text = data["translations"][0]["text"]
            text = re.sub(r"([^্ ])([য])",r"\1"+"জ" ,text)
            print(text)
            mpegPro = Popen(["ffmpeg", "-f", "pulse", "-i", "default", filename])
            azuretts.playtts(bangla(text))
            mpegPro.terminate()
            trac+=1
            if trac%10 == 0:
                azuretts.refesh()

            
        



# 
# azuretts.playtts(textsslbn)

# # driver.execute_script("document.getElementById(\"ttsssml\").value = \""+textssl+"\";")
# print(btnwapper.get_attribute("hidden"))



# textsslbn = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="en-US-JennyNeural"><prosody rate="0%" pitch="0%">আরেকটি ও ভালোভাবে কাজ করছে</prosody></voice></speak>"""
# driver.execute_script("document.getElementById(\"ttsssml\").value =\"\"")
# ssmlfild.send_keys(textsslbn)
# driver.execute_script("document.getElementById(\"playbtn\").click()")
# btnwapper = driver.find_element(By.ID, "playli")

# ActionChains(driver).move_to_element(ssmlbtn).perform()
# ssmlbtn.click()

# txbox = driver.find_element(By.ID, "ttsssml")


# txbox.send_keys(text)

# playbtn = driver.find_element(By.ID, "playbtn")
# playbtn.click()