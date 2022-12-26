from transitions.extensions import GraphMachine
from pyChatGPT import ChatGPT
import openai
from utils import send_text_message , send_image_url
from serpapi import GoogleSearch
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models.send_messages import ImageSendMessage
import random
import requests
from bs4 import BeautifulSoup


session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..vrQKLqYiApYmIQvA.r-iJtWG1Gi2ZGqkJD2YeAZT3fL32DFzs5LdB3WlTzxa2MmLbPlJiGvJ_wvFdgI_6MIwm4fDrt_5uAA6OTBIfFxBPIgm5LAZveslLmY9JHth3xmnk0M8_1S-sQvINstSdm8dCT6gIt5kmFU48vZV9eBEp1-D8j7x1no0M3D1WYiuewse4uIDeAoja-ZVzhXdxZ-1dprj_phsZknAhy3HrT75PxM145zGAgKH-Oe7ERztGrmk2YhrY54kZEEPtyZL_1K97jK6ERYvTFroHpeyRbMhVwebFXuM5d6JoljcDUV2rqBlBT_5dOy8SJ3LD5Z5FAVhciz6JWOe3xUQBNPbA69LkPzIhQ_K0m2H7dCgYNC16c_s0wEruLurRe5Gq1fr3V4tVuvbEMBecruZOYwCFOK4H-dMpxZa-vo5Vy_f1Qg0R4CeiZFGOlv5KUL-6fn9Pv3dByI0bT_U_XJvh1SJRxpwwpq6FweZDkUw4Xz0jiK09a9CiixhqqTMTpHs3AdA5ccV_eWqXH6-yzaerYSm8HYhHPo_Xe7Nls18xkzASppXvyWQPTriOsBFMZjZl5a-l9RqNCYX0Rs0Wul4CnRhBk7AVdlj_TIgekBOEShWB1kr1yxuFeUrTwKGDj3UezrOC2RuAkL1uxkAH60hbkfrUx7ZiZpGd80RHgVQK0QZZMVmf4N3w5H9T_umKOfdvWFmNJm5h1M3eiX_S_Of5nzHhA2owCSB1gq_v_3uWm82lo2GvBJFBsiLAUKEHvyeYEyne3Y_2F3bMxf1j2p2WEYciZkJDYtVjFRBfrKsQw-KXaNdLs4LbNBwlBe0pLTF9wKdvCU2Il-0GEKVbhzJofwD5thtP6dmyLUeiENEvzgD6LcgqJy4JTafxYHsHmuN5A_3wxjJ2-KGrggkcaFZsPfHcrpWJFqKkoApPcKCFpuPY-CqAbxyTUEq8F487F2igUGa6wZ3Dtxki0JHKr3jDvGXfdqoqlALJIPWwhrl9y8PtmYqIX85TSXgfwN0faRRTH4bCt5HKIrAGjna7FN3dSrfCI-T3-u2-h9WCnTvKTl6r9wiol_jaBCqg_oXRiSP0g2CNdJqVgzfmjP0QQvCd8FE_uDY__LXCeXaiAAack59gl7gO_BVcjARtCY1WrssXuLaF1aRqJiOHAAYakDLnXYo8RpdagUZwW_JhGBqnzC1D8Crfmra1MHI2JkF3oV0_7KVAkpzHR3N9WogSWk4r5gAc_--YxENRcrzZUSzY0lpt94ftCDyEuBGgHyPydB1Z5crBKlQvSQ-xhAw1KRAp6YXSjK0mRIf-jV43gGG4Ud_4Q95GSWL-Yo7QFuBFMbQCAfdHiJwxeoOhDYLr1AVbFTcQ3RpVWAIcwd84h7sEJQhy1HvuxGxKiYWbz1s3URvIS8EHNzB2TC8sjWpt5z6vOTT6aSHCu4iiHimkcKjdyO-MHAIydnno49Rwaa8OAHqjxEP3_tBTmdegTdKy8ACRdtsOrOrdPtOLuK63MmJDUG1PaFg8tx95Oc1OFZ2dliWCaF-SnC_pGYYpXTqKzzSpZrTeigWvisYbIvd4rqBZQ9BKaE4b7T6uvofSDIG7QDoe_5AQNjFsGJJEdju4TgXN5B01DlFd4Q7afs5EFMgYJN7Y-8dLGHE1n-CkA3Q9lpAlXbNp1SP_nKpDdmg_W7Q-p30AnDGBe1sEvxWXhrg5bg80N0nO-lcJYJ9QzqF6WnYnNBBFNA2EsVIHCbm3zYzkxwlMk_9EyyrS-CxTWETlQQJ1_B3UQ_4kJPKWJ5LB8yOraK8wfwuGYk6vwDANJY3qp_O_k0N6bFQTYqJ96dc_c-BVrUk7F0ZHBu9O7IHTcnVHO8f8f7KbFMjZgHiJA4XHN-Vfq5wTrNMnLbvg6OJxZbmfoSW8U6xOQWAgGUxtqBuc0g-qr7bifNHay8dvjH3ANtb9LOzHRBAg9sctzR6PnJfgOrRGzLR7o1Sof3gTjDLyaexQWiZhdnkEeGCtTHurUNzrUYsgPvwTooVBxMZviGZtVhNIK7U1NhdqjT4OC9y-8zcuiOWR3AX1HlRtIrx85TJ85AODP374A1xjl3yx_A80MYq2kPLopIl6P4n2YHWyIzj6AsLVLZZb-j1vD9ILm0ia5kTtFys00pqexVfKrk9fukbilkRtqiZwvfVj3IQfuL1pIfQDz1WQ255oy4ifBxl6_z75JTOefrAnxdvzGpzg54tQzDqjok54vt8yDdSnPdg1VRNJya1CmS-IG777zHCE9VlUmhBFS-v3SfGvqVu1XGU.on1X8EB8MPHuRrgjnb-Fnw'

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    #chatGPT state function
    def is_going_to_chatGPT(self, event):
        text = event.message.text.rstrip()
        
        if text == 'chat':
            return True

        return False

    def on_enter_chatGPT(self, event):
        print("I'm entering ChatGPT state")

        self.api = ChatGPT(session_token)

        reply_token = event.reply_token
        send_text_message(reply_token, "歡迎使用 chatGPT\n"+"您可以跟chatGPT自由對話\n"+"輸入exit即可返回user mode")


    def is_going_to_chatGPTexit(self, event):
        text = event.message.text.rstrip()
        
        if text == 'exit':
            return True

        return False

    def on_enter_chatGPTexit(self, event):
        print("I'm entering ChatGPT exit state")
        self.go_back()


    def is_going_to_chatGPTresponse(self, event):
        text = event.message.text.rstrip()
        
        if text != 'exit':
            return True

        return False

    def on_enter_chatGPTresponse(self, event):
        print("I'm entering ChatGPT response")

        text = event.message.text
        response = self.api.send_message(text)
        reply_token = event.reply_token
        send_text_message(reply_token, response["message"])
        self.go_back_chatGPT()

    #google search state function
    def is_going_to_search(self, event):
        text = event.message.text.rstrip()
        
        if text == 'search':
            return True

        return False

    def on_enter_search(self, event):
        print("I'm entering search state")


        reply_token = event.reply_token
        send_text_message(reply_token, "歡迎使用 Google 圖片功能\n"+"您可以輸入 名稱.jpg 來搜尋圖片\n"+"輸入exit即可返回user mode")


    def is_going_to_searchexit(self, event):
        text = event.message.text.rstrip()
        
        if text == 'exit':
            return True

        return False

    def on_enter_searchexit(self, event):
        print("I'm entering search exit state")
        self.go_back()


    def is_going_to_searchresult(self, event):
        text = event.message.text.rstrip()
        
        if text != 'exit':
            return True

        return False

    def on_enter_searchresult(self, event):
        reply_token = event.reply_token
        get_message = event.message.text.rstrip()

        if get_message[-4:].lower() == '.jpg':
            URL_list = []
            try:
                params = {
                    "engine": "google",
                    "tbm": "isch",
                    "api_key": "01242d37e40d56a1db89f05b2a309e0bce05a48c1bca5d31cc94e573a162a937",
                }
                params['q'] = get_message
                client = GoogleSearch(params)
                data = client.get_dict()
                imgs = data['images_results']
                x = 0
                for img in imgs:
                    if x < 5:
                        URL_list.append(img['original'])
                        x += 1
                print("success")
            except:
                url = 'https://www.google.com.tw/search?q=' + \
                    get_message+'&tbm=isch'
                request = requests.get(url=url)
                html = request.content
                bsObj = BeautifulSoup(html, 'html.parser')
                content = bsObj.findAll('img', {'class': 't0fcAb'})
                for i in content:
                    URL_list.append(i['src'])
        url = random.choice(URL_list)
        print(url)
        msg = ImageSendMessage(original_content_url=url, preview_image_url=url)
        #print(msg)
        send_image_url(reply_token , url)
        self.go_back_search()
    
    #help state


    def is_going_to_help(self, event):
        text = event.message.text
        text = text.rstrip()
        text = text.lower()

        
        if text == "help":
            help_msg = ""
            help_msg = help_msg + "在Menu 狀態下可以輸入 chat 進入 chatGPT mode 與 chatGPT聊天 \n\n"
            help_msg = help_msg + "在Menu 狀態下可以輸入 search 進入 search mode 輸入關鍵字爬蟲圖片\n\n"
            help_msg = help_msg + "在Menu 狀態下均可以輸入 help 查看本指令提示"
            help_msg = help_msg + "在chat GPT 狀態下可以輸入 任何訊息與ChatGPT聊天 但需要耐心等候\n\n"
            help_msg = help_msg + "在chat GPT 狀態下可以輸入 exit 離開 chatGPT mode 回到menu\n\n"
            help_msg = help_msg + "在search 狀態下可以輸入 欲查名稱.jpg 進入 search mode 來爬蟲所需的圖片\n\n "
            help_msg = help_msg + "在search 狀態下可以輸入 exit 離開 search mode 回到menu\n\n"
            reply_token = event.reply_token
            send_text_message(reply_token,help_msg)
        return False

    def on_enter_help(self, event):
        print("I'm entering state2")
        self.go_back()
