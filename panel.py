from flask import Flask, render_template, request, send_from_directory, abort
import subprocess, threading, socket, os, time
import psutil

app = Flask(__name__)

# ----------------- Configuration -----------------
SERVER_JAR = "paper-1.21.11-126.jar"
START_CMD = ["java", "-Xms8192M", "-Xmx8192M", "-jar", SERVER_JAR, "--nogui"]
BASE_DIR = os.path.abspath(".")
START_TIME_FILE = os.path.join(BASE_DIR, "server_start.tmp")

server_process = None
server_status = "OFFLINE"
logs = []
lock = threading.Lock()

# ----------------- Usage Tracking -----------------
cpu_usage = 0.0
ram_usage = 0.0

def reset_usage():
    """Reset CPU and RAM values to zero."""
    global cpu_usage, ram_usage
    cpu_usage = 0.0
    ram_usage = 0.0

def track_usage():
    """Track CPU & RAM of server + children like Task Manager."""
    global cpu_usage, ram_usage, server_process
    cpu_count = psutil.cpu_count(logical=True)
    
    while True:
        if server_process is None or server_process.poll() is not None:
            reset_usage()
            break  # exit thread

        try:
            parent = psutil.Process(server_process.pid)
            processes = [parent] + parent.children(recursive=True)

            sum_cpu = 0.0
            ram = 0.0
            for p in processes:
                try:
                    sum_cpu += p.cpu_percent(interval=0.1)  # short interval for spikes
                    ram += p.memory_info().rss
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            cpu_usage = round(min(100.0, sum_cpu / cpu_count), 1)
            ram_usage = round(ram / (1024 ** 3), 2)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            reset_usage()

        time.sleep(0.5)

    reset_usage()  # ensure reset at the end

# ----------------- Helper Functions -----------------
def mc_to_html(text):
    colors = {
        "§0": "#000000","§1": "#0000AA","§2": "#00AA00","§3": "#00AAAA",
        "§4": "#AA0000","§5": "#AA00AA","§6": "#FFAA00","§7": "#AAAAAA",
        "§8": "#555555","§9": "#5555FF","§a": "#55FF55","§b": "#55FFFF",
        "§c": "#FF5555","§d": "#FF55FF","§e": "#FFFF55","§f": "#FFFFFF"
    }
    for code,color in colors.items():
        text = text.replace(code,f'<span style="color:{color}">')
    if "<span" in text:
        text += "</span>"*text.count("<span")
    return text

def read_console():
    global server_process, server_status, logs
    while server_process and server_process.poll() is None:
        line = server_process.stdout.readline()
        if not line: break
        line = line.rstrip("\n")
        with lock:
            logs.append(line)
            if len(logs) > 1000: logs.pop(0)

        if "Done (" in line:
            server_status = "ONLINE"
            if not os.path.exists(START_TIME_FILE):
                with open(START_TIME_FILE,"w") as f:
                    f.write(str(time.time()))

    server_status = "OFFLINE"
    server_process = None
    if os.path.exists(START_TIME_FILE):
        os.remove(START_TIME_FILE)
    reset_usage()  # reset immediately when stopped

def is_server_online(host="127.0.0.1", port=25565):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

# ----------------- Routes -----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global server_process, server_status
    if server_process is None or server_process.poll() is not None:
        server_status = "STARTING"
        server_process = subprocess.Popen(
            START_CMD,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        # Initialize CPU counters
        try:
            parent = psutil.Process(server_process.pid)
            parent.cpu_percent(None)
            for child in parent.children(recursive=True):
                child.cpu_percent(None)
        except:
            pass

        threading.Thread(target=read_console, daemon=True).start()
        threading.Thread(target=track_usage, daemon=True).start()  # start usage tracker
    return "ok"

@app.route("/stop", methods=["POST"])
def stop():
    global server_process, server_status
    if server_process and server_process.poll() is None:
        server_status = "STOPPING"
        server_process.stdin.write("stop\n")
        server_process.stdin.flush()
    return "ok"

@app.route("/kill", methods=["POST"])
def kill():
    global server_process, server_status
    if server_process and server_process.poll() is None:
        os.system(f"taskkill /F /T /PID {server_process.pid}")
        server_process = None
        server_status = "OFFLINE"
    reset_usage()
    return "ok"

@app.route("/logs")
def get_logs():
    html = ""
    with lock:
        for line in logs[-60:]:
            prefix = '<span style="color:#FFD700;font-weight:bold;">&lt;DynoHost Panel&gt;</span> '
            if "WARN" in line:
                line = f'<span class="warn">{line}</span>'
            elif "ERROR" in line:
                line = f'<span class="error">{line}</span>'
            elif "INFO" in line:
                line = f'<span class="info">{line}</span>'
            html += prefix + mc_to_html(line) + "<br>"
    return html

@app.route("/status")
def status():
    global server_status
    if server_process is None or server_process.poll() is None:
        server_status = "ONLINE" if is_server_online() else "OFFLINE"

    start_time = None
    if os.path.exists(START_TIME_FILE):
        with open(START_TIME_FILE,"r") as f:
            start_time = float(f.read().strip())

    return f"{server_status}|{start_time}"

@app.route("/usage")
def usage():
    global cpu_usage, ram_usage
    return {
        "cpu": cpu_usage,
        "ram": ram_usage,
        "ram_total": 8
    }

@app.route("/command", methods=["POST"])
def send_command():
    global server_process
    if server_process and server_process.poll() is None:
        data = request.get_json()
        cmd = data.get("command")
        if cmd:
            server_process.stdin.write(cmd + "\n")
            server_process.stdin.flush()
    return "ok"

# ----------------- File Explorer -----------------
@app.route("/files/", defaults={"current_path": ""})
@app.route("/files/<path:current_path>")
def files(current_path):
    abs_path = os.path.join(BASE_DIR,current_path)
    if not os.path.abspath(abs_path).startswith(BASE_DIR): abort(403)
    if not os.path.exists(abs_path): abort(404)

    entries = [{"name":name,"is_dir":os.path.isdir(os.path.join(abs_path,name))} for name in os.listdir(abs_path)]
    return render_template("files.html", files=entries, current_path=current_path)

@app.route("/download/<path:filename>")
def download(filename):
    safe_path = os.path.join(BASE_DIR, filename)
    if not os.path.abspath(safe_path).startswith(BASE_DIR): abort(403)
    if os.path.isfile(safe_path):
        return send_from_directory(BASE_DIR, filename, as_attachment=True)
    abort(404)

# ----------------- File Editor -----------------
@app.route("/edit/<path:filename>")
def edit_file(filename):
    abs_path = os.path.join(BASE_DIR, filename)
    if not os.path.abspath(abs_path).startswith(BASE_DIR):
        abort(403)
    if not os.path.isfile(abs_path):
        abort(404)
    
    with open(abs_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return render_template("edit.html", filename=filename, content=content)

@app.route("/save/<path:filename>", methods=["POST"])
def save_file(filename):
    abs_path = os.path.join(BASE_DIR, filename)
    if not os.path.abspath(abs_path).startswith(BASE_DIR):
        abort(403)
    
    data = request.get_json()
    new_content = data.get("content", "")
    
    # Backup
    backup_path = abs_path + ".bak"
    if os.path.exists(abs_path):
        with open(abs_path, "r", encoding="utf-8") as f:
            with open(backup_path, "w", encoding="utf-8") as b:
                b.write(f.read())
    
    # Save
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return {"status":"ok"}

# ----------------- Run -----------------
from flask_socketio import SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)