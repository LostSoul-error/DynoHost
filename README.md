```
![DynoHost Banner](https://placehold.co/1000x250?text=DynoHost+Minecraft+Panel&bg=0f172a&fg=ffffff)

# 🎮 DynoHost v1 – Your Local Minecraft Server Control Panel

## 🚀 Overview

Tired of messy CMD windows and endless commands to run your Minecraft server? **DynoHost** is here to save your nights! 🌙

DynoHost v1 is a **local web-based Minecraft server control panel**. Start, stop, kill, and manage your server with live console logs, CPU/RAM monitoring, and a built-in file editor.

With DynoHost, you only need to **run your server once using CMD**, place the server files correctly, and from the next time onward, everything is **managed via this panel**.

> This project is **open-source**, made with love 💖, late-night learning sessions in Flask 🐍, and yes… AI helped me along the way 😅.

---

## 🖥️ Features (v1)

* ✅ **Start / Stop / Kill / Restart** your server from a sleek interface
* ✅ **Live console logs** with color-coded warnings, errors, and info
* ✅ **CPU & RAM monitoring** for your server only (no extra processes)
* ✅ **File editor** with VS-Code-style dark theme for editing configs, plugins, and worlds
* ✅ Fully **open-source**, lightweight, and simple to set up
* ✅ Works with **any Minecraft server version** (Paper, Spigot, Vanilla, Forge…)

---

## ⚡ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/YourUsername/DynoHost.git
cd DynoHost

```


2. **Place your Minecraft server files** in the folder.
3. **Rename your server JAR in the `panel.py` configuration**:
```python
SERVER_JAR = "your-server-file.jar"

```


Replace `"your-server-file.jar"` with your server runner (Paper, Spigot, Vanilla, Forge, etc.).
4. **Ensure the folder structure**:
```text
DynoHost/
├─ panel.py        # Main Flask application
├─ templates/
│  ├─ index.html   # Console UI
│  └─ files.html   # File editor
├─ static/         # Optional: icons, favicon
├─ server_start.tmp
└─ README.md       # This file

```


5. **Install Python dependencies**:
```bash
pip install flask flask-socketio psutil

```


6. **Run the server once via CMD** to generate the initial start time:
```bash
python panel.py

```


7. **Open your browser** and go to:
```text
http://127.0.0.1:5000

```


8. From now on, **DynoHost handles everything**.

---

## 📝 File Editor

* Edit server configs, plugin files, and world settings directly from the browser.
* Dark-theme, VS-Code-style interface with syntax highlighting.
* Supports single-file and multi-file navigation.
* Click **Files → Open**, select a file, make changes, and **Save**.

---

## 📊 Server Monitoring

* **CPU & RAM usage** only for the server process.
* **Live console logs** with filtering: INFO, WARN, ERROR.
* **Status & uptime** panel.

---

## 🔮 Future Plans (v2)

* Login system with **roles and permissions**
* Multi-server support
* Plugin and world management
* Scheduled backups and auto-restart
* Mobile-friendly UI
* Graphs for CPU/RAM/TPS over time

---

## 📂 Project Structure

```text
DynoHost/
├─ panel.py            # Main Flask server
├─ templates/          # HTML templates for console and file editor
│  ├─ index.html
│  └─ files.html
├─ static/             # CSS, JS, images
├─ server_start.tmp    # Temporary file for server start time
└─ README.md

```

> **Tip:** Always keep `panel.py` at the root and the `templates/` folder beside it for Flask to find HTML files.

---

## 🔧 Tech Stack

* **Python** + **Flask** + **Flask-SocketIO**
* **psutil** for process monitoring
* **HTML / CSS / JavaScript** for the front-end
* Works on **Windows**, **Linux**, and **macOS** (local server only)

---

## ⚡ How to Contribute

1. Fork this repo
2. Add features, fixes, or enhancements
3. Open a pull request with a detailed explanation

All contributions are welcome! 🌟

---

## 📝 License

MIT License – Free to use, modify, and share.

---

## 🙏 Credits

* **Rishav Digar** – Project author and late-night coder 🥱
* **AI tools** – Helped with planning, debugging, and formatting 🤖
* **Minecraft community** – Inspiration for building better tools 🎮

**DynoHost v1 – Make hosting Minecraft locally fun, easy, and powerful!**
## 🚀 Overview

Tired of messy CMD windows and endless commands to run your Minecraft server? **DynoHost** is here to save your nights! 🌙

DynoHost v1 is a **local web-based Minecraft server control panel**. Start, stop, kill, and manage your server with live console logs, CPU/RAM monitoring, and a built-in file editor.

With DynoHost, you only need to **run your server once using CMD**, place the server files correctly, and from the next time onward, everything is **managed via this panel**.

> This project is **open-source**, made with love 💖, late-night learning sessions in Flask 🐍, and yes… AI helped me along the way 😅.

---

## 🖥️ Features (v1)

* ✅ **Start / Stop / Kill / Restart** your server from a sleek interface
* ✅ **Live console logs** with color-coded warnings, errors, and info
* ✅ **CPU & RAM monitoring** for your server only (no extra processes)
* ✅ **File editor** with VS-Code-style dark theme for editing configs, plugins, and worlds
* ✅ Fully **open-source**, lightweight, and simple to set up
* ✅ Works with **any Minecraft server version** (Paper, Spigot, Vanilla, Forge…)

---

## ⚡ Installation

1. **Clone the repository**:
```bash
git clone https://github.com/YourUsername/DynoHost.git
cd DynoHost

```


2. **Place your Minecraft server files** in the folder.
3. **Rename your server JAR in the `panel.py` configuration**:
```python
SERVER_JAR = "your-server-file.jar"

```


Replace `"your-server-file.jar"` with your server runner (Paper, Spigot, Vanilla, Forge, etc.).
4. **Ensure the folder structure**:
```text
DynoHost/
├─ panel.py        # Main Flask application
├─ templates/
│  ├─ index.html   # Console UI
│  └─ files.html   # File editor
├─ static/         # Optional: icons, favicon
├─ server_start.tmp
└─ README.md       # This file

```


5. **Install Python dependencies**:
```bash
pip install flask flask-socketio psutil

```


6. **Run the server once via CMD** to generate the initial start time:
```bash
python panel.py

```


7. **Open your browser** and go to:
```text
http://127.0.0.1:5000

```


8. From now on, **DynoHost handles everything**.

---

## 📝 File Editor

* Edit server configs, plugin files, and world settings directly from the browser.
* Dark-theme, VS-Code-style interface with syntax highlighting.
* Supports single-file and multi-file navigation.
* Click **Files → Open**, select a file, make changes, and **Save**.

---

## 📊 Server Monitoring

* **CPU & RAM usage** only for the server process.
* **Live console logs** with filtering: INFO, WARN, ERROR.
* **Status & uptime** panel.

---

## 🔮 Future Plans (v2)

* Login system with **roles and permissions**
* Multi-server support
* Plugin and world management
* Scheduled backups and auto-restart
* Mobile-friendly UI
* Graphs for CPU/RAM/TPS over time

---

## 📂 Project Structure

```text
DynoHost/
├─ panel.py            # Main Flask server
├─ templates/          # HTML templates for console and file editor
│  ├─ index.html
│  └─ files.html
├─ static/             # CSS, JS, images
├─ server_start.tmp    # Temporary file for server start time
└─ README.md

```

> **Tip:** Always keep `panel.py` at the root and the `templates/` folder beside it for Flask to find HTML files.

---

## 🔧 Tech Stack

* **Python** + **Flask** + **Flask-SocketIO**
* **psutil** for process monitoring
* **HTML / CSS / JavaScript** for the front-end
* Works on **Windows**, **Linux**, and **macOS** (local server only)

---

## ⚡ How to Contribute

1. Fork this repo
2. Add features, fixes, or enhancements
3. Open a pull request with a detailed explanation

All contributions are welcome! 🌟

---

## 📝 License

MIT License – Free to use, modify, and share.

---

## 🙏 Credits

* **Rishav Digar** – Project author and late-night coder 🥱
* **AI tools** – Helped with planning, debugging, and formatting 🤖
* **Minecraft community** – Inspiration for building better tools 🎮

**DynoHost v1 – Make hosting Minecraft locally fun, easy, and powerful!**

```
