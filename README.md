# 无镜AI扫描 V3 (Wujing AI Scanner V3)

基于大语言模型（LLM）驱动的自动化安全渗透测试工具，集成多种专业安全工具链。

## 核心功能

- **资产收集**：集成 `OneForAll` 进行子域名收集。
- **端口探测**：集成 `Nmap` 进行服务识别与端口扫描。
- **目录爆破**：集成 `Dirsearch`，支持用户自定义字典。
- **漏洞扫描**：集成 `Nuclei` 进行全量漏洞扫描。
- **AI 分析**：利用 LLM 对扫描结果进行深度分析，提供加固建议。
- **Web 界面**：提供直观的扫描管理与实时日志查看。

## 快速开始

1. 安装依赖：
   ```bash
   pip3 install -r requirements.txt
   ```
2. 启动 Web 服务：
   ```bash
   python3 web_app.py
   ```

## 工具集成说明

本项目内置了以下工具：
- [OneForAll](https://github.com/shmilylty/OneForAll)
- [dirsearch](https://github.com/maurosoria/dirsearch)
- [nuclei](https://github.com/projectdiscovery/nuclei)
- [nmap](https://nmap.org/)

## 免责声明

本工具仅用于授权的安全测试，严禁用于非法用途。

## 本地编译指南

由于 GitHub 文件大小限制，建议在本地环境中将工具编译为 EXE：

1. **安装 PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **编译 dirsearch**:
   ```bash
   cd tools/dirsearch
   pyinstaller --onefile --name dirsearch dirsearch.py
   ```

3. **编译 OneForAll**:
   ```bash
   cd tools/OneForAll
   pyinstaller --onefile --name oneforall oneforall.py
   ```

编译后的文件将位于各自目录的 `dist` 文件夹中。请将它们移动到 `tools/bin/` 目录下，并在 `config.json` 中更新路径。
