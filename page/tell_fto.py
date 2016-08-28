import util
import identity

from untwisted.magic import sign

link = util.LinkSet()
installed = False

identity.add_credentials('tell.father',
    ('access', 'Bruce'),
    ('prev_hosts', 3))

def install(bot):
    global installed
    if installed: raise util.AlreadyInstalled
    util.event_sub(bot, 'TELL_SENT', 'tell_fto.TELL_SENT')
    link.install(bot)
    installed = True

def uninstall(bot):
    global installed
    if not installed: raise util.NotInstalled
    link.uninstall(bot)
    util.event_sub(bot, 'tell_fto.TELL_SENT', 'TELL_SENT')
    installed = False

install, uninstall = util.depend(install, uninstall,
    'identity', 'tell')

@link('TELL_SENT')
def h_tell_sent(bot, id, target, sent_msgs, reply_msg=None):
    father = yield identity.check_access(bot, id, 'tell.father')
    if father: reply_msg = 'Yes, father'
    yield sign('tell_fto.TELL_SENT', bot, id, target, sent_msgs, reply_msg)
