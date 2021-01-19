from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random
import os
import winsound

api_id = 2673392 #Enter Your 7 Digit Telegram API ID.
api_hash = '8471e5f5f3ac2fad2d4553a16d8d8cc5'   #Enter Yor 32 Character API Hash
phone = '+34 650 662 192'   #Enter Your Mobilr Number With Country Code.
SLEEP_TIME = 120

def authclient(client):
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter verification code: '))
    print("Connected")

def getgrups(client):
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

    result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
    chats.extend(result.chats)
 
    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    return groups

def printgroups(groups):
    print('To Which Group You Want to Add Members:')
    i=0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i+=1

def addmembers(input_file, target_group_entity, client):
    membersadded = 0
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            try:
                print ("Adding {}".format(row[3]))
                user_to_add = InputPeerUser(int(row[1]), int(row[2]))
                client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                membersadded +=1
                time.sleep(random.randrange(90, 120)) # You can't send more than 19 request over 30 minuts
            except PeerFloodError:
                print("Getting Flood Error from telegram. They caught you.")
                print("Added: "+str(membersadded)+" members")
                winsound.Beep(2500, 30000)
                break
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping.")
                time.sleep(random.randrange(0, 5))
            except:
                traceback.print_exc()
                print("Unexpected Error")
                continue

def main():
    printtitle()
    client = TelegramClient(phone, api_id, api_hash)
    authclient(client)
    groups = getgrups(client)
    printgroups(groups)
    g_index = input("Please, enter your selection: ")
    target_group=groups[int(g_index)]
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
    print(target_group_entity)
    for entryfile in os.listdir("./sreleoutput/"):
        addmembers("./sreleoutput/"+entryfile, target_group_entity, client)


def printtitle():
    print ("")
    print ("++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++")
    print ("+  ____                                    ____ _           _    _         + ")
    print ("- / ___|  __ _ _ __ ___   ___  ___ _ __   / ___| |__   ___ | | _| |_   _   -  ")
    print ("+ \___ \ / _` | '_ ` _ \ / _ \/ _ \ '__| | |   | '_ \ / _ \| |/ / | | |    + ")
    print ("-  ___) | (_| | | | | | |  __/  __/ |    | |___| | | | (_) |   <| | |_| |  -  ")
    print ("+ |____/ \__,_|_| |_| |_|\___|\___|_|     \____|_| |_|\___/|_|\_\_|\__, |  +  ")
    print ("-                                                                  |___/   -  ")
    print ("++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++")
    print ("++++++---++++++++++++----Edited by radurulf----++++---++++++++++++---++++++")
    print ("")

if __name__ == "__main__":
    main()