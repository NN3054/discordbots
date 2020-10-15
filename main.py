import discord
import csv
from matplotlib import style
style.use("fivethirtyeight")

print(discord.__version__)

token = open("token.txt", "r").read()
client = discord.Client()

# variables
# sponsorcodevariable (placeholder)
sponsorcode = 0

# channels variable
commandschannel = 725239550946836522  # commandschannelID
logschannel = 701500381087137802  # logschannelID

# userid variables for whitelist
NN = 315205903282339840  # USERID of NN
Test_nn = 657731227687845918  # USERID of Test_nn

# server ID where the bot is used
serverid = 698161014230745129


# lists
# liste mit userIDs der User welche Berechtigung haben den !code command auszuführen
whitelist = [str(NN), str(Test_nn)]
# liste mit channelIDs in welchen der !code command ausgeführt werden darf
channellist = [str(commandschannel)]


# check if user input is an integer -> no random text input
def iscodeint(s):
    try:
        int(s)
        return True

    except ValueError:
        return False

# check if user input is 7 digits (only valid codes have 7 digits)


def iscode7digits(x):
    if len(x) == 7:
        try:
            return int(x)
        except ValueError:
            return False


# check if userid who executed the command is in the whitelist
def is_id_in_whitelist(list, search):
    for i in range(len(list)):
        if list[i] == search:
            return True

        elif i not in range(len(list)):
            return False

# check if channelid is in the channellist


def is_channelid_in_channellist(list, search):
    for j in range(len(list)):
        if list[j] == search:
            return True

        elif j not in range(len(list)):
            return False

# event that happens when there is a user input with a pre-defined expected value


def check_all(channellist, channelid,  whitelist, authorid):

    return is_channelid_in_channellist(channellist, str(channelid)) and is_id_in_whitelist(whitelist, str(authorid))


@client.event
async def on_message(message):

    # global variables

    global sponsorcode
    global whitelist

    # local variables for easier usage

    authorid = message.author.id
    authorname = message.author.name
    channelid = message.channel.id
    testserver = client.get_guild(serverid)

    # membercount of the server

    if "!membercount" == message.content.lower():
        await message.channel.send(f"```{testserver.member_count}```")

    # add user to whitelist so he can execute commands
    elif message.content.startswith("!addwl"):

        if check_all(channellist, channelid, whitelist, authorid):
            userinfo = message.content[7:]
            whitelist.append(str(userinfo))
            await message.channel.send(f'```Id {userinfo} has been added to the whitelist```')
            print(whitelist)

        else:
            await message.channel.send("```Seems like you do not have the permissions to perform this command```")

    # safe code + user ID by !code input in csv "usercodes"

    elif message.content.startswith("!code"):
        # ignore the first 6 digits of the input
        sponsorcode = message.content[6:]

        # check if the channelID of the channel in which the !code command got written is on the allowed channellist
        # check if the userID who wrote the !code is on the whitelist
        if check_all(channellist, channelid, whitelist, authorid):

            # check if the input after !code is 7digits long as well as numbers(int)
            if iscode7digits(sponsorcode) and iscodeint(sponsorcode):

                authorid = str(authorid)
                with open("usercodes.csv", "a") as uc:
                         uc.write(f"{sponsorcode};'{authorid}; {authorname}\n")
                await message.channel.send(f'```The sponsorcode {sponsorcode} of the User {authorname} (id={authorid}) has been saved successfully```')

            # if the input after !code is no integer and 7 digits long, send this error message
            else:
                await message.channel.send("```Your input is incorrect, please try again (format: !code <yourcode>)``` ")

        elif authorid not in whitelist:
                await message.channel.send(f"```You are not allowed to use that command or you are in the wrong channel \n If you think that is an error please contact an admin```")

        # with an unknown error, send this message

        else:
            await message.channel.send("`Unknown Error, please contact an Admin`")

    # output the all codes

    elif message.content.startswith("!getallcodes"):

        if check_all(channellist, channelid, whitelist, authorid):

            with open('usercodes.csv', newline='') as myFile:
                reader = csv.reader(myFile)
                for row in reader:
                    await message.channel.send(row)
                    print(row)

    # logout the bot

    elif "!close" == message.content.lower():
        if check_all(channellist, channelid, whitelist, authorid):
             await client.close()

# start the bot
client.run(token)
