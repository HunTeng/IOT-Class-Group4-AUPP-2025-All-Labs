# IOT-Class-AUPP-2025-Hun-Teng-Group4
# 🌡️ ESP32 Telegram Temperature Bot with Relay Control — **LAB1 README**

> **Course Lab**: Temperature Sensor with Relay Control (Telegram)
>
> **Hardware**: ESP32 + DHT11/DHT22 + Relay module
> **Firmware**: MicroPython
> **Control**: Telegram Bot commands `/status`, `/on`, `/off`
> **Threshold**: 30 °C (alerts & auto‑OFF logic)

---

## 1) Overview

Build a tiny IoT node that reads temperature & humidity from a DHT sensor and controls a relay. The ESP32 connects to Wi‑Fi and talks to your Telegram bot. When temperature ≥ 30 °C, the bot sends alerts. You can remotely turn the relay **ON**/**OFF** from Telegram; once the temperature drops below 30 °C, the relay turns **OFF automatically** and the bot sends a one‑time notice.

---

## 2) Learning Outcomes (CLO Alignment)

* Design & implement an IoT system (sensing, actuation, networking) on **ESP32 + MicroPython**.
* Apply programming techniques for **periodic sampling**, error handling, and **simple state machines**.
* Develop a **chat‑based remote control** using the **Telegram Bot API** (HTTP requests).
* **Document** system design, wiring, setup, test evidence (screenshots/video), and reflect on reliability/ethics.
* Evaluate performance (sampling interval, API rate limits) and **safety** (relay loads, power isolation).

---

## 3) Equipment

* ESP32 Dev Board (**with MicroPython flashed**)
* DHT22 (or DHT11) temperature/humidity sensor
* 1‑channel relay module (5 V/3.3 V logic compatible)
* Jumper wires + breadboard (optional)
* USB cable + laptop with **Thonny**
* Wi‑Fi with internet access

> **Note**: If you use a DHT11, you can keep the code but readings are less precise. The code can print with **2 decimals** to meet lab requirements.

---

## 4) Wiring


**Default pins in code**:

* **DHT** → GPIO **4**
* **Relay** → GPIO **5**
* **Relay\_ACTIVE\_LOW** set to `False` (change if your relay is inverted)

```
ESP32 (3V3) ────── VCC (DHT)
ESP32 (GND) ────── GND (DHT)
ESP32 GPIO4 ────── DATA (DHT)

ESP32 (5V/3V3*) ── VCC (Relay)   (*depends on your relay board)
ESP32 (GND) ────── GND (Relay)
ESP32 GPIO5 ────── IN (Relay)
```

**Important wiring notes**

* If your relay board needs **5 V**, power VCC from 5 V. Most logic inputs still accept 3.3 V, but check your module specs.
* If you switch **AC mains** with the relay, **isolate** the low‑voltage side, use proper enclosures, and follow electrical safety rules.

**Photo/Diagram placeholders** 
*[image alt](https://github.com/Yunweisheng/IOT-Class-AUPP-2025-Hun-Teng-Group4/blob/adbf964f665646d409eff3ef05d750807c5c5bd0/IMAGE%202025-09-07%2018%3A12%3A16.jpg)*

  

---

## 5) Software Setup

1. **Flash MicroPython** to your ESP32 (if not already).
2. Open **Thonny** → select interpreter: **MicroPython (ESP32)**.
3. Create a new file `main.py` and paste your lab code.
4. Update the **config** section at the top of the file:

   * `WIFI_SSID = "Robotic WIFI"`
   * `WIFI_PASSWORD = "rbtWIFI@2025"`
   * `BOT_TOKEN = "8239071008:AAE7sZfmDBJ_4rKoxrV_oxGukAqObOmLWj8"` 
   * `CHAT_IDS = [1032247155, 1039563806, -4985603296, 741464258]`
5. **Save to device** as `main.py`. It will auto‑run on boot.

> **Finding your chat id**: DM your bot first, or add it to a group. Use `/whoami` from this code to discover IDs. Your code already accepts a list of chat/group IDs.


---

## 6) Telegram Bot Setup

1. In Telegram, talk to **@BotFather** → `/newbot` → get the **BOT\_TOKEN**.
2. Add the bot to your group (if needed) and send a message so the bot can see the chat.
3. Put the token in your `main.py`. 

**Supported commands** (in this lab):

* `/status` → returns **Relay** state and **last Temperature** (see 12 to include Humidity if desired)
* `/on` → **turns relay ON** (also arms auto‑OFF if T ≥ 30 °C)
* `/off` → **turns relay OFF** immediately
* `/temp` → on‑demand **Temperature & Humidity**
* `/whoami` → shows your chat ID
* `/help` → command list

---

## 7) Run & Test

1. Power the ESP32 in Thonny → view the **Shell** for logs.
2. The device connects to Wi‑Fi (auto‑reconnect is implemented).
3. Every **5 s**: read DHT, process alerts/state, and respond to Telegram commands.
4. In Telegram, send `/status`, `/on`, `/off`, `/temp` and observe responses.
5. Heat the sensor gently (hand warmth or warm air) to reach **≥ 30 °C** and observe alert behavior, then let it cool **< 30 °C** to see auto‑OFF.

**Expected behaviors**

* **T < 30 °C** → no alerts. `/status` works; relay stays as commanded.
* **T ≥ 30 °C** & relay **OFF** → **alert every 5 s** until `/on`.
* After `/on` at high temp → **alerts stop**. When **T < 30 °C**, relay **auto‑OFF** once and bot sends **one** notice.

---

## 8) Block Diagram

```
+-----------+      +-----------+      +----------------+      +-----------+
|  DHT22    | ---> |  ESP32    | ---> | Telegram (HTTP)| ---> |  Telegram |
|  Sensor   |      |  Logic    | <--- |   Bot API      | <--- |  Client   |
+-----------+      +-----------+      +----------------+      +-----------+
       |                   |
       v                   v
   Temperature        Relay Control
     & Humidity       (GPIO5)
```

---

## 9) Flowchart (Main Loop / State Machine)

```
        ┌───────────────┐
        │    Boot       │
        └──────┬────────┘
               v
      ┌───────────────────┐
      │ Wi‑Fi connect     │─(fail?)─┐
      └──────┬────────────┘         │ retry
             v                      │
   ┌───────────────────┐            │
   │ Read DHT (5 s)    │<───────────┘
   │ (skip on OSError) │
   └──────┬────────────┘
          v
  ┌──────────────────────┐
  │ Handle bot commands  │  /status /on /off /temp
  └──────┬───────────────┘
         v
  ┌──────────────────────┐   T<30?   yes → No alerts
  │ If T ≥ 30 °C         │───────────────┐
  │   & Relay OFF        │               │
  │ → send alert (5 s)   │               │
  └──────┬───────────────┘               │
         v                                │
  ┌──────────────────────┐                │
  │ If Relay ON & T<30   │                │
  │ → auto‑OFF + notice  │                │
  └─────────┬────────────┘                │
            v                             │
        (sleep 5 s) ──────────────────────┘
```

---

## 10) Configuration Snippets

```python
# =======================
# CONFIG (from this repo's main.py)
# =======================
WIFI_SSID     = "Robotic WIFI"
WIFI_PASSWORD = "rbtWIFI@2025"  # 

BOT_TOKEN     = "<8239071008:AAE7sZfmDBJ_4rKoxrV_oxGukAqObOmLWj8>" 
CHAT_IDS      = [1032247155, 1039563806, -4985603296, 741464258]

API = "https://api.telegram.org/bot" + BOT_TOKEN

RELAY_PIN        = 5        # GPIO5
RELAY_ACTIVE_LOW = False    # True if your relay is inverted
DEBUG            = True

# Telegram long-poll timeout (smaller = more responsive)
POLL_TIMEOUT_S   = 1

# DHT config
DHT_PIN          = 4        # GPIO4 for DHT
SENSOR_TYPE      = "DHT22"  # set "DHT11" if using DHT11

# Temperature logic
TEMP_THRESHOLD_C          = 30.0  # "hot" if strictly above this
TEMP_CHECK_INTERVAL_S     = 5     # read sensor every 5s (matches alert cadence)
NOTIFY_COOLDOWN_S         = 300   # 5 min cooldown when relay is ON & hot
ALERT_WHEN_OFF_INTERVAL_S = 5     # when relay OFF & hot, alert every 5s
```

---

## 10.1) Exact Runtime Parameters (from code)

* **Pins**: `DHT_PIN=4`, `RELAY_PIN=5`, `RELAY_ACTIVE_LOW=False`
* **Loop cadence**: `TEMP_CHECK_INTERVAL_S=5`
* **Hot threshold**: `TEMP_THRESHOLD_C=30.0` (strictly `>` hot; `≤` is normal)
* **Alert policy**:

  * Relay **OFF & hot**: every **5 s** (`ALERT_WHEN_OFF_INTERVAL_S=5`)
  * Relay **ON & hot**: one warning, then every **5 min** (`NOTIFY_COOLDOWN_S=300`)
* **Telegram**: long‑poll `POLL_TIMEOUT_S=1`; extra commands implemented: `/temp`, `/whoami`, `/help`
* **Robustness**: Wi‑Fi auto‑reconnect, HTTP error handling, DHT `OSError` skip, capped error restarts

---

## 11) Marking Tasks & Evidence Checklist

Use this **self‑check** to make sure you’ve met every rubric item. *The current code meets the logic below; add screenshots/video to complete the submission.*

* [ ] **Task 1 – Sensor Read & Print (10 pts)**
  ✅ Reads every **5 s**
  ✅ Serial logs of **T/H** (add **2‑decimal formatting** in prints if your grader requires exact formatting)
  ☐ **Serial screenshot** saved: `images/serial_readings.png`

* [ ] **Task 2 – Telegram Send (15 pts)**
  ✅ `send_message()` and `broadcast()` implemented
  ☐ **Chat screenshot** saved: `images/test_message.png`

* [ ] **Task 3 – Bot Commands (15 pts)**
  ✅ `/status` (Relay state + Temp), `/on`, `/off` implemented
  🔎 *Rubric asks for T/H in `/status`. Current code shows **Temp** (and **Humidity** via `/temp`). Either keep README as‑is and show `/temp` alongside `/status`, or update code to include Humidity in `/status`.*
  ☐ **Chat screenshot**: `images/commands.png`

* [ ] **Task 4 – Alert Logic (20 pts)**
  ✅ No messages while **T < 30 °C**
  ✅ If **T ≥ 30 °C** & relay **OFF** → alert **every 5 s** until `/on`
  ✅ After `/on`, alerts stop
  ✅ When **T < 30 °C**, relay **auto‑OFF** + **one‑time notice**
  ☐ **Short demo video** (60–90 s) link added in README

* [ ] **Task 5 – Robustness (10 pts)**
  ✅ Auto **Wi‑Fi reconnect**
  ✅ Handle **Telegram HTTP** errors (print status; skip)
  ✅ Handle **DHT OSError** (skip cycle)

* [ ] **Task 6 – Documentation (30 pts)**
  ✅ This **README.md** (setup/usage)
  ☐ **Wiring photo/diagram**
  ☐ **Screenshots**: `/status`, alerts
  ✅ **Flowchart** or **block diagram**
  ☐ **Video link** showing high‑temp behavior and cool‑down auto‑OFF

---

## 12) Usage Guide (Commands & Scenarios)

**Implemented bot commands** (from this code):

* `/status` → shows **Relay state** and **last Temp** (add Humidity here if you prefer)
* `/on` → **turns relay ON** (arms auto‑OFF if hot)
* `/off` → **turns relay OFF** immediately
* `/temp` → reads **Temperature & Humidity** on demand
* `/whoami` → replies with your chat ID (useful to fill `CHAT_IDS`)
* `/help` → command list and notes

**Examples**

* `/status` → `📊 Relay status: OFF\n🌡️ 29.75°C`
* `/temp` → `🌡️ Temperature: 31.02°C\n💧 Humidity: 62.10%`
* `/on` while T≥30 → bot: `✅ Relay: ON` + `🟠 Auto-off armed…`
* Cooldown below 30 → bot: `⛳ Auto-off…` + `✅ Back to normal…`

---

## 13) Troubleshooting

* **401 Unauthorized** when sending messages
  → BOT\_TOKEN wrong or bot not added to the chat. Verify with BotFather; ensure you’ve messaged in the chat so the bot can see it.
* **No responses**
  → Check Wi‑Fi SSID/password; confirm `CHAT_IDS` are correct (negative for groups). Use `/whoami` to capture IDs.
* **DHT OSError**
  → Loose wiring; wrong pin; add a small delay; keep sampling at **≥ 2 s** (we use **5 s**).
* **Relay inverted**
  → Set `RELAY_ACTIVE_LOW = True` if your relay turns ON when you set pin **LOW**.
* **Exact formatting (2 decimals)**
  → If required, format readings using `"{:.2f}".format(value)` before printing/sending.
* **Rate limits**
  → Our cadence (5 s loop, 5 min reminders) is Telegram‑friendly.

---

## 14) Safety Notes (Relay Loads)

* If switching **AC mains**, use proper insulation, fuses, and a certified enclosure.
* Keep sensor/ESP32 away from high‑voltage wiring.
* Never touch mains when powered; disconnect before rewiring.

## 15) Submission (Academic Integrity)

Create a **private GitHub repo** and add the instructor as a collaborator. Include:

* `/src/` → your `.py` files (e.g., `main.py`)
* `README.md` (this file) with wiring photo/diagram and video link
* `/images/` → screenshots: serial readings, command tests, alert behavior
* **Short demo video link** (e.g., unlisted YouTube/Drive) showing:

  1. T rising above **30 °C** with alerts
  2. `/on` stops alerts
  3. Cooldown below **30 °C** → **auto-OFF** + one-time notice


## 🎥 Demo

### Video
[![Watch the demo](https://img.youtube.com/vi/UzbG9PChk_c/0.jpg)](https://youtu.be/UzbG9PChk_c?si=t1REvn6xUxy5IgRf)


*(Click the thumbnail to watch the video)*

### Image
## Telegram Chat 
![](https://github.com/Yunweisheng/IOT-Class-AUPP-2025-Hun-Teng-Group4/blob/6502552b7a7e12080a1c5d0d4b0abd52123ee235/2025-09-06%2020.21.44.jpg)
## Wire Setup
![](https://github.com/Yunweisheng/IOT-Class-AUPP-2025-Hun-Teng-Group4/blob/6502552b7a7e12080a1c5d0d4b0abd52123ee235/2025-09-06%2020.33.41.jpg)


## Main Loop Flowchart
           ┌────────────────────────────────────────┐
           │                START                   │
           └───────────────┬────────────────────────┘
                           v
                 ┌────────────────────┐
                 │ Connect to Wi-Fi   │
                 └───────┬────────────┘
                         v
                 ┌────────────────────┐
                 │ Init Relay OFF      │
                 └───────┬────────────┘
                         v
               ┌────────────────────────┐
               │ LOOP (runs forever)    │
               └────────┬───────────────┘
                        v
       ┌─────────────────────────────────────────┐
       │ Poll Telegram getUpdates (timeout=1s)   │
       └───────────────┬─────────────────────────┘
                       v
            ┌───────────────────────────┐
            │ Any new messages?         │───No──┐
            └──────────────┬────────────┘       │
                           v Yes                 │
                 ┌────────────────────────────┐  │
                 │ Handle command:            │  │
                 │  /on → relay ON; if hot →  │  │
                 │         auto_off_pending=1 │  │
                 │  /off → relay OFF; clear   │  │
                 │         auto_off_pending   │  │
                 │  /status → show T/H/relay  │  │
                 │  /temp → read & show T/H   │  │
                 └────────────────────────────┘  │
                                                v
                       ┌─────────────────────────────────┐
                       │ Every 5s: read DHT22 (T,H)      │
                       └───────────────┬─────────────────┘
                                       v
                     ┌────────────────────────────────────────────┐
                     │ Evaluate alerting (LAB1 rules):            │
                     │  • T ≤ 30°C → no alerts                    │
                     │  • First hot transition → one-time warning │
                     │  • Relay OFF & hot → alert every 5s        │
                     │  • Relay ON & hot → NO periodic reminders  │
                     └───────────────┬────────────────────────────┘
                                     v
                     ┌────────────────────────────────────────────┐
                     │ Auto-off check:                            │
                     │  if auto_off_pending AND T ≤ 30°C:         │
                     │     relay OFF; send one-time auto-OFF msg  │
                     │     clear auto_off_pending                 │
                     └───────────────┬────────────────────────────┘
                                     v
                           ┌────────────────────┐
                           │ Small sleep (50ms) │
                           └─────────┬──────────┘
                                     │
                                     └───────→ back to LOOP

# FLOWCHART
![](https://github.com/Yunweisheng/IOT-Class-AUPP-2025-Hun-Teng-Group4/blob/8594585e94e492daa9e5ecc0645beabd9baab30f/FlowchartIOT.png)

                                     
## Alerting & Auto-OFF State (Quick Reference)
States:
- NORMAL: T ≤ 30°C → no alerts
- HOT_FIRST: T just crossed > 30°C → send one-time "Warning"
- HOT_OFF: relay OFF & T > 30°C → alert every 5s
- HOT_ON:  relay ON  & T > 30°C → suppress periodic reminders

Auto-OFF:
- When user sends /on while hot → auto_off_pending = 1
- If later T ≤ 30°C → relay OFF + one-time "auto-OFF"


  ## Wiring Diagram 

```text
+-------------------+            +------------------+
|      ESP32        |            |      DHT22       |
|                   |            |                  |
|      3V3 ---------+------------+ VCC              |
|       GND --------+------------+ GND              |
|    GPIO4 ---------+------------+ DATA             |
|                   |            |                  |
+-------------------+            +------------------+

+-------------------+            +------------------+
|      ESP32        |            |   RELAY MODULE   |
|                   |            |                  |
|      3V3 ---------+------------+ VCC / JD-VCC (*) |
|       GND --------+------------+ GND              |
|    GPIO5 ---------+------------+ IN               |
|                   |            |                  |
+-------------------+            +------------------+

Notes:
• DHT22: add a 10kΩ pull-up between DATA and VCC if your board doesn’t include one.  
• RELAY: connect the relay’s COM/NO to your external load circuit; keep mains isolation.  
• If your relay logic is inverted, set RELAY_ACTIVE_LOW = True in the code.  




