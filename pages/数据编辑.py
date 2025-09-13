import streamlit as st
from datetime import datetime, timedelta

# 导入自定义模块
from utils.data_manager import load_schedule_data, save_schedule_data
from utils.ui_components import render_course_editor, render_club_editor, render_duty_editor

# 设置页面配置
st.set_page_config(
    page_title="乐知班数据编辑器",
    page_icon="📅",
    layout="wide"
)

# 标题和说明
st.title("📅乐知班数据编辑器")

# 加载课程安排数据
if "schedule_data" not in st.session_state:
    st.session_state.schedule_data = load_schedule_data()

schedule_data = st.session_state.schedule_data

# 创建标签页用于不同类型的编辑
tab1, tab2, tab3 = st.tabs(["课程安排", "社团安排", "值日安排"])

# 课程安排编辑
with tab1:
    edited_course_data = render_course_editor(schedule_data)
    schedule_data["课程安排"] = edited_course_data

# 社团安排编辑
with tab2:
    edited_club_data = render_club_editor(schedule_data)
    schedule_data["社团安排"] = edited_club_data

# 值日安排编辑
with tab3:
    edited_duty_data = render_duty_editor(schedule_data)
    schedule_data["值日安排"] = edited_duty_data

# 保存按钮
if st.button("保存所有更改"):
    if save_schedule_data(schedule_data):
        st.success("数据已保存成功！")
        st.session_state.schedule_data = schedule_data
    else:
        st.error("数据保存失败！")

# 返回主页面的链接
st.markdown("---")
if st.button("返回主页面"):
    st.switch_page("温馨提醒生成器.py")