"""
Dedicatoria a nuestro abuelo — versión Streamlit
--------------------------------------------------
Coloca este archivo, junto con:
  - "Noches-Vacias.mpeg"  (música de fondo, mismo directorio)
  - "abuelo.jpg"          (foto principal, opcional, mismo directorio)
en la misma carpeta, y ejecútalo con:
 
    streamlit run dedicatoria_abuelito.py
"""
 
import base64
import os
 
import streamlit as st
 
# --------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="A nuestro abuelo: Un hombre, un ejemplo, una historia de lucha y amor",
    page_icon="❤️",
    layout="centered",
)
 
AUDIO_FILE = "Noches-Vacias.mpeg"
PHOTO_FILE = "abuelo.jpg"  # coloca aquí la foto principal si la tienes
 
# --------------------------------------------------------------------------
# ESTILOS (recreando la paleta dorada / crema del HTML original)
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,400&display=swap');
 
    :root {
        --bg-crema: #faf6f0;
        --navy-primary: #111d33;
        --gold-accent: #d4af37;
    }
    .stApp {
        background-color: var(--bg-crema);
        background-image:
            radial-gradient(rgba(212, 175, 55, 0.12) 1px, transparent 0),
            radial-gradient(rgba(17, 29, 51, 0.05) 1px, #faf6f0 1px);
        background-size: 30px 30px;
        background-position: 0 0, 15px 15px;
    }

    /* -------- Barra superior fija (música / imprimir) -------- */
    .barra-superior {
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 24px;
        background: rgba(250, 246, 240, 0.92);
        backdrop-filter: blur(6px);
        border-bottom: 1px solid rgba(212, 175, 55, 0.25);
    }
    .pastilla-boton {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #fff;
        border: 1px solid rgba(212, 175, 55, 0.5);
        border-radius: 999px;
        padding: 8px 16px;
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        font-size: .95rem;
        color: #333;
        cursor: pointer;
        text-decoration: none;
    }
    .pastilla-boton.imprimir {
        background: #c1770f;
        color: #fff;
        border: none;
    }

    /* Espacio para que la barra fija no tape el contenido */
    .main .block-container {
        position: relative;
        padding-top: 90px;
    }
    /* Marcas de esquina doradas, estilo "marco de página" */
    .main .block-container::before,
    .main .block-container::after {
        content: '';
        position: absolute;
        top: 8px;
        width: 30px;
        height: 30px;
        border-top: 2px solid #b8860b;
    }
    .main .block-container::before {
        left: 0;
        border-left: 2px solid #b8860b;
    }
    .main .block-container::after {
        right: 0;
        border-right: 2px solid #b8860b;
    }

    @media print {
        .barra-superior { display: none !important; }
    }

    .titulo-dedicatoria {
        font-family: 'Cinzel', serif;
        text-align: center;
        color: #111d33;
        font-weight: 800;
        letter-spacing: .5px;
        font-size: 2rem;
        margin-bottom: 0;
    }
    .etiqueta-dorada {
        display: inline-block;
        margin: 0 auto 10px auto;
        padding: 4px 18px;
        background: rgba(212, 175, 55, 0.18);
        color: #7a5c10;
        border-radius: 999px;
        font-size: .75rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        border: 1px solid rgba(212, 175, 55, 0.5);
    }
    .texto-dedicatoria {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.35rem;
        line-height: 1.8;
        text-align: justify;
        color: #2b231d;
    }
    .cita-destacada {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        font-size: 1.5rem;
        text-align: center;
        color: #7a5c10;
        background: rgba(255, 245, 220, 0.6);
        padding: 18px;
        border-left: 4px solid #d4af37;
        border-radius: 10px;
    }
    .firma-familia {
        text-align: center;
        font-size: .85rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #6b6b6b;
        margin-top: 6px;
    }
    .marco-foto img {
        border-radius: 16px;
        border: 8px solid;
        border-image: linear-gradient(145deg, #f7e6b5, #b8860b, #e6ca65, #8a6508) 1;
        box-shadow: 0 20px 40px -10px rgba(17,29,51,0.35), 0 0 25px rgba(212,175,55,0.4);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
 
# --------------------------------------------------------------------------
# MÚSICA DE FONDO — se reproduce automáticamente al abrir la página
# (los navegadores pueden bloquear el autoplay con sonido hasta que el
# usuario interactúe una vez con la pestaña; es una restricción del propio
# navegador, no de Streamlit)
# --------------------------------------------------------------------------
if os.path.exists(AUDIO_FILE):
    with open(AUDIO_FILE, "rb") as f:
        audio_bytes = f.read()
    b64_audio = base64.b64encode(audio_bytes).decode()
    st.markdown(
        f"""
        <audio
            id="audio-fondo"
            autoplay
            loop
            onplay="document.getElementById('music-label').innerText='🎵 Música de fondo: Reproduciendo'"
            onpause="document.getElementById('music-label').innerText='🎵 Música de fondo: Pausada'"
        >
            <source src="data:audio/mpeg;base64,{b64_audio}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True,
    )
else:
    st.warning(
        f"No se encontró '{AUDIO_FILE}' en la carpeta del proyecto. "
        "Copia el archivo de música ahí para que suene automáticamente."
    )

# --------------------------------------------------------------------------
# BARRA SUPERIOR: toggle de música + botón de imprimir/guardar PDF
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="barra-superior">
        <span
            id="music-label"
            class="pastilla-boton"
            onclick="
                var a = document.getElementById('audio-fondo');
                if (a) { a.paused ? a.play() : a.pause(); }
            "
        >🎵 Música de fondo: Pausada</span>
        <span class="pastilla-boton imprimir" onclick="window.print()">
            🖨️ Guardar / Imprimir PDF
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
 
# --------------------------------------------------------------------------
# ENCABEZADO / RETRATO
# --------------------------------------------------------------------------
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    st.markdown('<div class="marco-foto">', unsafe_allow_html=True)
    if os.path.exists(PHOTO_FILE):
        st.image(PHOTO_FILE, use_container_width=True)
    else:
        st.info("Coloca 'abuelo.jpg' en esta carpeta para mostrar la fotografía.")
    st.markdown("</div>", unsafe_allow_html=True)
 
st.markdown(
    '<p style="text-align:center;"><span class="etiqueta-dorada">'
    "Homenaje de Amor y Gratitud</span></p>",
    unsafe_allow_html=True,
)
st.markdown(
    '<h1 class="titulo-dedicatoria">A nuestro abuelo: Un hombre, un ejemplo, '
    "una historia de lucha y amor</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")
 
# --------------------------------------------------------------------------
# TEXTO DE LA DEDICATORIA
# --------------------------------------------------------------------------
parrafos = [
    "Desde las tierras altas de Apurímac hasta el suelo de Chilca, tu camino estuvo "
    "trazado por la valentía y la determinación. Llegaste buscando a un hermano y "
    "encontraste un hogar, una vida y un destino. Fue aquí donde conociste a nuestra "
    "abuela Elena y, juntos, sembraron la semilla de una gran familia que floreció en "
    "12 hijos, convirtiéndose en el pilar más firme de tu vida.",
    "Como hombre, nos enseñaste el verdadero significado de la palabra lealtad y "
    "trabajo duro. Enfrentaste adversidades sin doblarte: defendiste con coraje y "
    "dignidad lo que con esfuerzo y justicia te correspondía, demostrando que a ti "
    "nada te regaló la vida sin que lo lucharas hasta el final. Sin embargo, aun en "
    "los momentos de mayor escasez, tu corazón nunca supo de egoísmo. Jamás le negaste "
    "la mano a un amigo ni le dijiste \"no\" a quien te pidió ayuda.",
    "La prosperidad llegó a tu vida como fruto de tu perseverancia. Con paciencia y "
    "visión, transformaste el trabajo en logros: fundaste el barrio Mayta Cápac, "
    "viste nacer tu anhelado Centro Recreacional que lleva ese mismo nombre, y "
    "pudiste vivir una de tus grandes pasiones en el fútbol y los torneos "
    "interbarrios. Tu esfuerzo dio frutos y compartiste ese éxito con los tuyos.",
    "Como padre, tu presencia fue incondicional. Caminaste al lado de cada uno de "
    "tus hijos en sus triunfos y los sostuviste en sus momentos difíciles. Seguiste "
    "adelante, de pie, con la mirada puesta en tus hijos y con el abrazo listo para "
    "recibir a tus primeros nietos y bisnietos.",
]
 
for p in parrafos:
    st.markdown(f'<p class="texto-dedicatoria">{p}</p>', unsafe_allow_html=True)
 
st.markdown(
    '<p class="cita-destacada">Hoy honramos al hombre que abrió el camino, al esposo '
    "compañero, al padre presente, al abuelo generoso y al bisabuelo sabio. Tu "
    "historia de superación y tu legado viven en cada uno de nosotros.</p>",
    unsafe_allow_html=True,
)
 
st.markdown(
    '<p class="cita-destacada" style="margin-top:24px;">Gracias por tu fuerza, por tu '
    "generosidad sin límites y por enseñarnos a luchar siempre por lo nuestro.</p>",
    unsafe_allow_html=True,
)
st.markdown('<p class="firma-familia">Con amor eterno, tu familia</p>', unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# --------------------------------------------------------------------------
# ABRAZO VIRTUAL (equivalente al confeti/corazones del HTML original)
# --------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("❤️ Enviar un Abrazo Virtual", use_container_width=True):
        st.balloons()
 
st.markdown("---")
 
# --------------------------------------------------------------------------
# GALERÍA DE RECUERDOS FAMILIARES (dinámica, como en el HTML)
# --------------------------------------------------------------------------
st.subheader("📷 Galería de Recuerdos Familiares")
st.caption("Puedes agregar más fotos especiales con tu abuelo")
 
if "galeria" not in st.session_state:
    st.session_state.galeria = []
 
with st.form("agregar_foto", clear_on_submit=True):
    nueva_foto = st.file_uploader("Agregar foto familiar", type=["png", "jpg", "jpeg"])
    nota = st.text_input("Escribe una nota para esta foto:", value="Recuerdo especial")
    enviado = st.form_submit_button("Agregar a la galería")
    if enviado and nueva_foto is not None:
        st.session_state.galeria.insert(0, (nueva_foto.getvalue(), nota))
        st.success("¡Foto agregada!")
        st.balloons()
 
if st.session_state.galeria:
    cols = st.columns(3)
    for i, (foto_bytes, nota) in enumerate(st.session_state.galeria):
        with cols[i % 3]:
            st.image(foto_bytes, use_container_width=True, caption=nota)
else:
    st.info("Aún no hay fotos agregadas a la galería.")
 
st.markdown("---")
st.caption("Página de Homenaje Especial dedicada a nuestro querido abuelo ❤️")
