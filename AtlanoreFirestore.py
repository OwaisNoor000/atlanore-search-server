import firebase_admin
from firebase_admin import credentials, firestore
from google.api_core.exceptions import NotFound
from threading import Lock

class AtlanoreFirestore():

    def __init__(self,db):
        self.db=db
        self.lock = Lock()

    def persistColorSearch(self,datetime,color,response):
        
        try:
            collection = "color-search"

            col_exists = False
            
            self.lock.acquire()
            for col in self.db.collections():
                if col.id == collection:
                    col_exists = True
                    break
            self.lock.release()

            if not col_exists:
                print("collection does not exist")
                return -1
            
            data = {
                "datatime":datetime,
                "color":color,
                "response":response
            }

            self.lock.acquire()
            self.db.collection(collection).add(data)
            self.lock.release()
            print("Color search successfully added to firestore")
        except Exception as e:
            print("Failed to add color search to firestore:")
            print(e)
        # finally:
            # firebase_admin.delete_app(firebase_admin.get_app())

    def persistFeelingSearch(self,datetime,search,result):
        
        try:
            collection = "feeling-search"

            col_exists = False

            self.lock.acquire()
            for col in self.db.collections():
                if col.id == collection:
                    col_exists = True
                    break
            self.lock.release()

            if not col_exists:
                print("collection does not exist")
                return -1
            
            data = {
                "datatime":datetime,
                "search":search,
                "result":result
            }
            self.lock.acquire()
            self.db.collection(collection).add(data)
            self.lock.release()

            print("Color search successfully added to firestore")
        except Exception as e:
            print("Failed to add color search to firestore:")
            print(e)
        # finally:
        #     firebase_admin.delete_app(firebase_admin.get_app())

    def persistChatbotQuery(self,datetime,session_id,query,response):
        
        try:
            collection = "chatbot-query"

            col_exists = False
            self.lock.acquire()
            for col in self.db.collections():
                if col.id == collection:
                    col_exists = True
                    break
            self.lock.release()

            if not col_exists:
                print("collection does not exist")
                return -1
            
            data = {
                "datatime":datetime,
                "session_id":session_id,
                "query":query,
                "response":response
            }
            self.lock.acquire()
            self.db.collection(collection).add(data)
            self.lock.release()
            
            print("Color search successfully added to firestore")
        except Exception as e:
            print("Failed to add color search to firestore:")
            print(e)
        # finally:
        #     firebase_admin.delete_app(firebase_admin.get_app())
        
# AFS = AtlanoreFirestore()
# AFS.persistChatbotQuery("2025-02-13 23:06:07-58","NC9843NF989R9","Do you have any colorful socks","*recommends socks*")