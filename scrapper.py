from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv


api_id =  #Enter Your 7 Digit Telegram API ID.
api_hash = ''   #Enter Yor 32 Character API Hash
phone = ''   #Enter Your Mobilr Number With Country Code.

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
    count = 0
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
            count+=1
            groups.append(chat)
        except:
            continue
    return groups, count

def printgroups(groups):
    print('From Which Group Yow Want To Scrap A Members:')
    i=0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i+=1
    print(str(i) + '- All')

def getmembers(client, target_group):
    print('Fetching Members...')
    return client.get_participants(target_group, aggressive=True)

def savefile(all_participants, target_group):
    print('Saving In file...')
    try:
        with open(""+target_group.title+".csv","w",encoding='UTF-8') as f: # Output data directory
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
            for user in all_participants:
                if user.username:
                    username= user.username
                else:
                    username= ""
                if user.first_name:
                    first_name= user.first_name
                else:
                    first_name= ""
                if user.last_name:
                    last_name= user.last_name
                else:
                    last_name= ""
                name= (first_name + ' ' + last_name).strip()
                writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
        print('Members scraped successfully.......')
        print('Happy Hacking......')
    except:
        pass

def main():
    printtitle()
    client = TelegramClient(phone, api_id, api_hash)
    authclient(client)
    groups, count = getgrups(client)
    printgroups(groups)
    g_index = input("Please, enter your selection: ")
    print(g_index)
    print(count)
    for i in range(int(g_index)+1):
        if (count != int(g_index) and i != int(g_index)):
            continue
        if i == count:
            print("break")
            break
        target_group=groups[i]
        participants = getmembers(client, target_group)
        savefile(participants,  target_group)

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
