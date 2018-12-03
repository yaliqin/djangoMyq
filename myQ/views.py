from django.http import HttpResponse
from os import path
import sys
sys.path.append(path.abspath('/home/pi/python/myq_working'))
sys.path.append(path.abspath('/home/pi/python/private'))
# below are the methods defined in myq_working project
from MyQAPI import MyQAPI
from constants import Const
from send_email_html import send_mail
from senstive import email_info
from senstive import liftmaster
import time

longTime = 1
close_door_index=Const.doorName['Small']
# Create your views here.


def index(request):
    # give the links to activate period monitor
    response = HttpResponse()
#    url = path(myQ.urls.urlpatterns['check_door_status/'])
    html = """\
    <html>
      <head></head>
      <body>
        <a href="/myQ/check_door_status" target="_blank">start to monitor door state</a>
        <p>Text and HTML</p>
      </body>
    </html>
    """

    response.write("<p> Here's the text of the web page. </p>")
    response.write(html)
    return response


#  periodically monitor the door status,if door open time meet threshold, send email notification
#  there is a confirm to close link in email, when click, it goes to confirm_set_door() method
def check_door_status(request,email_info,liftmaster):
    r= MyQAPI()
    r.usr=liftmaster.user
    r.pwd=liftmaster.pwd
    door_open_cnt = [0,0]
    r.login()
    while True:
        door_info=r.get_door_info() #doorInfo consists id,name,state
        for index in range(len(door_info)):
            if door_info[index][2]==Const.doorState['DoorClose']:
                door_open_cnt[index] += 1
                print (str(door_info[index][1])+" is open for " + str(door_open_cnt[index]) +" minutes")
                # print(door_info[index][2])
            else:
                door_open_cnt[index] = 0
            if door_open_cnt[index] >= longTime:
                url = "http://127.0.0.1:8000/myQ/confirm_set_door"
                send_mail(longTime,email_info.address,email_info.password,url)
                global close_door_index
                close_door_index= Const.doorName[door_info[index][1]]
                # print(close_door_index)
                sentence = str(door_info[index][1])+' is open' + str(door_open_cnt[index])+ 'minutes'
                return HttpResponse(sentence)
                time.sleep(120.0)
        time.sleep(60.0 )


#  send email notification of opening door too long
def confirm_set_door(request,liftmaster):
    r= MyQAPI()
    r.usr=liftmaster.user
    r.pwd=liftmaster.pwd
    r.login()
    global close_door_index
    # print(close_door_index)
    resp= r.setDeviceState('desireddoorstate',Const.doorState['DoorClose'],close_door_index)
    print(resp.status_code)
    if resp.status_code == 200:
        return HttpResponse('Door is Closed')
    else:
        return HttpResponse('Door not closed')
