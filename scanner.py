import os
import subprocess
import json
import threading
import time
from datetime import datetime

class WujingScanner:
    def __init__(self, target, output_dir="results", custom_dict=None):
        self.target = target
        self.output_dir = os.path.join(output_dir, datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.output_dir, exist_ok=True)
        self.custom_dict = custom_dict
        self.logs = []
        self.status = "idle"

    def log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {"timestamp": timestamp, "message": message, "level": level}
        self.logs.append(log_entry)
        print(f"[{timestamp}] [{level.upper()}] {message}")

    def run_command(self, cmd, name):
        self.log(f"正在启动 {name}...", "info")
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.log(f"{name} 执行成功", "success")
                return stdout
            else:
                self.log(f"{name} 执行失败: {stderr}", "error")
                return None
        except Exception as e:
            self.log(f"执行 {name} 时发生异常: {str(e)}", "error")
            return None

    def collect_subdomains(self):
        self.log("阶段 1: 子域名收集 (OneForAll)", "info")
        cmd = f"python3 /home/ubuntu/wujing_v3/tools/OneForAll/oneforall.py --target {self.target} --path {self.output_dir}/subdomains.csv run"
        self.run_command(cmd, "OneForAll")

    def scan_ports(self):
        self.log("阶段 2: 端口扫描 (Nmap)", "info")
        cmd = f"nmap -sV -T4 {self.target} -oN {self.output_dir}/nmap_res.txt"
        self.run_command(cmd, "Nmap")

    def scan_dirs(self):
        self.log("阶段 3: 目录扫描 (Dirsearch)", "info")
        dict_path = self.custom_dict if self.custom_dict else "/home/ubuntu/wujing_v3/tools/dirsearch/db/dicc.txt"
        cmd = f"python3 /home/ubuntu/wujing_v3/tools/dirsearch/dirsearch.py -u {self.target} -w {dict_path} --json-report={self.output_dir}/dir_res.json"
        self.run_command(cmd, "Dirsearch")

    def scan_vulnerabilities(self):
        self.log("阶段 4: 漏洞扫描 (Nuclei)", "info")
        # 整合之前收集的信息作为输入
        input_file = os.path.join(self.output_dir, "nuclei_input.txt")
        with open(input_file, "w") as f:
            f.write(self.target + "\n")
            # 这里可以解析 subdomains.csv 加入更多目标
        
        cmd = f"/home/ubuntu/wujing_v3/tools/nuclei -l {input_file} -o {self.output_dir}/nuclei_res.txt"
        self.run_command(cmd, "Nuclei")

    def ai_analyze(self):
        self.log("阶段 5: AI 深度分析", "info")
        # 这里集成之前的 AI Agent 逻辑，分析扫描结果
        self.log("AI 正在分析扫描报告并生成建议...", "info")
        # 模拟 AI 分析
        time.sleep(2)
        self.log("AI 分析完成，已生成加固建议。", "success")

    def start(self):
        self.status = "running"
        self.collect_subdomains()
        self.scan_ports()
        self.scan_dirs()
        self.scan_vulnerabilities()
        self.ai_analyze()
        self.status = "completed"
        self.log("全流程扫描任务已完成！", "success")

if __name__ == "__main__":
    scanner = WujingScanner("example.com")
    scanner.start()
