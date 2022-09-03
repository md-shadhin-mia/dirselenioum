from asyncore import write
import base64
import json
from msilib.schema import File
import subprocess
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import http.client

conn = http.client.HTTPSConnection("api.quran.com")

payload = "{}"



driver = webdriver.Firefox()

driver.get("C:\\Users\\Shadhin\\Documents\\code\\autometions\\dirselenioum\\canvastest.html")

conn.request("GET",  "/api/v4/verses/by_key/2:255?fields=text_uthmani&translations=161&language=en", payload)
res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))
farame = 25*5


count = [0]
def setPoint():
    send = 0
    for i in range(farame):
        utl = str(i)+"."+data["verse"]["text_uthmani"]
        driver.execute_script("setarray(\""+utl+"\");")
        send += 1
        if send >= 4:
            while(count[0] < i):
                pass
            send = 0
        
def writeto():
    # ffmepg = subprocess.Popen(["ffmpeg","-r", "25", "-i", "-", "ovid.mkv"], stdin=subprocess.PIPE)
    filout = open("tempfile.tmp", "wb")
    while count[0] < farame:
        output = driver.execute_script("return getArray();")
        count[0] += len(output)
        print(count[0])
        for u in output:
            filout.write(bytearray(u))
    filout.close()
    # ffmepg.stdin.close()
    # ffmepg.wait()

# 
# # coding 

# for i in range(25*10):
#         #getting byte from canvas
#         utl = str(i)+"."+data["verse"]["text_uthmani"]
#         driver.execute_script("setarray(\""+utl+"\");")
#         output = driver.execute_script("return getArray();")
#         while output == None:
#             output = driver.execute_script("return getArray();")
#         print(output)
point = Thread(target=setPoint)
writer = Thread(target=writeto)

point.start()
writer.start()

point.join()
point.join()




# ffmepg.stdin.close()
# ffmepg.wait()
