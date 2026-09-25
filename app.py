import streamlit as st
import sqlite3
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import os

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ==========================================
st.set_page_config(
    page_title="MateIA - Tutor Basado en Secuencias Didácticas (MINERD/PUCMM)",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('''
    <style>
    :root {
        --primary: #1F618D;
        --secondary: #2980B9;
        --accent: #8E44AD;
        --bg-card: #F4F6F7;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F8F9F9 0%, #EBF5FB 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(120deg, #1B4F72 0%, #2980B9 45%, #6C3483 100%);
        color: white;
        padding: 28px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 8px 20px rgba(31, 97, 141, 0.25);
        margin-bottom: 25px;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
    }
    .main-header p {
        font-size: 1.15rem;
        opacity: 0.95;
        margin-top: 6px;
    }

    .card-box {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border-left: 6px solid #2980B9;
        margin-bottom: 20px;
    }
    
    .curriculum-badge {
        background-color: #E8F8F5;
        color: #117864;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 8px;
        border: 1px solid #A3E4D7;
    }

    .hint-box {
        background-color: #FEF9E7;
        padding: 16px;
        border-radius: 12px;
        border-left: 6px solid #F1C40F;
        color: #7D6608;
        font-weight: 500;
        margin-bottom: 12px;
    }
    
    .badge-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 2px solid #E5E7E9;
    }
    .badge-unlocked {
        border-color: #2ECC71;
        background-color: #EAFAF1;
    }
    </style>
''', unsafe_allow_html=True)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_asset_image(filename):
    path = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(path):
        return Image.open(path)
    return None

# ==========================================
# 2. BASE DE DATOS Y PROGRESO
# ==========================================
DB_NAME = "mateia_progress.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    estudiante TEXT,
                    tema TEXT,
                    ejercicio TEXT,
                    resultado TEXT,
                    intentos INTEGER,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

def log_progress(estudiante, tema, ejercicio, resultado, intentos):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO progress (estudiante, tema, ejercicio, resultado, intentos) VALUES (?, ?, ?, ?, ?)", 
              (estudiante, tema, ejercicio, resultado, intentos))
    conn.commit()
    conn.close()

def get_progress():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM progress ORDER BY fecha DESC", conn)
    conn.close()
    return df

# ==========================================
# 3. NAVEGACIÓN Y SESIÓN
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Inicio"
if 'student_name' not in st.session_state:
    st.session_state.student_name = "Estudiante 1"
if 'grado_curricular' not in st.session_state:
    st.session_state.grado_curricular = "5to Grado Primaria (PDF)"

st.sidebar.image(load_asset_image("hero_banner.jpg") or Image.new('RGB', (300, 150), color='#1F618D'), use_container_width=True)
st.sidebar.markdown("### 🧮 MateIA - Curriculum MINERD")

st.sidebar.subheader("📚 Nivel Educativo (PDFs):")
grado_select = st.sidebar.selectbox(
    "Selecciona el Grado Oficial:",
    ["5to Grado Primaria (PDF)", "6to Grado Primaria (PDF)"],
    index=0 if "5to" in st.session_state.grado_curricular else 1
)
st.session_state.grado_curricular = grado_select

st.sidebar.markdown("---")
menu = [
    "🏠 Inicio",
    "👨‍🏫 Tutor Secuencias Didácticas",
    "🧪 Laboratorio Visual & 3D",
    "🎲 Prácticas por Secuencias",
    "📊 Mi Progreso & Insignias"
]

choice = st.sidebar.radio("Navegación:", menu, index=menu.index(st.session_state.page) if st.session_state.page in menu else 0)
if choice != st.session_state.page:
    st.session_state.page = choice
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Perfil de Usuario")
student_input = st.sidebar.text_input("Nombre del Estudiante", value=st.session_state.student_name)
if student_input != st.session_state.student_name:
    st.session_state.student_name = student_input

# ==========================================
# 4. VISTAS PRINCIPALES
# ==========================================

# ------------------------------------------
# VISTA 1: INICIO / LANDING PAGE
# ------------------------------------------
if st.session_state.page == "🏠 Inicio":
    st.markdown('''
        <div class="main-header">
            <h1>🧮 MateIA - Tutor Basado en Secuencias Didácticas</h1>
            <p>Integración oficial de las Guías Pedagógicas de 5.º y 6.º Grado Primaria (MINERD / PUCMM - CIEDHumano)</p>
        </div>
    ''', unsafe_allow_html=True)
    
    hero_img = load_asset_image("hero_banner.jpg")
    if hero_img:
        st.image(hero_img, use_container_width=True, caption="MateIA: Tutoría basada en el currículo oficial dominicano de Matemática")

    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("<span class=\"curriculum-badge\">📘 Integración Curricular Oficial</span>", unsafe_allow_html=True)
        st.markdown("### 🎯 Fundamentación Pedagógica del Proyecto")
        st.write("""
        Las tutorías y ejercicios de **MateIA** se extraen directamente de los libros oficiales de texto:
        - **Secuencias Didácticas de Matemática 5.° Grado** *(PUCMM - CIEDHumano / INAFOCAM / MINERD)*
        - **Secuencias Didácticas de Matemática 6.° Grado** *(PUCMM - CIEDHumano / INAFOCAM / MINERD)*
        
        Cada actividad contextualiza la matemática con la realidad dominicana: **plazas comerciales (Sambil, Ágora, Megacentro), transacciones bancarias en pesos dominicanos (RD$), medición de túneles y geometría de infraestructuras**.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("<span class=\"curriculum-badge\">📊 Malla de Secuencias Curriculares</span>", unsafe_allow_html=True)
        st.markdown("#### 📖 Secuencias Disponibles en los Textos PDF:")
        st.markdown('''
        * **5.° Grado:**
          - *Secuencia 1:* Números > 1,000,000 y Adición (Plazas Comerciales)
          - *Secuencia 2:* Sustracción, Multiplicación y Billete de RD$ 2,000
          - *Secuencia 3:* División, Potenciación y Radicación
          - *Secuencia 4:* Medidas de Longitud (Sistema Métrico e Inglés)
          - *Secuencia 5:* Números Fraccionarios y Decimales
          - *Secuencia 6 a 10:* Geometría, Círculo, Perímetro y Estadística
        * **6.° Grado:**
          - *Secuencia 1:* Números Naturales, Enteros y Bancos en Rep. Dom.
          - *Secuencia 2 y 3:* Números Decimales y Fracciones
          - *Secuencia 4:* Geometría y Teorema de Pitágoras
          - *Secuencia 5 y 6:* Mediciones de Área, Volumen y Túneles Circulares
        ''')
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("<span class=\"curriculum-badge\">👩‍🏫 Ficha del Proyecto</span>", unsafe_allow_html=True)
        st.info("""
        **Autora y Educadora:** Liskeidy Rosario Pérez  
        **Ubicación:** Villa Altagracia, San Cristóbal, Rep. Dom.  
        **Fuentes Curriculares:** Textos oficiales MINERD / PUCMM  
        **Enfoque:** Didáctica de las Matemáticas con Andamiaje Cognitivo
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown("### 🚀 Acceso Inmediato")
        if st.button("👨‍🏫 Iniciar Tutoría con Secuencias del PDF", type="primary", use_container_width=True):
            st.session_state.page = "👨‍🏫 Tutor Secuencias Didácticas"
            st.rerun()
        if st.button("🧪 Abrir Laboratorio Visual 2D/3D", use_container_width=True):
            st.session_state.page = "🧪 Laboratorio Visual & 3D"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📸 Galería Didáctica Integrada (Ilustraciones de los Libros)")
    
    t1, t2, t3 = st.tabs(["💵 Descomposición Monetaria RD$", "🍕 Fracciones y Medicamentos", "📐 Túneles Circulares y Geometría"])
    with t1:
        c1, c2 = st.columns([1, 1])
        with c1:
            img = load_asset_image("moneda_rd.jpg")
            if img: st.image(img, use_container_width=True, caption="Descomposición del Billete de RD$ 2,000 (Plazas Comerciales)")
        with c2:
            st.write(r"""
            **Secuencia Didáctica 2 (5.º Grado - PDF Oficial):**  
            Alexander y su padre van a la Plaza Internacional de Santiago con un billete de **RD$ 2,000**.  
            Se aplican los conceptos de **descomposición posicional y valor de denominación**:
            $$\text{RD\$ } 2,000 = 4 \times 500 = 10 \times 200 = 20 \times 100$$
            Este apoyo gráfico facilita la intuición aritmética antes de pasar a operaciones abstractas.
            """)

    with t2:
        c1, c2 = st.columns([1, 1])
        with c1:
            img = load_asset_image("fracciones_visual.jpg")
            if img: st.image(img, use_container_width=True, caption="Representación Gráfica de Fracciones y Porcentajes")
        with c2:
            st.write(r"""
            **Secuencia Didáctica 5 (5.º y 6.º Grado - PDF Oficial):**  
            Análisis de consumo familiar de sobres de medicamentos y raciones de alimentos:
            Si 2 sobres contienen 16 pastillas y quedan 4, se han consumido $\frac{12}{16} = \frac{3}{4}$ partes (75% del total).
            """)

    with t3:
        c1, c2 = st.columns([1, 1])
        with c1:
            img = load_asset_image("tunel_circular.jpg")
            if img: st.image(img, use_container_width=True, caption="Perímetro de Entrada a Túnel Circular (r = 5.75 m)")
        with c2:
            st.write(r"""
            **Secuencia Didáctica 6 (6.º Grado - PDF Oficial):**  
            Cálculo de perímetro en infraestructuras viales dominicanas:  
            Entrada circular de un túnel con radio $r = 5.75\text{ m}$.  
            Perímetro: $P = 2 \pi r = 2 \times 3.1416 \times 5.75 \approx 36.13\text{ metros}$.
            """)

# ------------------------------------------
# VISTA 2: TUTOR SECUENCIAS DIDÁCTICAS (PDF)
# ------------------------------------------
elif st.session_state.page == "👨‍🏫 Tutor Secuencias Didácticas":
    st.title("👨‍🏫 Tutoría Guiada con Problemas de los PDFs Oficiales")
    st.write(f"Nivel Seleccionado actualmente: **{st.session_state.grado_curricular}**")
    
    if "5to" in st.session_state.grado_curricular:
        ejercicios_pdf = {
            "Secuencia 1: Adición en Plazas Comerciales (Visitas anuales)": {
                "pregunta": "En la Plaza Comercial Sambil asistieron 1,250,000 personas en enero y 850,000 en febrero. ¿Cuál es el total acumulado de visitantes?",
                "ans": "2100000",
                "pasos": [
                    "Identifica los sumandos: 1,250,000 y 850,000.",
                    "Suma las unidades de mil primero: 250,000 + 850,000 = 1,100,000.",
                    "Suma la unidad de millón restante: 1,000,000 + 1,100,000 = 2,100,000.",
                    "Resultado final: 2,100,000 personas."
                ],
                "tipo": "suma_grandes"
            },
            "Secuencia 2: Descomposición de Billete de RD$ 2,000 (Plaza Santiago)": {
                "pregunta": "En la boletería de Plaza Internacional, el padre de Alexander cambia un billete de RD$ 2,000 por billetes de RD$ 500. ¿Cuántos billetes de RD$ 500 recibe?",
                "ans": "4",
                "pasos": [
                    "Plantea la división de la cantidad entre la denominación: 2000 / 500.",
                    "Cancela los ceros de ambos lados: 20 / 5.",
                    "Resuelve 20 ÷ 5 = 4.",
                    "Recibe exactamente 4 billetes de RD$ 500."
                ],
                "tipo": "dinero"
            },
            "Secuencia 3: División y Empaque de Raciones": {
                "pregunta": "En un centro de acopio escolar de Villa Altagracia hay 1,440 raciones de alimento para entregar a 12 escuelas primarias en partes iguales. ¿Cuántas raciones le corresponden a cada escuela?",
                "ans": "120",
                "pasos": [
                    "Plantea la división: 1,440 ÷ 12.",
                    "Calcula 144 ÷ 12 = 12.",
                    "Agrega el cero: 120 raciones por escuela."
                ],
                "tipo": "dinero"
            },
            "Secuencia 4: Campo de Fútbol en Yardas y Pies": {
                "pregunta": "El campo de fútbol escolar mide 120 yardas de largo. Si 1 yarda equivale a 3 pies, ¿cuál es la longitud total del campo en pies?",
                "ans": "360",
                "pasos": [
                    "Multiplica el número de yardas por 3.",
                    "Calcula 120 × 3.",
                    "Resultado: 360 pies."
                ],
                "tipo": "suma_grandes"
            },
            "Secuencia 5: Fracciones de Medicamentos": {
                "pregunta": "La familia de Nelly compró 2 sobres con 8 pastillas cada uno (16 en total). Si quedan 4 pastillas, ¿qué fracción reducida del total se tomaron? (Escribe la fracción ej. 3/4)",
                "ans": "3/4",
                "pasos": [
                    "Calcula las pastillas consumidas: 16 - 4 = 12 pastillas.",
                    "Plantea la fracción: 12 / 16.",
                    "Simplifica dividiendo numerador y denominador entre 4: 12÷4 = 3, 16÷4 = 4.",
                    "Resultado simplificado: 3/4."
                ],
                "tipo": "fracciones"
            }
        }
    else:
        ejercicios_pdf = {
            "Secuencia 1: Números Enteros y Depósitos Bancarios": {
                "pregunta": "Un cliente en el Banco Nacional tenía un saldo de RD$ 15,000. Realizó un retiro de RD$ 8,500 y luego un depósito de RD$ 3,200. ¿Cuál es su saldo final?",
                "ans": "9700",
                "pasos": [
                    "Representa el retiro como número negativo (-8,500) y el depósito como positivo (+3,200).",
                    "Resta el retiro del saldo inicial: 15,000 - 8,500 = 6,500.",
                    "Suma el nuevo depósito: 6,500 + 3,200 = 9,700.",
                    "Saldo final en el banco: RD$ 9,700."
                ],
                "tipo": "banco"
            },
            "Secuencia 2: Compra en Supermercado con Decimales": {
                "pregunta": "María compra arroz por RD$ 245.50, aceite por RD$ 380.25 y leche por RD$ 174.25. Si paga con un billete de RD$ 1,000, ¿cuánto dinero le devuelven de cambio?",
                "ans": "200",
                "pasos": [
                    "Suma el costo total de los productos: 245.50 + 380.25 + 174.25 = 800.00.",
                    "Resta del billete de 1,000: 1,000 - 800.",
                    "Cambio devuelto: RD$ 200."
                ],
                "tipo": "dinero"
            },
            "Secuencia 4: Teorema de Pitágoras - Escalera apoyada (14 ft y 8 ft)": {
                "pregunta": "Una escalera se apoya en una pared a una altura de 14 pies y su base está a 8 pies de la pared. Calcula la longitud de la escalera redondeada al entero más cercano (ft).",
                "ans": "16",
                "pasos": [
                    "Aplica la fórmula c² = a² + b².",
                    "Sustituye los valores: 8² + 14² = 64 + 196 = 260.",
                    "Calcula c = √260 ≈ 16.12 pies.",
                    "Redondeado al entero más cercano: 16 pies."
                ],
                "tipo": "pitagoras"
            },
            "Secuencia 5: Capacidad de Cisterna en Litros": {
                "pregunta": "Una cisterna de agua escolar tiene base 2 m × 3 m y profundidad de 2 m (Volumen = 12 m³). Si 1 m³ contiene 1,000 Litros, ¿cuál es su capacidad total en Litros?",
                "ans": "12000",
                "pasos": [
                    "Calcula el volumen V = 2 × 3 × 2 = 12 m³.",
                    "Multiplica por 1,000 litros.",
                    "Capacidad total: 12,000 Litros."
                ],
                "tipo": "tunel"
            },
            "Secuencia 6: Perímetro de Túnel Circular (r = 5.75 m)": {
                "pregunta": "La entrada a un túnel circular en la carretera tiene un radio de 5.75 m. Calcula su perímetro aproximado redondeado a un decimal (usa π = 3.1416).",
                "ans": "36.1",
                "pasos": [
                    "Aplica la fórmula del perímetro del círculo: P = 2 × π × r.",
                    "Multiplica el radio por 2: 2 × 5.75 = 11.5 m.",
                    "Multiplica por pi: 11.5 × 3.1416 = 36.1284 m.",
                    "Redondeado a un decimal: 36.1 metros."
                ],
                "tipo": "tunel"
            }
        }

    prob_sel = st.selectbox("Elige el problema de la Secuencia Didáctica:", list(ejercicios_pdf.keys()))
    prob_data = ejercicios_pdf[prob_sel]

    c_left, c_right = st.columns([1, 1])

    with c_left:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown(f"<span class=\"curriculum-badge\">📖 Problema Extraído del PDF</span>", unsafe_allow_html=True)
        st.subheader(prob_sel.split(":")[0])
        st.write(f"**Planteamiento:** {prob_data['pregunta']}")
        
        # Imagen temática directamente relacionada con el problema de la tutoría
        img_name_map = {
            "dinero": "moneda_rd.jpg",
            "suma_grandes": "moneda_rd.jpg",
            "fracciones": "fracciones_visual.jpg",
            "pitagoras": "pitagoras_escalera.jpg",
            "tunel": "tunel_circular.jpg",
            "banco": "moneda_rd.jpg"
        }
        topic_img_file = img_name_map.get(prob_data['tipo'], "hero_banner.jpg")
        topic_img = load_asset_image(topic_img_file)
        if topic_img:
            st.image(topic_img, use_container_width=True, caption=f"Ilustración Didáctica para {prob_sel.split(':')[0]}")
            
        st.markdown('</div>', unsafe_allow_html=True)

        if 'intentos' not in st.session_state:
            st.session_state.intentos = 0
        if 'pistas_pdf' not in st.session_state:
            st.session_state.pistas_pdf = 0

        user_input = st.text_input("Ingresa tu respuesta:", key=f"pdf_ans_{prob_sel}")
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button("✅ Comprobar Respuesta", type="primary", use_container_width=True):
                st.session_state.intentos += 1
                if user_input.strip() == prob_data['ans']:
                    st.balloons()
                    st.success("🎉 ¡Excelente! Respuesta conforme a la Secuencia Didáctica.")
                    log_progress(st.session_state.student_name, st.session_state.grado_curricular, prob_sel, "Correcto", st.session_state.intentos)
                    st.session_state.intentos = 0
                    st.session_state.pistas_pdf = 0
                else:
                    st.error("❌ Respuesta incorrecta. Consulta las pistas del docente.")
                    log_progress(st.session_state.student_name, st.session_state.grado_curricular, prob_sel, "Incorrecto", st.session_state.intentos)

        with b2:
            if st.button("💡 Pista Didáctica del PDF", use_container_width=True):
                if st.session_state.pistas_pdf < len(prob_data['pasos']):
                    st.session_state.pistas_pdf += 1
                else:
                    st.info("Has desbloqueado todas las orientaciones del libro.")

        if st.session_state.pistas_pdf > 0:
            st.markdown("#### 🔍 Pasos del Libro Didáctico:")
            for i in range(st.session_state.pistas_pdf):
                st.markdown(f'<div class="hint-box"><b>Paso {i+1}:</b> {prob_data["pasos"][i]}</div>', unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.subheader("📊 Gráfico Interactivo de Soporte")
        
        tipo_g = prob_data['tipo']
        
        if tipo_g == "suma_grandes":
            fig = go.Figure(data=[
                go.Bar(name='Enero', x=['Sambil'], y=[1250000], marker_color='#1F618D'),
                go.Bar(name='Febrero', x=['Sambil'], y=[850000], marker_color='#5DADE2')
            ])
            fig.update_layout(barmode='stack', title="Acumulado de Visitantes en Plaza Comercial", height=380)
            st.plotly_chart(fig, use_container_width=True)

        elif tipo_g == "dinero":
            billetes = st.slider("Ajusta billetes de RD$ 500 para igualar RD$ 2,000:", 1, 6, 2)
            total_rd = billetes * 500
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=total_rd,
                title={'text': f"{billetes} billetes de RD$ 500 = RD$ {total_rd}"},
                gauge={'axis': {'range': [0, 3000]}, 'bar': {'color': "#27AE60"},
                       'threshold': {'line': {'color': "gold", 'width': 4}, 'value': 2000}}
            ))
            st.plotly_chart(fig, use_container_width=True)

        elif tipo_g == "fracciones":
            fig = px.pie(names=['Consumidas (12)', 'Restantes (4)'], values=[12, 4],
                         color_discrete_sequence=['#E74C3C', '#2ECC71'], hole=0.4,
                         title="Sobres de Pastillas (12/16 = 3/4 consumidas)")
            st.plotly_chart(fig, use_container_width=True)

        elif tipo_g == "banco":
            fig = go.Figure(data=[
                go.Bar(x=['Saldo Inicial', 'Retiro', 'Depósito', 'Saldo Final'],
                       y=[15000, -8500, 3200, 9700],
                       marker_color=['#2980B9', '#E74C3C', '#2ECC71', '#8E44AD'])
            ])
            fig.update_layout(title="Movimientos Bancarios (RD$)", height=380)
            st.plotly_chart(fig, use_container_width=True)

        elif tipo_g == "pitagoras":
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.plot([0, 8, 0, 0], [0, 0, 14, 0], color='#1F618D', linewidth=3, label='Escalera (c ≈ 16.12 ft)')
            ax.fill([0, 8, 0], [0, 0, 14], color='#EBF5FB', alpha=0.6)
            ax.text(4, -1, 'Base = 8 ft', fontsize=10, fontweight='bold', color='#B03A2E')
            ax.text(-1.5, 7, 'Pared = 14 ft', fontsize=10, fontweight='bold', color='#B03A2E')
            ax.set_xlim(-2, 10)
            ax.set_ylim(-2, 16)
            ax.set_title("Escalera Apoyada en la Pared (Secuencia 4)", fontsize=10, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.4)
            st.pyplot(fig)

        elif tipo_g == "tunel":
            r_val = st.slider("Ajusta el radio del túnel circular (m):", 1.0, 10.0, 5.75)
            perim = 2 * np.pi * r_val
            theta = np.linspace(0, 2*np.pi, 100)
            x_c = r_val * np.cos(theta)
            y_c = r_val * np.sin(theta)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_c, y=y_c, mode='lines', fill="toself", fillcolor="rgba(41, 128, 185, 0.2)",
                                     line=dict(color="#1F618D", width=3), name=f"Túnel r={r_val}m"))
            fig.update_layout(title=f"Entrada del Túnel Circular (Perímetro = {perim:.2f} m)", height=380)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# VISTA 3: LABORATORIO VISUAL & 3D
# ------------------------------------------
elif st.session_state.page == "🧪 Laboratorio Visual & 3D":
    st.title("🧪 Laboratorio Visual & Modelado Tridimensional")
    st.write("Simuladores conceptuales para experimentar las secuencias didácticas de 5.º y 6.º Grado.")
    
    t1, t2, t3 = st.tabs(["💵 Simulador Monetario RD$", "📐 Geometría de Túneles Circulares", "🧊 Visor 3D de Cuerpos"])
    
    with t1:
        st.subheader("💵 Simulador de Descomposición Monetaria (Secuencia 2 - 5to Grado)")
        st.write("Alexander y su padre descomponen un billete de **RD$ 2,000**:")
        
        cant_2000 = st.number_input("Cantidad de billetes de RD$ 2,000:", min_value=1, max_value=10, value=1)
        total = cant_2000 * 2000
        
        st.markdown(f"### Total a cambiar: **RD$ {total:,}**")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("En papeletas de RD$ 500", f"{total // 500} billetes")
        with c2:
            st.metric("En papeletas de RD$ 200", f"{total // 200} billetes")
        with c3:
            st.metric("En papeletas de RD$ 100", f"{total // 100} billetes")

        fig = px.bar(
            x=["Papeletas de RD$ 500", "Papeletas de RD$ 200", "Papeletas de RD$ 100"],
            y=[total // 500, total // 200, total // 100],
            color=["RD$ 500", "RD$ 200", "RD$ 100"],
            labels={'x': 'Denominación', 'y': 'Cantidad de Billetes'},
            title="Comparativa de Billetes Obtenidos al Cambiar"
        )
        st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.subheader("📐 Simulador de Perímetro y Área de Túneles (Secuencia 6 - 6to Grado)")
        r_tunel = st.slider("Selecciona el radio del túnel en metros (r):", 1.0, 15.0, 5.75)
        
        perim_tunel = 2 * np.pi * r_tunel
        area_tunel = np.pi * (r_tunel ** 2)
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Perímetro de la entrada (2πr)", f"{perim_tunel:.2f} m")
        col_m2.metric("Área de la sección transversal (πr²)", f"{area_tunel:.2f} m²")
        
        theta = np.linspace(0, np.pi, 100) # Semicírculo o túnel completo
        x = r_tunel * np.cos(theta)
        y = r_tunel * np.sin(theta)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', fill='tozeroy', line=dict(color='#8E44AD', width=4), name='Túnel Vial'))
        fig.update_layout(title=f"Arco del Túnel Circular (r = {r_tunel} m)", xaxis_title="Metros", yaxis_title="Altura (m)", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with t3:
        st.subheader("🧊 Modelos Tridimensionales Interactivos 360°")
        cuerpo = st.selectbox("Selecciona Sólido Geométrico:", ["Cilindro", "Pirámide Cuadrangular", "Esfera", "Cubo"])
        
        if cuerpo == "Cilindro":
            r = st.slider("Radio r (m):", 1.0, 6.0, 3.0)
            h = st.slider("Altura h (m):", 1.0, 10.0, 5.0)
            z = np.linspace(0, h, 30)
            theta = np.linspace(0, 2*np.pi, 30)
            tg, zg = np.meshgrid(theta, z)
            xg, yg = r * np.cos(tg), r * np.sin(tg)
            fig = go.Figure(data=[go.Surface(x=xg, y=yg, z=zg, colorscale='Viridis')])
            fig.update_layout(title="Cilindro Tridimensional", height=450)
            st.plotly_chart(fig, use_container_width=True)
            
        elif cuerpo == "Pirámide Cuadrangular":
            b = st.slider("Lado de la Base (m):", 2.0, 8.0, 4.0)
            h = st.slider("Altura h (m):", 2.0, 10.0, 6.0)
            fig = go.Figure(data=[go.Mesh3d(
                x=[-b/2, b/2, b/2, -b/2, 0],
                y=[-b/2, -b/2, b/2, b/2, 0],
                z=[0, 0, 0, 0, h],
                i=[0, 0, 1, 2, 3], j=[1, 4, 2, 3, 0], k=[2, 1, 4, 4, 4],
                color='#E67E22', opacity=0.85
            )])
            fig.update_layout(title="Pirámide 3D", height=450)
            st.plotly_chart(fig, use_container_width=True)

        elif cuerpo == "Esfera":
            r = st.slider("Radio r (m):", 1.0, 6.0, 3.0)
            u, v = np.linspace(0, 2*np.pi, 30), np.linspace(0, np.pi, 30)
            x = r * np.outer(np.cos(u), np.sin(v))
            y = r * np.outer(np.sin(u), np.sin(v))
            z = r * np.outer(np.ones(np.size(u)), np.cos(v))
            fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Blues')])
            fig.update_layout(title="Esfera 3D", height=450)
            st.plotly_chart(fig, use_container_width=True)

        elif cuerpo == "Cubo":
            l = st.slider("Lado l (m):", 1.0, 6.0, 3.0)
            fig = go.Figure(data=[go.Mesh3d(
                x=[0, l, l, 0, 0, l, l, 0], y=[0, 0, l, l, 0, 0, l, l], z=[0, 0, 0, 0, l, l, l, l],
                i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2], j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3], k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                color='#2980B9', opacity=0.8
            )])
            fig.update_layout(title="Cubo 3D", height=450)
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# VISTA 4: PRÁCTICAS POR SECUENCIAS
# ------------------------------------------
elif st.session_state.page == "🎲 Prácticas por Secuencias":
    st.title("🎲 Prácticas Generadas de las Secuencias Didácticas")
    st.write("Genera ejercicios contextualizados basados en las unidades de los PDFs de 5.º y 6.º Grado.")
    
    secuencia_opt = st.selectbox(
        "Selecciona la Secuencia Didáctica para Practicar:",
        [
            "Secuencia 1: Adición y Gran Numeración (>1,000,000)",
            "Secuencia 2: Sustracción y Moneda Dominicana (RD$)",
            "Secuencia 3: División y Estimación",
            "Secuencia 4: Pitágoras y Geometría Aplicada",
            "Secuencia 5/6: Mediciones, Círculos y Perímetros"
        ]
    )

    if 'quiz_pdf' not in st.session_state:
        st.session_state.quiz_pdf = None

    if st.button("🎲 Generar Ejercicio de la Secuencia", type="primary"):
        if "Secuencia 1" in secuencia_opt:
            v1 = random.randint(100, 900) * 10000
            v2 = random.randint(100, 500) * 10000
            st.session_state.quiz_pdf = {
                "pregunta": f"En el centro comercial Megacentro se registraron {v1:,} visitas en el primer trimestre y {v2:,} en el segundo. ¿Cuántas visitas hubo en total?",
                "ans": str(v1 + v2),
                "tema": "Adición de Grandes Números"
            }
        elif "Secuencia 2" in secuencia_opt:
            papeletas_500 = random.randint(4, 12)
            st.session_state.quiz_pdf = {
                "pregunta": f"Un comerciante cambia {papeletas_500} billetes de RD$ 500. ¿A cuántos pesos dominicanos (RD$) equivale en total?",
                "ans": str(papeletas_500 * 500),
                "tema": "Moneda Dominicana RD$"
            }
        elif "Secuencia 3" in secuencia_opt:
            total_items = random.randint(5, 15) * 10
            personas = 5
            st.session_state.quiz_pdf = {
                "pregunta": f"Se deben repartir {total_items} cuadernos entre {personas} escuelas primarias en partes iguales. ¿Cuántos cuadernos le tocan a cada escuela?",
                "ans": str(total_items // personas),
                "tema": "División de Cantidades"
            }
        elif "Secuencia 4" in secuencia_opt:
            a = 3 * random.randint(1, 4)
            b = 4 * random.randint(1, 4)
            c = int(np.sqrt(a**2 + b**2))
            st.session_state.quiz_pdf = {
                "pregunta": f"En un triángulo rectángulo de catetos a = {a} m y b = {b} m, calcula la hipotenusa c.",
                "ans": str(c),
                "tema": "Teorema de Pitágoras"
            }
        else:
            r = random.randint(2, 10)
            perim = int(round(2 * 3.1416 * r))
            st.session_state.quiz_pdf = {
                "pregunta": f"Una rueda circular de parque tiene un radio de {r} metros. Calcula su perímetro aproximado redondeado al entero más cercano (usa π = 3.1416).",
                "ans": str(perim),
                "tema": "Perímetro del Círculo"
            }

    if st.session_state.quiz_pdf:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown(f"<span class=\"curriculum-badge\">📝 Ejercicio Práctico - {st.session_state.quiz_pdf['tema']}</span>", unsafe_allow_html=True)
        st.subheader(st.session_state.quiz_pdf['pregunta'])
        
        user_res = st.text_input("Tu respuesta numérica:", key="ans_quiz_pdf")
        
        if st.button("Validar Respuesta"):
            if user_res.strip().replace(",", "").replace(".", "") == st.session_state.quiz_pdf['ans']:
                st.balloons()
                st.success("🎉 ¡Excelente! Respuesta correcta.")
                log_progress(st.session_state.student_name, st.session_state.quiz_pdf['tema'], st.session_state.quiz_pdf['pregunta'], "Correcto", 1)
            else:
                st.error(f"❌ Respuesta incorrecta. La respuesta correcta era: {st.session_state.quiz_pdf['ans']}")
                log_progress(st.session_state.student_name, st.session_state.quiz_pdf['tema'], st.session_state.quiz_pdf['pregunta'], "Incorrecto", 1)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# VISTA 5: MI PROGRESO & INSIGNIAS
# ------------------------------------------
elif st.session_state.page == "📊 Mi Progreso & Insignias":
    st.title("📊 Panel Analytics de Progreso e Insignias (PDF Curriculum)")
    st.write(f"Registro del estudiante: **{st.session_state.student_name}**")
    
    df = get_progress()
    
    if not df.empty:
        df_est = df[df['estudiante'] == st.session_state.student_name]
        
        if not df_est.empty:
            aciertos = df_est[df_est['resultado'] == "Correcto"].shape[0]
            errores = df_est[df_est['resultado'] == "Incorrecto"].shape[0]
            total = df_est.shape[0]
            tasa = (aciertos / total * 100) if total > 0 else 0
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Ejercicios Intentados", total)
            m2.metric("Aciertos ✅", aciertos)
            m3.metric("Oportunidades de Mejora ❌", errores)
            m4.metric("Tasa de Éxito 🎯", f"{tasa:.1f}%")
            
            st.markdown("---")
            
            c1, c2 = st.columns(2)
            with c1:
                fig_pie = px.pie(names=["Correctos", "Incorrectos"], values=[aciertos, errores],
                                 color_discrete_sequence=['#2ECC71', '#E74C3C'], hole=0.4,
                                 title="Distribución de Aciertos vs Errores")
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with c2:
                df_tema = df_est.groupby(['tema', 'resultado']).size().reset_index(name='cantidad')
                fig_bar = px.bar(df_tema, x='tema', y='cantidad', color='resultado', barmode='group',
                                 color_discrete_map={'Correcto': '#2ECC71', 'Incorrecto': '#E74C3C'},
                                 title="Rendimiento por Secuencia Didáctica")
                st.plotly_chart(fig_bar, use_container_width=True)
                
            st.markdown("---")
            st.subheader("🏆 Insignias Educativas del Plan Didáctico")
            
            ins1, ins2, ins3, ins4 = st.columns(4)
            with ins1:
                desb = total >= 1
                st.markdown(f'''
                    <div class="badge-card {"badge-unlocked" if desb else ""}">
                        <h3>🥉</h3>
                        <b>Iniciador Didáctico</b><br>
                        <small>1 ejercicio completado</small><br>
                        <b>{"✅ Conseguido" if desb else "🔒 Bloqueado"}</b>
                    </div>
                ''', unsafe_allow_html=True)

            with ins2:
                desb = aciertos >= 3
                st.markdown(f'''
                    <div class="badge-card {"badge-unlocked" if desb else ""}">
                        <h3>🥈</h3>
                        <b>Dominador de Secuencias</b><br>
                        <small>3 aciertos correctos</small><br>
                        <b>{"✅ Conseguido" if desb else "🔒 Bloqueado"}</b>
                    </div>
                ''', unsafe_allow_html=True)

            with ins3:
                desb = aciertos >= 7
                st.markdown(f'''
                    <div class="badge-card {"badge-unlocked" if desb else ""}">
                        <h3>🥇</h3>
                        <b>Maestro Currículo MINERD</b><br>
                        <small>7 aciertos correctos</small><br>
                        <b>{"✅ Conseguido" if desb else "🔒 Bloqueado"}</b>
                    </div>
                ''', unsafe_allow_html=True)

            with ins4:
                desb = tasa >= 80 and total >= 5
                st.markdown(f'''
                    <div class="badge-card {"badge-unlocked" if desb else ""}">
                        <h3>💎</h3>
                        <b>Gran Matemático 5to/6to</b><br>
                        <small>Tasa > 80% en 5+ ejercicios</small><br>
                        <b>{"✅ Conseguido" if desb else "🔒 Bloqueado"}</b>
                    </div>
                ''', unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("📜 Trazabilidad de Intentos en el Sistema")
            st.dataframe(df_est, use_container_width=True)

        else:
            st.info(f"Aún no hay registros de actividad para '{st.session_state.student_name}'. ¡Completa ejercicios en el Tutor de Secuencias!")
    else:
        st.info("La base de datos de progreso está vacía.")
