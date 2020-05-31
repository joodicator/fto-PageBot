import dominions
import util
import urllib2
import json

link, install, uninstall = util.LinkSet().triple()

USER_AGENT = 'PageBot (https://github.com/joodicator/pagebot, 1.0)'

conf = util.fdict('conf/dominions_discord.py')

class DiscordFormatter(dominions.TextFormatter):
    @staticmethod
    def bold(text):
        return '**%s**' % text

@link('dominions.new_turn_report')
def h_new_turn_report(bot, report, prev_report):
    for channel in conf.itervalues():
        if report.name not in channel['games']: continue
        message = report.show_diff_text(prev_report, DiscordFormatter)
        urllib2.urlopen(urllib2.Request(
            url=channel['webhook'],
            data=json.dumps({'content': message}),
            headers={'User-Agent': USER_AGENT, 'Content-Type': 'application/json'}
        ))
