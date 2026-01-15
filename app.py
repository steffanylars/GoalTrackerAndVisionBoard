"""
app.py - Focus Flow: Goal & Focus Tracker

Aplicación principal de Streamlit - Versión Interactiva Completa.
Una herramienta elegante para tracking de metas y sesiones de enfoque.

Autor: Steffany Lara :)
contacto:
    correo - steffany.lars@gmail.com
    instragram - steffanylars
    linkedin - steffanylars

Versión: 2.1.0
"""

import streamlit as st
import time
from datetime import date, datetime
import pandas as pd

# Importar módulos locales
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_manager import (
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
    get_project_by_id,
)
from src.visualizations import (
    create_progress_ring,
    create_multi_ring,
    create_monthly_heatmap,
    COLORS,
    PROJECT_COLORS,
)
from src.components import (
    inject_custom_css,
    color_picker_grid,
)
from src.utils import (
    format_minutes,
    format_timer,
    get_month_name,
    get_available_months,
    calculate_percentage,
    get_progress_status,
    get_goal_type_label,
    is_valid_project_name,
    POMODORO_DURATION,
)


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 CONFIGURACIÓN INICIAL

st.set_page_config(
    page_title="Flow",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 ESTADO DE LA SESIÓN

def init_session_state():
    """Inicializa el estado de la sesión de Streamlit."""
    
    defaults = {
        'timer_running': False,
        'timer_seconds': POMODORO_DURATION * 60,
        'timer_initial': POMODORO_DURATION * 60,
        'selected_project_id': None,
        'timer_mode': "pomodoro",
        'current_view': "dashboard",
        'edit_project_id': None,
        'show_new_project_form': False,
        'selected_year': date.today().year,
        'selected_month': date.today().month,
        'selected_color': "#ff7eb6",
        'confirm_delete': None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 SIDEBAR - NAVEGACIÓN

def render_sidebar():
    """Renderiza la barra lateral de navegación."""
    
    with st.sidebar:
        # Logo y título
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <h1 style="
                font-size: 1.8rem;
                background: linear-gradient(135deg, #ff7eb6, #b8a9ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
            ">✨ Flow de Dariux</h1>
            <p style="color: #6b6b6b; font-size: 0.85rem; margin-top: 0.5rem;">
                Tu tracker de metas
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Navegación con radio buttons
        view_options = {
            "dashboard": "Dashboard",
            "projects": "Proyectos", 
            "timer": "Focus Timer",
            "monthly": "Vista Mensual",
        }
        
        selected = st.radio(
            "Navegación",
            options=list(view_options.keys()),
            format_func=lambda x: view_options[x],
            index=list(view_options.keys()).index(st.session_state.current_view),
            label_visibility="collapsed"
        )
        
        if selected != st.session_state.current_view:
            st.session_state.current_view = selected
            st.rerun()
        
        st.divider()
        
        # Resumen rápido
        daily = calculate_daily_progress()
        st.markdown(f"""
        <div style="
            background: #1a1a1a;
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
        ">
            <p style="color: #6b6b6b; font-size: 0.75rem; margin: 0;">HOY</p>
            <p style="color: #ff7eb6; font-size: 1.5rem; font-weight: 700; margin: 0.25rem 0;">
                {format_minutes(daily['total_minutes'])}
            </p>
            <p style="color: #6b6b6b; font-size: 0.85rem; margin: 0;">
                {daily['total_pomodoros']} 🍅 · {daily['total_sessions']} sesiones
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()



        # Logo y título
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <h1 style="
                font-size: 1.8rem;
                background: linear-gradient(135deg, #ff7eb6, #b8a9ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
            "></h1>
            <p style="color: #6b6b6b; font-size: 0.85rem; margin-top: 0.5rem;">
                Powered by Steff 
            </p>
        </div>
        """, unsafe_allow_html=True)


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 VISTA: DASHBOARD

def render_dashboard():
    """Renderiza la vista del dashboard principal."""
    
    st.markdown("# Dashboard")
    st.markdown("*Si llegas a tu meta, te compro un collar.*")
    st.markdown("")
    
    # Obtener datos
    daily = calculate_daily_progress()
    monthly = calculate_monthly_progress()
    projects = get_all_projects()
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tiempo hoy", format_minutes(daily['total_minutes']))
    
    with col2:
        st.metric("Pomodoros hoy", daily['total_pomodoros'])
    
    with col3:
        st.metric(f"Total {get_month_name(monthly['month'])}", format_minutes(monthly['total_minutes']))
    
    with col4:
        st.metric("Racha", monthly['active_days'])
    
    st.markdown("")
    st.divider()
    
    # Anillos de progreso por proyecto
    if projects:
        st.markdown("### Progreso por Proyecto")
        
        # Crear datos para visualización
        ring_data = []
        project_stats = []
        
        for project in projects:
            progress = calculate_project_progress(project['id'])
            if progress:
                ring_data.append({
                    'percentage': progress['percentage'],
                    'color': project.get('color', COLORS['primary'])
                })
                project_stats.append(progress)
        
        col_ring, col_legend = st.columns([1, 2])
        
        with col_ring:
            if ring_data:
                fig = create_multi_ring(ring_data[:4], size=280)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key="dashboard_multi_ring")
        
        with col_legend:
            for stat in project_stats[:4]:
                col_info, col_pct = st.columns([3, 1])
                with col_info:
                    st.markdown(f"""
                    <div style="
                        padding: 0.5rem 0;
                        border-left: 4px solid {stat['project_color']};
                        padding-left: 12px;
                        margin-bottom: 8px;
                    ">
                        <strong style="color: #fafafa;">{stat['project_name']}</strong><br>
                        <span style="color: #6b6b6b; font-size: 0.85rem;">
                            {stat['current']} / {stat['monthly_goal']} {get_goal_type_label(stat['goal_type']).lower()}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_pct:
                    st.markdown(f"""
                    <div style="text-align: right; padding-top: 8px;">
                        <span style="font-size: 1.2rem; font-weight: 700; color: {stat['project_color']};">
                            {int(stat['percentage'])}%
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
    
    else:
        st.info("Bienvenido! Crea tu primer proyecto para comenzar a trackear tu progreso.")
        if st.button("Crear mi primer proyecto", type="primary"):
            st.session_state.current_view = "projects"
            st.session_state.show_new_project_form = True
            st.rerun()


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 VISTA: PROYECTOS

def render_projects():
    """Renderiza la vista de gestión de proyectos."""
    
    st.markdown("# Proyectos")
    st.markdown("*Gestiona tus proyectos y metas*")
    st.markdown("")
    
    # Botón para nuevo proyecto
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("+ Nuevo Proyecto", type="primary", use_container_width=True):
            st.session_state.show_new_project_form = True
            st.session_state.edit_project_id = None
    
    st.markdown("")
    
    # Formulario de nuevo proyecto
    if st.session_state.show_new_project_form:
        render_new_project_form()
    
    # Lista de proyectos existentes
    projects = get_all_projects()
    
    if projects:
        st.markdown("### Tus Proyectos")
        
        for project in projects:
            render_project_card(project)
    
    elif not st.session_state.show_new_project_form:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 3rem;
            background: #1a1a1a;
            border-radius: 20px;
            border: 2px dashed #2a2a2a;
            margin-top: 2rem;
        ">
            <p style="font-size: 3rem; margin-bottom: 1rem;">📁</p>
            <p style="color: #fafafa; font-size: 1.1rem; margin-bottom: 0.5rem;">
                No tienes proyectos aún
            </p>
            <p style="color: #6b6b6b;">
                Crea tu primer proyecto para comenzar a trackear
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_new_project_form():
    """Formulario para crear un nuevo proyecto."""
    
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, #1f1f1f, #151515);
            border: 1px solid #ff7eb6;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        ">
        """, unsafe_allow_html=True)
        
        st.markdown("#### Nuevo Proyecto")
        
        with st.form("new_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    "Nombre del proyecto *",
                    placeholder="Ej: Estudio de alemán"
                )
                
                goal_type = st.selectbox(
                    "Tipo de meta",
                    options=['pomodoro', 'time', 'sessions'],
                    format_func=lambda x: {
                        'pomodoro': '🍅 Pomodoros',
                        'time': 'Minutos',
                        'sessions': 'Sesiones'
                    }.get(x, x)
                )
            
            with col2:
                monthly_goal = st.number_input(
                    "Meta mensual *",
                    min_value=1,
                    max_value=10000,
                    value=20,
                    help="Cantidad a alcanzar cada mes"
                )
                
                color = st.selectbox(
                    "Color del proyecto",
                    options=list(color_picker_grid()),
                    format_func=lambda x: {
                        "#ff7eb6": "🩷 Rosa",
                        "#b8a9ff": "💜 Lavanda", 
                        "#ffb86c": "🧡 Peach",
                        "#7ee8fa": "💙 Cyan",
                        "#98d8aa": "💚 Menta",
                        "#ffd93d": "💛 Amarillo",
                        "#ff6b6b": "❤️ Coral",
                        "#c9b1ff": "💟 Lila",
                        "#a8e6cf": "🌿 Verde claro",
                        "#ffc8dd": "🌸 Rosa claro",
                    }.get(x, x)
                )
            
            col_cancel, col_submit = st.columns(2)
            
            with col_cancel:
                cancel = st.form_submit_button("Cancelar", use_container_width=True)
            
            with col_submit:
                submit = st.form_submit_button("Crear Proyecto", type="primary", use_container_width=True)
            
            if cancel:
                st.session_state.show_new_project_form = False
                st.rerun()
            
            if submit:
                is_valid, error_msg = is_valid_project_name(name)
                
                if not is_valid:
                    st.error(f"{error_msg}")
                else:
                    create_project(
                        name=name.strip(),
                        color=color,
                        goal_type=goal_type,
                        monthly_goal=monthly_goal
                    )
                    st.success(f"Proyecto '{name}' creado exitosamente!")
                    st.session_state.show_new_project_form = False
                    time.sleep(0.5)
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)


def render_project_card(project: dict):
    """Renderiza una tarjeta de proyecto con acciones."""
    
    progress = calculate_project_progress(project['id'])
    
    with st.container():
        col_main, col_ring, col_actions = st.columns([3, 1, 1])
        
        with col_main:
            st.markdown(f"""
            <div style="
                background: #1a1a1a;
                border-radius: 12px;
                padding: 1rem;
                border-left: 4px solid {project.get('color', '#ff7eb6')};
            ">
                <h4 style="margin: 0; color: #fafafa;">{project['name']}</h4>
                <p style="color: #6b6b6b; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                    Meta: {project['monthly_goal']} {get_goal_type_label(project['goal_type']).lower()} / mes
                </p>
                <p style="color: #6b6b6b; margin: 0.25rem 0 0 0; font-size: 0.85rem;">
                    Progreso: {progress['current'] if progress else 0} / {project['monthly_goal']}
                    ({progress['percentage'] if progress else 0}%)
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_ring:
            if progress:
                fig = create_progress_ring(
                    progress['percentage'],
                    color=project.get('color'),
                    size=100,
                    show_percentage=True
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"project_ring_{project['id']}")
        
        with col_actions:
            st.markdown("<div style='padding-top: 20px;'>", unsafe_allow_html=True)
            
            # Botón eliminar con confirmación
            if st.session_state.confirm_delete == project['id']:
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("Si", key=f"yes_{project['id']}", help="Confirmar"):
                        delete_project(project['id'])
                        st.session_state.confirm_delete = None
                        st.rerun()
                with col_no:
                    if st.button("No", key=f"no_{project['id']}", help="Cancelar"):
                        st.session_state.confirm_delete = None
                        st.rerun()
            else:
                if st.button("Eliminar", key=f"del_{project['id']}", help="Eliminar proyecto"):
                    st.session_state.confirm_delete = project['id']
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("")


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 VISTA: FOCUS TIMER

def render_timer():
    """Renderiza la vista del timer/pomodoro."""
    
    st.markdown("# ⏱️ Focus Timer")
    st.markdown("*Mantén tu enfoque con el método Pomodoro*")
    st.markdown("")
    
    projects = get_all_projects()
    
    if not projects:
        st.warning("Necesitas crear al menos un proyecto para usar el timer.")
        if st.button("Crear proyecto", type="primary"):
            st.session_state.current_view = "projects"
            st.session_state.show_new_project_form = True
            st.rerun()
        return
    
    # Configuración del timer
    col1, col2 = st.columns(2)
    
    with col1:
        project_options = {p['id']: f"{p['name']}" for p in projects}
        project_list = list(project_options.keys())
        
        # Asegurar que hay un proyecto seleccionado válido
        if st.session_state.selected_project_id not in project_list:
            st.session_state.selected_project_id = project_list[0]
        
        selected_idx = project_list.index(st.session_state.selected_project_id)
        
        selected_project = st.selectbox(
            "Proyecto",
            options=project_list,
            format_func=lambda x: project_options.get(x, x),
            index=selected_idx
        )
        st.session_state.selected_project_id = selected_project
    
    with col2:
        timer_mode = st.selectbox(
            "Modo",
            options=['pomodoro', 'custom'],
            format_func=lambda x: '🍅 Pomodoro (25 min)' if x == 'pomodoro' else 'Personalizado'
        )
        st.session_state.timer_mode = timer_mode
    
    # Duración personalizada
    if timer_mode == 'custom':
        custom_minutes = st.slider(
            "Duración (minutos)",
            min_value=5,
            max_value=120,
            value=25,
            step=5
        )
        target_seconds = custom_minutes * 60
    else:
        target_seconds = POMODORO_DURATION * 60
    
    # Actualizar timer si no está corriendo
    if not st.session_state.timer_running and st.session_state.timer_seconds == st.session_state.timer_initial:
        st.session_state.timer_seconds = target_seconds
        st.session_state.timer_initial = target_seconds
    
    st.markdown("")
    
    # Display del timer
    minutes, seconds = format_timer(st.session_state.timer_seconds)
    progress_pct = (st.session_state.timer_seconds / st.session_state.timer_initial) * 100 if st.session_state.timer_initial > 0 else 0
    
    # Estado del timer
    if st.session_state.timer_running:
        status_text = "EN PROGRESO"
        border_color = "#ff7eb6"
        glow = "0 0 40px rgba(255, 126, 182, 0.4)"
    elif st.session_state.timer_seconds < st.session_state.timer_initial:
        status_text = "PAUSADO"
        border_color = "#ffd93d"
        glow = "0 0 20px rgba(255, 217, 61, 0.3)"
    else:
        status_text = "LISTO"
        border_color = "#2a2a2a"
        glow = "none"
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 2rem;
        background: linear-gradient(145deg, #1a1a1a, #0f0f0f);
        border-radius: 24px;
        border: 3px solid {border_color};
        box-shadow: {glow};
        margin: 1rem 0 2rem 0;
    ">
        <p style="color: #6b6b6b; font-size: 0.9rem; margin-bottom: 0.5rem;">
            {status_text}
        </p>
        <p style="
            font-size: 5rem;
            font-weight: 700;
            color: #fafafa;
            margin: 0;
            font-family: monospace;
        ">{minutes:02d}:{seconds:02d}</p>
        <div style="
            width: 80%;
            height: 8px;
            background: #2a2a2a;
            border-radius: 4px;
            margin: 1.5rem auto 0;
            overflow: hidden;
        ">
            <div style="
                width: {progress_pct}%;
                height: 100%;
                background: linear-gradient(90deg, #ff7eb6, #b8a9ff);
                border-radius: 4px;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Controles
    col_start, col_reset, col_save = st.columns(3)
    
    with col_start:
        btn_label = "Pausar" if st.session_state.timer_running else "Iniciar"
        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state.timer_running = not st.session_state.timer_running
            st.rerun()
    
    with col_reset:
        if st.button("Reiniciar", use_container_width=True):
            st.session_state.timer_running = False
            st.session_state.timer_seconds = target_seconds
            st.session_state.timer_initial = target_seconds
            st.rerun()
    
    with col_save:
        if st.button("Guardar Sesión", use_container_width=True):
            # Calcular tiempo trabajado
            elapsed_seconds = st.session_state.timer_initial - st.session_state.timer_seconds
            elapsed_minutes = max(1, elapsed_seconds // 60)
            
            # Determinar pomodoros
            pomodoros = 1 if timer_mode == 'pomodoro' and elapsed_minutes >= 20 else 0
            
            # Guardar sesión
            create_session(
                project_id=st.session_state.selected_project_id,
                minutes=elapsed_minutes,
                session_type=timer_mode,
                pomodoros=pomodoros
            )
            
            st.success(f"Sesión guardada! {elapsed_minutes} minutos registrados")
            
            # Reset timer
            st.session_state.timer_running = False
            st.session_state.timer_seconds = target_seconds
            st.session_state.timer_initial = target_seconds
            time.sleep(1)
            st.rerun()
    
    # Auto-decrement timer
    if st.session_state.timer_running:
        st.markdown("""
        <p style="text-align: center; color: #6b6b6b; font-size: 0.85rem; margin-top: 1rem;">
            El timer se actualiza automáticamente
        </p>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        if st.session_state.timer_seconds > 0:
            st.session_state.timer_seconds -= 1
            st.rerun()
        else:
            # Timer completado!
            st.session_state.timer_running = False
            
            elapsed_minutes = st.session_state.timer_initial // 60
            pomodoros = 1 if timer_mode == 'pomodoro' else 0
            
            create_session(
                project_id=st.session_state.selected_project_id,
                minutes=elapsed_minutes,
                session_type=timer_mode,
                pomodoros=pomodoros
            )
            
            st.balloons()
            st.success(f"Completado! {elapsed_minutes} minutos guardados automáticamente")
            
            st.session_state.timer_seconds = target_seconds
            st.session_state.timer_initial = target_seconds


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 VISTA: MENSUAL

def render_monthly():
    """Renderiza la vista mensual con heatmap y progreso por proyecto."""
    
    st.markdown("# Vista Mensual")
    st.markdown("*Tu actividad en perspectiva*")
    st.markdown("")
    
    # Selector de mes
    available_months = get_available_months()
    
    if available_months:
        month_options = {f"{y}-{m}": name for y, m, name in available_months}
        current_key = f"{st.session_state.selected_year}-{st.session_state.selected_month}"
        
        if current_key not in month_options:
            current_key = list(month_options.keys())[0]
            parts = current_key.split('-')
            st.session_state.selected_year = int(parts[0])
            st.session_state.selected_month = int(parts[1])
        
        selected_month_key = st.selectbox(
            "Seleccionar mes",
            options=list(month_options.keys()),
            format_func=lambda x: month_options.get(x, x),
            index=list(month_options.keys()).index(current_key)
        )
        
        parts = selected_month_key.split('-')
        st.session_state.selected_year = int(parts[0])
        st.session_state.selected_month = int(parts[1])
    
    year = st.session_state.selected_year
    month = st.session_state.selected_month
    
    st.divider()
    
    # Heatmap de actividad
    st.markdown("### Actividad Diaria")
    
    activity_data = get_daily_activity_for_month(year, month)
    
    if activity_data:
        fig = create_monthly_heatmap(activity_data, year, month)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key="monthly_heatmap")
        
        # Leyenda
        st.markdown("""
        <p style="text-align: center; color: #6b6b6b; font-size: 0.8rem;">
            Más oscuro = menos actividad · Más brillante = más actividad
        </p>
        """, unsafe_allow_html=True)
    else:
        st.info("Sin actividad registrada este mes. Comienza una sesión de enfoque!")
    
    st.divider()
    
    # Progreso por proyecto con círculos
    st.markdown("### Progreso de Metas")
    
    projects = get_all_projects()
    
    if projects:
        # Mostrar proyectos en grid
        num_cols = min(len(projects), 3)
        cols = st.columns(num_cols)
        
        for i, project in enumerate(projects):
            progress = calculate_project_progress(project['id'], year, month)
            
            if progress:
                with cols[i % num_cols]:
                    # Círculo de progreso
                    fig = create_progress_ring(
                        progress['percentage'],
                        color=project.get('color', '#ff7eb6'),
                        size=180,
                        show_percentage=False,
                        center_text=f"{progress['current']}/{progress['monthly_goal']}",
                        center_subtext=get_goal_type_label(progress['goal_type'])
                    )
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"monthly_ring_{project['id']}")
                    
                    # Info del proyecto
                    goal_reached = "META ALCANZADA!" if progress['percentage'] >= 100 else f"{int(progress['percentage'])}% completado"
                    
                    st.markdown(f"""
                    <div style="text-align: center; margin-top: -15px;">
                        <p style="color: {project.get('color', '#ff7eb6')}; font-weight: 600; margin: 0; font-size: 1.1rem;">
                            {project['name']}
                        </p>
                        <p style="color: {'#98d8aa' if progress['percentage'] >= 100 else '#6b6b6b'}; font-size: 0.85rem; margin: 0.25rem 0 0 0;">
                            {goal_reached}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("")
    else:
        st.info("No hay proyectos. Crea uno para ver tu progreso aquí.")
    
    st.divider()
    
    # Resumen del mes
    st.markdown("### Resumen del Mes")
    
    monthly_stats = calculate_monthly_progress(year, month)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tiempo total", format_minutes(monthly_stats['total_minutes']))
    
    with col2:
        st.metric("Pomodoros 🍅", monthly_stats['total_pomodoros'])
    
    with col3:
        st.metric("Sesiones", monthly_stats['total_sessions'])
    
    with col4:
        st.metric("Racha", monthly_stats['active_days'])


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 AGREGAR SESIÓN MANUAL

def render_add_session_form():
    """Formulario para agregar sesión manual."""
    
    with st.expander("Agregar sesión manual", expanded=False):
        projects = get_all_projects()
        
        if not projects:
            st.warning("Primero crea un proyecto")
            return
        
        with st.form("add_session_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_id = st.selectbox(
                    "Proyecto",
                    options=[p['id'] for p in projects],
                    format_func=lambda x: next((p['name'] for p in projects if p['id'] == x), x)
                )
                
                minutes = st.number_input("Minutos", min_value=1, max_value=480, value=25)
            
            with col2:
                session_date = st.date_input("Fecha", value=date.today())
                
                session_type = st.selectbox(
                    "Tipo",
                    options=['pomodoro', 'custom'],
                    format_func=lambda x: '🍅 Pomodoro' if x == 'pomodoro' else 'Custom'
                )
            
            if st.form_submit_button("Guardar Sesión", type="primary", use_container_width=True):
                pomodoros = 1 if session_type == 'pomodoro' else 0
                create_session(
                    project_id=project_id,
                    minutes=minutes,
                    session_type=session_type,
                    pomodoros=pomodoros,
                    session_date=session_date.isoformat()
                )
                st.success("Sesión agregada!")
                time.sleep(0.5)
                st.rerun()


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 MAIN

def main():
    """Función principal de la aplicación."""
    
    # Renderizar sidebar
    render_sidebar()
    
    # Renderizar vista actual
    if st.session_state.current_view == "dashboard":
        render_dashboard()
    elif st.session_state.current_view == "projects":
        render_projects()
    elif st.session_state.current_view == "timer":
        render_timer()
        st.divider()
        render_add_session_form()
    elif st.session_state.current_view == "monthly":
        render_monthly()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
