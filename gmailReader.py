import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email

class GmailReader():
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
    
    #TODO Expand out query for date, confirm its orange theory info
    def getUnreadMessageIds(self):
        response = self.service.users().messages().list(userId='me', q="label:unread").execute()
        messageIds = [x['id'] for x in response['messages']]
        return messageIds
    
    #TODO if we get succesfully  set messages to be true
    def getMessageById(self, mId):
        return self.service.users().messages().get(userId='me', id=mId, format='raw').execute()

    def getUnreadMessages(self):
        messages = []
        ids = self.getUnreadMessageIds()
        for mId in ids:
            rawMessage = self.getMessageById(mId)
            messages.append(self.convertMessageToText(rawMessage))
        return messages

    def convertMessageToText(self, message):
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ascii'))
        mime_msg = email.message_from_bytes(msg_str)
        payload = mime_msg.get_payload()
        if len(payload) > 1:
            ret = payload[1].get_payload()
            return ret
        else:
            ret = payload[0].get_payload()
            return ret[0].get_payload()


if __name__ == "__main__":
    gmail = GmailReader()
    messages = gmail.getUnreadMessages()