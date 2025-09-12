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

# 提供的JSON数据
schedule_data = {
    "课程安排": {
        "星期二": {
            "上午": [
                "数学",
                "语文",
                "书法",
                "道德与法治"
            ],
            "下午": [
                "体育",
                "音乐",
                "数学作业辅导",
                "经典领读"
            ]
        },
        "星期三": {
            "上午": [
                "语文",
                "数学",
                "体育",
                "英语"
            ],
            "下午": [
                "心理健康-单 | 综合实践-双",
                "信息技术",
                "英语作业辅导",
                "语文作业辅导"
            ]
        },
        "星期四": {
            "上午": [
                "语文",
                "数学",
                "体育",
                "美术"
            ],
            "下午": [
                "英语",
                "道德与法治",
                "诵读",
                "数学作业辅导"
            ]
        },
        "星期五": {
            "上午": [
                "数学",
                "语文",
                "阅读",
                "美术"
            ],
            "下午": [
                "劳动",
                "英语",
                "自然拼读",
                "语文作业辅导"
            ]
        },
        "星期一": {
            "上午": [
                "语文",
                "班队活动/美丽江西",
                "数学",
                "体育"
            ],
            "下午": [
                "科学",
                "音乐",
                "语文作业辅导",
                "思维探险队"
            ]
        }
    },
    "社团安排": {
        "星期二": [
            {
                "成员": [
                    "夏润修"
                ],
                "社团名称": "武术（全年级）"
            }
        ],
        "星期三": [
            {
                "成员": [
                    "徐纯熙",
                    "廖将来"
                ],
                "社团名称": "彩笔画社团（3-5年级）"
            }
        ],
        "星期四": [
            {
                "成员": [
                    "徐若灵",
                    "赵翊然"
                ],
                "社团名称": "3D打印社团（2-5年级）"
            },
            {
                "成员": [
                    "王梓桐",
                    "余欣妍",
                    "郑婉诺"
                ],
                "社团名称": "创意美术社团（3-5年级）"
            },
            {
                "成员": [
                    "王宸亿",
                    "陈梓卿",
                    "徐之妍"
                ],
                "社团名称": "国画社团（3-5年级）"
            },
            {
                "成员": [
                    "朱祉漩",
                    "王赟艺"
                ],
                "社团名称": "拉丁舞社团（3-5年级）"
            },
            {
                "成员": [
                    "徐弘岩"
                ],
                "社团名称": "篮球（3-5年级）"
            },
            {
                "成员": [
                    "邱文轩",
                    "汤凌晟",
                    "徐彦哲"
                ],
                "社团名称": "硬笔书法（3-5年级）"
            },
            {
                "成员": [
                    "蒋濛颀",
                    "杨浩铭"
                ],
                "社团名称": "足球社团（3-5年级）"
            }
        ],
        "星期五": [
            {
                "成员": [
                    "丁冉熙"
                ],
                "社团名称": "葫芦丝社团（3-5年级）"
            },
            {
                "成员": [
                    "钟紫彤"
                ],
                "社团名称": "花样跳绳（3-5年级）"
            },
            {
                "成员": [
                    "廖子康",
                    "廖子安"
                ],
                "社团名称": "科普社团（3-5年级）"
            },
            {
                "成员": [
                    "李溍堃",
                    "占承航"
                ],
                "社团名称": "乒乓球（3-5年级）"
            },
            {
                "成员": [
                    "刘飞雪",
                    "詹华旭"
                ],
                "社团名称": "趣味心理社团（3-5年级）"
            },
            {
                "成员": [
                    "郏宸唯"
                ],
                "社团名称": "软笔书法（4-5年级）"
            },
            {
                "成员": [
                    "徐之恒",
                    "涂致远",
                    "郑子其"
                ],
                "社团名称": "田径社团（4-5年级）"
            },
            {
                "成员": [
                    "周致远"
                ],
                "社团名称": "线描画社团（3-5年级）"
            },
            {
                "成员": [
                    "姜懿恩"
                ],
                "社团名称": "英语绘本阅读（全年级）"
            },
            {
                "成员": [
                    "余书洛",
                    "章奕杰",
                    "章一诺",
                    "姜海逸"
                ],
                "社团名称": "羽毛球（3-5年级）"
            },
            {
                "成员": [
                    "曹欣念",
                    "蒋诗怡"
                ],
                "社团名称": "中国舞社团（3-5年级）"
            }
        ]
    },
    "值日安排": {
        "星期二": "苏心怡，徐之妍，周致远，李溍堃，余书洛，王赟艺，姜懿恩，郑子其",
        "星期三": "丁冉熙，朱祉漩，章奕杰，徐彦哲，姜海逸，陈梓卿，王宸亿，邱文轩",
        "星期四": "钟紫彤，蒋诗怡，廖子康，徐之恒，郏宸唯，廖子安，刘飞雪，詹华旭",
        "星期五": "徐纯熙，徐若灵，廖将来，赵翊然，汤凌晟，郑婉诺，蒋濛颀，涂志宏",
        "星期一": "曹欣念，王梓桐，徐弘岩，涂致远，占承航，夏润修，杨浩铭，章一诺"
    }
}

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
        reminder += f"明日无课程安排\n\n"
    
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
        reminder += f"❗️明天是星期一，大家穿校服，戴红领巾。\n\n"
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
