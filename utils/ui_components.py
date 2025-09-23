import streamlit as st
from typing import Dict, Any, List
import os
import json
import pandas as pd
from utils.data_manager import save_schedule_data, load_schedule_data

def render_data_editor(schedule_data: Dict[str, Any]) -> None:
    """
    渲染数据编辑界面
    
    Args:
        schedule_data (Dict[str, Any]): 当前的课程安排数据
    """
    st.subheader(".schedule_data.json 数据编辑界面")
    
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
            st.rerun()

def render_course_editor(schedule_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    渲染课程安排编辑界面（表格形式）
    
    Args:
        schedule_data (Dict[str, Any]): 当前的课程安排数据
        
    Returns:
        Dict[str, Any]: 编辑后的课程安排数据
    """
    st.subheader("课程安排编辑")
    course_data = schedule_data.get("课程安排", {})
    
    # 为每个星期创建编辑区域
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五"]
    edited_course_data = {}
    
    # 创建一个选项卡用于每个星期
    weekday_tabs = st.tabs(weekdays)
    
    for i, weekday in enumerate(weekdays):
        with weekday_tabs[i]:
            weekday_data = course_data.get(weekday, {"上午": [], "下午": []})
            
            # 获取上午和下午的课程
            morning_classes = weekday_data.get("上午", [])
            afternoon_classes = weekday_data.get("下午", [])
            
            # 确保上午和下午的课程列表长度一致（至少8节课）
            max_classes = max(len(morning_classes), len(afternoon_classes), 8)
            
            # 创建DataFrame用于编辑
            course_df_data = {
                "节次": [f"第{j+1}节" for j in range(max_classes)],
                "上午": morning_classes + [""] * (max_classes - len(morning_classes)),
                "下午": afternoon_classes + [""] * (max_classes - len(afternoon_classes))
            }
            
            course_df = pd.DataFrame(course_df_data)
            
            # 使用data_editor编辑课程表
            st.markdown(f"##### {weekday} 课程表")
            edited_df = st.data_editor(
                course_df,
                num_rows="fixed",
                key=f"course_editor_{weekday}",
                use_container_width=True
            )
            
            # 从编辑后的DataFrame中提取数据
            edited_morning = [row["上午"] for _, row in edited_df.iterrows() if row["上午"].strip()]
            edited_afternoon = [row["下午"] for _, row in edited_df.iterrows() if row["下午"].strip()]
            
            edited_course_data[weekday] = {
                "上午": edited_morning,
                "下午": edited_afternoon
            }
    
    return edited_course_data

def render_club_editor(schedule_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    渲染社团安排编辑界面（表格形式）
    
    Args:
        schedule_data (Dict[str, Any]): 当前的社团安排数据
        
    Returns:
        Dict[str, Any]: 编辑后的社团安排数据
    """
    st.subheader("社团安排编辑")
    club_data = schedule_data.get("社团安排", {})
    
    # 为每个星期创建编辑区域
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五"]
    edited_club_data = {}
    
    # 创建一个选项卡用于每个星期
    weekday_tabs = st.tabs(weekdays)
    
    for i, weekday in enumerate(weekdays):
        with weekday_tabs[i]:
            weekday_clubs = club_data.get(weekday, [])
            
            # 如果没有社团数据，创建一个空的社团列表
            if not weekday_clubs:
                weekday_clubs = [{"社团名称": "", "成员": []}]
            
            # 创建社团数据列表用于编辑
            club_edit_data = []
            for j, club in enumerate(weekday_clubs):
                club_edit_data.append({
                    "社团名称": club.get("社团名称", ""),
                    "成员": "，".join(club.get("成员", []))
                })
            
            # 如果社团数量较少，添加一些空行以便编辑
            while len(club_edit_data) < 5:
                club_edit_data.append({"社团名称": "", "成员": ""})
            
            # 创建DataFrame用于编辑
            club_df = pd.DataFrame(club_edit_data)
            
            # 使用data_editor编辑社团表
            st.markdown(f"##### {weekday} 社团安排")
            edited_df = st.data_editor(
                club_df,
                num_rows="dynamic",
                key=f"club_editor_{weekday}",
                use_container_width=True,
                column_config={
                    "社团名称": st.column_config.TextColumn("社团名称", required=False),
                    "成员": st.column_config.TextColumn("成员（用逗号分隔）", required=False)
                }
            )
            
            # 从编辑后的DataFrame中提取数据
            edited_clubs = []
            for _, row in edited_df.iterrows():
                # 检查空值并处理
                club_name = row["社团名称"] or ""
                members_str = row["成员"] or ""
                if club_name.strip() or members_str.strip():
                    # 将成员字符串转换为列表
                    members = [m.strip() for m in members_str.split("，") if m.strip()]
                    edited_clubs.append({
                        "社团名称": club_name,
                        "成员": members
                    })
            
            edited_club_data[weekday] = edited_clubs
    
    return edited_club_data

def render_duty_editor(schedule_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    渲染值日安排编辑界面（表格形式）
    
    Args:
        schedule_data (Dict[str, Any]): 当前的值日安排数据
        
    Returns:
        Dict[str, Any]: 编辑后的值日安排数据
    """
    st.subheader("值日安排编辑")
    duty_data = schedule_data.get("值日安排", {})
    
    # 为每个星期创建编辑区域
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五"]
    
    # 创建一个DataFrame用于编辑所有星期的值日生
    duty_edit_data = []
    for weekday in weekdays:
        duty_students = duty_data.get(weekday, "")
        duty_edit_data.append({
            "星期": weekday,
            "值日生": duty_students
        })
    
    duty_df = pd.DataFrame(duty_edit_data)
    
    # 使用data_editor编辑值日生表
    st.markdown("##### 值日生安排表")
    edited_df = st.data_editor(
        duty_df,
        num_rows="fixed",
        key="duty_editor",
        use_container_width=True,
        column_config={
            "星期": st.column_config.TextColumn("星期", disabled=True),
            "值日生": st.column_config.TextColumn("值日生（用逗号分隔）", required=False)
        }
    )
    
    # 从编辑后的DataFrame中提取数据
    edited_duty_data = {}
    for _, row in edited_df.iterrows():
        edited_duty_data[row["星期"]] = row["值日生"]
    
    return edited_duty_data