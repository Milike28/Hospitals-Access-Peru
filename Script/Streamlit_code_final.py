"""
Aplicación Streamlit: Análisis Geoespacial de Hospitales en Perú
Curso: Data Science con Python

Esta aplicación presenta el análisis completo de hospitales públicos operacionales en Perú
usando los archivos ya generados por los scripts anteriores.
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import numpy as np
import os
import streamlit.components.v1 as components
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
## CONFIGURACIÓN INICIAL DE STREAMLIT
# =============================================================================

st.set_page_config(
    page_title="Hospitales en Perú - Análisis Geoespacial", 
    layout="wide", 
    page_icon="🏥"
)

st.title("🏥 Análisis Geoespacial de Hospitales en Perú")
st.markdown("**Análisis de accesibilidad y distribución de hospitales públicos operacionales**")

# =============================================================================
## CONFIGURACIÓN DE RUTAS
# =============================================================================

INPUT_PATH = r"C:\Users\ASUS\OneDrive - Universidad del Pacífico\Tareas Data Science\Hospitals-Access-Peru\Input"
OUTPUT_PATH = r"C:\Users\ASUS\OneDrive - Universidad del Pacífico\Tareas Data Science\Hospitals-Access-Peru\Output"

# =============================================================================
## FUNCIONES AUXILIARES
# =============================================================================

def load_csv_safe(file_path):
    """Carga CSV de forma segura con diferentes encodings"""
    if not os.path.exists(file_path):
        return None
    
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except:
            continue
    return None

def load_html_file(file_path):
    """Carga archivo HTML si existe"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def show_image_safe(image_path, caption="", width=None):
    """Muestra imagen si existe"""
    if os.path.exists(image_path):
        if width:
            st.image(image_path, caption=caption, width=width)
        else:
            st.image(image_path, caption=caption, use_container_width=True)
    else:
        st.warning(f"⚠️ Imagen no encontrada: {os.path.basename(image_path)}")

# =============================================================================
## CARGAR DATOS BÁSICOS
# =============================================================================

## Cargar datos principales si existen
csv_path = os.path.join(OUTPUT_PATH, "Resumen_Hospitales.csv")
hospitals_df = load_csv_safe(csv_path)

dept_summary_path = os.path.join(OUTPUT_PATH, "resumen_departamentos.csv")
dept_summary = load_csv_safe(dept_summary_path)

# =============================================================================
## CREACIÓN DE PESTAÑAS
# =============================================================================

tab1, tab2, tab3 = st.tabs(["🗂️ Data Description", "🗺️ Static Maps", "🌍 Dynamic Maps"])

# =============================================================================
## TAB 1: DESCRIPCIÓN DE DATOS
# =============================================================================

with tab1:
    st.header("🗂️ Descripción de los Datos")
    
    ## Métricas principales
    if hospitals_df is not None:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🏥 Total de Hospitales", f"{len(hospitals_df):,}")
        
        with col2:
            dept_count = hospitals_df['Departamento'].nunique() if 'Departamento' in hospitals_df.columns else 0
            st.metric("🗺️ Departamentos", f"{dept_count}")
        
        with col3:
            dist_count = hospitals_df['Distrito'].nunique() if 'Distrito' in hospitals_df.columns else 0
            st.metric("📍 Distritos", f"{dist_count}")
        
        with col4:
            st.metric("✅ Análisis", "Completo")
    
    else:
        st.warning("⚠️ No se encontraron datos procesados. Ejecuta primero el análisis principal.")
    
    st.markdown("---")
    
    ## Información metodológica
    st.subheader("📊 Metodología del Análisis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Unidad de Análisis:**
        - Hospitales públicos operacionales en Perú
        - Solo establecimientos con condición "EN FUNCIONAMIENTO"
        - Excluye establecimientos privados
        - Solo hospitales generales y especializados
        
        **📐 Sistema de Coordenadas:**
        - Análisis: EPSG:4326 (WGS84)
        - Rango válido Perú: Lat [-18.5, 0], Lon [-81.5, -68.5]
        """)
    
    with col2:
        st.markdown("""
        **📋 Fuentes de Datos:**
        - 🏥 **MINSA - IPRESS**: Registro Nacional de Establecimientos
        - 🗺️ **IGN**: Límites administrativos (distritos)
        - 📍 **INEI**: Centros poblados para análisis de proximidad
        
        **🔧 Herramientas Utilizadas:**
        - GeoPandas para análisis geoespacial
        - Folium para mapas interactivos
        - Matplotlib para visualizaciones estáticas
        """)
    
    st.markdown("---")
    
    ## Tabla de datos si existe
    if hospitals_df is not None:
        st.subheader("📋 Muestra de Datos Procesados")
        
        display_columns = ['Nombre del establecimiento', 'Departamento', 'Provincia', 
                          'Distrito', 'Clasificación', 'lat', 'lon']
        
        available_columns = [col for col in display_columns if col in hospitals_df.columns]
        
        if available_columns:
            st.dataframe(
                hospitals_df[available_columns].head(20), 
                width=1200,
                height=400
            )
    
    ## Distribución por departamento
    if dept_summary is not None:
        st.subheader("📈 Distribución por Departamento")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Identificar la estructura correcta del DataFrame
            if 'Num_Hospitales' in dept_summary.columns:
                # Caso: DataFrame con columna Num_Hospitales
                dept_data = dept_summary.head(10)
                departamentos = dept_data.index.tolist()
                valores = dept_data['Num_Hospitales'].values
            else:
                # Caso: DataFrame con estructura diferente - usar primera columna numérica
                numeric_cols = dept_summary.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    dept_data = dept_summary.head(10)
                    departamentos = dept_data.index.tolist()
                    valores = dept_data[numeric_cols[0]].values
                else:
                    # Fallback: asumir que la primera columna son valores
                    dept_data = dept_summary.head(10)
                    departamentos = dept_data.index.tolist()
                    valores = dept_data.iloc[:, 0].values
            
            # Crear gráfico de barras manualmente para control total
            bars = ax.bar(range(len(departamentos)), valores, color='skyblue', edgecolor='navy')
            
            # Configurar ejes con nombres correctos
            ax.set_xticks(range(len(departamentos)))
            ax.set_xticklabels(departamentos, rotation=45, ha='right')
            ax.set_title('Top 10 Departamentos con Más Hospitales', fontsize=12, fontweight='bold')
            ax.set_xlabel('Departamento')
            ax.set_ylabel('Número de Hospitales')
            ax.grid(axis='y', alpha=0.3)
            
            # Agregar valores encima de las barras
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{int(height)}', ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            map10_path = os.path.join(OUTPUT_PATH, "top10_departamentos.png")
            show_image_safe(map10_path, "Top 10 departamentos con mayor concentración hospitalaria")

            
        
        with col2:
            st.markdown("**📊 Estadísticas:**")
            if 'Num_Hospitales' in dept_summary.columns:
                max_val = dept_summary['Num_Hospitales'].max()
                min_val = dept_summary['Num_Hospitales'].min()
                avg_val = dept_summary['Num_Hospitales'].mean()
                max_dept = dept_summary['Num_Hospitales'].idxmax()
                min_dept = dept_summary['Num_Hospitales'].idxmin()
                st.write(f"• **Máximo:** {max_val} hospitales ({max_dept})")
                st.write(f"• **Mínimo:** {min_val} hospitales ({min_dept})")
                st.write(f"• **Promedio:** {avg_val:.1f} hospitales")
                st.write(f"• **Total departamentos:** {len(dept_summary)}")
            else:
                # Para cualquier estructura de datos
                numeric_cols = dept_summary.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    col_name = numeric_cols[0]
                    max_val = dept_summary[col_name].max()
                    min_val = dept_summary[col_name].min()
                    avg_val = dept_summary[col_name].mean()
                    st.write(f"• **Máximo:** {max_val}")
                    st.write(f"• **Mínimo:** {min_val}")
                    st.write(f"• **Promedio:** {avg_val:.1f}")
                else:
                    st.write("• Ver tabla para estadísticas detalladas")

# =============================================================================
## TAB 2: MAPAS ESTÁTICOS
# =============================================================================

with tab2:
    st.header("🗺️ Mapas Estáticos & Análisis por Departamento")
    
    ## MAPAS ESTÁTICOS GENERADOS
    st.subheader("🗺️ Mapas Estáticos Generados")
    
    ## Mapa 1: Total hospitales por distrito
    st.markdown("### 📍 Mapa 1: Total de Hospitales por Distrito")
    map1_path = os.path.join(OUTPUT_PATH, "mapa1_hospitales_distrito.png")
    show_image_safe(map1_path, "Distribución del número de hospitales por distrito")
    
    ## Mapa 2: Distritos sin hospitales
    st.markdown("### 🚫 Mapa 2: Distritos Sin Hospitales")
    map2_path = os.path.join(OUTPUT_PATH, "mapa2_distritos_sin_hospitales.png")
    show_image_safe(map2_path, "Distritos sin acceso a hospitales públicos")
    
    ## Mapa 3: Top 10 distritos
    st.markdown("### 🏆 Mapa 3: Top 10 Distritos con Más Hospitales")
    map3_path = os.path.join(OUTPUT_PATH, "mapa3_top10_distritos.png")
    show_image_safe(map3_path, "Distritos con mayor concentración hospitalaria")
    
    st.markdown("---")
    
    ## ANÁLISIS DEPARTAMENTAL
    st.subheader("🏛️ Análisis Departamental Completo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Tabla Resumen Departamental")
        if dept_summary is not None:
            st.dataframe(dept_summary, width=600)
            
            ## Descargar CSV
            csv = dept_summary.to_csv()
            st.download_button(
                label="📥 Descargar Tabla (CSV)",
                data=csv,
                file_name="resumen_departamentos.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No se encontró tabla resumen departamental")
    
    with col2:
        st.markdown("#### 📊 Gráfico de Barras Departamental")
        graph_path = os.path.join(OUTPUT_PATH, "grafico_departamentos.png")
        if os.path.exists(graph_path):
            show_image_safe(graph_path, "Hospitales por departamento")
        else:
            ## Generar gráfico básico si existe dept_summary
            if dept_summary is not None:
                fig, ax = plt.subplots(figsize=(8, 10))
                if 'Num_Hospitales' in dept_summary.columns:
                    dept_summary['Num_Hospitales'].plot(kind='barh', ax=ax, color='coral', edgecolor='darkred')
                else:
                    dept_summary.iloc[:, 0].plot(kind='barh', ax=ax, color='coral', edgecolor='darkred')
                ax.set_title('Hospitales por Departamento', fontsize=12, fontweight='bold')
                ax.set_xlabel('Número de Hospitales')
                ax.grid(axis='x', alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)

# =============================================================================
## TAB 3: MAPAS DINÁMICOS
# =============================================================================

with tab3:
    st.header("🌍 Mapas Dinámicos Interactivos")
    
    ## MAPA NACIONAL COROPLÉTICO
    st.subheader("🗺️ Mapa Nacional Interactivo")
    
    national_map_path = os.path.join(OUTPUT_PATH, "mapa_nacional_coropletico.html")
    national_html = load_html_file(national_map_path)
    
    if national_html:
        st.markdown("**Mapa nacional con coropleta de densidad + clusters de hospitales por departamento**")
        components.html(national_html, height=600, scrolling=False)
    else:
        st.warning("⚠️ No se encontró el mapa nacional. Ejecuta el análisis principal primero.")
        st.info("Archivo esperado: mapa_nacional_coropletico.html")
    
    st.markdown("---")
    
    ## ANÁLISIS DE PROXIMIDAD LIMA Y LORETO
    st.subheader("📍 Análisis de Proximidad: Lima vs Loreto")
    st.markdown("**Análisis de accesibilidad hospitalaria con buffers de 10km**")
    
    col1, col2 = st.columns(2)
    
    ## PROXIMIDAD LIMA
    with col1:
        st.markdown("#### 🏙️ Lima - Concentración Urbana")
        
        lima_map_path = os.path.join(OUTPUT_PATH, "mapa_proximidad_lima.html")
        lima_html = load_html_file(lima_map_path)
        
        if lima_html:
            components.html(lima_html, height=500, scrolling=False)
            st.info("**Lima:** Alta concentración urbana mejora accesibilidad en el centro metropolitano.")
        else:
            st.warning("⚠️ No se encontró el mapa de proximidad de Lima")
            st.info("Archivo esperado: mapa_proximidad_lima.html")
    
    ## PROXIMIDAD LORETO
    with col2:
        st.markdown("#### 🌳 Loreto - Dispersión Geográfica")
        
        loreto_map_path = os.path.join(OUTPUT_PATH, "mapa_proximidad_loreto.html")
        loreto_html = load_html_file(loreto_map_path)
        
        if loreto_html:
            components.html(loreto_html, height=500, scrolling=False)
            st.info("**Loreto:** Dispersión geográfica y barreras naturales limitan accesibilidad.")
        else:
            st.warning("⚠️ No se encontró el mapa de proximidad de Loreto")
            st.info("Archivo esperado: mapa_proximidad_loreto.html")
    
    ## ANÁLISIS ESCRITO FINAL
    st.markdown("---")
    st.subheader("📝 Análisis Comparativo Final")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🏙️ Lima - Concentración Urbana:**
        - **Ventaja:** Alta densidad hospitalaria en área metropolitana
        - **Accesibilidad:** Múltiples hospitales dentro de 10km en zonas céntricas
        - **Transporte:** Red vial desarrollada facilita acceso
        - **Desafío:** Posible saturación de servicios en centro vs. periferia
        """)
    
    with col2:
        st.markdown("""
        **🌳 Loreto - Dispersión Amazónica:**
        - **Desafío:** Grandes distancias entre establecimientos
        - **Geografía:** Ríos como principales vías de transporte
        - **Accesibilidad:** Pocos hospitales por área, acceso limitado
        - **Oportunidad:** Telemedicina y unidades móviles como alternativas
        """)
    
    ## Archivos adicionales disponibles
    st.markdown("---")
    st.subheader("📁 Archivos de Análisis Disponibles")
    
    ## Listar archivos en OUTPUT_PATH
    if os.path.exists(OUTPUT_PATH):
        files = os.listdir(OUTPUT_PATH)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🗺️ Mapas Estáticos:**")
            for file in files:
                if file.endswith('.png'):
                    st.text(f"• {file}")
        
        with col2:
            st.markdown("**🌍 Mapas Interactivos:**")
            for file in files:
                if file.endswith('.html'):
                    st.text(f"• {file}")
        
        with col3:
            st.markdown("**📊 Datos y Reportes:**")
            for file in files:
                if file.endswith('.csv') or file.endswith('.txt'):
                    st.text(f"• {file}")

## INFORMACIÓN TÉCNICA ADICIONAL
st.markdown("---")
with st.expander("ℹ️ Información Técnica", expanded=False):
    st.markdown("""
    **🔧 Herramientas Utilizadas:**
    - **Streamlit:** Aplicación web interactiva
    - **GeoPandas:** Análisis geoespacial y spatial joins
    - **Folium:** Mapas interactivos con Leaflet.js
    - **Matplotlib:** Gráficos estáticos
    - **Pandas:** Procesamiento de datos

    **📊 Parámetros del Análisis:**
    - **Radio de análisis:** 10 km para buffers de proximidad
    - **Sistema de coordenadas:** EPSG:4326 (WGS84)
    - **Filtros aplicados:** Solo hospitales públicos operacionales
    - **Rango geográfico:** Territorio peruano [-18.5°, 0°] lat, [-81.5°, -68.5°] lon

    **📝 Metodología:**
    1. Carga y filtrado de datos IPRESS
    2. Corrección automática de coordenadas
    3. Spatial joins para análisis por distrito
    4. Cálculo de centroides para análisis de proximidad
    5. Visualización con mapas estáticos e interactivos
    
    **📂 Ubicaciones de Archivos:**
    - **Input:** Datos originales IPRESS.csv y shapefiles
    - **Output:** Mapas, gráficos y análisis generados
    """)

# =============================================================================
## PIE DE PÁGINA
# =============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
<small>
📊 Análisis Geoespacial de Hospitales en Perú | 
Curso: Data Science con Python | 
Universidad del Pacífico 2025
</small>
</div>
""", unsafe_allow_html=True)