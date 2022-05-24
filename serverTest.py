import json
import urllib.request
import os
import socket
from datetime import datetime
import smtplib

danger = False 
response = str(datetime.now()) + "\n"
with open("listServers.json", "r" ) as f:
    listServers = json.load(f)
for server in listServers["Items"]:

    ping = os.system("ping -c 1 " + server["ip"])
    if ping == 0:
        response +=server["name"] + " is up" + "\n"
        print(server["name"], "is up")
    else:
        response += server["name"] + " is DOWN" + "\n"
    if server["port"] == 80:
        try:
            res = urllib.request.urlopen(server["url"]).getcode()
            if res == 200:
                response += server["name"] + " " + server["url"] + " ok status " + str(res)+"\n"
        except:
            response += server["name"] + " " + server["url"] + " port " + str(server["port"]) + " " + "DOWN\n"
            danger = True
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((server["ip"], server["port"]))
            s.shutdown(2)
            response += server["name"] + " " + str(server["port"]) + " up\n"
        except:
            response  += server["name"] + " " + str(server["port"]) + " DOWN\n"
            danger = True
    response += "*****************************\n"
print(response)

user = "sysadmin@myDomen"
passwd = "Superpassword"
server = "smtp.mail.server"
port = 587
if danger == False:
    subject = "Server test"
else:
    subject = "Server DANGER"
to = "andrey@dynfor.ru"
charset = 'Content-Type: text/plain; charset=utf-8'
mime = 'MIME-Version: 1.0'
# text = response

body = "\r\n".join((f"From: {user}", f"To: {to}",
       f"Subject: {subject}", mime, charset, "", response))

try:
    smtp = smtplib.SMTP(server, port)
    smtp.starttls()
    smtp.ehlo()
    smtp.login(user, passwd)
    smtp.sendmail(user, to, body.encode('utf-8'))
    print("email sent")
except smtplib.SMTPException as err:
    print('Что - то пошло не так...')
    raise err
finally:
    smtp.quit()
