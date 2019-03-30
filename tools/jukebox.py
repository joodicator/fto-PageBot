#!/usr/bin/env python2.7

import os
import os.path
import sys
import re
import pickle
import atexit

os.chdir(os.path.join(os.path.dirname(__file__), '../'))
sys.path[0:0] = ['.', 'tools']

import main
import dice
from youtube import youtube

from rd_util import enum_defn

CHANNEL = '#fto'
DEFINITION = sys.argv[1] if len(sys.argv) > 1 else 'jukebox'

def main():
    print('Content-Type: text/html')
    print('')
    print('<!DOCTYPE html>')
    print('<head>')
    print('  <meta charset="utf8">')
    print('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    print('  <title>PageBot {{#fto/%s}} Catalogue</title>' % DEFINITION)
    print('  <style type="text/css">')
    print('    body { background:#D8D8E0; font-family:sans-serif;')
    print('        text-align:center; margin-left:0; margin-right:0; }')
    print('    div#top { display:inline-block; }')
    print('    table#main { border-collapse:collapse; background:#FFF; }')
    print('    #main td, #main th { border:1px solid black; vertical-align:top;')
    print('        overflow:hidden; padding:5px }')
    print('    #main td { text-align:left }')
    print('    #main td:first-child { width:120px; height:90px; padding:0px;')
    print('        background:#445; text-align:center; vertical-align:middle }')
    print('    #main img { display:block; width:120px; height:90px }')
    print('    #main tr.nsfw td:first-child:not(:hover) img { display:none; }')
    print('    #main tr.nsfw td:first-child:not(:hover)::before {')
    print('        content:"NSFW"; color:#FFF }')
    print('    #main tr.nsfw td:first-child { background:#422; }')
    print('    #github { position:absolute; left:8px; top:8px; opacity:0.2 }')
    print('    #github:hover { opacity:1 }')
    print('    #main code { font-size:larger }')
    print('    #main .error { color:red; font-style:italic }')
    print('    #main .title { font-weight:bold; color:#000; text-decoration:none }')
    print('  </style>')
    print('</head>')
    print('<body>')
    print('  <a id="github" href="https://github.com/joodicator/fto-PageBot/tree/master/tools/jukebox.py" title="View source code on GitHub"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNiAoTWFjaW50b3NoKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpFNTE3OEEyRTk5QTAxMUUyOUExNUJDMTA0NkE4OTA0RCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDpFNTE3OEEyRjk5QTAxMUUyOUExNUJDMTA0NkE4OTA0RCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOkU1MTc4QTJDOTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOkU1MTc4QTJEOTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+FYrpWAAABrNJREFUeNrkW2ls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" width="32" height="32" /></a>')
    print('  <div id="top">')
    print('  <h3>Entries in PageBot\'s <code>{{%s}}</code> roll definition in #fto</h3>' % DEFINITION)
    print('  <table id="main">')
    print('    <thead>')
    print('      <tr>')
    print('        <th>Thumbnail</th>')
    print('        <th>Title</th>')
    print('        <th>Notes</th>')
    print('        <th>Video ID</th>')
    print('        <th>Definition</th>')
    print('        <th>Chance</th>')
    print('      </tr>')
    print('    </thead>')
    print('    <tbody>')
    for item, prob in reversed(list(enum_defn(CHANNEL, DEFINITION))):
        v_id = ''.join(t for (t, d) in item[1:])
        match = re.match(r'(?P<id>.*)\s+\((?P<notes>.*)\)$', v_id)
        if match:
            v_id, notes = match.group('id', 'notes')
        else:
            notes = ''
        nsfw = 'NSFW' in notes.upper()

        title = video_title(v_id)

        v_url = item[0][0] + v_id
        t_url = 'https://i3.ytimg.com/vi/%s/default.jpg' % v_id

        print('      <tr%s>' % (' class="nsfw"' if nsfw else ''))
        print('        <td><a href="%s"><img src="%s" /></a></td>'
            % (html_escape(v_url), html_escape(t_url)))
        print('        <td><a class="title" href="%s">%s</a></td>' % (
            v_url, '<br>'.join(html_escape(l.encode('utf8')) for l in title)
            if title else '<span class="error">Video unavailable.</span>'))
        print('        <td>%s</td>' % html_escape(notes))
        print('        <td nowrap><code>%s</code></td>' % html_escape(v_id))
        print('        <td nowrap><code>%s</code></td>' % html_escape(item[1][1]))
        print('        <td>%d/%d</td>' % (prob.numerator, prob.denominator))
        print('      </tr>')
    print('    </tbody>')
    print('  </table>')
    print('  </div>')
    print('</body>')

def html_escape(text):
    return text.replace('&', '&apos;') \
               .replace('"', '&quot;') \
               .replace('<', '&lt;') \
               .replace('>', '&gt;')

video_title_cache = None
def video_title(v_id):
    global video_title_cache
    if video_title_cache is None:
        if os.path.exists('tools/.jukebox-cache'):
            with open('tools/.jukebox-cache', 'rb') as file:
                video_title_cache = pickle.load(file)
        else:
            video_title_cache = {}
        def save_cache():
            with open('tools/.jukebox-cache', 'wb') as file:
                pickle.dump(video_title_cache, file)
        atexit.register(save_cache)

    if v_id in video_title_cache:
        return video_title_cache[v_id]

    result = youtube.videos().list(id=v_id, hl='en', part='snippet').execute()
    if result['items']:
        snippet = result['items'][0]['snippet']
        title_dl = snippet['title']
        title_en = snippet['localized']['title']
        dl = snippet.get('defaultLanguage')
        if dl and title_en != title_dl:
            title = ('%s (%s)' % (title_dl, dl),
                     '%s (en)' % title_en)
        else:
            title = (title_dl,)
    else:
        title = None

    video_title_cache[v_id] = title
    return title

if __name__ == '__main__':
    main()
