
# 🏥 Hospitals-Access-Peru

**Análisis geoespacial de hospitales públicos operacionales en el Perú**, enfocado en accesibilidad, distribución y visualización interactiva a través de `GeoPandas`, `Folium` y `Streamlit`.

---

## 🗂️ Estructura del Repositorio

```
Hospitals-Access-Peru/
│
├── Input/                     # Datos crudos (hospitales, shapefiles, población)
├── Output/                    # Mapas, CSVs y análisis generados
├── Script/                    # Códigos utilizados
  ├── Folium_code.ipynb          # Notebook con generación de mapas y cálculos
  ├── Streamlit_code_final.py    # Aplicación interactiva Streamlit
├── requirements.txt           # Dependencias necesarias
└── README.md                  # Este archivo
```

---

## 📦 Requisitos del Entorno

```bash
conda create -n geopandas_env python=3.10
conda activate geopandas_env
conda install -c conda-forge geopandas folium streamlit matplotlib pandas
```

O simplemente:

```bash
pip install -r requirements.txt
```

---

## 📍 Unidad de Análisis

- Hospitales públicos operacionales (clasificación general y especializada)
- Datos filtrados por “EN FUNCIONAMIENTO” según MINSA-IPRESS
- Solo registros con coordenadas válidas

---

## 📊 Estructura de la Aplicación (Streamlit)

**📂 Tab 1: Data Description**

- Resumen general del dataset
- Métricas por departamento y distrito
- Fuentes oficiales utilizadas (MINSA, INEI, IGN)

**🗺️ Tab 2: Static Maps**

- Mapa 1: Conteo de hospitales por distrito
- Mapa 2: Distritos sin hospitales
- Mapa 3: Top 10 distritos con más hospitales
- Gráfico de barras y tabla resumen por departamento

**🌍 Tab 3: Dynamic Maps (Folium)**

- Mapa nacional coroplético con `Folium`
- Clusters interactivos de hospitales
- Análisis de proximidad en Lima y Loreto con buffers de 10 km
- Círculo rojo: aislamiento, círculo verde: concentración

---

## 🧪 Scripts principales

- `Folium_code.ipynb`: 
  - Generación de mapas estáticos
  - Análisis departamental y distrital
  - Exportación de gráficos y tablas (CSV, PNG)

- `Streamlit_code_final.py`: 
  - WebApp interactiva con pestañas
  - Carga de HTMLs, imágenes, CSVs
  - Visualización comparativa Lima vs Loreto

---

## 🗃️ Datasets utilizados

| Fuente        | Descripción                            |
|---------------|----------------------------------------|
| MINSA – IPRESS | Registro nacional de hospitales        |
| IGN           | Shapefiles de distritos                |
| INEI          | Centros poblados (para proximidad)     |

Todos los datos fueron transformados al CRS `EPSG:4326` para compatibilidad con mapas y distancias.

---

## 🔍 Metodología Breve

1. **Filtrado** por “EN FUNCIONAMIENTO”
2. **Validación** de coordenadas
3. **Agrupación** por distrito y departamento
4. **Proximidad**: buffers de 10km desde centros poblados
5. **Visualización**: mapas estáticos y dinámicos con folium/streamlit

---

## 📤 Cómo Ejecutar

### ✅ Paso 1: Generar mapas y análisis

Corre el notebook:

```bash
jupyter notebook Folium_code.ipynb
```

Esto generará archivos en la carpeta `Output/`.

### ✅ Paso 2: Lanzar la app Streamlit

```bash
streamlit run Streamlit_code_final.py
```

---

## 📌 Entrega

- 📁 Repositorio GitHub: `Hospitals-Access-Peru`
- 🌐 Dashboard Deploy (Streamlit Cloud): Network URL: http://192.168.18.11:8501

---

