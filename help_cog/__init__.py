import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __int__(self, bot):
        self.bot = bot
        self.help_message = """
'''
Comandos gerais:
!help - Exibe todos os comandos disponíveis.
!play - Toca uma música selecionada do YouTube.
!pause - Pausa a música atualmente sendo reproduzida.
!resume - Continua a reprodução da música.
!skip - Pula a música atualmente sendo reproduzida.
!queue - Exibe as músicas atualmente na fila.
!clear - Para a música e limpa a fila.
!leave - Expulsa o bot do canal de voz.
'''
"""
        self.text_channel_list = []


    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

        await self.send_to_all(self.help_message)

    @commands.command(name='help', help='Exibe todos os comandos disponíveis.')
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)