import streamlit as st
import requests
import json
import os
from datetime import datetime, timedelta, date
from typing import Optional

# 天气缓存文件路径
WEATHER_CACHE_FILE = 'data/weather_cache.json'

def get_weather_info(city: str, target_date: date) -> str:
    """
    获取指定日期的天气信息，带缓存机制
    
    Args:
        city (str): 城市代码
        target_date (date): 目标日期
        
    Returns:
        str: 天气信息描述
    """
    try:
        # 计算目标日期与今天相差的天数
        today = datetime.now().date()
        days_ahead = (target_date - today).days
        
        # 检查缓存
        cached_weather = get_cached_weather(city, target_date)
        if cached_weather:
            return cached_weather
        
        # 使用指定的天气API获取天气信息
        url = f"http://t.weather.sojson.com/api/weather/city/{city}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            weather_data = response.json()
            # 检查API响应状态
            if weather_data.get('status') == 200 and 'data' in weather_data:
                # 获取天气预报数据
                forecast = weather_data['data']['forecast']
                
                # 确保目标日期在预报范围内（0-7天）
                if 0 <= days_ahead < len(forecast):
                    day_weather = forecast[days_ahead]
                    weather_desc = day_weather['type']
                    high_temp = day_weather['high']
                    low_temp = day_weather['low']
                    weather_info = f"{weather_desc}，{low_temp}~{high_temp}"
                    
                    # 缓存天气信息
                    cache_weather(city, target_date, weather_info)
                    return weather_info
                else:
                    return "日期超出天气预报范围，可手动输入天气信息"
        
        return "查询天气信息失败，可手动输入天气信息"  # 默认天气
    except requests.Timeout:
        st.warning("获取天气信息超时，可手动输入天气信息")
        return "查询天气信息失败，可手动输入天气信息"
    except requests.RequestException as e:
        st.warning(f"网络请求失败: {str(e)} 可手动输入天气信息")
        return "查询天气信息失败，可手动输入天气信息"
    except Exception as e:
        st.warning(f"获取天气信息失败: {str(e)} 可手动输入天气信息")
        return "查询天气信息失败，可手动输入天气信息"

def get_cached_weather(city: str, target_date: date) -> Optional[str]:
    """
    从缓存获取指定日期的天气信息
    
    Args:
        city (str): 城市代码
        target_date (date): 目标日期
        
    Returns:
        Optional[str]: 缓存的天气信息，如果没有有效缓存则返回None
    """
    try:
        if not os.path.exists(WEATHER_CACHE_FILE):
            return None
            
        with open(WEATHER_CACHE_FILE, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # 创建缓存键（city_date格式）
        cache_key = f"{city}_{target_date}"
        
        # 检查是否有该城市和日期的缓存
        if cache_key not in cache_data:
            return None
            
        # 检查缓存是否过期（缓存有效期1小时）
        cached_entry = cache_data[cache_key]
        cached_time = datetime.fromisoformat(cached_entry['timestamp'])
        if datetime.now() - cached_time > timedelta(hours=1):
            # 缓存过期，删除该条目
            del cache_data[cache_key]
            # 更新缓存文件
            with open(WEATHER_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            return None
            
        return cached_entry['weather_info']
    except Exception:
        # 缓存读取失败，忽略缓存
        return None

def cache_weather(city: str, target_date: date, weather_info: str) -> None:
    """
    缓存指定日期的天气信息
    
    Args:
        city (str): 城市代码
        target_date (date): 目标日期
        weather_info (str): 天气信息
    """
    try:
        # 确保缓存目录存在
        os.makedirs(os.path.dirname(WEATHER_CACHE_FILE), exist_ok=True)
        
        # 读取现有缓存
        cache_data = {}
        if os.path.exists(WEATHER_CACHE_FILE):
            with open(WEATHER_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
        
        # 更新缓存
        cache_key = f"{city}_{target_date}"
        cache_data[cache_key] = {
            'weather_info': weather_info,
            'timestamp': datetime.now().isoformat()
        }
        
        # 保存缓存
        with open(WEATHER_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # 缓存失败不影响主要功能
        pass