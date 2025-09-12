import streamlit as st
from typing import Dict, Any, List
import os
import json
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
    渲染课程安排编辑界面
    
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
    
    for weekday in weekdays:
        st.markdown(f"#### {weekday}")
        weekday_data = course_data.get(weekday, {"上午": [], "下午": []})
        
        # 编辑上午课程
        st.markdown("##### 上午课程")
        morning_classes = weekday_data.get("上午", [])
        morning_count = st.number_input(
            f"{weekday}上午课程数量", 
            min_value=0, 
            max_value=10, 
            value=len(morning_classes), 
            key=f"{weekday}_morning_count"
        )
        
        edited_morning = []
        for i in range(morning_count):
            default_value = morning_classes[i] if i < len(morning_classes) else ""
            class_name = st.text_input(
                f"{weekday}上午第{i+1}节课", 
                value=default_value, 
                key=f"{weekday}_morning_{i}"
            )
            edited_morning.append(class_name)
        
        # 编辑下午课程
        st.markdown("##### 下午课程")
        afternoon_classes = weekday_data.get("下午", [])
        afternoon_count = st.number_input(
            f"{weekday}下午课程数量", 
            min_value=0, 
            max_value=10, 
            value=len(afternoon_classes), 
            key=f"{weekday}_afternoon_count"
        )
        
        edited_afternoon = []
        for i in range(afternoon_count):
            default_value = afternoon_classes[i] if i < len(afternoon_classes) else ""
            class_name = st.text_input(
                f"{weekday}下午第{i+1}节课", 
                value=default_value, 
                key=f"{weekday}_afternoon_{i}"
            )
            edited_afternoon.append(class_name)
        
        edited_course_data[weekday] = {
            "上午": edited_morning,
            "下午": edited_afternoon
        }
    
    return edited_course_data

def render_club_editor(schedule_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    渲染社团安排编辑界面
    
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
    
    for weekday in weekdays:
        st.markdown(f"#### {weekday}")
        weekday_clubs = club_data.get(weekday, [])
        
        # 控制社团数量
        club_count = st.number_input(
            f"{weekday}社团数量", 
            min_value=0, 
            max_value=20, 
            value=len(weekday_clubs), 
            key=f"{weekday}_club_count"
        )
        
        edited_clubs = []
        for i in range(club_count):
            club = weekday_clubs[i] if i < len(weekday_clubs) else {"成员": [], "社团名称": ""}
            
            st.markdown(f"##### 社团 {i+1}")
            club_name = st.text_input(
                f"{weekday}社团{i+1}名称", 
                value=club.get("社团名称", ""), 
                key=f"{weekday}_club_{i}_name"
            )
            
            # 编辑成员列表
            members = club.get("成员", [])
            member_str = st.text_area(
                f"{weekday}社团{i+1}成员（用逗号分隔）", 
                value="，".join(members), 
                key=f"{weekday}_club_{i}_members"
            )
            
            # 将成员字符串转换为列表
            member_list = [m.strip() for m in member_str.split("，") if m.strip()]
            
            edited_clubs.append({
                "社团名称": club_name,
                "成员": member_list
            })
        
        edited_club_data[weekday] = edited_clubs
    
    return edited_club_data

def render_duty_editor(schedule_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    渲染值日安排编辑界面
    
    Args:
        schedule_data (Dict[str, Any]): 当前的值日安排数据
        
    Returns:
        Dict[str, Any]: 编辑后的值日安排数据
    """
    st.subheader("值日安排编辑")
    duty_data = schedule_data.get("值日安排", {})
    
    # 为每个星期创建编辑区域
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五"]
    edited_duty_data = {}
    
    for weekday in weekdays:
        duty_students = duty_data.get(weekday, "")
        edited_duty = st.text_area(
            f"{weekday}值日生", 
            value=duty_students, 
            key=f"{weekday}_duty_students",
            help="请输入值日生姓名，用逗号或顿号分隔"
        )
        edited_duty_data[weekday] = edited_duty
    
    return edited_duty_data