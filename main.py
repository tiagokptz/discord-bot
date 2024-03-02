import discord
import asyncio
from discord.ext import commands
from music_cog import music_cog


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
i = 1

#evento de inciação do bot
@bot.event
async def on_ready():
    print(f'Estou pronto. Estou conectado como {bot.user}')
    await bot.add_cog(music_cog(bot))


#evento que adiciona um cargo e envia uma mensagem todas as vezes que entrar alguem novo
@bot.event
async def on_member_join(member):
    image_url = 'https://cdn.discordapp.com/attachments/705422207744081931/1145871206613004308/mario_rpg.jpg'
    channel = bot.get_channel(1144263671422406799)
    starter_role = member.guild.get_role(1144265779647365180)
    if starter_role is not None:
        await member.add_roles(starter_role)
        print(f'{member} recebeu o cargo {starter_role.name}')
        embed = discord.Embed(
            title=f'Bem-vindo {member.name}!',
            description='Reaja a mensagem para enviar a solicitação.',
            color=15105570
        )
        embed.set_author(name='Canal do Estreito', icon_url='https://cdn.discordapp.com/emojis/1063905436429975693.webp?size=128&quality=lossless')
        embed.add_field(name='O presidente irá analisar seu caso.', value='')
        embed.set_image(url=image_url)
        message = await channel.send(embed=embed)
        await message.add_reaction('👍')


#manda para uma mensagem de solicitação para o canal de solicitação
@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    welcome_channel_id = 1144263671422406799
    member = reaction.message.guild.get_member(user.id)
    request_channel_id = 1144656317135470604
    request_channel = bot.get_channel(request_channel_id)
    if str(reaction.emoji) == '👍' and member.bot == False and channel.id == welcome_channel_id:
        image_url = 'https://i.pinimg.com/564x/6e/47/d3/6e47d31045dec9d2671c8df0004043e1.jpg'
        print(f'{member} reagiu {reaction.emoji}')
        embed = discord.Embed(
            title=f'{user.name} enviou uma solicitação!',
            description='Devo deixa-lo participar?',
            colour=15105570
        )
        embed.set_author(name='Canal do Estreito', icon_url='https://cdn.discordapp.com/emojis/1063905436429975693.webp?size=128&quality=lossless')
        embed.set_image(url=image_url)
        message = await request_channel.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')
        await reaction.message.delete()
        await asyncio.sleep(3)
        await channel.purge(limit=None)
    #aqui o bot reconhece se o pedido foi aceito ou negado, se foi aceito ele da um novo cargo senão ele bane
    elif channel.id == request_channel_id and not user.bot:
        starter_role = member.guild.get_role(1144265779647365180)
        final_role = member.guild.get_role(696036017832198274)
        if str(reaction.emoji) == '👍':
            print(f'{user.name} confirmou a entrada.')
            list = bot.get_channel(1144263671422406799)
            users = list.members
            user = users[-1]
            await user.add_roles(final_role)
            await user.remove_roles(starter_role)
            await reaction.message.delete()
            await asyncio.sleep(3)
            await channel.purge(limit=None)

        elif str(reaction.emoji) == '👎':
            print(f'{user.name} negou a entrada.')
            list = bot.get_channel(1144263671422406799)
            users = list.members
            user = users[-1]
            await user.guild.ban(user, reason='Pedido negado')
            await reaction.message.delete()
            await asyncio.sleep(3)
            await channel.purge(limit=None)

@bot.command(name='oi')
async def send_hi(ctx):
    await ctx.send(f'iai, {ctx.author.name} como posso ajudar?')


@bot.command(name='change', aliases=["c"])
async def change_name_channel(ctx, name):
    try:
        new_name = "🎮Jogando: " + name + "👾"
        chat_channel = ctx.author.voice.channel
        voice_channel_jogando = 1149337091386392618
        if chat_channel.id == voice_channel_jogando:
            await chat_channel.edit(name=new_name)
            await ctx.send(f"Nome do canal foi alterado para {new_name}.")
        else:
            await ctx.send(f"Esse comando só funciona para o canal 🎮Jogando: 👾.")

    except AttributeError:
        await ctx.send(f"{ctx.author} você precisa estar conectado em um canal de voz para executar esse comando.")


bot.run("TOKEN")
