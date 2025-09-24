#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成适合手机阅读的温馨提醒网页
"""

import re
import os
from datetime import datetime, timedelta

def parse_reminder_content(reminder_text):
    """
    解析温馨提醒内容，提取各个部分信息
    
    Args:
        reminder_text (str): 温馨提醒文本内容
        
    Returns:
        dict: 解析后的提醒信息字典
    """
    result = {
        'date': '',
        'weekday': '',
        'weather': '',
        'weather_emoji': '',
        'morning_courses': [],
        'afternoon_courses': [],
        'clubs': [],
        'duty_students': [],
        'dress_code': '',
        'special_notes': []
    }
    
    # 提取日期和星期
    date_match = re.search(r'⏰・\[(.*?)\] \[(.*?)\]⏰', reminder_text)
    if date_match:
        result['date'] = date_match.group(1)
        result['weekday'] = date_match.group(2)
    
    # 提取天气信息
    weather_match = re.search(r'(.*?)明日天气：\n・(.*?)\n', reminder_text)
    if weather_match:
        result['weather_emoji'] = weather_match.group(1)
        result['weather'] = weather_match.group(2)
    
    # 提取上午课程
    morning_match = re.search(r'・上午：(.*?)\n', reminder_text)
    if morning_match:
        morning_text = morning_match.group(1)
        # 提取【】中的课程名称
        result['morning_courses'] = re.findall(r'【(.*?)】', morning_text)
    
    # 提取下午课程
    afternoon_match = re.search(r'・下午：(.*?)\n', reminder_text)
    if afternoon_match:
        afternoon_text = afternoon_match.group(1)
        # 提取【】中的课程名称
        result['afternoon_courses'] = re.findall(r'【(.*?)】', afternoon_text)
    
    # 提取社团安排
    club_section = re.search(r'🎨社团课程安排：\n(.*?)\n\n', reminder_text, re.DOTALL)
    if club_section:
        club_lines = club_section.group(1).strip().split('\n')
        for line in club_lines:
            if line.startswith('・'):
                # 提取社团名称和成员
                club_match = re.search(r'・【(.*?)】：(.*)', line)
                if club_match:
                    result['clubs'].append({
                        'name': club_match.group(1),
                        'members': club_match.group(2)
                    })
    
    # 提取值日生安排
    duty_match = re.search(r'🧹值日生安排：\n・(.*)\n', reminder_text)
    if duty_match:
        duty_text = duty_match.group(1)
        # 解析值日生，识别组长
        duty_items = duty_text.split('、')
        for item in duty_items:
            if '[组长]' in item:
                result['duty_students'].append({
                    'name': item.replace('[组长]', ''),
                    'is_leader': True
                })
            else:
                result['duty_students'].append({
                    'name': item,
                    'is_leader': False
                })
    
    # 提取着装提醒
    dress_match = re.search(r'👔着装提醒：\n・(.*)\n', reminder_text)
    if dress_match:
        result['dress_code'] = dress_match.group(1)
    
    # 提取特别注意事项
    special_section = re.search(r'⚠️📢特别注意事项：\n(.*?)\n\n', reminder_text, re.DOTALL)
    if special_section:
        special_lines = special_section.group(1).strip().split('\n')
        for line in special_lines:
            if line.startswith('・❗️'):
                result['special_notes'].append(line.replace('・❗️', '').strip())
    
    return result

def generate_mobile_html(reminder_info, template_path='templates/image_template.html'):
    """
    根据提醒信息生成适合手机阅读的HTML页面
    
    Args:
        reminder_info (dict): 解析后的提醒信息
        template_path (str): 模板文件路径
        
    Returns:
        str: 生成的HTML内容
    """
    
    # 读取模板文件
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # 构建课程安排HTML
    courses_html = ""
    if reminder_info['morning_courses'] or reminder_info['afternoon_courses']:
        courses_html += '<div class="course-section">'
        if reminder_info['morning_courses']:
            courses_html += '<div class="course-period">'
            courses_html += '<div class="period-label">上午：</div>'
            courses_html += '<div class="course-list">'
            for course in reminder_info['morning_courses']:
                courses_html += f'<div class="course-item">{course}</div>'
            courses_html += '</div></div>'
        
        if reminder_info['afternoon_courses']:
            courses_html += '<div class="course-period">'
            courses_html += '<div class="period-label">下午：</div>'
            courses_html += '<div class="course-list">'
            for course in reminder_info['afternoon_courses']:
                courses_html += f'<div class="course-item">{course}</div>'
            courses_html += '</div></div>'
        courses_html += '</div>'
    
    # 构建社团安排HTML
    clubs_html = ""
    for club in reminder_info['clubs']:
        clubs_html += '<div class="club-item">'
        clubs_html += f'<span class="emoji">🎨</span>'
        clubs_html += f'<span><strong>{club["name"]}：</strong>{club["members"]}</span>'
        clubs_html += '</div>'
    
    # 构建值日生安排HTML
    duty_html = ""
    if reminder_info['duty_students']:
        duty_html += '<div class="duty-list">'
        for duty in reminder_info['duty_students']:
            leader_class = ' group-leader' if duty['is_leader'] else ''
            duty_html += f'<div class="duty-item{leader_class}">{duty["name"]}</div>'
        duty_html += '</div>'
    
    # 构建特别注意事项HTML
    special_html = ""
    if reminder_info['special_notes']:
        special_html += '<div class="notice-content">'
        for note in reminder_info['special_notes']:
            # 高亮显示书名号中的内容
            note_with_highlight = re.sub(r'《(.*?)》', r'<span class="highlight">《\1》</span>', note)
            special_html += f'<span class="emoji">❗️</span> {note_with_highlight} <span class="emoji">☺️</span>'
        special_html += '</div>'
    
    # 替换模板中的占位符
    html_content = template_content.replace(
        '<h2><span class="emoji">⏰</span> 9月23日 星期二</h2>',
        f'<h2><span class="emoji">⏰</span> {reminder_info["date"]} {reminder_info["weekday"]}</h2>'
    )
    
    html_content = html_content.replace(
        '<span class="emoji">🌧️</span>\n                <span>小雨，低温 25℃~高温 33℃</span>',
        f'<span class="emoji">{reminder_info["weather_emoji"]}</span>\n                <span>{reminder_info["weather"]}</span>'
    )
    
    html_content = html_content.replace(
        '<div class="course-section">\n                <div class="course-period">\n                    <div class="period-label">上午：</div>\n                    <div class="course-list">\n                        <div class="course-item">数学</div>\n                        <div class="course-item">语文</div>\n                        <div class="course-item">书法</div>\n                        <div class="course-item">道德与法治</div>\n                    </div>\n                </div>\n                <div class="course-period">\n                    <div class="period-label">下午：</div>\n                    <div class="course-list">\n                        <div class="course-item">体育</div>\n                        <div class="course-item">音乐</div>\n                        <div class="course-item">数学作业辅导</div>\n                        <div class="course-item">经典领读</div>\n                    </div>\n                </div>\n            </div>',
        courses_html
    )
    
    html_content = html_content.replace(
        '<div class="club-item">\n                <span class="emoji">🥋</span>\n                <span><strong>武术：</strong>夏润修</span>\n            </div>',
        clubs_html
    )
    
    html_content = html_content.replace(
        '<div class="duty-list">\n                <div class="duty-item group-leader">周致远</div>\n                <div class="duty-item">苏心怡</div>\n                <div class="duty-item">徐之妍</div>\n                <div class="duty-item">徐之恒</div>\n                <div class="duty-item">余书洛</div>\n                <div class="duty-item">王赟艺</div>\n                <div class="duty-item">王宸亿</div>\n                <div class="duty-item">郑子其</div>\n            </div>',
        duty_html
    )
    
    html_content = html_content.replace(
        '<p>干净舒适即可</p>',
        f'<p>{reminder_info["dress_code"]}</p>'
    )
    
    if special_html:
        html_content = html_content.replace(
            '<div class="notice-content">\n                    <span class="emoji">❗️</span> 周三有录课安排，麻烦家长们提醒孩子们听\n                    <span class="highlight">《爱我中华》</span>和\n                    <span class="highlight">《我和我的祖国》</span>\n                    两首歌，会跟着哼唱 <span class="emoji">☺️</span>\n                </div>',
            special_html
        )
    else:
        # 如果没有特别注意事项，隐藏整个特别注意事项卡片
        html_content = re.sub(
            r'<div class="card">\s*<div class="card-title">\s*<span class="emoji">👔</span>\s*<span>着装提醒</span>\s*</div>\s*<p>.*?</p>\s*</div>\s*<div class="card">\s*<div class="notice-section">\s*<div class="notice-title">\s*<span class="emoji">⚠️</span>\s*<span>特别注意事项</span>\s*</div>\s*<div class="notice-content">\s*<span class="emoji">❗️</span>.*?<span class="emoji">☺️</span>\s*</div>\s*</div>\s*</div>',
            '<div class="card">\n                <div class="card-title">\n                    <span class="emoji">👔</span>\n                    <span>着装提醒</span>\n                </div>\n                <p>' + reminder_info["dress_code"] + '</p>\n            </div>',
            html_content,
            flags=re.DOTALL
        )
    
    return html_content

def generate_mobile_page(reminder_text, target_date=None):
    """
    生成手机网页文件
    
    Args:
        reminder_text (str): 温馨提醒文本内容
        target_date (datetime): 目标日期，如果为None则使用明天
        
    Returns:
        tuple: (html_content, file_path) 生成的HTML内容和文件路径
    """
    # 解析提醒内容
    reminder_info = parse_reminder_content(reminder_text)
    
    # 生成HTML内容
    html_content = generate_mobile_html(reminder_info)
    
    # 确定输出文件名
    if target_date is None:
        target_date = datetime.now().date() + timedelta(days=1)
    
    # 创建输出目录
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 保存文件
    filename = f'lezhiban_reminder_{target_date.strftime("%Y%m%d")}.html'
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_content, file_path
