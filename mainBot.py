from flask import Flask, request
from pymessenger.bot import Bot
import random
app = Flask(__name__)
ACCESS_TOKEN = 'EAAGdGnNJHfABAFJAVckbJKSt16MFh14VyARtHXaErCmhczHs17iJjIYMsAPRub5gnQTE2fpahTEmP5DoO4hC0xKQ2AA4dmWHxrlfC9t98oSisO47mZC7hvmfdYGDncGgSHUX81QLo7AM3ojJAlk0LoSTB26P9EBhGN4F2bAZDZD'
VERIFY_TOKEN = 'maiverifai'
bot = Bot(ACCESS_TOKEN)

class vocab:
    definition = 'hello world'
    word = []
    
    def __init__(self, definition, word):
        self.word = word
        self.definition = definition

def send_definition(sender_ID, Index):
    global subWordList
    bot.send_text_message(sender_ID, 'Enter the definition of the following word, prefix or suffix: ' + subWordList[Index].definition)
    return "success"

def check_word(sender_ID, Index, word):
    global subWordList
    stringtong = ""
    for string in subWordList[Index].word:
        stringtong += string + ", "
    stringtong = stringtong[:-2]
    for string in subWordList[Index].word:
        if word == string:
            bot.send_text_message(sender_ID, "Your definition was CORRECT. The full definition of " + subWordList[Index].definition + " is " + stringtong)
            return 'naisu'
    bot.send_text_message(sender_ID, "Your definition was INCORRECT. The full definition of " + subWordList[Index].definition + " is " + stringtong)
    return 'nope'

@app.route('/', methods = ['GET', 'POST'])
def messageProcessing():
    if request.method == 'GET':
        token_sent = request.args.get('hub.verify_token')
        return tokenVerify(token_sent)
    if request.method == 'POST':
        print('calleh')
        global subWordList
        global index, state
        output = request.get_json()
        for Entry in output['entry']:
            messaging = Entry['messaging']
            for Message in messaging:
                sender_ID = Message['sender']['id']
                if  Message['message'].get('text') or Message['message'].get('attachments') or index < len(subWordList):
                    if index == -1:
                        bot.send_text_message(sender_ID, 'Weocom tu app do` bai` sinh. enter anything tu start')
                        index += 1
                    else:
                        if state == 0:
                            #send the definition
                            send_definition(sender_ID, index)
                            state = 1
                        else:
                            #check the word entered and send following definition
                            check_word(sender_ID, index, ((Message['message'].get('text')).lower()))
                            index += 1
                            if (index >= len(subWordList)):
                                index = len(subWordList) - 1
                            send_definition(sender_ID, index)
                #out of words
                if index == len(subWordList) - 1:
                    bot.send_text_message(sender_ID, 'Datz it. continue if you wan tu ritri')
                    index = -1
                    random.shuffle(subWordList)


        return 'Message Processed'
                


def tokenVerify(token_sent):
    if (token_sent) == VERIFY_TOKEN:
        print('naisu')
        return request.args.get('hub.challenge')
    return 'nope'



if __name__ == "__main__":
    global subWordList
    global index, state
    index = -1
    state = 0
    subWordList = []

    #getting words from list
    f = open("subWordList.txt", 'r')
    i = 1

    for line in f:
        linez = line.lower()
        linez = line.replace(" ", "")
        linez = line.replace("\n", "")
        if linez == '':
            i = 1
        else:
            if (i == 1):
                i = 0
                subWordList.append(vocab(linez, []))
                print('1 ' + linez)
            else:
                subWordList[-1].word.append(linez)
                print('0 ' + linez)
    #randomizing
    random.shuffle(subWordList)

    f.close()
    app.run()