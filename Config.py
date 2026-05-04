import os
import json
import base64
from dotenv import load_dotenv

class Config:

    def __init__(self) -> None:
        load_dotenv()

        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        self.CHAT_SALT = os.getenv('CHAT_SALT')
        self.prices_file = 'jsons/prices.json'
        self.chats_file = 'jsons/chats.json'
        self.dir = 'jsons'

        if not self.BOT_TOKEN:
            self.BOT_TOKEN = ''

        self.createJSON()

    def createDIR(self) -> None:
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def createJSON(self) -> None:
        self.createDIR()

        if not os.path.exists(self.prices_file):
            with open(self.prices_file, 'w') as gf:
                json.dump({"price": None, "time": None}, gf)

        if not os.path.exists(self.chats_file):
            with open(self.chats_file, 'w') as cf:
                json.dump({"chats_id": []}, cf)

    def encodeChat(self, chat_id):
        combined = f"{self.CHAT_SALT}:{chat_id}"

        return base64.b64encode(combined.encode()).decode()
    
    def decodeChat(self, encoded):
        try:
            decoded = base64.b64decode(encoded.encode()).decode()
            original_id = decoded.split(':', 1)[1]

            return int(original_id)
        
        except:
            return None


    def addChat(self, chat_id):
        chats = self.getChats()

        if chat_id not in chats:
            chats.append(chat_id)

            encoded_chats = [self._encode(cid) for cid in chats]
            with open(self.chats_file, 'w') as cf:
                json.dump({'chats_id': encoded_chats}, cf)
            
            return True

        return False
    
    def removeChat(self, chat_id):
        chats = self.getChats()
        
        if chat_id in chats:
            chats.remove(chat_id)
            with open(self.chats_file, 'w') as cf:
                json.dump({"chats_id": chats}, cf)

            return True
        
        return False


    def getChats(self) -> list:
        if os.path.exists(self.chats_file):
            with open(self.chats_file, 'r') as cf:
                chats = json.load(cf)

                return chats.get('chats_id', [])
        
        return []