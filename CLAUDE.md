# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit web application called "乐知班每日温馨提醒生成器" (Lezhi Class Daily Warm Reminder Generator). It generates daily reminders for an elementary school class with schedule information, weather forecasts, and other important notices.

## Code Structure

- `class_reminder.py`: Main Streamlit application that generates daily class reminders
- `schedule_data.json`: JSON data file containing class schedules, club activities, and duty assignments
- `utils/`: Directory containing utility modules
  - `data_manager.py`: Handles data loading, saving, validation, and backup
  - `weather_service.py`: Manages weather API calls with caching mechanism
  - `reminder_generator.py`: Contains logic for generating reminder content
  - `ui_components.py`: Manages UI components for data editing
- `data/`: Directory for data storage
  - `backups/`: Directory for data file backups
  - `weather_cache.json`: Cache file for weather information
- `README.md`: Project documentation

## Key Features

1. Weather information retrieval with caching mechanism
2. Class schedule management for different weekdays
3. Club activity scheduling
4. Duty student assignments
5. Automatic reminder generation with formatted output
6. Visual data editing interface
7. Data backup functionality

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

## Common Development Tasks

1. Updating schedule data through the visual editor
2. Modifying the weather API integration
3. Adjusting the reminder text formatting
4. Adding new sections to the daily reminder
5. Extending the data validation logic
