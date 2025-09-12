import streamlit as st
from datetime import datetime, timedelta

# 导入自定义模块
from utils.data_manager import load_schedule_data
from utils.weather_service import get_weather_info
from utils.reminder_generator import generate_reminder_content
from utils.ui_components import render_data_editor

# 设置页面配置
st.set_page_config(
    page_title="乐知班每日温馨提醒生成器",
    page_icon="📅",
    layout="wide"
)

# 标题和说明
st.title("📅乐知班每日温馨提醒生成器")
# st.write("点击下方按钮生成明日的班级温馨提示")

# 加载课程安排数据
schedule_data = load_schedule_data()

# 获取当前日期和明日日期
today = datetime.now()

# 添加日期选择器
selected_date = st.date_input("日期（默认为明天）", value=today + timedelta(days=1))
# selected_date = st.markdown(today + timedelta(days=1))

# 获取星期几（中文）
weekday_map = {
    0: "星期一",
    1: "星期二",
    2: "星期三",
    3: "星期四",
    4: "星期五",
    5: "星期六",
    6: "星期日"
}

selected_weekday = weekday_map[selected_date.weekday()]

# 显示日期信息
col1, col2 = st.columns(2)
with col1:
    st.info(f"当前日期：{today.strftime('%Y年%m月%d日')} {weekday_map[today.weekday()]}")
with col2:
    st.info(f"生成对象：{selected_date.strftime('%Y年%m月%d日')} {selected_weekday}")

# 默认城市设置为上饶市信州区
city = '101240701' # "上饶市信州区"

# 当日期改变时，自动更新天气信息
# 使用session_state来存储天气信息，避免每次重新计算
if 'weather_info' not in st.session_state or 'last_selected_date' not in st.session_state or st.session_state.last_selected_date != selected_date:
    st.session_state.weather_info = get_weather_info(city)
    st.session_state.last_selected_date = selected_date if selected_date else None

# 创建两列布局，一列用于天气输入框，另一列用于更新按钮
weather_col, button_col = st.columns([3, 1])
with weather_col:
    weather = st.text_input("天气查询结果", st.session_state.weather_info, key="weather_input_field")
with button_col:
    # 添加更新天气按钮
    if st.button("更新天气", key="update_weather_btn", use_container_width=True):
        # 手动更新天气信息
        with st.spinner("正在获取最新天气信息..."):
            st.session_state.weather_info = get_weather_info(city)
            st.session_state.last_selected_date = selected_date
            # 重新运行应用以更新界面
            st.rerun()

# LLM API设置
# with st.expander("LLM API设置（可选）"):
#     api_provider = st.selectbox("选择API提供商", ["不使用", "OpenAI", "Anthropic"], index=0)
#     api_key = st.text_input("API密钥", type="password")

# 生成温馨提示的函数
def generate_reminder():
    return generate_reminder_content(selected_date, selected_weekday, weather, schedule_data)

# 生成按钮
if st.button("生成乐知班温馨提示", key="generate_btn", use_container_width=True):
    reminder_text = generate_reminder()
    
    # 显示生成的提示
    st.subheader("生成的温馨提示：")
    st.code(reminder_text, language="``")
    
    # # 复制功能
    # st.download_button(
    #     label="复制/下载温馨提示",
    #     data=reminder_text,
    #     file_name=f"班级每日温馨提示_{selected_date.strftime('%Y%m%d')}.md",
    #     mime="text/markdown"
    # )
    # st.success("点击上方按钮可复制或下载温馨提示内容！")

# 在页面底部添加编辑界面的入口
st.markdown("---")
if st.checkbox("显示数据编辑界面"):
    render_data_editor(schedule_data)
