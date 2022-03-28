import discord
import requests
import json
import random

client = discord.Client()
client.guessCount = 0
client.word = ""
print(client.word+"||")

client.unusedLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                        'n','o','p','q','r','s','t','u','v','w','x','y','z']
client.goodLetters = []
client.badLetters = []
client.activeGame = False
client.wordLength = 0


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def update_list(letter, present):  # 0 == no, 1 == exists in word
    if letter in client.unusedLetters:
        client.unusedLetters.remove(letter)

        if present == 0:
            client.badLetters.append(letter)
        elif present == 1:
            client.goodLetters.append(letter)


@client.event
async def on_message(message):
    msg = message.content
    response = ""
    ltrsRight = 0

    #print(str(msg.startswith("$guess"))+"|||"+str(client.word)+"|||"+str(client.wordLength)+"|||"+str(client.activeGame))

    if msg.startswith("$newGame"):
        client.wordLength = msg[9:10]

        if int(client.wordLength) == 4 or int(client.wordLength) == 5 or int(client.wordLength) == 7:
            file = open(client.wordLength + 'words.txt')
            client.wordList = file.readlines()

            wordNum = random.randint(0, 3130)
            client.word = client.wordList[wordNum]
            client.word = client.word[0:int(client.wordLength)]
            client.word = client.word.lower()
            client.activeGame = True
            print("WORD: " + client.word + " line num = 1+" + str(wordNum))
            await message.channel.send("Starting game of word size " + client.wordLength)
            client.guessCount = 0
        else:
            await message.channel.send("Please format your request as: '$newGame [either 4,5 or 7]'")


    elif msg.startswith("$guess") and len(client.word) == int(client.wordLength) and client.activeGame:
        #print("YES!")
        if len(msg) != 7+int(client.wordLength):
            await message.channel.send("Guess not proper size '$guess [5 letter word]'")
        else:
            guess = msg[7:7+int(client.wordLength)]
            for i in range(0,int(client.wordLength)):
                anyMatch = False

                for j in range(0,int(client.wordLength)):
                    #print(client.wordLength+"|"+guess[i] + "|" + client.word[j])
                    if guess[i] == client.word[j]:
                        anyMatch = True

                if guess[i] == client.word[i]:
                    response += "\U0001F7E9"
                    ltrsRight += 1
                    update_list(guess[i],1)
                elif anyMatch:
                    response += "\U0001F7E8"
                    update_list(guess[i],1)
                else:
                    response += "\U0001F7E5"
                    update_list(guess[i],0)

            client.guessCount += 1

            await message.channel.send("Guess #"+str(client.guessCount)+"/10: "+response)
            await message.channel.send("Included Letters: " + str(client.goodLetters))
            await message.channel.send("Missing Letters: " + str(client.badLetters))
            await message.channel.send("Unknown Letters: " + str(client.unusedLetters))

            #print(str(ltrsRight)+"vs"+str(client.wordLength)+"%"+str(client.guessCount))
            if int(ltrsRight) == int(client.wordLength):
                #print("yay")
                await message.channel.send("You guessed the word in "+str(client.guessCount)+" attempts.")
                client.activeGame = False
                client.guessCount = 0

        if int(client.guessCount) >= 10:
            await message.channel.send("Out of guesses")
            await message.channel.send("=====================================================")
            client.activeGame = False

# 2. double letters and square colors
# 6. upload bot to server
# 7. new modes: longer words, different word lists
# 8. AFTER THAT: upload to github and build a new bot
# 9. only guess acutally words
# 10. ability to see instructions for the bot


client.run("OTU2Njk5NTk3MTY4ODY5NDI2.Yj0B7g.V7IPq0rTV02rPtIgecQQqbigei8")