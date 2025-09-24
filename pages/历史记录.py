import streamlit as st
import streamlit.components.v1 as components
from utils.history_manager import load_history_records, clear_history_records, format_history_record
from utils.mobile_page_generator import generate_mobile_page
import json
import os
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="历史记录",
    page_icon="📚",
    layout="wide"
)

# 页面标题
st.title("📚 历史记录")

# 从session state获取要删除的记录ID列表
if "records_to_delete" not in st.session_state:
    st.session_state.records_to_delete = []

# 加载历史记录
history_records = load_history_records()

if history_records:
    # 按时间倒序排列
    history_records.reverse()
    
    # 显示统计信息
    st.info(f"共找到 {len(history_records)} 条历史记录")
    
    # 添加全选/取消全选按钮
    col1, col2, col3, col4 = st.columns([2, 2, 2, 4])
    with col1:
        if st.button("全选"):
            st.session_state.records_to_delete = [record.get("timestamp", "") for record in history_records]
            st.rerun()
    with col2:
        if st.button("取消全选"):
            st.session_state.records_to_delete = []
            st.rerun()
    with col3:
        if st.button("删除选中"):
            if st.session_state.records_to_delete:
                # 删除选中的记录
                records_to_keep = [
                    record for record in history_records 
                    if record.get("timestamp", "") not in st.session_state.records_to_delete
                ]
                
                # 保存剩余记录
                try:
                    with open("data/history_records.json", "w", encoding="utf-8") as f:
                        json.dump(records_to_keep[::-1], f, ensure_ascii=False, indent=2)  # 重新反转以保持正确顺序
                    
                    st.success(f"成功删除 {len(st.session_state.records_to_delete)} 条记录！")
                    st.session_state.records_to_delete = []
                    st.rerun()
                except Exception as e:
                    st.error(f"删除记录时出错: {e}")
            else:
                st.warning("请先选择要删除的记录")
    
    with col4:
        if st.button("清空所有记录"):
            clear_history_records()
            st.session_state.records_to_delete = []
            st.success("所有历史记录已清空！")
            st.rerun()
    
    # 显示记录列表
    st.markdown("---")
    
    # 使用分页显示记录
    records_per_page = 10
    total_pages = (len(history_records) - 1) // records_per_page + 1
    
    # 获取当前页码
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1
    
    # 页码控制
    if total_pages > 1:
        col_prev, col_pages, col_next = st.columns([1, 8, 1])
        with col_prev:
            if st.button("上一页") and st.session_state.current_page > 1:
                st.session_state.current_page -= 1
                st.rerun()
        
        with col_next:
            if st.button("下一页") and st.session_state.current_page < total_pages:
                st.session_state.current_page += 1
                st.rerun()
        
        with col_pages:
            st.markdown(f"<div style='text-align: center; padding: 10px;'>第 {st.session_state.current_page} 页 / 共 {total_pages} 页</div>", unsafe_allow_html=True)
    
    # 计算当前页的记录范围
    start_idx = (st.session_state.current_page - 1) * records_per_page
    end_idx = min(start_idx + records_per_page, len(history_records))
    
    # 显示当前页的记录
    for i in range(start_idx, end_idx):
        record = history_records[i]
        timestamp = record.get("timestamp", "")
        date_str = record.get("date", "未知日期")
        weekday = record.get("weekday", "未知星期")
        
        # 创建唯一的key
        record_key = timestamp if timestamp else f"record_{i}"
        
        with st.expander(f"记录 {i+1} - {date_str} {weekday}"):
            # 显示记录详情
            st.text(format_history_record(record))
            
            # 显示完整内容（使用按钮切换显示/隐藏）
            if f"show_full_{record_key}" not in st.session_state:
                st.session_state[f"show_full_{record_key}"] = False
            
            if st.button("查看/隐藏完整内容", key=f"toggle_{record_key}"):
                st.session_state[f"show_full_{record_key}"] = not st.session_state[f"show_full_{record_key}"]
            
            if st.session_state[f"show_full_{record_key}"]:
                st.text_area("", value=record.get("reminder_content", ""), height=200, key=f"full_content_{record_key}")
            
            # 查看网页功能
            if f"show_web_{record_key}" not in st.session_state:
                st.session_state[f"show_web_{record_key}"] = False
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("查看手机网页", key=f"web_{record_key}"):
                    reminder_content = record.get("reminder_content", "")
                    if reminder_content:
                        # 从日期字符串解析日期对象
                        try:
                            # 尝试解析日期格式如 "2025年09月25日"
                            date_obj = datetime.strptime(date_str, "%Y年%m月%d日").date()
                        except:
                            # 如果解析失败，使用当前日期
                            date_obj = datetime.now().date()
                        
                        # 生成手机网页
                        with st.spinner("正在生成手机网页..."):
                            html_content, file_path = generate_mobile_page(reminder_content, date_obj)
                            st.session_state[f"html_content_{record_key}"] = html_content
                            st.session_state[f"file_path_{record_key}"] = file_path
                            st.session_state[f"show_web_{record_key}"] = True
                    else:
                        st.error("此记录没有提醒内容，无法生成网页")
            
            with col2:
                # 下载网页按钮（只有在生成网页后才显示）
                if f"html_content_{record_key}" in st.session_state:
                    st.download_button(
                        label="下载网页",
                        data=st.session_state[f"html_content_{record_key}"],
                        file_name=f"乐知班温馨提醒_{date_str.replace('年', '').replace('月', '').replace('日', '')}.html",
                        mime="text/html",
                        key=f"download_{record_key}"
                    )
            
            # 显示网页预览
            if st.session_state[f"show_web_{record_key}"] and f"html_content_{record_key}" in st.session_state:
                st.markdown("#### 手机网页预览")
                components.html(st.session_state[f"html_content_{record_key}"], height=600, scrolling=True)
                st.info(f"网页文件已保存至：{st.session_state[f'file_path_{record_key}']}")
            
            # 删除选项
            is_selected = record_key in st.session_state.records_to_delete
            if st.checkbox("选择删除", value=is_selected, key=f"select_{record_key}"):
                if record_key not in st.session_state.records_to_delete:
                    st.session_state.records_to_delete.append(record_key)
            else:
                if record_key in st.session_state.records_to_delete:
                    st.session_state.records_to_delete.remove(record_key)
            
            # 单条删除按钮
            if st.button("删除此记录", key=f"delete_{record_key}"):
                # 删除单条记录
                records_to_keep = [
                    r for r in history_records
                    if r.get("timestamp", "") != timestamp
                ]
                
                # 保存剩余记录
                try:
                    with open("data/history_records.json", "w", encoding="utf-8") as f:
                        json.dump(records_to_keep[::-1], f, ensure_ascii=False, indent=2)  # 重新反转以保持正确顺序
                    
                    # 从待删除列表中移除
                    if record_key in st.session_state.records_to_delete:
                        st.session_state.records_to_delete.remove(record_key)
                    
                    # 清理相关的session_state
                    keys_to_remove = [f"show_full_{record_key}", f"show_web_{record_key}",
                                    f"html_content_{record_key}", f"file_path_{record_key}"]
                    for key in keys_to_remove:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    st.success("记录已删除！")
                    st.rerun()
                except Exception as e:
                    st.error(f"删除记录时出错: {e}")
else:
    st.info("暂无历史记录")

# 返回主页面按钮
if st.button("返回主页面"):
    st.switch_page("温馨提醒生成器.py")
