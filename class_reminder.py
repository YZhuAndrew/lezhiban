import streamlit as st
import json
from datetime import datetime, timedelta
import requests

# 设置页面配置
st.set_page_config(
    page_title="乐知班每日温馨提醒生成器",
    page_icon="📅",
    layout="wide"
)

# 获取天气信息的函数
def get_weather_info(city):
    try:
        # 使用指定的天气API获取天气信息
        url = f"http://t.weather.sojson.com/api/weather/city/{city}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            weather_data = response.json()
            # 检查API响应状态
            if weather_data.get('status') == 200 and 'data' in weather_data:
                # 获取天气预报数据
                forecast = weather_data['data']['forecast']
                # 获取明天的天气预报（索引1为明天）
                if len(forecast) > 1:
                    tomorrow_weather = forecast[1]
                    weather_desc = tomorrow_weather['type']
                    high_temp = tomorrow_weather['high']
                    low_temp = tomorrow_weather['low']
                    return f"{weather_desc}，{low_temp}~{high_temp}"
        
        return "查询天气信息失败，可手动输入天气信息"  # 默认天气
    except Exception as e:
        st.warning(f"获取天气信息失败: {str(e)} 可手动输入天气信息")
        return "查询天气信息失败，可手动输入天气信息"  # 出错时返回默认天气

# 标题和说明
st.title("📅乐知班每日温馨提醒生成器")
# st.write("点击下方按钮生成明日的班级温馨提示")

# 从session_state获取天气信息或使用默认值
# auto_weather = st.session_state.get('auto_weather', '多云，气温 26-35℃')
# weather = st.text_input("明日天气", auto_weather, key="weather_input")

# 从外部JSON文件加载数据
def load_schedule_data():
    try:
        with open('schedule_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("找不到schedule_data.json文件，请确保文件存在")
        return {}
    except json.JSONDecodeError:
        st.error("schedule_data.json文件格式错误，请检查JSON格式")
        return {}

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
    # 提取选定日期的信息
    courses = schedule_data["课程安排"].get(selected_weekday, {})
    clubs = schedule_data["社团安排"].get(selected_weekday, [])
    duty_students = schedule_data["值日安排"].get(selected_weekday, "")
    
    # 格式化日期
    date_str = f"{selected_date.month}月{selected_date.day}日"
    
    # 构建提示内容
    reminder = f"📅乐知班明日温馨提醒\n"
    # reminder = f"# 📅 班级每日温馨提示\n\n"
    reminder += f"⏰・[{date_str}] [{selected_weekday}]⏰\n\n"
    # reminder += f"**⏰ 明日日期・[{date_str}] [{selected_weekday}]⏰**\n\n"
    
    # 天气信息
    reminder += f"🌤️明日天气：\n"
    reminder += f"・{weather}\n\n"
    # reminder += f"**🌤️ 明日天气：**\n"
    # reminder += f"{weather}\n\n"
    
    # 课程安排
    reminder += f"📚明日课程安排：\n"
    # reminder += f"**📚 明日课程安排：**\n"
    if courses:
        morning_classes = courses.get("上午", [])
        afternoon_classes = courses.get("下午", [])
        reminder += f"・上午：{', '.join([f'[{cls}]' for cls in morning_classes])}\n"
        reminder += f"・下午：{', '.join([f'[{cls}]' for cls in afternoon_classes])}\n\n"
    else:
        reminder += f"・明日无课程安排\n\n"
    
    # 社团安排
    # reminder += f"**🎨 社团课程安排：**\n"
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
    # reminder += f"**🧹 值日生安排：**\n"
    reminder += f"・{duty_students}\n\n" if duty_students else "・明日无值日生安排\n\n"
    
    # 着装提醒
    # reminder += f"**👔 着装提醒：**\n"
    reminder += f"👔着装提醒：\n"
    if selected_weekday == "星期一":
        reminder += f"・❗️明天是星期一，大家穿校服，戴红领巾。\n\n"
    reminder += f"・干净舒适即可\n\n"
    
    # 其他注意事项 - 可以使用LLM生成
    reminder += f"📌其他注意事项\n"
    
    api_provider = "不使用"
    api_key = ""
    # 如果启用了LLM，调用API生成额外提示
    if api_provider != "不使用" and api_key:
        with st.spinner("正在通过AI生成额外注意事项..."):
            try:
                # 根据选择的API提供商构建不同的请求
                if api_provider == "OpenAI":
                    # OpenAI API调用
                    response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_key}"
                        },
                        json={
                            "model": "gpt-3.5-turbo",
                            "messages": [
                                {"role": "system", "content": "你是一名小学班主任，根据明天的课程和活动安排，生成3-5条适合小学生的温馨提示。语气要亲切友好。"},
                                {"role": "user", "content": f"明天是{selected_weekday}，天气{weather}，有这些课程：{courses}，还有这些社团活动：{[club['社团名称'] for club in clubs]}。请生成相关的温馨提示。"}
                            ]
                        }
                    )
                    
                    # 检查API响应状态
                    if response.status_code == 200:
                        llm_response = response.json()
                        additional_notes = llm_response['choices'][0]['message']['content']
                    else:
                        additional_notes = f"API调用失败，状态码：{response.status_code}\n请检查API密钥是否正确。"
                    
                elif api_provider == "Anthropic":
                    # Anthropic API调用
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "Content-Type": "application/json",
                            "x-api-key": api_key,
                            "anthropic-version": "2023-06-01"
                        },
                        json={
                            "model": "claude-3-sonnet-20240229",
                            "messages": [
                                {"role": "user", "content": f"你是一名小学班主任，根据明天的课程和活动安排，生成3-5条适合小学生的温馨提示。语气要亲切友好。明天是{selected_weekday}，天气{weather}，有这些课程：{courses}，还有这些社团活动：{[club['社团名称'] for club in clubs]}。请生成相关的温馨提示。"}
                            ],
                            "max_tokens": 300
                        }
                    )
                    
                    # 检查API响应状态
                    if response.status_code == 200:
                        llm_response = response.json()
                        additional_notes = llm_response['content'][0]['text']
                    else:
                        additional_notes = f"API调用失败，状态码：{response.status_code}\n请检查API密钥是否正确。"
                
                reminder += additional_notes
                
            except Exception as e:
                reminder += f"生成额外提示时出错：{str(e)}\n请检查API设置或稍后再试。"
    else:
        reminder += "・1.请带好明天所需的学习用品和课本\n"
        reminder += "・2.注意休息，保证充足睡眠，准时到校\n"
    
    return reminder

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
    st.subheader(".schedule_data.json 数据编辑界面")
    
    # 添加保存函数
    def save_schedule_data(data):
        try:
            with open('schedule_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            st.success("数据已保存成功！")
        except Exception as e:
            st.error(f"保存数据时出错：{str(e)}")
    
    # 创建标签页用于不同类型的编辑
    tab1, tab2, tab3 = st.tabs(["课程安排", "社团安排", "值日安排"])
    
    # 课程安排编辑
    with tab1:
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
            morning_count = st.number_input(f"{weekday}上午课程数量", min_value=0, max_value=10, 
                                          value=len(morning_classes), key=f"{weekday}_morning_count")
            
            edited_morning = []
            for i in range(morning_count):
                default_value = morning_classes[i] if i < len(morning_classes) else ""
                class_name = st.text_input(f"{weekday}上午第{i+1}节课", value=default_value, 
                                         key=f"{weekday}_morning_{i}")
                edited_morning.append(class_name)
            
            # 编辑下午课程
            st.markdown("##### 下午课程")
            afternoon_classes = weekday_data.get("下午", [])
            afternoon_count = st.number_input(f"{weekday}下午课程数量", min_value=0, max_value=10, 
                                            value=len(afternoon_classes), key=f"{weekday}_afternoon_count")
            
            edited_afternoon = []
            for i in range(afternoon_count):
                default_value = afternoon_classes[i] if i < len(afternoon_classes) else ""
                class_name = st.text_input(f"{weekday}下午第{i+1}节课", value=default_value, 
                                         key=f"{weekday}_afternoon_{i}")
                edited_afternoon.append(class_name)
            
            edited_course_data[weekday] = {
                "上午": edited_morning,
                "下午": edited_afternoon
            }
        
        # 更新课程安排数据
        schedule_data["课程安排"] = edited_course_data
    
    # 社团安排编辑
    with tab2:
        st.subheader("社团安排编辑")
        club_data = schedule_data.get("社团安排", {})
        
        # 为每个星期创建编辑区域
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五"]
        edited_club_data = {}
        
        for weekday in weekdays:
            st.markdown(f"#### {weekday}")
            weekday_clubs = club_data.get(weekday, [])
            
            # 控制社团数量
            club_count = st.number_input(f"{weekday}社团数量", min_value=0, max_value=20, 
                                       value=len(weekday_clubs), key=f"{weekday}_club_count")
            
            edited_clubs = []
            for i in range(club_count):
                club = weekday_clubs[i] if i < len(weekday_clubs) else {"成员": [], "社团名称": ""}
                
                st.markdown(f"##### 社团 {i+1}")
                club_name = st.text_input(f"{weekday}社团{i+1}名称", 
                                        value=club.get("社团名称", ""), 
                                        key=f"{weekday}_club_{i}_name")
                
                # 编辑成员列表
                members = club.get("成员", [])
                member_str = st.text_area(f"{weekday}社团{i+1}成员（用逗号分隔）", 
                                        value="，".join(members), 
                                        key=f"{weekday}_club_{i}_members")
                
                # 将成员字符串转换为列表
                member_list = [m.strip() for m in member_str.split("，") if m.strip()]
                
                edited_clubs.append({
                    "社团名称": club_name,
                    "成员": member_list
                })
            
            edited_club_data[weekday] = edited_clubs
        
        # 更新社团安排数据
        schedule_data["社团安排"] = edited_club_data
    
    # 值日安排编辑
    with tab3:
        st.subheader("值日安排编辑")
        duty_data = schedule_data.get("值日安排", {})
        
        # 为每个星期创建编辑区域
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五"]
        edited_duty_data = {}
        
        for weekday in weekdays:
            duty_students = duty_data.get(weekday, "")
            edited_duty = st.text_area(f"{weekday}值日生", value=duty_students, 
                                     key=f"{weekday}_duty_students",
                                     help="请输入值日生姓名，用逗号或顿号分隔")
            edited_duty_data[weekday] = edited_duty
        
        # 更新值日安排数据
        schedule_data["值日安排"] = edited_duty_data
    
    # 保存按钮
    if st.button("保存所有更改"):
        save_schedule_data(schedule_data)
        st.rerun()
