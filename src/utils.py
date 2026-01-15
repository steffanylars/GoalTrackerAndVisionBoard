"""
utils.py - Utilidades generales

Funciones auxiliares para la aplicación.

Autor: Focus Flow Team
"""

from datetime import datetime, date, timedelta
import calendar
from typing import Tuple, List


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 FORMATO DE TIEMPO

def format_minutes(minutes: int) -> str:
    """
    Formatea minutos en un string legible.
    
    Args:
        minutes: Cantidad de minutos
        
    Returns:
        String formateado (ej: "2h 30m")
        
    Examples:
        >>> format_minutes(45)
        '45m'
        >>> format_minutes(90)
        '1h 30m'
        >>> format_minutes(120)
        '2h'
    """
    if minutes < 60:
        return f"{minutes}m"
    
    hours = minutes // 60
    mins = minutes % 60
    
    if mins == 0:
        return f"{hours}h"
    
    return f"{hours}h {mins}m"


def format_timer(seconds: int) -> Tuple[int, int]:
    """
    Convierte segundos a formato (minutos, segundos).
    
    Args:
        seconds: Total de segundos
        
    Returns:
        Tupla (minutos, segundos)
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return minutes, remaining_seconds


def format_date_display(date_str: str) -> str:
    """
    Formatea una fecha ISO a formato legible.
    
    Args:
        date_str: Fecha en formato YYYY-MM-DD
        
    Returns:
        String formateado (ej: "15 Ene 2024")
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        months = [
            "Ene", "Feb", "Mar", "Abr", "May", "Jun",
            "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
        ]
        return f"{dt.day} {months[dt.month - 1]} {dt.year}"
    except:
        return date_str


def get_month_name(month: int) -> str:
    """
    Obtiene el nombre del mes en español.
    
    Args:
        month: Número del mes (1-12)
        
    Returns:
        Nombre del mes
    """
    months = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    return months[month - 1] if 1 <= month <= 12 else ""


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 CÁLCULOS DE FECHA

def get_current_month_info() -> Tuple[int, int, int]:
    """
    Obtiene información del mes actual.
    
    Returns:
        Tupla (año, mes, días_en_mes)
    """
    today = date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    return today.year, today.month, days_in_month


def get_month_date_range(year: int, month: int) -> Tuple[date, date]:
    """
    Obtiene el rango de fechas de un mes.
    
    Args:
        year: Año
        month: Mes
        
    Returns:
        Tupla (primer_dia, ultimo_dia)
    """
    first_day = date(year, month, 1)
    days_in_month = calendar.monthrange(year, month)[1]
    last_day = date(year, month, days_in_month)
    return first_day, last_day


def get_days_passed_in_month() -> int:
    """
    Calcula los días transcurridos en el mes actual.
    
    Returns:
        Número de días
    """
    return date.today().day


def get_week_start(target_date: date = None) -> date:
    """
    Obtiene el inicio de la semana (Lunes).
    
    Args:
        target_date: Fecha de referencia (hoy por defecto)
        
    Returns:
        Fecha del Lunes de esa semana
    """
    if target_date is None:
        target_date = date.today()
    
    # weekday() retorna 0 para Lunes
    days_since_monday = target_date.weekday()
    return target_date - timedelta(days=days_since_monday)


def get_available_months(start_year: int = 2024) -> List[Tuple[int, int, str]]:
    """
    Genera lista de meses disponibles para selección.
    
    Args:
        start_year: Año inicial
        
    Returns:
        Lista de tuplas (año, mes, nombre_display)
    """
    today = date.today()
    months = []
    
    for year in range(start_year, today.year + 1):
        start_month = 1
        end_month = 12 if year < today.year else today.month
        
        for month in range(start_month, end_month + 1):
            name = f"{get_month_name(month)} {year}"
            months.append((year, month, name))
    
    return months[::-1]  # Más reciente primero


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 CÁLCULOS DE PROGRESO

def calculate_percentage(current: int, goal: int) -> float:
    """
    Calcula el porcentaje de progreso.
    
    Args:
        current: Valor actual
        goal: Meta objetivo
        
    Returns:
        Porcentaje (0-100+)
    """
    if goal <= 0:
        return 0.0
    return round((current / goal) * 100, 1)


def get_progress_status(percentage: float) -> Tuple[str, str]:
    """
    Determina el estado del progreso.
    
    Args:
        percentage: Porcentaje de progreso
        
    Returns:
        Tupla (estado, emoji)
    """
    if percentage >= 100:
        return "Completado", "🎉"
    elif percentage >= 75:
        return "Casi listo", "🔥"
    elif percentage >= 50:
        return "A mitad", "💪"
    elif percentage >= 25:
        return "En progreso", "✨"
    else:
        return "Iniciando", "🌱"


def get_goal_type_label(goal_type: str) -> str:
    """
    Obtiene la etiqueta legible del tipo de meta.
    
    Args:
        goal_type: Tipo de meta (pomodoro/time/sessions)
        
    Returns:
        Etiqueta en español
    """
    labels = {
        "pomodoro": "Pomodoros",
        "time": "Minutos",
        "sessions": "Sesiones"
    }
    return labels.get(goal_type, goal_type)


def get_goal_unit(goal_type: str, value: int) -> str:
    """
    Formatea el valor con su unidad apropiada.
    
    Args:
        goal_type: Tipo de meta
        value: Valor numérico
        
    Returns:
        String formateado
    """
    if goal_type == "pomodoro":
        return f"{value} 🍅"
    elif goal_type == "time":
        return format_minutes(value)
    else:  # sessions
        return f"{value} sesiones"


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 VALIDACIONES

def is_valid_color(color: str) -> bool:
    """
    Valida que un string sea un color hex válido.
    
    Args:
        color: String de color
        
    Returns:
        True si es válido
    """
    if not color or not isinstance(color, str):
        return False
    
    if not color.startswith('#'):
        return False
    
    if len(color) not in [4, 7]:  # #RGB o #RRGGBB
        return False
    
    try:
        int(color[1:], 16)
        return True
    except ValueError:
        return False


def is_valid_project_name(name: str) -> Tuple[bool, str]:
    """
    Valida el nombre de un proyecto.
    
    Args:
        name: Nombre a validar
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if not name or not name.strip():
        return False, "El nombre no puede estar vacío"
    
    if len(name.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    
    if len(name) > 50:
        return False, "El nombre no puede tener más de 50 caracteres"
    
    return True, ""


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 CONSTANTES

# Duración estándar de un pomodoro (minutos)
POMODORO_DURATION = 25

# Duración del descanso corto (minutos)
SHORT_BREAK = 5

# Duración del descanso largo (minutos)
LONG_BREAK = 15

# Pomodoros antes del descanso largo
POMODOROS_BEFORE_LONG_BREAK = 4

# Metas por defecto
DEFAULT_MONTHLY_GOAL = 20

# Tipos de meta válidos
VALID_GOAL_TYPES = ["pomodoro", "time", "sessions"]

# Tipos de sesión válidos
VALID_SESSION_TYPES = ["pomodoro", "custom"]

