class Game1(_DominionsGame):
    name = 'Game1'
    prefix = ':yin_yang: '

class Game2(_DominionsGame):
    name = 'Game2'
    prefix = ':star: '

class Channel1(_DiscordChannel):
    webhook = 'https://discordapp.com/api/webhooks/EXAMPLE/EXAMPLE'
    games = [Game1, Game2]
