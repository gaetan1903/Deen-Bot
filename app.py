from threading import Thread
import os, re, sys, datetime, random
from flask import Flask, request, jsonify
import json, time
import requests, requests_toolbelt
from unidecode import unidecode
from messenger import Messenger

ID_ADMIN = "2967189363337819"
ACCESS_TOKEN = "EAAMnENRUnygBAEJOSdZClbfUCZB0nBIvWjMpvb5LOfcvyhL12qd7tkr68k9ZCUsEBZCsTNAJykhjVmiehtZBrLWOtDrVFmtxcr9mGoGbCM7Wlsu6ztRZB1JP9muHN242H5NbB3hCmbAiRGkGK6pjd8Ef6dnHmrjzpkiT0rddKdv7XQVMrQa5FZBnnJa3fjiZAVIZD"
VERIFY_TOKEN = 'jedeconne'


app = Flask(__name__)


bot = Messenger(ACCESS_TOKEN)



@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    elif request.method == "POST":
        body = request.get_json()
        proc = Execute(body)
        proc.start()

    return "receive", 200


class Execute(Thread):
    def __init__(self, body):
        Thread.__init__(self)
        self.body = body


    def run(self):
        for event in self.body['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    #bot.persistent_menu(recipient_id, "DELETE")
                    bot.persistent_menu(recipient_id, "PUT")
                    if message['message'].get('quick_reply'):
                        traitement_text(message['message'].get('quick_reply').get('payload'), recipient_id)
                    
                    elif message['message'].get('text'):
                        # response_sent_text = get_message()
                        traitement_text(message['message'].get('text'), recipient_id)


                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    pst_title = message['postback']['title']
                    pst_payload = message['postback']['payload']

                    
                    traitement_text(pst_payload, recipient_id)

                            
def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def traitement_text(msg, id):

    val = msg.strip().split()
    print(val)
    if val[0].upper() == 'MUSIQUE':
        print(bot.send_result_search(id).text)
    elif val[0] == 'LISTEN':
        print(bot.send_file(id, "audio", val[1]).text)
    elif val[0]== 'DOWNLOAD':
        print(bot.send_file(id, "file", val[1]).text)
    elif val[0].lower() == 'test':
        bot.send_message_text(id, "test reussi")
    
    


if __name__ == "__main__":
    app.run()
