import os
import sys
from llm_agent import AIAgent
from config_manager import ConfigManager

def main():
    if len(sys.argv) < 2:
        print("用法: python scanner.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    config = ConfigManager()
    
    # 检查 API Key
    if config.get("ai.api_key") == "YOUR_API_KEY_HERE":
        print("[!] 请先在 config.json 中配置您的 AI API Key")
        sys.exit(1)

    agent = AIAgent()
    print(f"[+] 开始对目标 {target} 进行 AI 驱动的安全分析...")
    
    analysis_results = agent.execute_workflow(target)
    
    print("\n" + "="*50)
    print("AI 安全分析报告")
    print("="*50)
    for tool, analysis in analysis_results.items():
        print(f"\n[工具: {tool.upper()}]")
        print(analysis)
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
