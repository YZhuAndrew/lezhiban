import json
import os
from datetime import datetime
from typing import List, Dict, Any

# 历史记录文件路径
HISTORY_FILE = "data/history_records.json"

def save_history_record(record: Dict[str, Any]) -> bool:
    """
    保存生成记录到历史文件
    
    Args:
        record (Dict[str, Any]): 生成记录数据
        
    Returns:
        bool: 保存成功返回True，否则返回False
    """
    try:
        # 确保data目录存在
        os.makedirs("data", exist_ok=True)
        
        # 读取现有记录
        records = load_history_records()
        
        # 添加时间戳
        record["timestamp"] = datetime.now().isoformat()
        
        # 添加到记录列表
        records.append(record)
        
        # 保存到文件（只保留最近100条记录）
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(records[-100:], f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"保存历史记录时出错: {e}")
        return False

def load_history_records() -> List[Dict[str, Any]]:
    """
    从文件加载历史记录
    
    Returns:
        List[Dict[str, Any]]: 历史记录列表
    """
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"加载历史记录时出错: {e}")
        return []

def clear_history_records() -> bool:
    """
    清空历史记录
    
    Returns:
        bool: 清空成功返回True，否则返回False
    """
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return True
    except Exception as e:
        print(f"清空历史记录时出错: {e}")
        return False

def format_history_record(record: Dict[str, Any]) -> str:
    """
    格式化历史记录为显示文本
    
    Args:
        record (Dict[str, Any]): 历史记录数据
        
    Returns:
        str: 格式化后的显示文本
    """
    try:
        # 解析时间戳
        timestamp = record.get("timestamp", "")
        if timestamp:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_str = "未知时间"
        
        # 获取日期信息
        date_str = record.get("date", "未知日期")
        weekday = record.get("weekday", "未知星期")
        
        # 获取天气信息
        weather = record.get("weather", "未知天气")
        
        # 获取特别注意事项
        special_notes = record.get("special_notes", "")
        
        # 构建显示文本
        display_text = f"时间: {time_str}\n"
        display_text += f"日期: {date_str} {weekday}\n"
        display_text += f"天气: {weather}\n"
        
        if special_notes and special_notes.strip():
            display_text += f"特别注意事项: {special_notes}\n"
        
        return display_text
    except Exception as e:
        return f"格式化记录时出错: {e}"