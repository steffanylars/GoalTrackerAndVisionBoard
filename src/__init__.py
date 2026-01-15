"""
Focus Flow - Goal & Focus Tracker
Módulo principal de la aplicación
"""

from .data_manager import (
    get_all_projects,
    get_all_sessions,
    create_project,
    update_project,
    delete_project,
    create_session,
    delete_session,
    calculate_daily_progress,
    calculate_monthly_progress,
    calculate_project_progress,
    get_daily_activity_for_month,
)

__version__ = "1.0.0"
__author__ = "Focus Flow Team"
