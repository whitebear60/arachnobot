import asyncio
import copy

from twitchio import Context
from twitchio.ext import commands


@commands.cog()
class ElvenCog:
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

        s1 = "&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL;\"ZXCVBNM<>?`~"
        s2 = "?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ёЁ"
        self.trans = str.maketrans(s1, s2)

    @commands.command(name='translit', aliases=('translate', 'tr'))
    async def translit(self, ctx: Context):
        params = ctx.message.content.split()[1:]
        # print("translit(): ", params)
        if len(params) < 1 or len(params) > 2:
            return

        if len(params) == 1:
            try:
                count = int(params[0])
                author = ctx.author.name.lstrip('@')
            except ValueError:
                author = params[0].lstrip('@')
                count = 1
        else:
            author = params[0]
            count = int(params[1])

        # print(f"translit(): author {author}, count {count}")

        if self.last_messages.get(author, None) is None:
            asyncio.ensure_future(ctx.send(f"{author} ещё ничего не посылал!"))
            return

        if len(self.last_messages[author]) < count:
            count = len(self.last_messages[author])

        messages = copy.copy(self.last_messages[author])
        messages.reverse()

        res = ["Перевод окончен"]

        format_fields = ['', '', '']
        format_fields[0] = '' if count == 1 else str(count) + ' '
        format_fields[1] = 'ее' if count == 1 else 'их'
        format_fields[2] = {1: 'е', 2: 'я', 3: 'я', 4: 'я'}.get(count, 'й')

        for i in range(count):
            message = messages[i].translate(self.trans)
            res.append(f'{message}')

        res.append("Перевожу {0}последн{1} сообщени{2} @{author}:".format(*format_fields, author=author))

        for m in reversed(res):
            await ctx.send(m)