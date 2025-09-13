# 乐知班每日温馨提醒生成器

## 项目简介

这是一个Streamlit Web应用程序，用于为小学班级生成每日温馨提醒，包含课程安排、天气预报和其他重要通知。

## 功能特性

- 自动生成每日班级温馨提示
- 天气信息查询与缓存
- 课程安排管理
- 社团活动安排
- 值日生安排
- 特别注意事项添加
- 历史记录查看与管理

## 开发命令

- 运行应用: `streamlit run 温馨提醒生成器.py`
- 依赖: streamlit, requests

## 项目结构

```text
lezhiban/
├── 温馨提醒生成器.py          # 主应用文件
├── schedule_data.json         # 课程安排数据文件
├── README.md                  # 项目说明文档
├── CLAUDE.md                  # Claude Code指导文档
├── data/                      # 数据存储目录
│   ├── backups/               # 数据备份目录
│   ├── weather_cache.json     # 天气信息缓存文件
│   └── history_records.json   # 历史记录文件
├── pages/                     # 页面文件目录
│   ├── 历史记录.py             # 历史记录页面
│   └── 数据编辑.py             # 数据编辑页面
└── utils/                     # 工具模块目录
    ├── data_manager.py        # 数据管理模块
    ├── weather_service.py     # 天气服务模块
    ├── reminder_generator.py  # 提醒内容生成模块
    ├── ui_components.py       # UI组件模块
    └── history_manager.py     # 历史记录管理模块
```

## 架构说明

应用采用模块化结构设计：

1. 主应用文件 (`温馨提醒生成器.py`) 负责协调UI和用户交互
2. 数据管理模块 (`data_manager.py`) 处理所有数据操作
3. 天气服务模块 (`weather_service.py`) 管理天气API调用和缓存
4. 提醒生成模块 (`reminder_generator.py`) 处理内容生成逻辑
5. UI组件模块 (`ui_components.py`) 管理数据编辑界面
6. 历史记录管理模块 (`history_manager.py`) 管理生成记录的保存和加载

## 使用说明

1. 运行应用后，系统会自动显示明天的日期和默认天气信息
2. 可以手动修改日期和天气信息
3. 在"特别注意事项"文本框中可添加额外的重要信息
4. 点击"生成乐知班温馨提示"按钮生成提醒内容
5. 通过底部按钮可访问数据编辑界面和历史记录页面
6. 历史记录页面支持查看、删除单条或多条记录