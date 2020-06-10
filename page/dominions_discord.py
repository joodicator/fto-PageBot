import dominions
import util
import urllib2
import json

link, install, uninstall = util.LinkSet().triple()

CONF_PATH = 'conf/dominions_discord.py'
USER_AGENT = 'PageBot (https://github.com/joodicator/pagebot, 1.0)'

def required_class_attr(attr_name):
    def get_required_class_attr(self):
        raise util.UserError("Error: the '%s' attribute of %s subclasses in %s"
            " must be present." % (attr_name, type(self).__name__, CONF_PATH))
    return util.classproperty(get_required_class_attr)

class ConfEntry(object):
    pass

class DiscordChannel(ConfEntry):
    webhook = required_class_attr('webhook')

class DominionsGame(ConfEntry):
    name = required_class_attr('name')
    channel = required_class_attr('channel')
    prefix = ''
    suffix = ''

class DiscordFormatter(dominions.TextFormatter):
    @staticmethod
    def bold(text):
        return '**%s**' % text

conf = util.fdict(CONF_PATH, globals={
    '_DiscordChannel': DiscordChannel,
    '_DominionsGame': DominionsGame,
}, locals=None, class_dict=False)

@link('dominions.new_turn_report')
def h_new_turn_report(bot, report, prev_report):
    for game in conf.itervalues():
        if not issubclass(game, DominionsGame): continue
        if report.name != game.name: continue

        for channel in conf.itervalues():
            if not issubclass(channel, DiscordChannel): continue
            if game not in channel.games: continue

            message = report.show_diff_text(prev_report, DiscordFormatter)
            message = game.prefix + message + game.suffix
            urllib2.urlopen(urllib2.Request(
                url=channel.webhook,
                data=json.dumps({'content': message}),
                headers={
                    'User-Agent': USER_AGENT,
                    'Content-Type': 'application/json'
                },
            ))
