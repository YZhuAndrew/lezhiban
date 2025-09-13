from typing import Dict, Any
from datetime import date

def generate_reminder_content(
    selected_date: date, 
    selected_weekday: str, 
    weather: str, 
    schedule_data: Dict[str, Any],
    special_notes: str = ""
) -> str:
    """
    生成班级温馨提示内容
    
    Args:
        selected_date (datetime): 选定的日期
        selected_weekday (str): 选定的星期
        weather (str): 天气信息
        schedule_data (Dict[str, Any]): 课程安排数据
        special_notes (str): 特别注意事项（可选）
        
    Returns:
        str: 生成的提醒内容
    """
    # 提取选定日期的信息
    courses = schedule_data.get("课程安排", {}).get(selected_weekday, {})
    clubs = schedule_data.get("社团安排", {}).get(selected_weekday, [])
    duty_students = schedule_data.get("值日安排", {}).get(selected_weekday, "")
    
    # 格式化日期
    date_str = f"{selected_date.month}月{selected_date.day}日"
    
    # 构建提示内容
    reminder = f"📅乐知班明日温馨提醒\n"
    reminder += f"⏰・[{date_str}] [{selected_weekday}]⏰\n\n"
    
    # 天气信息
    reminder += f"🌤️明日天气：\n"
    reminder += f"・{weather}\n\n"
    
    # 课程安排
    reminder += f"📚明日课程安排：\n"
    if courses:
        morning_classes = courses.get("上午", [])
        afternoon_classes = courses.get("下午", [])
        reminder += f"・上午：{', '.join([f'[{cls}]' for cls in morning_classes])}\n"
        reminder += f"・下午：{', '.join([f'[{cls}]' for cls in afternoon_classes])}\n\n"
    else:
        reminder += f"・明日无课程安排\n\n"
    
    # 社团安排
    reminder += f"🎨社团课程安排：\n"
    if clubs:
        for club in clubs:
            # 提取社团名称的主要部分（去除括号内容）
            club_name = club["社团名称"].split("（")[0]
            # 处理特殊字符，如"-"或"/"
            if "-" in club_name or "/" in club_name:
                club_name = club_name.split("-")[0].split("/")[0]
            members = ", ".join(club["成员"])
            reminder += f"・{club_name}小组：{members}\n"
        reminder += "\n"
    else:
        reminder += f"・明日无社团活动\n\n"
    
    # 值日生安排
    reminder += f"🧹值日生安排：\n"
    reminder += f"・{duty_students}\n\n" if duty_students else "・明日无值日生安排\n\n"
    
    # 着装提醒
    reminder += f"👔着装提醒：\n"
    if selected_weekday == "星期一":
        reminder += f"・❗️明天是星期一，大家穿校服，戴红领巾。\n\n"
    reminder += f"・干净舒适即可\n\n"
    
    # 特别注意事项
    if special_notes and special_notes.strip():
        reminder += f"❗📢特别注意事项：\n"
        # 将特别注意事项按行分割并添加项目符号
        notes_lines = special_notes.strip().split('\n')
        for line in notes_lines:
            if line.strip():  # 忽略空行
                reminder += f"・{line.strip()}\n"
        reminder += "\n"
    
    # 其他注意事项
    reminder += f"📌其他注意事项\n"
    reminder += "・1.请带好明天所需的学习用品和课本\n"
    reminder += "・2.注意休息，保证充足睡眠，准时到校\n\n"
    
    return reminder

def format_club_name(club_name: str) -> str:
    """
    格式化社团名称，去除括号和特殊字符
    
    Args:
        club_name (str): 原始社团名称
        
    Returns:
        str: 格式化后的社团名称
    """
    # 去除括号内容
    if "（" in club_name:
        club_name = club_name.split("（")[0]
    
    # 处理特殊字符
    if "-" in club_name:
        club_name = club_name.split("-")[0]
    if "/" in club_name:
        club_name = club_name.split("/")[0]
    
    return club_name.strip()