"""
data_manager.py - Módulo de persistencia de datos JSON

Este módulo maneja todas las operaciones CRUD para los archivos JSON.
Garantiza que los datos nunca se pierdan y se actualicen de forma segura.

Autor: Focus Flow Team
"""

import json
import uuid
import os
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pathlib import Path


# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================

# Obtener el directorio base del proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Rutas de archivos JSON
PROJECTS_FILE = DATA_DIR / "projects.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
SETTINGS_FILE = DATA_DIR / "settings.json"


# ============================================================================
# FUNCIONES DE INICIALIZACIÓN
# ============================================================================

def ensure_data_directory():
    """
    Crea el directorio de datos si no existe.
    Se ejecuta automáticamente al importar el módulo.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def initialize_json_file(filepath: Path, default_content: List = None):
    """
    Inicializa un archivo JSON si no existe.
    
    Args:
        filepath: Ruta del archivo a crear
        default_content: Contenido inicial (lista vacía por defecto)
    """
    if default_content is None:
        default_content = []
    
    if not filepath.exists():
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(default_content, f, indent=2, ensure_ascii=False)
        print(f"✅ Archivo creado: {filepath}")


def initialize_all_files():
    """
    Inicializa todos los archivos JSON necesarios.
    Esta función es idempotente - puede llamarse múltiples veces sin problema.
    """
    ensure_data_directory()
    initialize_json_file(PROJECTS_FILE, [])
    initialize_json_file(SESSIONS_FILE, [])
    initialize_json_file(SETTINGS_FILE, {
        "default_pomodoro_minutes": 25,
        "default_break_minutes": 5,
        "sound_enabled": True,
        "theme": "dark"
    })


# ============================================================================
# FUNCIONES DE LECTURA (READ)
# ============================================================================

def read_json_file(filepath: Path) -> Any:
    """
    Lee y retorna el contenido de un archivo JSON.
    
    Args:
        filepath: Ruta del archivo a leer
        
    Returns:
        Contenido del archivo (lista o diccionario)
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el JSON es inválido
    """
    # Asegurar que el archivo existe
    if not filepath.exists():
        initialize_all_files()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_projects() -> List[Dict]:
    """
    Obtiene todos los proyectos.
    
    Returns:
        Lista de diccionarios con los proyectos
    """
    return read_json_file(PROJECTS_FILE)


def get_all_sessions() -> List[Dict]:
    """
    Obtiene todas las sesiones.
    
    Returns:
        Lista de diccionarios con las sesiones
    """
    return read_json_file(SESSIONS_FILE)


def get_settings() -> Dict:
    """
    Obtiene la configuración del usuario.
    
    Returns:
        Diccionario con las preferencias
    """
    return read_json_file(SETTINGS_FILE)


def get_project_by_id(project_id: str) -> Optional[Dict]:
    """
    Busca un proyecto por su ID.
    
    Args:
        project_id: UUID del proyecto
        
    Returns:
        Diccionario del proyecto o None si no existe
    """
    projects = get_all_projects()
    for project in projects:
        if project.get('id') == project_id:
            return project
    return None


def get_sessions_by_project(project_id: str) -> List[Dict]:
    """
    Obtiene todas las sesiones de un proyecto específico.
    
    Args:
        project_id: UUID del proyecto
        
    Returns:
        Lista de sesiones del proyecto
    """
    sessions = get_all_sessions()
    return [s for s in sessions if s.get('project_id') == project_id]


def get_sessions_by_date(target_date: str) -> List[Dict]:
    """
    Obtiene todas las sesiones de una fecha específica.
    
    Args:
        target_date: Fecha en formato YYYY-MM-DD
        
    Returns:
        Lista de sesiones de esa fecha
    """
    sessions = get_all_sessions()
    return [s for s in sessions if s.get('date') == target_date]


def get_sessions_by_month(year: int, month: int) -> List[Dict]:
    """
    Obtiene todas las sesiones de un mes específico.
    
    Args:
        year: Año (ej: 2024)
        month: Mes (1-12)
        
    Returns:
        Lista de sesiones del mes
    """
    sessions = get_all_sessions()
    month_prefix = f"{year}-{month:02d}"
    return [s for s in sessions if s.get('date', '').startswith(month_prefix)]


# ============================================================================
# FUNCIONES DE ESCRITURA (WRITE)
# ============================================================================

def write_json_file(filepath: Path, data: Any):
    """
    Escribe datos en un archivo JSON de forma segura.
    
    Usa escritura atómica para prevenir corrupción de datos:
    1. Escribe en archivo temporal
    2. Renombra al archivo final
    
    Args:
        filepath: Ruta del archivo
        data: Datos a guardar
    """
    # Asegurar que el directorio existe
    ensure_data_directory()
    
    # Escribir con formato legible
    temp_filepath = filepath.with_suffix('.tmp')
    
    try:
        with open(temp_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        # Renombrar atómicamente
        temp_filepath.replace(filepath)
        
    except Exception as e:
        # Limpiar archivo temporal si existe
        if temp_filepath.exists():
            temp_filepath.unlink()
        raise e


# ============================================================================
# FUNCIONES DE PROYECTOS (CRUD)
# ============================================================================

def create_project(
    name: str,
    color: str = "#ff7eb6",
    goal_type: str = "pomodoro",
    monthly_goal: int = 20
) -> Dict:
    """
    Crea un nuevo proyecto.
    
    Args:
        name: Nombre del proyecto
        color: Color hexadecimal (ej: #ff7eb6)
        goal_type: Tipo de meta (pomodoro | time | sessions)
        monthly_goal: Meta mensual (pomodoros, minutos o sesiones)
        
    Returns:
        Diccionario del proyecto creado
    """
    # Cargar proyectos existentes
    projects = get_all_projects()
    
    # Crear nuevo proyecto
    new_project = {
        "id": str(uuid.uuid4()),
        "name": name,
        "color": color,
        "goal_type": goal_type,
        "monthly_goal": monthly_goal,
        "created_at": date.today().isoformat()
    }
    
    # Agregar y guardar
    projects.append(new_project)
    write_json_file(PROJECTS_FILE, projects)
    
    return new_project


def update_project(project_id: str, updates: Dict) -> Optional[Dict]:
    """
    Actualiza un proyecto existente.
    
    Args:
        project_id: UUID del proyecto
        updates: Diccionario con los campos a actualizar
        
    Returns:
        Proyecto actualizado o None si no existe
    """
    projects = get_all_projects()
    
    for i, project in enumerate(projects):
        if project.get('id') == project_id:
            # Actualizar solo los campos proporcionados
            # NO sobrescribir id ni created_at
            allowed_updates = {
                k: v for k, v in updates.items() 
                if k not in ['id', 'created_at']
            }
            projects[i].update(allowed_updates)
            write_json_file(PROJECTS_FILE, projects)
            return projects[i]
    
    return None


def delete_project(project_id: str) -> bool:
    """
    Elimina un proyecto y todas sus sesiones asociadas.
    
    Args:
        project_id: UUID del proyecto
        
    Returns:
        True si se eliminó, False si no existía
    """
    projects = get_all_projects()
    original_count = len(projects)
    
    # Filtrar proyectos (eliminar el indicado)
    projects = [p for p in projects if p.get('id') != project_id]
    
    if len(projects) < original_count:
        # Proyecto eliminado, guardar
        write_json_file(PROJECTS_FILE, projects)
        
        # También eliminar sesiones asociadas
        sessions = get_all_sessions()
        sessions = [s for s in sessions if s.get('project_id') != project_id]
        write_json_file(SESSIONS_FILE, sessions)
        
        return True
    
    return False


# ============================================================================
# FUNCIONES DE SESIONES (CRUD)
# ============================================================================

def create_session(
    project_id: str,
    minutes: int,
    session_type: str = "pomodoro",
    pomodoros: int = 1,
    session_date: str = None
) -> Optional[Dict]:
    """
    Crea una nueva sesión de enfoque.
    
    Args:
        project_id: UUID del proyecto asociado
        minutes: Duración en minutos
        session_type: Tipo (pomodoro | custom)
        pomodoros: Número de pomodoros (1 para pomodoro estándar)
        session_date: Fecha opcional (usa hoy si no se especifica)
        
    Returns:
        Diccionario de la sesión creada o None si el proyecto no existe
    """
    # Verificar que el proyecto existe
    if not get_project_by_id(project_id):
        return None
    
    # Cargar sesiones existentes
    sessions = get_all_sessions()
    
    # Crear nueva sesión
    new_session = {
        "id": str(uuid.uuid4()),
        "project_id": project_id,
        "date": session_date or date.today().isoformat(),
        "minutes": minutes,
        "pomodoros": pomodoros,
        "session_type": session_type,
        "created_at": datetime.now().isoformat()
    }
    
    # Agregar y guardar
    sessions.append(new_session)
    write_json_file(SESSIONS_FILE, sessions)
    
    return new_session


def delete_session(session_id: str) -> bool:
    """
    Elimina una sesión específica.
    
    Args:
        session_id: UUID de la sesión
        
    Returns:
        True si se eliminó, False si no existía
    """
    sessions = get_all_sessions()
    original_count = len(sessions)
    
    sessions = [s for s in sessions if s.get('id') != session_id]
    
    if len(sessions) < original_count:
        write_json_file(SESSIONS_FILE, sessions)
        return True
    
    return False


# ============================================================================
# FUNCIONES DE CÁLCULO Y AGREGACIÓN
# ============================================================================

def calculate_daily_progress(target_date: str = None) -> Dict:
    """
    Calcula el progreso del día.
    
    Args:
        target_date: Fecha en formato YYYY-MM-DD (hoy por defecto)
        
    Returns:
        Diccionario con estadísticas del día
    """
    if target_date is None:
        target_date = date.today().isoformat()
    
    sessions = get_sessions_by_date(target_date)
    
    total_minutes = sum(s.get('minutes', 0) for s in sessions)
    total_pomodoros = sum(s.get('pomodoros', 0) for s in sessions)
    total_sessions = len(sessions)
    
    return {
        "date": target_date,
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 2),
        "total_pomodoros": total_pomodoros,
        "total_sessions": total_sessions
    }


def calculate_monthly_progress(year: int = None, month: int = None) -> Dict:
    """
    Calcula el progreso del mes.
    
    Args:
        year: Año (año actual por defecto)
        month: Mes (mes actual por defecto)
        
    Returns:
        Diccionario con estadísticas del mes
    """
    today = date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    
    sessions = get_sessions_by_month(year, month)
    
    total_minutes = sum(s.get('minutes', 0) for s in sessions)
    total_pomodoros = sum(s.get('pomodoros', 0) for s in sessions)
    total_sessions = len(sessions)
    
    # Días activos (días únicos con al menos una sesión)
    active_days = len(set(s.get('date') for s in sessions))
    
    return {
        "year": year,
        "month": month,
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 2),
        "total_pomodoros": total_pomodoros,
        "total_sessions": total_sessions,
        "active_days": active_days
    }


def calculate_project_progress(project_id: str, year: int = None, month: int = None) -> Dict:
    """
    Calcula el progreso de un proyecto específico en un mes.
    
    Args:
        project_id: UUID del proyecto
        year: Año (año actual por defecto)
        month: Mes (mes actual por defecto)
        
    Returns:
        Diccionario con estadísticas del proyecto
    """
    today = date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    
    project = get_project_by_id(project_id)
    if not project:
        return None
    
    # Obtener sesiones del proyecto en el mes
    all_month_sessions = get_sessions_by_month(year, month)
    project_sessions = [s for s in all_month_sessions if s.get('project_id') == project_id]
    
    total_minutes = sum(s.get('minutes', 0) for s in project_sessions)
    total_pomodoros = sum(s.get('pomodoros', 0) for s in project_sessions)
    total_sessions = len(project_sessions)
    
    # Calcular progreso según tipo de meta
    goal_type = project.get('goal_type', 'pomodoro')
    monthly_goal = project.get('monthly_goal', 20)
    
    if goal_type == 'pomodoro':
        current = total_pomodoros
    elif goal_type == 'time':
        current = total_minutes
    else:  # sessions
        current = total_sessions
    
    percentage = min(100, round((current / monthly_goal) * 100, 1)) if monthly_goal > 0 else 0
    goal_reached = current >= monthly_goal
    
    return {
        "project_id": project_id,
        "project_name": project.get('name'),
        "project_color": project.get('color'),
        "goal_type": goal_type,
        "monthly_goal": monthly_goal,
        "current": current,
        "percentage": percentage,
        "goal_reached": goal_reached,
        "total_minutes": total_minutes,
        "total_pomodoros": total_pomodoros,
        "total_sessions": total_sessions
    }


def get_daily_activity_for_month(year: int, month: int) -> Dict[str, int]:
    """
    Obtiene la actividad diaria para un mes (para el heatmap).
    
    Args:
        year: Año
        month: Mes
        
    Returns:
        Diccionario {fecha: minutos_totales}
    """
    sessions = get_sessions_by_month(year, month)
    
    activity = {}
    for session in sessions:
        date_str = session.get('date')
        minutes = session.get('minutes', 0)
        activity[date_str] = activity.get(date_str, 0) + minutes
    
    return activity


def get_sessions_by_year(year: int) -> List[Dict]:
    """
    Obtiene todas las sesiones de un año específico.
    
    Args:
        year: Año (ej: 2024)
        
    Returns:
        Lista de sesiones del año
    """
    sessions = get_all_sessions()
    year_prefix = f"{year}-"
    return [s for s in sessions if s.get('date', '').startswith(year_prefix)]


def get_year_activity_by_project(year: int) -> Dict[str, set]:
    """
    Obtiene los días con actividad para cada proyecto en un año.
    
    Args:
        year: Año
        
    Returns:
        Diccionario {project_id: set(fechas_con_actividad)}
    """
    sessions = get_sessions_by_year(year)
    
    activity = {}
    for session in sessions:
        project_id = session.get('project_id')
        date_str = session.get('date')
        
        if project_id and date_str:
            if project_id not in activity:
                activity[project_id] = set()
            activity[project_id].add(date_str)
    
    return activity


# ============================================================================
# INICIALIZACIÓN AL IMPORTAR
# ============================================================================

# Asegurar que los archivos existen al importar el módulo
initialize_all_files()