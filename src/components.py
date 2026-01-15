"""
components.py - Componentes UI reutilizables

Este módulo contiene componentes de interfaz personalizados
con estilos CSS para el tema girly-pop.

Autor: Focus Flow Team
"""

import streamlit as st
from typing import Tuple


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 ESTILOS CSS GLOBALES

def inject_custom_css():
    """
    Inyecta CSS personalizado para el tema girly-pop dark mode.
    Debe llamarse al inicio de la aplicación.
    """
    st.markdown("""
    <style>
        /* IMPORTAR FUENTE */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* VARIABLES CSS */
        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #1a1a1a;
            --bg-tertiary: #252525;
            --color-primary: #ff7eb6;
            --color-secondary: #b8a9ff;
            --color-accent: #ffb86c;
            --color-text: #fafafa;
            --color-muted: #6b6b6b;
            --color-success: #98d8aa;
            --color-danger: #ff6b6b;
            --font-main: 'Plus Jakarta Sans', sans-serif;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 20px;
            --shadow-glow: 0 0 20px rgba(255, 126, 182, 0.3);
        }
        
        /* BASE STYLES */
        .stApp {
            font-family: var(--font-main);
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            font-family: var(--font-main) !important;
            font-weight: 600 !important;
        }
        
        h1 {
            background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* CARDS Y CONTENEDORES */
        .metric-card {
            background: linear-gradient(145deg, #1f1f1f, #171717);
            border: 1px solid #2a2a2a;
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            border-color: var(--color-primary);
            box-shadow: var(--shadow-glow);
            transform: translateY(-2px);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--color-primary);
            line-height: 1.2;
        }
        
        .metric-label {
            font-size: 0.875rem;
            color: var(--color-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 0.5rem;
        }
        
        /* Project Card */
        .project-card {
            background: var(--bg-secondary);
            border: 1px solid #2a2a2a;
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            margin: 0.75rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
            transition: all 0.3s ease;
        }
        
        .project-card:hover {
            transform: translateX(8px);
            border-color: var(--color-primary);
        }
        
        .project-color-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        
        .project-name {
            font-weight: 600;
            color: var(--color-text);
            flex-grow: 1;
        }
        
        .project-progress {
            font-size: 0.875rem;
            color: var(--color-muted);
        }
        
        /* BOTONES */
        .stButton > button {
            font-family: var(--font-main) !important;
            font-weight: 600 !important;
            border-radius: var(--radius-md) !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-glow) !important;
        }
        
        /* Primary Button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--color-primary), #ff9ecc) !important;
            color: #0a0a0a !important;
            border: none !important;
        }
        
        /* Secondary Button */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            border: 2px solid var(--color-primary) !important;
            color: var(--color-primary) !important;
        }
        
        /* TIMER DISPLAY */
        .timer-display {
            font-size: 6rem;
            font-weight: 700;
            font-family: 'Plus Jakarta Sans', monospace;
            color: var(--color-text);
            text-align: center;
            padding: 2rem;
            background: linear-gradient(145deg, #1a1a1a, #0f0f0f);
            border-radius: var(--radius-lg);
            border: 2px solid var(--color-primary);
            box-shadow: 0 0 40px rgba(255, 126, 182, 0.2);
            margin: 2rem 0;
        }
        
        .timer-active {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 40px rgba(255, 126, 182, 0.2); }
            50% { box-shadow: 0 0 60px rgba(255, 126, 182, 0.4); }
        }
        
        /* INPUTS Y SELECTORES */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div {
            background-color: var(--bg-secondary) !important;
            border: 1px solid #2a2a2a !important;
            border-radius: var(--radius-md) !important;
            color: var(--color-text) !important;
            font-family: var(--font-main) !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--color-primary) !important;
            box-shadow: 0 0 0 2px rgba(255, 126, 182, 0.2) !important;
        }
        
        /* TABS */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background-color: var(--bg-secondary);
            padding: 0.5rem;
            border-radius: var(--radius-lg);
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            color: var(--color-muted);
            border-radius: var(--radius-md);
            padding: 0.75rem 1.5rem;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--color-primary) !important;
            color: #0a0a0a !important;
        }
        
        /* SIDEBAR */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f0f, #0a0a0a);
            border-right: 1px solid #1a1a1a;
        }
        
        [data-testid="stSidebar"] .stRadio label {
            padding: 0.75rem 1rem;
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
        }
        
        [data-testid="stSidebar"] .stRadio label:hover {
            background-color: var(--bg-secondary);
        }
        
        /* PROGRESS BARS */
        .stProgress > div > div {
            background: linear-gradient(90deg, var(--color-primary), var(--color-secondary)) !important;
            border-radius: var(--radius-sm);
        }
        
        /* DIVIDERS */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #2a2a2a, transparent);
            margin: 2rem 0;
        }
        
        /* SCROLLBAR */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--bg-tertiary);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--color-muted);
        }
        
        /* ANIMACIONES */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease forwards;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .slide-in {
            animation: slideIn 0.4s ease forwards;
        }
        
        /* TOAST / NOTIFICACIONES */
        .success-toast {
            background: linear-gradient(135deg, #1a3a2a, #0f2a1a);
            border: 1px solid var(--color-success);
            border-radius: var(--radius-md);
            padding: 1rem 1.5rem;
            color: var(--color-success);
            font-weight: 500;
        }
        
        .error-toast {
            background: linear-gradient(135deg, #3a1a1a, #2a0f0f);
            border: 1px solid var(--color-danger);
            border-radius: var(--radius-md);
            padding: 1rem 1.5rem;
            color: var(--color-danger);
            font-weight: 500;
        }
        
        /* BADGE / TAGS */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .badge-primary {
            background: rgba(255, 126, 182, 0.2);
            color: var(--color-primary);
        }
        
        .badge-success {
            background: rgba(152, 216, 170, 0.2);
            color: var(--color-success);
        }
        
        /* OCULTAR ELEMENTOS DEFAULT */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* RESPONSIVE */
        @media (max-width: 768px) {
            .timer-display {
                font-size: 4rem;
                padding: 1.5rem;
            }
            
            .metric-value {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 COMPONENTES HTML PERSONALIZADOS

def metric_card(value: str, label: str, icon: str = ""):
    """
    Renderiza una tarjeta de métrica estilizada.
    
    Args:
        value: Valor principal a mostrar
        label: Etiqueta descriptiva
        icon: Emoji o icono (opcional)
    """
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def project_card(name: str, color: str, progress: str, percentage: float):
    """
    Renderiza una tarjeta de proyecto con indicador de color.
    
    Args:
        name: Nombre del proyecto
        color: Color hex del proyecto
        progress: Texto de progreso (ej: "15/20")
        percentage: Porcentaje de completitud
    """
    # Determinar si la meta fue alcanzada
    badge = ""
    if percentage >= 100:
        badge = '<span class="badge badge-success">✓ META</span>'
    
    st.markdown(f"""
    <div class="project-card">
        <div class="project-color-dot" style="background-color: {color};"></div>
        <div class="project-name">{name}</div>
        <div class="project-progress">{progress} {badge}</div>
    </div>
    """, unsafe_allow_html=True)


def timer_display(minutes: int, seconds: int, is_active: bool = False):
    """
    Renderiza el display del timer con estilo.
    
    Args:
        minutes: Minutos restantes
        seconds: Segundos restantes
        is_active: Si el timer está corriendo (activa animación)
    """
    active_class = "timer-active" if is_active else ""
    st.markdown(f"""
    <div class="timer-display {active_class}">
        {minutes:02d}:{seconds:02d}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    """
    Renderiza un encabezado de sección estilizado.
    
    Args:
        title: Título principal
        subtitle: Subtítulo opcional
    """
    subtitle_html = f'<p style="color: #6b6b6b; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="margin-bottom: 0;">{title}</h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def success_message(text: str):
    """Muestra un mensaje de éxito estilizado."""
    st.markdown(f"""
    <div class="success-toast">
        ✓ {text}
    </div>
    """, unsafe_allow_html=True)


def error_message(text: str):
    """Muestra un mensaje de error estilizado."""
    st.markdown(f"""
    <div class="error-toast">
        ✕ {text}
    </div>
    """, unsafe_allow_html=True)


def color_picker_grid() -> Tuple[str, ...]:
    """
    Retorna la paleta de colores disponible para proyectos.
    
    Returns:
        Tupla de colores hex
    """
    return (
        "#ff7eb6",  # Rosa neón
        "#b8a9ff",  # Lavanda
        "#ffb86c",  # Peach
        "#7ee8fa",  # Cyan
        "#98d8aa",  # Verde menta
        "#ffd93d",  # Amarillo
        "#ff6b6b",  # Coral
        "#c9b1ff",  # Lila
        "#a8e6cf",  # Verde claro
        "#ffc8dd",  # Rosa claro
    )


def spacer(height: int = 20):
    """Agrega un espaciador vertical."""
    st.markdown(f'<div style="height: {height}px;"></div>', unsafe_allow_html=True)


def divider():
    """Renderiza un divisor estilizado."""
    st.markdown('<hr>', unsafe_allow_html=True)


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 COMPONENTES DE NAVEGACIÓN

def nav_item(icon: str, label: str, is_active: bool = False) -> str:
    """
    Genera HTML para un item de navegación.
    
    Args:
        icon: Emoji del icono
        label: Texto del item
        is_active: Si está seleccionado
        
    Returns:
        String HTML
    """
    active_style = "background: rgba(255, 126, 182, 0.2); color: #ff7eb6;" if is_active else ""
    return f"""
    <div style="
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin: 0.25rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
        {active_style}
    ">
        {icon} {label}
    </div>
    """


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 UTILIDADES DE LAYOUT

def centered_container(content: str, max_width: int = 800):
    """
    Envuelve contenido en un contenedor centrado.
    
    Args:
        content: HTML a centrar
        max_width: Ancho máximo en píxeles
    """
    st.markdown(f"""
    <div style="
        max-width: {max_width}px;
        margin: 0 auto;
        padding: 0 1rem;
    ">
        {content}
    </div>
    """, unsafe_allow_html=True)


def grid_layout(columns: int = 2):
    """
    Crea un layout de grid CSS.
    
    Args:
        columns: Número de columnas
        
    Returns:
        Objeto de columnas de Streamlit
    """
    return st.columns(columns, gap="medium")


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 INICIALIZACIÓN

def init_page_config():
    """
    Configura la página de Streamlit con los ajustes correctos.
    Debe llamarse al inicio de app.py
    """
    st.set_page_config(
        page_title="Focus Flow ✨",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
