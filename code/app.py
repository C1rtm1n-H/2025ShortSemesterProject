import streamlit as st
import asyncio
from langchain_openai import ChatOpenAI
from agent_logic import create_travel_agent, create_html_agent, get_langchain_plan, generate_html_itinerary, review_and_optimize_html
from tools_update1 import generate_ics_content
from datetime import datetime, timedelta

# ==================== Streamlit UI 设置 ====================
st.title("GGGroup 的AI 旅行计划器 ✈️ ")
st.caption("由大语言模型驱动，为您自动规划个性化行程。")

# 初始化 session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# ==================== 侧边栏配置 ====================
with st.sidebar:
    st.header("⚙️ 配置")
    
    model_type = st.selectbox(
        "选择您的 AI 模型:",
        ("OpenAI GPT-4o", "阿里云 Qwen (DashScope)")
    )

    api_key = None
    base_url = None
    model_id = None

    if model_type == "阿里云 Qwen (DashScope)":
        base_url = st.text_input(
            "API 基地址 (Base URL)",
            value="https://dashscope.aliyuncs.com/compatible-mode/v1",
            help="DashScope 提供的与 OpenAI 兼容的 API 地址。"
        )
        api_key = st.text_input("阿里云 DashScope API Key", type="password")
        model_id = "qwen-max"
    elif model_type == "OpenAI GPT-4o":
        api_key = st.text_input("输入 OpenAI API Key", type="password")
        model_id = "gpt-4o"

    serp_api_key = st.text_input("输入 Serp API Key (用于网络搜索)", type="password")

# ==================== 初始化客户端和 Agent ====================
agent_executor = None
html_agent_executor = None
if api_key and serp_api_key:
    try:
        llm = ChatOpenAI(
            model=model_id,
            api_key=api_key,
            base_url=base_url,
            temperature=0,
            streaming=True
        )
        agent_executor = asyncio.run(create_travel_agent(llm, serp_api_key))
        html_agent_executor = asyncio.run(create_html_agent(llm))
        html_agent_executor2 = asyncio.run(create_html_agent(llm))
    except Exception as e:
        st.error(f"初始化 AI 客户端或 Agent 时出错: {e}")

# ==================== 主界面 ====================
if agent_executor:
    st.header("📝 输入您的旅行需求")
    from_station = st.text_input("您的出发地", placeholder="例如：北京")
    to_station = st.text_input("您想去哪里？", placeholder="例如：日本东京")
    num_days = st.number_input("您想旅行多少天？", min_value=1, max_value=30, value=7)
    start_date = st.date_input("出发日期", value=datetime.today())
    
    if st.button("🚀 生成行程", use_container_width=True):
        if not to_station or not from_station:
            st.warning("请输入出发地和目的地。")
        else:
            st.session_state.itinerary = None
            with st.spinner("AI Agent 正在思考和规划中..."):
                try:
                    itinerary_text = asyncio.run(get_langchain_plan(agent_executor, from_station, to_station, num_days, start_date=start_date.strftime("%Y-%m-%d")))
                    st.session_state.itinerary = itinerary_text
                except Exception as e:
                    st.error(f"Agent 执行出错: {e}")
                    st.stop()

    if st.session_state.itinerary:
        st.header("📅 您的专属行程")
        st.markdown(st.session_state.itinerary)
    
        try:
            ics_content = generate_ics_content(st.session_state.itinerary)
            st.download_button(
            label="📥 下载为日历文件 (.ics)",
            data=ics_content,
            file_name=f"{to_station}_travel_itinerary.ics",
            mime="text/calendar",
            use_container_width=True
            )        
        except Exception as e:
            st.error(f"生成日历文件时出错: {e}")
        try:
            # 第一步：生成初始HTML
            initial_html = asyncio.run(generate_html_itinerary(html_agent_executor, st.session_state.itinerary))
                
            # 第二步：进行二次审查和优化
            with st.spinner("正在进行代码审查和优化..."):
                final_html = asyncio.run(review_and_optimize_html(html_agent_executor2, initial_html))
                
            st.session_state.final_html = final_html
                
            # 显示HTML预览
            st.subheader("HTML行程表预览")
            st.components.v1.html(final_html, height=800, scrolling=True)
                
            # 添加HTML下载按钮
            st.download_button(
                label="📥 下载HTML行程表 (.html)",
                data=final_html,
                file_name=f"{to_station}_travel_itinerary.html",
                mime="text/html",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"生成HTML文件时出错: {e}")
else:
    st.warning("👈 请在左侧边栏完成 API Key 配置以启动 Agent。")
