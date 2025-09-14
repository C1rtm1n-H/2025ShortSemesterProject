# 2025ShortSemesterProject
# AI 旅行计划 Agent ✈️

这是一个基于大语言模型（LLM）的智能旅行计划 Agent。它可以根据用户的个性化需求，自动生成一份详尽、合理、图文并茂的旅行计划。

本项目是 2025 短学期课程《人工智能工程实践》的大作业。

## 核心功能

- **个性化输入**: 用户可以提供目的地、旅行天数以及兴趣偏好。
- **智能行程规划**: Agent 能理解用户需求，并调用外部工具（如地图API）来获取真实的景点和餐厅信息。
- **优化路线**: 自动将地理位置相近的地点规划在同一天，避免行程奔波。
- **结构化输出**: 生成一份清晰的每日行程单（Day-by-Day Itinerary），包含活动、餐饮和交通建议。

## 技术架构

本项目采用以 LLM 为核心的 Agent 架构，主要技术栈如下：

- **语言模型 (LLM)**: 支持工具调用（Tool Calling）功能的大模型。
- **Agent 框架**: [LangChain](https://www.langchain.com/)，用于实现 Agent 的核心逻辑（思考、调用工具、整合信息）。
- **外部工具 (APIs)**:
    - **网页搜索**: `search_web`，对接 **SerpAPI**，提供通用网络搜索能力。
    - **其他搜索**: `search_google_maps`, `search_weather`, `search_flights`，对接 **Apify** 平台上的多个Actor，分别用于抓取地图、天气和航班数据。
    - **12306车票查询**: 通过 `langchain-mcp-adapters` 库启动一个本地的 `12306-mcp` 服务，使其成为Agent可以调用的工具，实现了国内火车票信息的查询。
    - **B站视频搜索**:通过 `langchain-mcp-adapters` 库启动一个本地的 `bilibili-mcp-server` 服务，使其成为Agent可以调用的工具，实现了对B站视频的搜索和信息获取。
    - **日历生成**: 函数`generate_ics_content`，利用 `icalendar` 库将文本行程解析并生成标准的日历文件。
- **应用界面 (UI)**: [Streamlit](https://streamlit.io/)，用于快速搭建交互式 Web 界面。
- **编程语言**: Python

## 文件结构

项目代码结构如下：

```
.
├── README.md                   # 项目说明
├── recommendation.md           # 初期规划文档
└── code                        # Python 依赖包
    ├── app.py                  # Streamlit 应用主程序
    ├── agent_logic.py          # Agent 核心逻辑
    ├── tools.py                # 外部 API 工具函数
    └── requirements.txt        # 项目依赖
```

## 如何运行

1.  **12306-mcp**：
    - 下载node.js:https://nodejs.org/zh-cn/download
    - 下载12306-mcp:
    ```bash
        git clone https://github.com/Joooook/12306-mcp.git
        cd 12306-mcp
        npm i
        cd ..
    ```

2.  **bilibili-mcp-server**：
    - 下载uv：
    ```bash
        pip install uv
    ```
    - 下载bilibilib-mcp-server：
    ```bash
        git clone https://github.com/huccihuang/bilibili-mcp-server.git
        cd bilibili-mcp-server
        uv sync
        cd ..
    ```

3.  **切换到 code 目录**：
    ```bash
        cd ./code
    ```

4.  **安装依赖**:
    ```bash
        pip install -r requirements.txt
    ```
5.  **启动应用**:
    ```bash
        streamlit run app.py
    ```

之后在浏览器中打开相应地址即可与旅行 Agent 进行交互。
