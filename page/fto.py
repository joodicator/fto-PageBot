# coding: utf8

from untwisted.magic import sign, hold

import re
import time
import random

from channel import not_quiet
import message
import channel
import runtime
import util
import limit

link, install, uninstall = util.LinkSet().triple()

#===============================================================================
@link('MESSAGE')
@not_quiet()
def h_message(bot, id, target, msg):
    if not target: return
    if limit.is_ignored(id): return
    yield sign('FTO_MSG', bot, target, msg)
    if bot.activity: limit.mark_activity(bot, id)

@link('PROXY_MSG')
@not_quiet()
def h_proxy_msg(bot, id, target, msg, **kwds):
    if not target.startswith('#'): return
    yield sign('FTO_MSG', bot, target, msg)

#===============================================================================
@link('FTO_MSG')
def h_fto_msg(bot, chan, msg):
    reply = lambda rmsg: bot.send_msg(chan, rmsg)
    strip_msg, cstrip_msg = strip(msg), cstrip(msg)
    sstrip_msg, csstrip_msg = sstrip(msg), csstrip(msg)

    #---------------------------------------------------------------------------
    # Nichijou Opening 2
    # http://www.youtube.com/watch?v=kZn7i9rg3a0
    if re.search(ur'j(ou?|ō)j(ou?|ō)y(uu?|ū)j(ou?|ō)banjimajikaich(ou?|ō)',
    strip_msg) and 'nana' not in strip_msg and u'なな' not in strip_msg:
        reply('Nanananananana!')

    #---------------------------------------------------------------------------
    # Rathergoodstuff - Agamemnon
    # http://www.youtube.com/watch?v=Kxp8qPEwSXM
    elif 'iammightyagamemnon' in strip_msg and 'legolambnon' not in strip_msg:
        reply('I am tasty Legolambnon!')

    elif 'isailedtotroywiththenavy' in strip_msg \
    and not re.search(r'taste great|spuds|gravy', sstrip_msg):
        reply('I taste great with spuds and gravy!')
    
    elif 'iamkingagamemnon' in strip_msg and 'legolambnon' not in strip_msg:
        reply('La la la la la la la la la Legolambnon!')
    
    elif re.search(r'i command all of the ar.*ives', sstrip_msg) \
    and 'roastmeup' not in strip_msg and 'gasmarkfive' not in strip_msg:
        reply('Roast me up at gas mark five!')
    
    elif 'allachaeansbowtome' in strip_msg and 'rosemary' not in strip_msg:
        reply('I taste great with rosemary-hee!')

    elif 'icommandmankillerachilles' in strip_msg \
    and 'withsomepeas' not in strip_msg:
        reply('Why not have me with some peas?')

    elif 'ispillentrailsofourtrojanfoe' in strip_msg \
    and not re.search(r'nice with|garlic|dont you know', sstrip_msg):
        reply("I'm nice with garlic, don't you know?")

    #---------------------------------------------------------------------------
    # 【MMD】With pleasant companions『Go!Go!Carlito!』【PV】
    # http://www.youtube.com/watch?v=1jJsYbVBnaE
    elif 'mewannayouwannaeverybodywanna' in strip_msg \
    and 'gogo' not in strip_msg:
        reply('\2Go! Go! Go!')

    elif re.search(r'whos(the|that)boy(wanna|wantto)beamigo', strip_msg) \
    and 'carlito' not in strip_msg:
        reply('\2Carlito! Carlito!')

    elif re.search(r'whos(the|that)boy(iwill|ill)neverletgo', strip_msg) \
    and 'carlito' not in strip_msg:
        reply('\2Carli-Carlito! Carli-Carlito!')

    elif re.search(r'whos(the|that)boycomeanddanceamigo', strip_msg) \
    and 'carlito' not in strip_msg:
        reply('\2Carlito! Carlito! Carli-Carlito!')

    elif re.search(r'whos(the|that)boytakeachanceonmenow', strip_msg) \
    and not re.search(ur'se[ñn]orita|carlita', strip_msg):
        reply(u'\2Eyy, Señorita, where you going? You wanna be my Carlita?!')

    elif (re.search(r'icansingandicandanceia?mveryniceandhotandspicy', strip_msg)
    and not any(s in strip_msg for s in ('ihavethelooks', 'cookataco'))):
        reply('I have the looks and I can cook a TACO!')

    #---------------------------------------------------------------------------
    # Dark Souls: The Wrath of the Darkwraith
    # http://www.youtube.com/watch?v=WqacyIaq27o
    elif 'DRIVEHARD' == cstrip_msg:
        reply('DRIVE MUSTANG.')
    
    elif 'drivehard' == strip_msg:
        reply('Drive Mustang.')

    elif 'drivehard' in strip_msg and 'drivemustang' in strip_msg:
        reply('Why are you doing this?')

    #---------------------------------------------------------------------------
    # The Hobbit (1977) - Down, Down to Goblin Town
    # http://www.youtube.com/watch?v=ogTDa-vG2MQ
    elif 'yougomylad' == strip_msg or 'belowmylad' == strip_msg:
        reply('Ho, ho! my lad!')

    #---------------------------------------------------------------------------
    # The Muppet Show - Mahna Mahna
    # http://www.youtube.com/watch?v=8N_tupPBtWQ
    elif re.match(r'(doo+[dt]?){4}', strip_msg) \
    and 'mana' not in msg and 'mahna' not in msg:
        reply('Mahna mahna!')

    #---------------------------------------------------------------------------
    # Puni Puni Poemi, Episode 2
    # http://www.youtube.com/watch?v=U-BwZA70ZCI#t=168
    elif 'bananabanana' in strip_msg:
        remaining = [
            'bananabanana', 'cucumber', 'eggplant', 'caviar', 'papaya',
             'giantasparagus']
        start = time.clock()
        while True:
            part = ''
            while remaining and part + remaining[0] in strip_msg:
                part += remaining.pop(0)

            if len(remaining) <= 1: break

            bot.activity = True
            while True:
                _, (e_bot, e_chan, msg) = yield hold(bot, 'FTO_MSG')
                strip_msg = strip(msg)
                if e_chan and e_chan.lower() == chan.lower(): break
            if time.clock() - start > 3600: return
            if 'bananabanana' in strip_msg: return

        if remaining: reply('\2GIANT ASPARAGUS!')

    #---------------------------------------------------------------------------
    # HEYYEYAAEYAAAEYAEYAA
    # http://www.youtube.com/watch?v=6GggY4TEYbk
    elif re.search(r'ands?hetries', strip_msg) and not any(s in strip_msg \
    for s in ('ohmygod', 'doitry', 'itryallthetime', 'inthisinstitution')):
        reply('Oh my god, do I try!')
        yield runtime.sleep(1)
        reply('I try all the time... in this institution!')
    
    elif re.search(r'ands?heprays', strip_msg) and not any(s in strip_msg \
    for s in ('ohmygod', 'doipray', 'iprayeverysingleday', 'revolution')) \
    and not re.search(r'[mn]y[ea]+', strip_msg):
        reply('Oh my god, do I pray!')
        yield runtime.sleep(1)
        reply('I pray every single day...')
        start = time.clock()
        while time.clock() - start < 60:
            (_, (e_bot, e_chan, msg)) = yield hold(bot, 'FTO_MSG')
            strip_msg = strip(msg)
            if not e_chan or e_chan.lower() != chan.lower():
                continue
            if 'andheprays' in strip_msg:
                return
            if re.search(r'[mn]y[ea]+', strip_msg):
                reply('\2...FOR REVOLUTION!')
                return

    #---------------------------------------------------------------------------
    # Murray Head - One Night In Bangkok
    # http://www.youtube.com/watch?v=xqZCGTe5ISQ
    elif ('onetownsverylikeanother' in strip_msg or
    'yourheadsdownoveryourpiecesbrother' in strip_msg) and not any(
    s in strip_msg for s in ('itsadrag', 'itsabore', 'itsreallysuchapity',
    'lookingattheboard', 'looking at the city')):
        reply("It's a drag, it's a bore, it's really such a pity"
        " to be looking at the board, not looking at the city!")

    elif re.search(r'(ya|you(ve)?)seen?onecrowdedpollutedstinking?town',
    strip_msg):
        reply('Tea, girls, warm and sweet (warm! sweet!),'
        ' some are set up in the Somerset Maugham suite!')

    elif ('andifyoureluckythenthegodsashe' in strip_msg 
    or 'alittlefleshalittlehistory' in strip_msg) and not any(s in strip_msg \
    for s in ('icanfeel', 'anangel', 'slidinguptome')):
        reply('I can feel an angel sliding up to me~')

    elif 'cantbetoocarefulwithyourcompany' in strip_msg and not \
    any(s in strip_msg for s in ('icanfeel', 'thedevil', 'walkingnexttome')):
        reply('I can feel the devil walking next to me~')

    elif re.search(r'dontseeyou.*r(at|8)i?ngthekindofm(ate|8).*'
    r'contempl(at|8)i?ng', strip_msg) and not any(s in strip_msg for s in
    ('idletyouwatch', 'iwouldinviteyou', 'thequeensweuse', 'wouldnotexciteyou')):
        reply("I'd let you watch, I would invite you,"
        " but the queens \2we\2 use would not excite you.")

    #---------------------------------------------------------------------------
    # Hanazawa Kana - Renai Circulation
    # http://www.youtube.com/watch?v=lWTuzLz1C6o
    elif re.match(ur's[eē]+no', strip_msg):
        write = [
            ('Se~ no',
            ur's[eē]+no'),
            ('Demo sonnanja dame',
            ur'demosonn?anjadame'),
            ('Mou sonnanja hora~',
            ur'm(ou?|ō)sonn?anjahora'),
            ('Kokoro wa shinka suru yo motto motto~',
            ur'kokoro[wh]ashinkasuruyomott?omott?o')]
        read = ''
        while write and re.match(read + write[0][1], strip_msg):
            read += write.pop(0)[1]
        if not re.match(read + r'$', strip_msg):
            return
        for line in write:
            reply(line[0])
            yield runtime.sleep(1)

    #---------------------------------------------------------------------------
    # The Fellowship of the Ring (2001) - The Council of Elrond
    # https://www.youtube.com/watch?v=pxPGzj2L3n0
    elif re.search(r'^(you have|and) my \S+'
    '|(you have|and) my \S+( \S+)?$', sstrip_msg):
        global and_my_axe
        try:
            if time.time() < and_my_axe.get(chan.lower()): return
        except NameError:
            and_my_axe = dict()
        and_my_axe[chan.lower()] = time.time() + 60

        while time.time() < and_my_axe[chan.lower()]:
            _, (e_bot, e_chan, e_msg) = yield hold(bot, 'FTO_MSG')
            if not e_chan or e_chan.lower() != chan.lower():
                continue
            if re.search(r'^and( you have)? my \S+'
            '|and( you have)? my \S+( \S+)?$', sstrip(e_msg)):
                reply('AND MY AXE!')
                break

    #---------------------------------------------------------------------------
    # Blackout Crew - Put A Donk On It
    # https://www.youtube.com/watch?v=ckMvj1piK58
    elif re.search('you know what you (wanna|want to) do with that( right)?$',
    sstrip_msg) and not re.search(r'put a|banging|donk', sstrip_msg):
        reply('You wanna put a \2banging donk\2 on it!')

    elif strip_msg == 'bassline':
        reply('Aw, wicked! Now put a donk on it!')

    elif strip_msg == 'electro':
        reply("Ah, that's sick that m8! Put a donk on it!")

    elif strip_msg == 'techno':
        reply("Aw, now that is good! Put a donk on it!")

    #---------------------------------------------------------------------------
    # Excel Saga, Episode 3 - Nabeshin's "No Escape"
    # https://www.youtube.com/watch?v=tORRPhqu1Co
    elif 'wherearewegoinggeneral' in strip_msg and \
    not re.search(r'dont have|special (reason|raisin)', sstrip_msg):
        reply("Who cares? We don't have a special raisin!")

    elif sstrip_msg.endswith('then why should we fly') and \
    not re.search(r'its just for|direction|low budget movie', sstrip_msg):
        reply("It's just for the direction of low-budget movie.")

    #---------------------------------------------------------------------------
    # Repo! The Genetic Opera - Zydrate Anatomy
    # https://www.youtube.com/watch?v=aVTAf4FAXaU
    elif sstrip_msg.endswith(' a little glass vial') and \
    len(re.findall(r'alittleglassvial', strip_msg)) == 1:
        reply('A little glass vial?')
    
    elif (sstrip_msg.endswith(' into the gun like a battery') or \
    re.search(r'against(your|my|his|her|their|its)anatomy$', strip_msg)) \
    and not re.search(r'\b([ah]{2,} [ah]{2,})\b', sstrip_msg):
        reply('Hah~ hah~')

    elif (sstrip_msg.endswith(' ready for surgery') or \
    sstrip_msg.endswith(' surgery') and re.search(r' S\S+$', csstrip_msg) and \
    len(re.findall(r'\b[A-Z]\S+', msg)) < len(re.findall(r'\b[a-z]\S+', msg))) \
    and len(re.findall(r'\bsurgery\b', sstrip_msg)) == 1:
        reply('Surgery!')

    elif sstrip_msg.endswith(' addicted to the knife') and \
    len(re.findall(r'addictedtotheknife', strip_msg)) == 1:
        reply('Addicted to the knife?')

    elif sstrip_msg.endswith(' a little help with the agony') and \
    len(re.findall(r'agony', strip_msg)) == 1:
        reply('Agony~')

    elif re.search(r'\b(its clear)\b', sstrip_msg):
        end_time = time.time() + 300
        remain = ["it's clear", "it's pure", "it's rare"]
        while remain:
            if 'takesyouthere' in strip_msg: return
            rstr = r'^.*?\b(%s)\b' % re.escape(sstrip(remain[0]))
            sub_msg = re.sub(rstr, '', sstrip_msg)
            if sub_msg != sstrip_msg:
                del remain[0]
                msg = sub_msg
            else:
                e_chan = ''
                while e_chan.lower() != chan.lower():
                    _, (e_bot, e_chan, msg) = yield hold(bot, 'FTO_MSG')
                    sstrip_msg = sstrip(msg)
                    if time.time() > end_time: return
                if re.search(r'\b(its clear)\b', sstrip_msg): return
                bot.activity = True
        else:
            reply('It takes you there~')

    #---------------------------------------------------------------------------
    # Azumanga Daioh, Episode 21 - Saataa Andaagii
    # https://www.youtube.com/watch?v=b6swokLgCcU
    elif re.search(r'sa+ta+ a+nda+gi+', sstrip_msg):
        global saataa_andaagii
        try:
            if time.time() < saataa_andaagii.get(chan.lower()): return
        except NameError:
            saataa_andaagii = dict()
        saataa_andaagii[chan.lower()] = time.time() + 300

        count = 1
        while count < 3:
            if time.time() > saataa_andaagii.get(chan.lower()): break
            _, (e_bot, e_chan, e_msg) = yield hold(bot, 'FTO_MSG')
            if e_chan.lower() != chan.lower(): continue
            if not re.search(r'sa+ta+ a+nda+gi+', sstrip(e_msg)): continue
            count += 1
            bot.activity = True
        else:
            reply('\2Saataa andaagii!')

    #---------------------------------------------------------------------------
    # 1-800-CONTACTS TV Advert - "Overly Dramatic Dramatization"
    # https://www.youtube.com/watch?v=f9YBwa0O1Zc
    elif ('your contact lenses just arrived' in sstrip_msg
    and 'my brand' not in sstrip_msg and 'special eyes' not in sstrip_msg):
        reply("1-800-CONTACTS? They can't have my brand! I have special eyes...")
    elif ('look with your special eyes' in sstrip_msg
    and 'my brand' not in sstrip_msg):
        reply("My brand!")

    #---------------------------------------------------------------------------
    # Christopher Lee - The Bloody Verdict of Verden
    # https://www.youtube.com/watch?v=cvKRbi2ovDY
    elif re.search(r'\bs(a(xon|hson|ssen|chsen|ksen|xe)|eaxe)', sstrip_msg) \
    and not re.search(r'\bblood\b', sstrip_msg):
        global saxon
        saxon = globals().get('saxon', {})
        if saxon.get(chan.lower()) > time.time() - 24*3600: return

        count, end, ssmsg = 1, time.time()+300, sstrip_msg
        while count < 3:
            _, (e_bot, e_chan, e_msg) = yield hold(bot, 'FTO_MSG')
            if time.time() > end: break
            if e_chan.lower() != chan.lower(): continue

            ssmsg = sstrip(e_msg)
            if count < 2 and re.search(r'\bblood\b', ssmsg): break
            if not re.search(r'\bs(a(xon|hson|ssen|chsen|ksen|xe)|eaxe)', ssmsg):
                continue

            count += 1
            if count == 2:
                if saxon.get(chan.lower()) > time.time() - 24*3600: return

                parts = []
                if random.random() < 0.5: parts.append(
                    'I shed blood of Saxon men!')
                parts.append(
                    'I shed the blood of the Saxon men!')
                if random.random() < 0.5: parts.append(
                    'I shed the blood of four thousand Saxon men!')
                reply(' '.join(parts))
                saxon[chan.lower()] = time.time()

            elif count == 3:
                reply('I shed it at Verden!')
                saxon[chan.lower()] = time.time()

    elif re.match(r'i.*shed.*blood.*of.*saxon.*m[ea]n$', strip_msg) \
    and 'fourthousand' not in strip_msg:
        saxon = globals().get('saxon', {})
        if saxon.get(chan.lower()) > time.time() - 8*3600: return
        reply('I shed the blood of four thousand Saxon men!')
        saxon[chan.lower()] = time.time()

#===============================================================================
@link('!nuke')
def h_nuke(bot, id, target, args, full_msg):
    if not target: return
    if not channel.has_op_in(bot, bot.nick, target, 'h'): return

    global nuclear_launch
    target_id = (target.lower(), ('%s!%s@%s' % id).lower())
    try:
        if target_id in nuclear_launch: return
    except NameError:
        nuclear_launch = set()
    nuclear_launch.add(target_id)

    message.reply(bot, id, target, 'Nuclear launch detected.', prefix=False)
    yield runtime.sleep(15)
    bot.send_cmd('KICK %s %s :GIANT ASPARAGUS!' % (target, id.nick))
    
    ERR_CHANOPRIVSNEEDED = '482'
    UNREAL_ERR_CANNOTDOCOMMAND = '972'
    timeout = yield runtime.timeout(10)
    while True:
        event, args = yield hold(bot, timeout,
            UNREAL_ERR_CANNOTDOCOMMAND, ERR_CHANOPRIVSNEEDED)
        if event == UNREAL_ERR_CANNOTDOCOMMAND:
            e_bot, e_src, e_tgt, e_cmd, e_args = args
            if e_cmd.upper() != 'KICK': continue
            message.reply(bot, id, target,
                'Nuclear launch failed: "%s".' % e_args, prefix=False)
        elif event == ERR_CHANOPRIVSNEEDED:
            e_bot, e_src, e_tgt, e_chan, e_args = args
            if e_chan.lower() != target.lower(): continue
            message.reply(bot, id, target,
                'Nuclear launch failed: "%s".' % e_args, prefix=False)
        elif event == timeout:
            break

    nuclear_launch.discard(target_id)

#===============================================================================
def ustrip(_fun):
    def fun(text):
        try: return _fun(text.decode('utf-8'))
        except UnicodeDecodeError: return _fun(text)
    return fun

def _strip(text):
    return _cstrip(text.lower())
strip = ustrip(_strip)

def _cstrip(text):
    return re.sub(r'[^\w]|_', '', text, flags=re.U)
cstrip = ustrip(_cstrip)

def _sstrip(text):
    return _csstrip(text.lower())
sstrip = ustrip(_sstrip)

def _csstrip(text):
    text = re.sub(r'[^\w\s]|_', '', text, flags=re.U)
    text = re.sub(r'\s+', ' ', text, flags=re.U)
    text = re.sub(r'^\s+|\s+$', '', text, flags=re.U)
    return text
csstrip = ustrip(_csstrip)
