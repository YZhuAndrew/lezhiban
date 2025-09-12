# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Streamlit web application called "乐知班每日温馨提醒生成器" (Lezhi Class Daily Warm Reminder Generator). It generates daily reminders for a elementary school class with schedule information, weather forecasts, and other important notices.

## Code Structure
- `class_reminder.py`: Main Streamlit application that generates daily class reminders
- `README.md`: Project documentation

## Key Features
1. Weather information retrieval using weather API
2. Class schedule management for different weekdays
3. Club activity scheduling
4. Duty student assignments
5. Automatic reminder generation with formatted output

## Development Commands
- Run the application: `streamlit run class_reminder.py`
- Dependencies: streamlit, requests

## Architecture
The application is a single-file Streamlit app that:
1. Uses session state for weather data caching
2. Stores schedule data in a JSON structure
3. Integrates with a weather API for forecasts
4. Generates formatted text output for class reminders
5. Provides a date picker for selecting the target day

## Common Development Tasks
1. Updating schedule data in the JSON structure
2. Modifying the weather API integration
3. Adjusting the reminder text formatting
4. Adding new sections to the daily reminder