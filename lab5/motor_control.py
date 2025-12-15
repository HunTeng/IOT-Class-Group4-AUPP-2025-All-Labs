import network, socket, ure, time
from machine import Pin, PWM
import urequests

# =========================
# Wi-Fi
# =========================
WIFI_SSID = "Robotic WIFI"
WIFI_PASS = "rbtWIFI@2025i"   

def wifi_connect():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if not sta.isconnected():
        sta.connect(WIFI_SSID, WIFI_PASS)
        for _ in range(80):
            if sta.isconnected():
                break
            time.sleep(0.25)

    if not sta.isconnected():
        raise RuntimeError("WiFi connect failed")

    print("WiFi: connected")
    return sta.ifconfig()[0]

# =========================
# InfluxDB (InfluxDB v1)
# =========================
INFLUX_URL = "http://10.30.0.153:8086/write?db=motor_logs&precision=s"

def log_event(action, speed_pct):
    ts = int(time.time())  # seconds (precision=s)
    speed_pct = int(speed_pct)

    # line protocol: measurement,tag=value field=value timestamp
    # use integer field with "i" suffix (recommended)
    line = "motor_events,action={} speed={}i {}".format(action, speed_pct, ts)

    try:
        resp = urequests.post(
            INFLUX_URL,
            data=line,
            headers={"Content-Type": "text/plain; charset=utf-8"},
        )
        resp.close()
        print("Influx:", action, speed_pct, "OK")
    except Exception as e:
        print("Influx error:", e)

# =========================
# L298N motor pins (ESP32)
# =========================
IN1 = Pin(26, Pin.OUT)
IN2 = Pin(27, Pin.OUT)
ENA = PWM(Pin(25), freq=1000)

PWM_MAX = 1023
_speed_pct = 70

def set_speed(pct):
    global _speed_pct
    pct = int(max(0, min(100, pct)))
    _speed_pct = pct
    ENA.duty(int(PWM_MAX * (_speed_pct / 100.0)))
    print("Speed:", _speed_pct, "%")

def motor_forward():
    set_speed(_speed_pct)
    IN1.on()
    IN2.off()
    print("Forward")
    log_event("forward", _speed_pct)

def motor_backward():
    set_speed(_speed_pct)
    IN1.off()
    IN2.on()
    print("Backward")
    log_event("backward", _speed_pct)

def motor_stop():
    IN1.off()
    IN2.off()
    ENA.duty(0)
    print("Stop")
    log_event("stop", 0)

# =========================
# HTTP (bytes-safe)
# =========================
HEAD_OK_TEXT = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\n"
).encode()

HEAD_OK_HTML = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\n"
).encode()

HEAD_404 = (
    "HTTP/1.1 404 Not Found\r\n"
    "Content-Type: text/plain\r\n"
    "Access-Control-Allow-Origin: *\r\n"
    "Connection: close\r\n\r\nNot Found"
).encode()

HOME_HTML = ("""<!doctype html>
<meta name=viewport content="width=device-width,initial-scale=1">
<h3>ESP32 Motor</h3>
<p>
  <a href="/forward"><button>Forward</button></a>
  <a href="/backward"><button>Backward</button></a>
  <a href="/stop"><button>Stop</button></a>
</p>
<p>
  <label>Speed:</label>
  <input id="spd" type="range" min="0" max="100" value="70"
    oninput="fetch('/speed?value='+this.value).then(r=>r.text()).then(console.log);">
</p>
""").encode()

def _split_query(path):
    if "?" in path:
        p, q = path.split("?", 1)
        return p, q
    return path, ""

def route(path):
    p, q = _split_query(path)

    if p == "/" or p.startswith("/index"):
        return HEAD_OK_HTML + HOME_HTML

    if p == "/favicon.ico":
        return HEAD_OK_TEXT + b""

    if p == "/forward":
        motor_forward()
        return HEAD_OK_TEXT + b"forward"

    if p == "/backward":
        motor_backward()
        return HEAD_OK_TEXT + b"backward"

    if p == "/stop":
        motor_stop()
        return HEAD_OK_TEXT + b"stop"

    if p == "/speed":
        m = ure.search(r"(?:^|&)value=(\d+)", q)
        if m:
            v = int(m.group(1))
            set_speed(v)
            log_event("speed", v)
            return HEAD_OK_TEXT + ("speed=%d" % v).encode()
        return HEAD_OK_TEXT + b"usage: /speed?value=0..100"

    print("Unknown path:", path)
    return HEAD_404

def start_server(ip):
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(3)
    print("HTTP server running")

    while True:
        cl = None
        try:
            cl, _ = s.accept()
            cl.settimeout(2)

            req = cl.recv(1024)
            if not req:
                continue

            text = req.decode("utf-8", "ignore")
            first_line = text.split("\r\n", 1)[0]  # "GET /path HTTP/1.1"
            parts = first_line.split(" ")
            path = parts[1] if len(parts) >= 2 else "/"

            resp = route(path)
            cl.sendall(resp)

        except OSError as e:
            if getattr(e, "errno", None) != 116:  # ignore ETIMEDOUT
                print("Socket error:", e)
        except Exception as e:
            print("Server error:", e)
        finally:
            try:
                if cl:
                    cl.close()
            except:
                pass

# =========================
# main
# =========================
if __name__ == "__main__":
    motor_stop()
    set_speed(_speed_pct)
    ip = wifi_connect()
    start_server(ip)

