# 乐知班每日温馨提醒生成器

## Development Commands

- Run the application: `streamlit run class_reminder.py`
- Dependencies: streamlit, requests

## Architecture

The application has been refactored into a modular structure:

1. Main application file (`class_reminder.py`) orchestrates the UI and user interactions
2. Data management module (`data_manager.py`) handles all data operations
3. Weather service module (`weather_service.py`) manages weather API calls and caching
4. Reminder generator module (`reminder_generator.py`) handles content generation logic
5. UI components module (`ui_components.py`) manages the data editing interface
