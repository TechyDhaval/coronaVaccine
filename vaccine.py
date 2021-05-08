#########################################################################################################################################################
###################################################  Simple script to book corona vaccine ###############################################################
#########################################################################################################################################################

import requests
import json
import datetime
import time

url = 'https://cdn-api.co-vin.in/api'
headers = {'content-type': 'application/json'}

#genOtp = "/v2/auth/public/generateOTP"

## Change pin code as per center and keep tomorrow's and the day after tomorrow's date.
appointmentByPin = ["/v2/appointment/sessions/calendarByPin?pincode=560011&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560066&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560003&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560037&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560017&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560078&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560076&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560030&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560020&date=07-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560011&date=08-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560066&date=08-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560003&date=08-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560037&date=08-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560017&date=08-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560078&date=08-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560076&date=08-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560030&date=08-05-2021",
"/v2/appointment/sessions/calendarByPin?pincode=560020&date=08-05-2021"]

# Token timeout 15 min, Keep changing token at 15 min or automate this.
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI2ZWIwN2YyNS00ZGJkLTQ0YWMtYTRlZi1iMTliNzVjMTliMTkiLCJ1c2VyX2lkIjoiNmViMDdmMjUtNGRiZC00NGFjLWE0ZWYtYjE5Yjc1YzE5YjE5IiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo3NzYwOTU1NTk4LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjg3NDM1MzQ5MTYwMDQwLCJ1YSI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS85MC4wLjQ0MzAuNzIgU2FmYXJpLzUzNy4zNiBFZGcvOTAuMC44MTguNDIiLCJkYXRlX21vZGlmaWVkIjoiMjAyMS0wNS0wNlQwOToxOTozMS44NTJaIiwiaWF0IjoxNjIwMjkyNzcxLCJleHAiOjE2MjAyOTM2NzF9.nw_Ha3P_F5A1RfaqYEeD5iooz1XEaASNtjn4VvrSWeA"

headers["Authorization"] = "Bearer " + token
headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42"

bookApi = "https://cdn-api.co-vin.in/api/v2/appointment/schedule"
bookReq = {}
## beneficiary ids once you register your name in covin site. 
ben = ["87435349160040","51667158428580"]

bookReq["beneficiaries"] = ben
bookReq["slot"] = "01:00PM-03:00PM"
bookReq["dose"] = 1
flag = False

while(True):
    for appoint in appointmentByPin :
        time.sleep(1)
        g = requests.get(url+appoint, headers=headers)
        if g.status_code != 200 :
            print(g.status_code)
            continue
        res = json.loads(g.text)
        centers = res["centers"]
        final = []

        for center in centers:
            if center["sessions"][0]["min_age_limit"] < 45 :
                final.append(center)

        for fn in final:
            if fn["sessions"][0]["available_capacity"] > 0 :
                print("Booking at " + fn["name"])
                bookReq["center_id"] = fn["center_id"]
                bookReq["session_id"] = fn["sessions"][0]["session_id"]

                bres = requests.post(bookApi, data = json.dumps(bookReq), headers=headers)
                print(bres.text)
                print("Booked " + fn["name"])
                flag = True
                break

        if flag :
            break
        print("Not able to book at " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    if flag :
        break
    time.sleep(5)