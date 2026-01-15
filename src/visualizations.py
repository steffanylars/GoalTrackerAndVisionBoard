"""
visualizations.py - Visualizaciones tipo Apple Watch y GitHub

Este módulo contiene funciones para crear:
- Círculos de progreso estilo Apple Watch Activity Ringsss de Health
- Heatmap de actividad estilo GitHub Contributions

Autor: Focus Flow Team
"""

import plotly.graph_objects as go
import numpy as np
from datetime import date, timedelta
import calendar
from typing import Dict, List, Tuple


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 PALETA DE COLORES

COLORS = {
    'background': '#0a0a0a',
    'surface': '#1a1a1a',
    'primary': '#ff7eb6',      # Rosa neón
    'secondary': '#b8a9ff',    # Lavanda
    'accent': '#ffb86c',       # Peach
    'text': '#fafafa',
    'muted': '#6b6b6b',
    'ring_bg': '#2a2a2a',      # Fondo de anillos
}

# Colores predefinidos para proyectos
PROJECT_COLORS = [
    '#ff7eb6',  # Rosa neón
    '#b8a9ff',  # Lavanda
    '#ffb86c',  # Peach
    '#7ee8fa',  # Cyan
    '#98d8aa',  # Verde menta
    '#ffd93d',  # Amarillo
    '#ff6b6b',  # Coral
    '#c9b1ff',  # Lila
]


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 APPLE WATCH STYLE RINGS

def create_progress_ring(
    percentage: float,
    color: str = None,
    size: int = 200,
    thickness: float = 0.15,
    show_percentage: bool = True,
    center_text: str = None,
    center_subtext: str = None
) -> go.Figure:
    """
    Crea un anillo de progreso estilo Apple Watch.
    
    Args:
        percentage: Progreso de 0 a 100 (puede ser > 100)
        color: Color del anillo (rosa por defecto)
        size: Tamaño en píxeles
        thickness: Grosor del anillo (0.1 - 0.3)
        show_percentage: Mostrar porcentaje en el centro
        center_text: Texto principal en el centro
        center_subtext: Texto secundario debajo
        
    Returns:
        Figura de Plotly
    """
    if color is None:
        color = COLORS['primary']
    
    # Normalizar porcentaje para el arco (máximo 100% por vuelta)
    display_percentage = min(percentage, 100)
    
    # Crear el arco de fondo (anillo completo)
    theta_bg = np.linspace(0, 360, 100)
    
    # Crear el arco de progreso
    theta_progress = np.linspace(90, 90 - (display_percentage / 100) * 360, 100)
    
    # Radio interno y externo
    r_outer = 1
    r_inner = 1 - thickness
    
    fig = go.Figure()
    
    # Anillo de fondo (gris oscuro)
    fig.add_trace(go.Scatterpolar(
        r=[r_outer] * 100,
        theta=theta_bg,
        mode='lines',
        line=dict(color=COLORS['ring_bg'], width=size * thickness * 0.5),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Anillo de progreso
    if percentage > 0:
        fig.add_trace(go.Scatterpolar(
            r=[r_outer] * 100,
            theta=theta_progress,
            mode='lines',
            line=dict(color=color, width=size * thickness * 0.5),
            hoverinfo='skip',
            showlegend=False
        ))
    
    # Texto central
    annotations = []
    
    if center_text:
        annotations.append(dict(
            text=f"<b>{center_text}</b>",
            x=0.5, y=0.55,
            font=dict(size=24, color=COLORS['text']),
            showarrow=False,
            xref='paper', yref='paper'
        ))
        if center_subtext:
            annotations.append(dict(
                text=center_subtext,
                x=0.5, y=0.42,
                font=dict(size=12, color=COLORS['muted']),
                showarrow=False,
                xref='paper', yref='paper'
            ))
    elif show_percentage:
        annotations.append(dict(
            text=f"<b>{int(percentage)}%</b>",
            x=0.5, y=0.5,
            font=dict(size=28, color=COLORS['text']),
            showarrow=False,
            xref='paper', yref='paper'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1.2]),
            angularaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=size,
        height=size,
        margin=dict(l=20, r=20, t=20, b=20),
        annotations=annotations,
        showlegend=False
    )
    
    return fig


def create_multi_ring(
    data: List[Dict],
    size: int = 280
) -> go.Figure:
    """
    Crea múltiples anillos concéntricos (estilo Apple Watch con múltiples métricas).
    
    Args:
        data: Lista de diccionarios con:
            - percentage: Progreso 0-100
            - color: Color del anillo
            - label: Etiqueta (opcional)
        size: Tamaño en píxeles
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    
    n_rings = len(data)
    if n_rings == 0:
        return fig
    
    # Calcular radios para cada anillo
    thickness = 0.12
    gap = 0.03
    
    for i, ring_data in enumerate(data):
        percentage = ring_data.get('percentage', 0)
        color = ring_data.get('color', PROJECT_COLORS[i % len(PROJECT_COLORS)])
        
        # Radio para este anillo (de afuera hacia adentro)
        r = 1 - (i * (thickness + gap))
        
        # Anillo de fondo
        theta_bg = np.linspace(0, 360, 100)
        fig.add_trace(go.Scatterpolar(
            r=[r] * 100,
            theta=theta_bg,
            mode='lines',
            line=dict(color=COLORS['ring_bg'], width=size * 0.06),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Anillo de progreso
        if percentage > 0:
            display_pct = min(percentage, 100)
            theta_progress = np.linspace(90, 90 - (display_pct / 100) * 360, 100)
            fig.add_trace(go.Scatterpolar(
                r=[r] * 100,
                theta=theta_progress,
                mode='lines',
                line=dict(color=color, width=size * 0.06),
                hoverinfo='skip',
                showlegend=False
            ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1.3]),
            angularaxis=dict(visible=False),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=size,
        height=size,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    
    return fig


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3GITHUB STYLE HEATMAP

def create_monthly_heatmap(
    activity_data: Dict[str, int],
    year: int,
    month: int,
    base_color: str = None,
    cell_size: int = 35
) -> go.Figure:
    """
    Crea un heatmap mensual estilo GitHub Contributions.
    
    Args:
        activity_data: Diccionario {fecha_YYYY-MM-DD: minutos}
        year: Año
        month: Mes
        base_color: Color base para el gradiente (rosa por defecto)
        cell_size: Tamaño de cada celda
        
    Returns:
        Figura de Plotly
    """
    if base_color is None:
        base_color = COLORS['primary']
    
    # Obtener información del mes
    first_day = date(year, month, 1)
    days_in_month = calendar.monthrange(year, month)[1]
    first_weekday = first_day.weekday()  # 0=Lunes, 6=Domingo
    
    # Crear matriz para el calendario (7 filas x ~6 columnas)
    # Filas: Lun, Mar, Mié, Jue, Vie, Sáb, Dom
    num_weeks = (days_in_month + first_weekday + 6) // 7
    
    # Matrices para el heatmap
    z_values = []
    text_values = []
    
    for week in range(num_weeks):
        week_values = []
        week_text = []
        
        for day_of_week in range(7):
            day_num = week * 7 + day_of_week - first_weekday + 1
            
            if 1 <= day_num <= days_in_month:
                date_str = f"{year}-{month:02d}-{day_num:02d}"
                minutes = activity_data.get(date_str, 0)
                week_values.append(minutes)
                
                if minutes > 0:
                    hours = minutes // 60
                    mins = minutes % 60
                    if hours > 0:
                        time_str = f"{hours}h {mins}m"
                    else:
                        time_str = f"{mins}m"
                    week_text.append(f"Día {day_num}<br>{time_str}")
                else:
                    week_text.append(f"Día {day_num}<br>Sin actividad")
            else:
                week_values.append(None)
                week_text.append("")
        
        z_values.append(week_values)
        text_values.append(week_text)
    
    # Transponer para que las filas sean días de la semana
    z_transposed = list(map(list, zip(*z_values)))
    text_transposed = list(map(list, zip(*text_values)))
    
    # Invertir para que Lunes esté arriba
    z_transposed = z_transposed[::-1]
    text_transposed = text_transposed[::-1]
    
    # Crear escala de colores personalizada (de gris a rosa)
    colorscale = [
        [0.0, COLORS['surface']],
        [0.01, '#3d2a35'],
        [0.25, '#6b3d5c'],
        [0.5, '#994d7a'],
        [0.75, '#cc6699'],
        [1.0, base_color]
    ]
    
    # Encontrar el máximo para normalizar
    max_minutes = max(
        (v for row in z_transposed for v in row if v is not None and v > 0),
        default=60
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=z_transposed,
        text=text_transposed,
        hovertemplate='%{text}<extra></extra>',
        colorscale=colorscale,
        zmin=0,
        zmax=max_minutes,
        showscale=False,
        xgap=4,
        ygap=4,
    ))
    
    # Días de la semana (invertidos)
    day_labels = ['Dom', 'Sáb', 'Vie', 'Jue', 'Mié', 'Mar', 'Lun']
    
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            ticktext=[f'S{i+1}' for i in range(num_weeks)],
            tickvals=list(range(num_weeks)),
            tickfont=dict(color=COLORS['muted'], size=10),
            side='top'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            ticktext=day_labels,
            tickvals=list(range(7)),
            tickfont=dict(color=COLORS['muted'], size=10),
            autorange='reversed'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=20, t=40, b=20),
        height=280,
    )
    
    return fig


def create_contribution_heatmap(
    activity_data: Dict[str, int],
    year: int,
    month: int,
    base_color: str = None
) -> str:
    """
    Crea un heatmap de contribuciones usando HTML/CSS puro para mejor control visual.
    
    Args:
        activity_data: Diccionario {fecha_YYYY-MM-DD: minutos}
        year: Año
        month: Mes
        base_color: Color base (rosa por defecto)
        
    Returns:
        String HTML con el heatmap
    """
    if base_color is None:
        base_color = COLORS['primary']
    
    # Obtener información del mes
    first_day = date(year, month, 1)
    days_in_month = calendar.monthrange(year, month)[1]
    first_weekday = first_day.weekday()  # 0=Lunes
    
    # Calcular intensidades
    max_minutes = max(activity_data.values(), default=60) or 60
    
    # Generar celdas
    cells_html = []
    day_labels = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
    
    # Crear estructura de semanas
    current_day = 1
    week_start = -first_weekday  # Puede ser negativo para días vacíos
    
    while current_day <= days_in_month:
        for dow in range(7):
            actual_day = week_start + dow + 1
            
            if 1 <= actual_day <= days_in_month:
                date_str = f"{year}-{month:02d}-{actual_day:02d}"
                minutes = activity_data.get(date_str, 0)
                
                # Calcular opacidad basada en intensidad
                if minutes == 0:
                    opacity = 0.1
                else:
                    opacity = 0.2 + (minutes / max_minutes) * 0.8
                
                cells_html.append(
                    f'<div class="heatmap-cell" style="background-color: {base_color}; '
                    f'opacity: {opacity};" title="Día {actual_day}: {minutes} min"></div>'
                )
            else:
                cells_html.append('<div class="heatmap-cell empty"></div>')
        
        week_start += 7
        if week_start > days_in_month:
            break
    
    html = f'''
    <style>
        .heatmap-container {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 4px;
            max-width: 350px;
        }}
        .heatmap-cell {{
            aspect-ratio: 1;
            border-radius: 4px;
            min-height: 30px;
        }}
        .heatmap-cell.empty {{
            background-color: transparent;
        }}
        .heatmap-labels {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 4px;
            max-width: 350px;
            margin-bottom: 8px;
        }}
        .heatmap-label {{
            text-align: center;
            font-size: 11px;
            color: {COLORS['muted']};
        }}
    </style>
    <div class="heatmap-labels">
        {"".join(f'<span class="heatmap-label">{d}</span>' for d in day_labels)}
    </div>
    <div class="heatmap-container">
        {"".join(cells_html)}
    </div>
    '''
    
    return html


# <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 FUNCIONES AUXILIARES

def get_intensity_color(value: float, max_value: float, base_color: str) -> str:
    """
    Calcula el color basado en la intensidad.
    
    Args:
        value: Valor actual
        max_value: Valor máximo para normalizar
        base_color: Color base en formato hex
        
    Returns:
        Color hex ajustado
    """
    if max_value == 0:
        return COLORS['surface']
    
    intensity = min(value / max_value, 1.0)
    
    if intensity == 0:
        return COLORS['surface']
    
    # Convertir hex a RGB
    base_r = int(base_color[1:3], 16)
    base_g = int(base_color[3:5], 16)
    base_b = int(base_color[5:7], 16)
    
    # Color de fondo
    bg_r, bg_g, bg_b = 26, 26, 26  # #1a1a1a
    
    # Interpolar
    r = int(bg_r + (base_r - bg_r) * intensity)
    g = int(bg_g + (base_g - bg_g) * intensity)
    b = int(bg_b + (base_b - bg_b) * intensity)
    
    return f'#{r:02x}{g:02x}{b:02x}'


def format_time(minutes: int) -> str:
    """
    Formatea minutos en un string legible.
    
    Args:
        minutes: Cantidad de minutos
        
    Returns:
        String formateado (ej: "2h 30m")
    """
    if minutes < 60:
        return f"{minutes}m"
    
    hours = minutes // 60
    mins = minutes % 60
    
    if mins == 0:
        return f"{hours}h"
    
    return f"{hours}h {mins}m"
