from gaetanbot.__utils import *

class Messenger:
    def __init__(self, access_token):
        self.token = access_token
        self.url = "https://graph.facebook.com/v8.0/me"


    def __str__(self):
        """
            affichage du nom  du PAGE sur la classe
                                                    """
        params = {'fields': 'name', 'access_token': self.token}

        return "Messenger Bot: " + requests.get(self.url, params=params).json()['name']


    def send_message_text(self, destId, message):
        '''
            Cette fonction sert à envoyer une message texte
                à l'utilisateur en vue de répondre à un message
                                                                '''
        dataJSON = {
            'recipient':{
                "id": destId
            },

            'message':{
                "text": message
            }
        }

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}

        return requests.post(self.url + '/messages', json=dataJSON, headers=header, params=params)


    def send_result_search(self, destId):
        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient':{
                "id": destId
            },
            'message' : {
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"generic",
                        "elements": [
                            {
                                "title": "",
                                "image_url": "",

                                "subtitle": "",

                                "buttons":  [
                                    {
                                        "type":"postback",
                                        "title":"Ecouter",
                                        "payload": "LISTEN "
                                    },
                                    {
                                        "type":"postback",
                                        "title":"Télécharger",
                                        "payload": "MUSIQUE "
                                    },
                                ]
                            }
                        ], 
                    },
                },
                
            }
        }

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}

        return requests.post(self.url + '/messages', json=dataJSON, headers=header, params=params)


    def send_action(self, destId, action):
        if action not in ['mark_seen', 'typing_on', 'typing_off']:
            return None

        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient':{
                "id": destId
            },

            'sender_action': action
        }

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}

        return requests.post(self.url + '/messages', json=dataJSON, headers=header, params=params)


    def send_file(self, destId, file, type_="file", filename_=None):
        if filename_ is None: filename_ = file
        params = {
             "access_token": self.token
        }

        data = {
            'recipient': json.dumps( {'id': destId} ),

            'message': json.dumps({
                'attachment': {
                    'type': type_,
                    'payload': {
                        "is_reusable": True,
                    }
                }
            }),
            'filedata': (os.path.basename(filename_), open(f'data/{destId}/{file}', 'rb'), f"{type_}/{file.split('.')[-1]}")
        }

        # multipart encode the entire payload
        multipart_data = requests_toolbelt.MultipartEncoder(data)

        # multipart header from multipart_data
        header = {
            'Content-Type': multipart_data.content_type
        }

        return requests.post(self.url + '/messages', params=params, headers=header, data=multipart_data)



    def send_file_url(self, destId, filetype, url):
        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient':{
                "id": destId
            },

            'message': {
                'attachment' : {
                    'type' : filetype,
                    'payload' : {
                        "url": url,
                        "is_reusable": True
                    }
                }
            }
        }

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}

        return requests.post(self.url + '/messages', json=dataJSON, headers=header, params=params)



    def send_attachment(self, destId, type_, attachment_id):
        dataJSON = {
            'messaging_type': "RESPONSE",
            'recipient':{
                "id": destId
            },

            'message': {
                'attachment' : {
                    'type' : type_,
                    'payload' : {
                        'attachment_id' : attachment_id
                    }
                }
            }
        }

        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}

        return requests.post(self.url + '/messages', json=dataJSON, headers=header, params=params)

    

    def persistent_menu(self, destId, action):
        header = {'content-type' : 'application/json; charset=utf-8'}
        params = {"access_token" : self.token}
        if action == "PUT":
            dataJSON = {
                "psid": destId,

                "persistent_menu": [
                        {
                            "locale": "default",
                            "composer_input_disabled": False,
                            "call_to_actions": [
                                {
                                    "type": "postback",
                                    "title": "MUSIQUE",
                                    "payload": "MUSIQUE"
                                }
                            ]
                        }
                    ]
            }

            return requests.post(self.url + '/custom_user_settings', json=dataJSON, headers=header, params=params)

        elif action == "DELETE":
            params['params'] = "(persistent_menu)"
            params['psid'] = destId

            return requests.delete(self.url + '/custom_user_settings', headers=header, params=params)
        return None