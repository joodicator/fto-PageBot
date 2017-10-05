

import datetime

import util
import identity
import channel
import tell

link, install, uninstall = util.LinkSet().triple()
install, uninstall = util.depend(install, uninstall,
    'identity', 'tell')

identity.add_credentials('quora.Bruce',
    ('hostmask', 'Bruce!*@*'),
    ('hostmask', 'Bro*ose!*@*'),
    ('access', 'Bruce'),
    ('prev_hosts', 3))

notify = (
    ('#fto', 'Bruce/Bro*ose', 'quora.Bruce'),
)

@link('QUORA_POST')
def h_quora_post(bot, chan, question):
    for nchan, to_nick, a_name in notify:
        if nchan.lower() != chan.lower(): continue
        c_nicks = map(str.lower, channel.track_channels[chan])
        if to_nick.lower() in c_nicks: continue
        n_nicks = yield identity.enum_access(bot, a_name)
        if any(n.lower() in c_nicks for n in n_nicks): continue

        bot_id = yield identity.get_id(bot, bot.nick)

        tell_state = tell.get_state()
        tell_state.msgs.append(tell.Message(
            time_sent = datetime.datetime.utcnow(),
            channel   = nchan,
            from_id   = bot_id,
            to_nick   = to_nick,
            message   = question.text))
        tell.put_state(tell_state)
