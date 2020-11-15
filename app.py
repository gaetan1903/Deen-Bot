import sys
from gaetanbot import *
from threading import Thread
from fnmatch import fnmatch
from youtubesearchpython import searchYoutube


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
                    # bot.persistent_menu(recipient_id, "PUT")
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

    if val[0] == 'MUSIQUE':
        pass
    elif val[0] == 'LISTEN':
        pass
    elif val[0]== 'DOWNLOAD':
        pass
    

if __name__ == "__main__":
    app.run()
