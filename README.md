# linebot introduction

我的linebot主要有兩個功能，一個是跟chatGPT聊天，一個是使用google API 來做圖片爬蟲。

**我的finite state machine diagram:**

![](https://imgur.com/a/HpDXWiP)

**自動推播:**
當程式開始執行後，Linbot會自動傳給用戶歡迎的訊息:

## state介紹

1. MenuState :
在這個state用戶可以輸入指令(1)help 查詢指令 (2)chat 跟chatGPT聊天 (3) search 爬蟲圖片

2. chatGPT state :
在這個state可以跟chatGTP聊天 如圖:

![](https://imgur.com/a/jmRAtnZ)

我是利用註冊openai拿到token以後就可以自由跟他對話了，只要把返回的message送到line bot即可。
以下是我的部分程式碼：

```
def on_enter_chatGPTresponse(self, event):
        print("I'm entering ChatGPT response")

        text = event.message.text
        response = self.api.send_message(text)
        reply_token = event.reply_token
        send_text_message(reply_token, response["message"])
        self.go_back_chatGPT()
```

3. search state :
只要輸入的字句以.jpg做結尾，機器人呼叫google的api幫忙爬蟲，但是免費的帳號最多一個月只能爬蟲100次:

![](https://imgur.com/a/sulAALm)

以下是我的程式碼:

```
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
```

4. help state :
當輸入help的話就會輸出提示訊息:

![](https://imgur.com/a/DPe6qp0)

有任何問題歡迎寄信到我的信箱詢問!
email:f64096198@gs.ncku.edu.tw