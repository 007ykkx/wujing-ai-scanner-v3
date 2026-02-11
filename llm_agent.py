import os
import subprocess
import json
from openai import OpenAI
from config_manager import ConfigManager

class AIAgent:
    def __init__(self):
        self.config = ConfigManager()
        self.client = OpenAI(
            api_key=self.config.get("ai.api_key"),
            base_url=self.config.get("ai.base_url")
        )
        self.model = self.config.get("ai.model")

    def run_tool(self, command):
        """执行系统命令并返回结果"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}

    def analyze_results(self, tool_name, output):
        """让 AI 分析工具输出的结果"""
        prompt = f"""
        你是一个专业的渗透测试专家。以下是工具 {tool_name} 的扫描结果：
        ---
        {output}
        ---
        请分析这些结果，识别潜在的高危漏洞，并给出具体的加固建议。
        如果结果中包含大量数据，请总结最关键的安全风险。
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个安全专家，擅长分析扫描报告。"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI 分析失败: {str(e)}"

    def execute_workflow(self, target):
        """AI 驱动的自动化工作流"""
        results = {}
        
        # 1. Nmap 扫描
        nmap_path = self.config.get("tools.nmap_path")
        print(f"[*] 正在运行 Nmap 扫描: {target}")
        nmap_res = self.run_tool(f"{nmap_path} -F {target}")
        results['nmap'] = self.analyze_results("Nmap", nmap_res.get('stdout', ''))

        # 2. Nuclei 扫描
        nuclei_path = self.config.get("tools.nuclei_path")
        print(f"[*] 正在运行 Nuclei 扫描: {target}")
        nuclei_res = self.run_tool(f"{nuclei_path} -u {target} -silent")
        results['nuclei'] = self.analyze_results("Nuclei", nuclei_res.get('stdout', ''))

        return results
