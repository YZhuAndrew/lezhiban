import json
import streamlit as st
from typing import Dict, Any
import os

# 定义数据文件路径
DATA_FILE_PATH = 'schedule_data.json'
BACKUP_DIR = 'data/backups'

def load_schedule_data() -> Dict[str, Any]:
    """
    从JSON文件加载课程安排数据
    
    Returns:
        Dict[str, Any]: 课程安排数据
    """
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(f"找不到{DATA_FILE_PATH}文件，请确保文件存在")
        return {}
    except json.JSONDecodeError as e:
        st.error(f"{DATA_FILE_PATH}文件格式错误，请检查JSON格式: {str(e)}")
        return {}
    except Exception as e:
        st.error(f"加载数据时发生未知错误: {str(e)}")
        return {}

def save_schedule_data(data: Dict[str, Any]) -> bool:
    """
    将课程安排数据保存到JSON文件
    
    Args:
        data (Dict[str, Any]): 要保存的课程安排数据
        
    Returns:
        bool: 保存是否成功
    """
    try:
        # 创建备份
        create_backup()
        
        # 保存数据
        with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"保存数据时出错：{str(e)}")
        return False

def create_backup() -> bool:
    """
    创建数据文件备份
    
    Returns:
        bool: 备份是否成功
    """
    try:
        # 确保备份目录存在
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # 生成备份文件名（带时间戳）
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"schedule_data_backup_{timestamp}.json")
        
        # 复制当前数据文件作为备份
        if os.path.exists(DATA_FILE_PATH):
            import shutil
            shutil.copy2(DATA_FILE_PATH, backup_path)
            return True
        return False
    except Exception as e:
        st.warning(f"创建备份时出错：{str(e)}")
        return False

def validate_schedule_data(data: Dict[str, Any]) -> bool:
    """
    验证课程安排数据格式
    
    Args:
        data (Dict[str, Any]): 要验证的课程安排数据
        
    Returns:
        bool: 数据是否有效
    """
    try:
        # 检查必需的顶级键
        required_keys = ["课程安排", "社团安排", "值日安排"]
        for key in required_keys:
            if key not in data:
                st.error(f"数据缺少必需的键: {key}")
                return False
        
        # 验证课程安排结构
        course_data = data.get("课程安排", {})
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五"]
        for weekday in weekdays:
            if weekday in course_data:
                day_data = course_data[weekday]
                if not isinstance(day_data, dict):
                    st.error(f"{weekday}的课程安排格式错误")
                    return False
                if "上午" not in day_data or "下午" not in day_data:
                    st.error(f"{weekday}的课程安排缺少上午或下午字段")
                    return False
        
        # 验证社团安排结构
        club_data = data.get("社团安排", {})
        for weekday in weekdays:
            if weekday in club_data:
                clubs = club_data[weekday]
                if not isinstance(clubs, list):
                    st.error(f"{weekday}的社团安排格式错误")
                    return False
                for club in clubs:
                    if not isinstance(club, dict) or "社团名称" not in club or "成员" not in club:
                        st.error(f"{weekday}的社团信息格式错误")
                        return False
        
        # 验证值日安排结构
        duty_data = data.get("值日安排", {})
        for weekday in weekdays:
            if weekday in duty_data:
                if not isinstance(duty_data[weekday], str):
                    st.error(f"{weekday}的值日安排格式错误")
                    return False
        
        return True
    except Exception as e:
        st.error(f"验证数据时出错：{str(e)}")
        return False