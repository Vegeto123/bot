import discord
import time
import asyncio
import keep_alive
messages = joined = 0
client = discord.Client()

@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("vegeto") > 0:
            last = before.nick
            if last:
               await after.edit(nick="STOP")
            else:
               await after.edit(nick="NO_STOP")

@client.event
async def on_member_join(member):
    global  joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""bienvenue dans le serveur! {member.mention}""")

async def help_up():
    await client.wait_until_ready()
    while not client.is_closed():
        ch = client.get_channel(662356263988101171)
        embed = discord.Embed(title="help pou le BOT", description="commands utile")
        embed.add_field(name=".salut", value="dis bonjour")
        embed.add_field(name=".utilisateur", value="montre le nombre de membres")
        embed.add_field(name=".clear >nb", value="suprime nb messages")
        embed.add_field(name=".idée", value="propose une idée enregistrée")
        embed.add_field(name=".role >nom_utilisateur>role", value="change le role de l'utilisateur")
        embed.add_field(name="mmm", value="ceci est un message automatique envoyer toutes les 30 minutes")
        await ch.send(content=None, embed=embed)
        await asyncio.sleep(1800)

async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stat.txt", "a" )as f:
                f.write(f"time: {int(time.time())}, messages: {messages}, members joined {joined} \n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


@client.event
async def on_message(message):
    global messages
    messages += 1
    id = client.get_guild(660436752972120094)
    channels = ['bot_test']
    valid_users = ["vegeto123#2965",'first_bot#4928 ','DeusExImperator#1392']
    if str(message.author) != 'first_bot#4928':
        bad_words = ["tg","fdp","con","salopard","ordure","merde",'nike',"put"]
        for word in bad_words:
            if message.content.lower().count(word) > 0:
                await message.channel.purge(limit=1)
                await message.channel.send(f"un mauvais mot a été dit par {message.author}")
        if message.content.find('.clear') != -1 and str(message.author) == 'vegeto123#2965':
            m = message.content
            m = m.split('>')
            if m[-1].isnumeric():
                await message.channel.purge(limit=int(m[-1]))
            else:
                await message.channel.send('.clear >nb_de_message_a_suprimé')

        if message.content.find('.reset') != -1 and str(message.author) == 'vegeto123#2965':
            for mbr in id.members:

                if mbr.name == 'matheo':

                    test = discord.utils.get(mbr.guild.roles, name="ainé")
                    await  mbr.edit(roles=[test], nick = 'matheo')
        if message.content.find('.punition') != -1 and str(message.author) == 'vegeto123#2965':
            for mbr in id.members:
                if mbr.name == 'matheo':
                    test = discord.utils.get(mbr.guild.roles, name="intru")
                    await  mbr.edit(roles=[test], nick='PUNI')



        if str(message.author) == 'matheo#1953' and str(message.channel) in channels:
            await message.channel.send("mathéo n'est pas accépter ici !!!\n tu vas etre punis!!\ntu est un intru maintenant !!" )
            await message.author.edit(nick ='PUNITION')
            member = message.author
            test = discord.utils.get(member.guild.roles, name="intru")
            await  member.edit(roles=[test])

        if str(message.channel) in channels and str(message.author) in valid_users:

            if message.content == ".help":
                embed = discord.Embed(title="help pou le BOT", description="commands utile")
                embed.add_field(name=".salut", value="dis bonjour")
                embed.add_field(name=".utilisateur", value="montre le nombre de membres")
                embed.add_field(name=".clear >nb", value="suprime nb messages")
                embed.add_field(name=".idée", value="propose une idée enregistrée")
                embed.add_field(name=".role >nom_utilisateur>role", value="change le role de l'utilisateur")
                await message.channel.send(content=None, embed=embed)


            if message.content.find('.salut') != -1:
                await message.channel.send('bonjour')

            elif message.content == '.utilisateur':
                await message.channel.send(f"""{id.member_count} membres""")

            elif message.content.find('.clear') != -1:
                m = message.content
                m = m.split('>')
                if m[-1].isnumeric():
                    await message.channel.purge(limit=int(m[-1]+1))
                else: await message.channel.send('.clear >nb_de_message_a_suprimé')
            if message.content.find('.idée') != -1:
                try:
                    with open("ide.txt", "a")as f:
                        f.write(f" idée :{message.content}\n")
                        await message.channel.send("idée recue ps: tout est enregistré")
                except Exception as e:
                    print(e)
            if message.content.find('.role') != -1:
                m = message.content
                m = m.split('>')
                for mbr in id.members:
                    if mbr.name == m[-2]:
                        test = discord.utils.get(mbr.guild.roles, name=m[-1])
                        await  mbr.edit(roles=[test])
client.loop.create_task(help_up())
client.loop.create_task(update_stats())
keep_alive.keep_alive()

client.run('NjYyMzU3OTY3MDg0OTc4MTk1.Xg8zbg.MdDgUKsG9s15VSytNyfnZixQ7Sc')