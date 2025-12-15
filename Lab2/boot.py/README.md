# LAB2: IoT Webserver with LED, Sensors, and LCD Control

## 1) Overview
ESP32 + MicroPython project with a browser-based UI to:
- Toggle an **LED**
- Read **DHT11** (temperature/humidity) + **HC-SR04** (distance)
- Show selected sensor values on a **16×2 I²C LCD**
- Send **custom text** from the webpage to the LCD

Focus: event-driven interaction between web UI and hardware.

---

## 2) Learning Outcomes
- Build a MicroPython **webserver** with HTML controls
- Control an **LED** from the browser
- Read **DHT11** + **ultrasonic** and show on a webpage
- Send sensor values to **LCD** via buttons
- Send **custom text** (textbox → LCD)
- Document wiring and usage clearly

---

## 3) Equipment
- ESP32 Dev Board (with MicroPython)
- DHT11 sensor
- HC-SR04 ultrasonic sensor
- 16×2 LCD with **I²C** backpack
- Breadboard, jumper wires, USB cable
- Laptop with **Thonny**
- Wi-Fi access

---
## 4) Wiring


## 5) Tasks & Checkpoints
### ✅ Task 1 — LED Control (15 pts)
**Goal**
- Add two buttons (**ON / OFF**) on the web page.
- Clicking them should toggle the LED on **GPIO2**.

**How to verify**
- Click **LED ON** → LED turns on.
- Click **LED OFF** → LED turns off.

**Evidence to include in repo**
- Short video showing button click → LED changes  
  [![Watch the demo](https://img.youtube.com/vi/aZOX2eOIado/hqdefault.jpg)](https://youtu.be/aZOX2eOIado)

- (Optional) Screenshot of the web page with ON/OFF buttons  
  

### ✅ Task 2 — Sensor Read (15 pts)
**Goal**
- Read **DHT11** temperature (and humidity if shown) and **HC-SR04** distance.
- Display values on the web page, **auto-refresh every 1–2 seconds**.

**How to verify**
- Open the web page; confirm values update periodically without manual refresh.

**Evidence to include in repo**
- Screenshot of the web page with sensor values  
  - Place at: 

**Status**
- [ ] Sensors wired & read correctly
- [ ] Auto-refresh implemented (~1–2s)
- [ ] Evidence added

---

### ✅ Task 3 — Sensor → LCD (20 pts)
**Goal**
- Add two buttons on the web UI:
  - **Show Distance** → writes distance to **LCD line 1**
  - **Show Temp** → writes temperature to **LCD line 2**

**How to verify**
- Click **Show Distance** → LCD line 1 shows current distance.
- Click **Show Temp** → LCD line 2 shows current temperature.

**Evidence to include in repo**
- Photo of LCD showing distance after button click  
  - Place at: `docs/images/lcd_distance.jpg`
- Photo of LCD showing temperature after button click  
  - Place at: `docs/images/lcd_temp.jpg`

**Status**
- [ ] Buttons added
- [ ] Distance → LCD line 1
- [ ] Temp → LCD line 2
- [ ] Evidence added

---

### ✅ Task 4 — Textbox → LCD (20 pts)
**Goal**
- Add a **textbox + “Send”** button on the web page.
- Sending text should display it on the LCD (**scroll/trim if >16 chars**).

**How to verify**
- Type custom text in the browser → press **Send** → text appears on LCD.

**Evidence to include in repo**
- Short video of typing in browser → LCD displays the text  
  - Place at: `docs/custom_text.mp4` 

**Status**
- [ ] Textbox & Send button added
- [ ] Text reaches LCD (handles >16 chars)
- [ ] Evidence added

---

### ✅ Task 5 — Documentation (30 pts)
**Goal**
- Provide clear documentation for setup and usage.

**README must include**
- [ ] **Wiring diagram/photo** (e.g., `docs/images/wiring.jpg`)
- [ ] **Setup instructions** (Wi-Fi, running server)
- [ ] **Usage instructions** (LED control, sensor buttons, textbox → LCD)
- [ ] **Evidence**: source code, screenshots, and demo video



