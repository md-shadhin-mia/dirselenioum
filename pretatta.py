from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
        self.driver.execute_script("document.getElementById(\"ttsssml\").value =\"\"")
        self.ssmlfild.send_keys(text)
        self.driver.execute_script("document.getElementById(\"playbtn\").click()")
        while self.btnwapper.get_attribute("hidden")!=None:
            sleep(0.5)
        print("ending")







textssl = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="en-US-JennyNeural"><prosody rate="0%" pitch="0%">
that is working!
</prosody></voice></speak>
"""
textsslbn = """<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="en-US-JennyNeural"><prosody rate="0%" pitch="0%">এটি কাজ করছে</prosody></voice></speak>"""



azuretts = drivetts()


azuretts.playtts(textsslbn)

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