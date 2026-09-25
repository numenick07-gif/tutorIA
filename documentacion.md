# Documentación Técnica: MateIA - Tutor Visual e Interactivo

## 1. Fundamento Pedagógico
MateIA se construye bajo los principios de la **Didáctica de las Matemáticas** y la **Teoría de la Visualización Cognitiva**. No se limita a proporcionar la respuesta final de un ejercicio, sino que implementa una doble estrategia basada en los libros de texto oficiales del **MINERD / PUCMM (CIEDHumano)**:
1. **Andamiaje Cognitivo:** Solicitud de pistas progresivas extraídas de las secuencias didácticas oficiales.
2. **Representación Icónica Relacionada al Tema:** Infografías e ilustraciones diseñadas específicamente para cada problema curricular (moneda dominicana, teorema de Pitágoras con escaleras, perímetro de túneles y fracciones de alimentos/medicamentos).

## 2. Arquitectura de Software
La aplicación está desarrollada en Python utilizando el ecosistema Streamlit.
- **Frontend & Estilos:** Interfaz personalizada mediante CSS inyectado (`unsafe_allow_html`) con diseño limpio, tarjetas de problemas y badges de secuencias.
- **Gráficos e Interactividad:**
  - `Plotly (go & px)`: Gráficos de barras apiladas de visitas a plazas, medidores de cambio en RD$, diagramas de pastel interactivos y superficies 3D en 360°.
  - `Matplotlib`: Renderizado de triángulos rectángulos de Pitágoras con cotas de longitud y arcos de túneles.
- **Backend / Estado:** `st.session_state` administra el flujo entre páginas, contadores de pistas por ejercicio y el perfil del estudiante.
- **Base de Datos (SQLite):** Archivo `mateia_progress.db` con la tabla `progress` para registrar la trazabilidad de los intentos por secuencia didáctica.

## 3. Ilustraciones e Imágenes Didácticas Directamente Relacionadas a los Temas (`assets/`)
Cada tema de tutoría cuenta con su imagen didáctica específica:
- `moneda_rd.jpg`: Descomposición de billetes de República Dominicana (RD$ 2,000, RD$ 500) en contexto de Plazas Comerciales (Secuencias 1 y 2 - 5.º Grado).
- `fracciones_visual.jpg`: Representación visual de fracciones y consumo de sobres de medicamentos (Secuencia 5 - 5.º y 6.º Grado).
- `pitagoras_escalera.jpg`: Ilustración del Teorema de Pitágoras con la escalera apoyada en la pared ($a=8\text{ ft}, b=14\text{ ft} \implies c \approx 16.12\text{ ft}$) (Secuencia 4 - 6.º Grado).
- `tunel_circular.jpg`: Ilustración y diagrama geométrico de la entrada circular a un túnel vial ($r = 5.75\text{ m}, P = 36.13\text{ m}$) (Secuencia 6 - 6.º Grado).
- `hero_banner.jpg`: Ilustración general de bienvenida al Tutor IA.

## 4. Gamificación y Analítica
La sección de progreso calcula métricas en tiempo real (Aciertos, Errores, Tasa de Éxito por Secuencia) y desbloquea insignias dinámicas (*Iniciador Didáctico*, *Dominador de Secuencias*, *Maestro Currículo MINERD*, *Gran Matemático 5to/6to*).
