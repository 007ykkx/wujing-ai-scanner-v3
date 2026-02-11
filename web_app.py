import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from scanner import WujingScanner
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

active_scans = {}

@app.route('/')
def index():
    return "<h1>无镜AI扫描 V3</h1><p>后端运行中，请使用 API 或前端界面交互。</p>"

@app.route('/api/start_scan', methods=['POST'])
def start_scan():
    data = request.json
    target = data.get('target')
    custom_dict = data.get('custom_dict')
    
    if not target:
        return jsonify({"error": "未指定目标"}), 400
    
    scanner = WujingScanner(target, custom_dict=custom_dict)
    scan_id = target + "_" + str(len(active_scans))
    active_scans[scan_id] = scanner
    
    # 在后台线程运行扫描
    thread = threading.Thread(target=scanner.start)
    thread.start()
    
    return jsonify({"scan_id": scan_id, "message": "扫描已启动"}), 200

@app.route('/api/scan_status/<scan_id>', methods=['GET'])
def get_status(scan_id):
    scanner = active_scans.get(scan_id)
    if not scanner:
        return jsonify({"error": "扫描任务不存在"}), 404
    
    return jsonify({
        "status": scanner.status,
        "logs": scanner.logs
    })

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
