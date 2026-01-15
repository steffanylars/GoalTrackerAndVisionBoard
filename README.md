# 🎯 Focus Flow - Goal & Focus Tracker

Una aplicación elegante para tracking de metas y sesiones de enfoque, con estética girly-pop y visualizaciones inspiradas en Apple Watch y GitHub.

## 📁 Arquitectura del Proyecto

```
focus_tracker/
├── app.py                  # Entrada principal de Streamlit
├── requirements.txt        # Dependencias
├── README.md
│
├── data/                   # Persistencia JSON
│   ├── projects.json       # Proyectos del usuario
│   ├── sessions.json       # Sesiones de enfoque
│   └── settings.json       # Preferencias (opcional)
│
├── src/                    # Código fuente modular
│   ├── __init__.py
│   ├── data_manager.py     # CRUD para JSON files
│   ├── components.py       # Componentes UI reutilizables
│   ├── visualizations.py   # Gráficos (rings, heatmap)
│   └── utils.py            # Utilidades generales
│
└── .streamlit/
    └── config.toml         # Configuración de tema Streamlit
```

## 🎨 Diseño Visual

### Paleta de Colores
- **Background**: `#0a0a0a` (negro profundo)
- **Surface**: `#1a1a1a` (gris oscuro)
- **Primary**: `#ff7eb6` (rosa neón)
- **Secondary**: `#b8a9ff` (lavanda)
- **Accent**: `#ffb86c` (peach)
- **Text**: `#fafafa` (blanco suave)
- **Muted**: `#6b6b6b` (gris)

### Tipografía
- Headings: Plus Jakarta Sans (bold)
- Body: Plus Jakarta Sans (regular)

## 🚀 Instalación

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ✨ Características

- **Dashboard**: Vista general con progreso diario y mensual
- **Proyectos**: Gestión completa con metas personalizables
- **Timer**: Pomodoro integrado con sesiones custom
- **Vista Mensual**: Heatmap + círculos de progreso

## 📊 Estructura de Datos

### projects.json
```json
{
  "id": "uuid",
  "name": "German Study",
  "color": "#ff7eb6",
  "goal_type": "pomodoro | time | sessions",
  "monthly_goal": 40,
  "created_at": "YYYY-MM-DD"
}
```

### sessions.json
```json
{
  "id": "uuid",
  "project_id": "uuid",
  "date": "YYYY-MM-DD",
  "minutes": 25,
  "pomodoros": 1,
  "session_type": "pomodoro | custom",
  "created_at": "ISO timestamp"
}
```
