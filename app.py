"""
Dedicatoria a nuestro abuelo — versión Streamlit + Supabase
--------------------------------------------------
Archivos necesarios en la carpeta:
  - "Noches-Vacias.mpeg"
  - "abuelo.jpg" (opcional)
  - ".streamlit/secrets.toml" (con SUPABASE_URL y SUPABASE_KEY)
"""

import base64
import os
import random
import textwrap

import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client, Client

# --------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="A nuestro abuelo: Un hombre, un ejemplo, una historia de lucha y amor",
    page_icon="❤️",
    layout="centered",
)

AUDIO_FILE = "Noches-Vacias.mpeg"
PHOTO_FILE = "abuelo.jpg"

# --------------------------------------------------------------------------
# CONEXIÓN A SUPABASE
# --------------------------------------------------------------------------
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("Error al conectar con la base de datos de Supabase. Revisa las claves en secrets.toml.")
    supabase = None

def cargar_dedicatorias():
    if not supabase:
        return []
    try:
        response = supabase.table("dedicatorias").select("*").order("created_at", desc=True).execute()
        return [row["texto"] for row in response.data]
    except Exception as e:
        st.error(f"Error al cargar mensajes: {e}")
        return []

def guardar_dedicatoria(texto: str):
    if not supabase:
        return
    try:
        supabase.table("dedicatorias").insert({"texto": texto}).execute()
    except Exception as e:
        st.error(f"Error al guardar mensaje: {e}")

# Estado de la galería de recuerdos (fotos en sesión)
if "galeria" not in st.session_state:
    st.session_state.galeria = []

MIME_POR_EXTENSION = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}

def html(texto: str) -> str:
    return textwrap.dedent(texto).strip()

# --------------------------------------------------------------------------
# ESTILOS (Evitando bloqueos de Scroll)
# --------------------------------------------------------------------------
st.markdown(
    html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,400&display=swap');

        :root {
            --bg-crema: #faf6f0;
            --navy-primary: #111d33;
            --gold-accent: #d4af37;
        }

        [data-testid="stHeader"] {
            visibility: hidden !important;
            height: 0px !important;
        }
        footer { visibility: hidden !important; }

        .stApp {
            background-color: var(--bg-crema) !important;
            background-image:
                radial-gradient(rgba(212, 175, 55, 0.12) 1px, transparent 0),
                radial-gradient(rgba(17, 29, 51, 0.05) 1px, #faf6f0 1px) !important;
            background-size: 30px 30px;
            background-position: 0 0, 15px 15px;
        }

        .main .block-container {
            padding-top: 1rem !important;
            position: relative;
            z-index: 1;
        }

        .main .block-container::before,
        .main .block-container::after {
            content: '';
            position: absolute;
            top: 20px;
            width: 30px;
            height: 30px;
            border-top: 2px solid #b8860b;
        }
        .main .block-container::before {
            left: 20px;
            border-left: 2px solid #b8860b;
        }
        .main .block-container::after {
            right: 20px;
            border-right: 2px solid #b8860b;
        }

        @media print {
            .fondo-recuerdos { display: none !important; }
        }

        .fondo-recuerdos {
            position: fixed;
            inset: 0;
            z-index: 0;
            overflow: hidden;
            pointer-events: none !important;
        }
        .fondo-recuerdos img {
            position: absolute;
            opacity: 0.16;
            filter: sepia(0.35) contrast(0.9);
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(17,29,51,0.15);
            object-fit: cover;
            pointer-events: none !important;
        }
        .lista-recuerdos {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1rem;
            color: #6b6b6b !important;
            text-align: center;
            line-height: 1.9;
        }

        .lluvia-corazones {
            position: fixed;
            inset: 0;
            z-index: 1000000;
            overflow: hidden;
            pointer-events: none !important;
        }
        .lluvia-corazones span {
            position: absolute;
            bottom: -60px;
            color: #c1770f;
            animation-name: flotar-corazon;
            animation-timing-function: ease-in;
            animation-fill-mode: forwards;
        }
        @keyframes flotar-corazon {
            0%   { transform: translateY(0) scale(0.8); opacity: 0; }
            12%  { opacity: 1; }
            100% { transform: translateY(-110vh) scale(1.05); opacity: 0; }
        }

        .marco-foto {
            display: inline-block;
            border-radius: 16px;
            border: 8px solid;
            border-image: linear-gradient(145deg, #f7e6b5, #b8860b, #e6ca65, #8a6508) 1;
            box-shadow: 0 20px 40px -10px rgba(17,29,51,0.35), 0 0 25px rgba(212,175,55,0.4);
            overflow: hidden;
            line-height: 0;
        }
        .marco-foto img {
            display: block;
            width: 340px;
            max-width: 100%;
            border-radius: 8px;
        }

        .titulo-dedicatoria {
            font-family: 'Cinzel', serif;
            text-align: center;
            color: #111d33 !important;
            font-weight: 800;
            letter-spacing: .5px;
            font-size: 2rem;
            margin-bottom: 0;
        }
        .etiqueta-dorada {
            display: inline-block;
            margin: 0 auto 10px auto;
            padding: 4px 18px;
            background: rgba(212, 175, 55, 0.18) !important;
            color: #7a5c10 !important;
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
            color: #2b231d !important;
        }
        .cita-destacada {
            font-family: 'Cormorant Garamond', serif;
            font-weight: 600;
            font-size: 1.5rem;
            text-align: center;
            color: #7a5c10 !important;
            background: rgba(255, 245, 220, 0.6) !important;
            padding: 18px;
            border-left: 4px solid #d4af37;
            border-radius: 10px;
        }
        .firma-familia {
            text-align: center;
            font-size: .85rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #6b6b6b !important;
            margin-top: 6px;
        }

        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
        [data-testid="stHeading"] * { color: #111d33 !important; }
        [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] *,
        .main .stCaption { color: #6b6b6b !important; }
        [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label,
        .main label { color: #2b231d !important; }
        [data-testid="stFileUploaderDropzoneInstructions"],
        [data-testid="stFileUploaderDropzoneInstructions"] * { color: #2b231d !important; }
        [data-testid="stFileUploaderDropzone"] small,
        [data-testid="stFileUploaderDropzone"] span { color: #6b6b6b !important; }
        [data-testid="stAlert"], [data-testid="stAlert"] * { color: #2b231d !important; }
        .stTextArea textarea, .stTextInput input {
            color: #2b231d !important;
            background-color: #fffdf8 !important;
        }
        </style>
        """
    ),
    unsafe_allow_html=True,
)


def mostrar_fotos_de_fondo():
    if not st.session_state.galeria: return
    fotos = st.session_state.galeria[:14]
    piezas = ['<div class="fondo-recuerdos">']
    for i, (foto_bytes, _nota, mime) in enumerate(fotos):
        b64 = base64.b64encode(foto_bytes).decode()
        rnd = random.Random(i * 97 + 13)
        top, left = rnd.randint(-5, 85), rnd.randint(-5, 85)
        rot, ancho = rnd.randint(-18, 18), rnd.randint(150, 230)
        piezas.append(
            f'<img src="data:{mime};base64,{b64}" '
            f'style="top:{top}%; left:{left}%; width:{ancho}px; '
            f'transform: rotate({rot}deg);">'
        )
    piezas.append("</div>")
    st.markdown("".join(piezas), unsafe_allow_html=True)


def lluvia_corazones(cantidad: int = 18):
    simbolos = ["❤️", "🕊️", "✨", "🤍"]
    spans = []
    for i in range(cantidad):
        rnd = random.Random()
        izquierda, duracion = rnd.uniform(2, 96), rnd.uniform(4.5, 7.5)
        retraso, tamano = rnd.uniform(0, 1.4), rnd.uniform(1.3, 2.3)
        simbolo = rnd.choice(simbolos)
        spans.append(
            f'<span style="left:{izquierda:.1f}%; font-size:{tamano:.2f}rem; '
            f'animation-duration:{duracion:.2f}s; animation-delay:{retraso:.2f}s;">'
            f"{simbolo}</span>"
        )
    st.markdown(f'<div class="lluvia-corazones">{"".join(spans)}</div>', unsafe_allow_html=True)


mostrar_fotos_de_fondo()

# --------------------------------------------------------------------------
# MÚSICA DE FONDO + BARRA SUPERIOR
# --------------------------------------------------------------------------
if os.path.exists(AUDIO_FILE):
    with open(AUDIO_FILE, "rb") as f:
        audio_bytes = f.read()
    b64_audio = base64.b64encode(audio_bytes).decode()
    audio_tag = (
        f'<audio id="audio-fondo" autoplay loop>'
        f'<source src="data:audio/mpeg;base64,{b64_audio}" type="audio/mpeg">'
        f"</audio>"
    )
else:
    audio_tag = ""
    st.warning(f"No se encontró '{AUDIO_FILE}'. Colócalo en la carpeta para que suene la música.")

barra_superior_html = html(
    f"""
    <style>
        body {{ 
            margin: 0; background: transparent; 
            display: flex; flex-wrap: wrap; justify-content: center; gap: 12px;
            font-family: 'Cormorant Garamond', serif;
            padding: 5px;
        }}
        button {{
            border-radius: 999px; padding: 10px 20px; font-family: inherit;
            font-weight: 600; font-size: 1rem; cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: all 0.2s;
        }}
        #btn-musica {{
            background: #fff; border: 1px solid rgba(212,175,55,0.5); color: #333;
        }}
        #btn-imprimir {{
            background: #c1770f; border: none; color: #fff;
        }}
    </style>

    <button id="btn-musica">🎵 Música de fondo: Reproduciendo</button>
    <button id="btn-imprimir">🖨️ Guardar / Imprimir PDF</button>

    {audio_tag}

    <script>
        var audio = document.getElementById("audio-fondo");
        var btnMusica = document.getElementById("btn-musica");
        var btnImprimir = document.getElementById("btn-imprimir");
        var visualmenteReproduciendo = true;

        if (audio) {{
            audio.play().catch(function(e) {{
                console.log("El navegador bloqueó el autoplay temporalmente.");
            }});
        }}

        if (btnMusica) {{
            btnMusica.addEventListener("click", function () {{
                if (!audio) return;
                
                if (visualmenteReproduciendo) {{
                    audio.pause();
                    visualmenteReproduciendo = false;
                    btnMusica.innerText = "🎵 Música de fondo: Pausada";
                }} else {{
                    audio.play();
                    visualmenteReproduciendo = true;
                    btnMusica.innerText = "🎵 Música de fondo: Reproduciendo";
                }}
            }});
        }}

        if (btnImprimir) {{
            btnImprimir.addEventListener("click", function () {{
                try {{ window.parent.print(); }} catch (e) {{ window.print(); }}
            }});
        }}
    </script>
    """
)

components.html(barra_superior_html, height=110)
st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# ENCABEZADO / RETRATO
# --------------------------------------------------------------------------
if os.path.exists(PHOTO_FILE):
    with open(PHOTO_FILE, "rb") as f:
        foto_principal_bytes = f.read()
    foto_principal_b64 = base64.b64encode(foto_principal_bytes).decode()
    _, ext_foto = os.path.splitext(PHOTO_FILE.lower())
    mime_foto_principal = MIME_POR_EXTENSION.get(ext_foto, "image/jpeg")
    st.markdown(
        html(
            f"""
            <div style="text-align:center;">
                <div class="marco-foto">
                    <img src="data:{mime_foto_principal};base64,{foto_principal_b64}">
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
else:
    st.info("Coloca 'abuelo.jpg' en esta carpeta para mostrar la fotografía.")

st.markdown('<p style="text-align:center;"><span class="etiqueta-dorada">Homenaje de Amor y Gratitud</span></p>', unsafe_allow_html=True)
st.markdown('<h1 class="titulo-dedicatoria">A nuestro abuelo: Un hombre, un ejemplo, una historia de lucha y amor</h1>', unsafe_allow_html=True)
st.markdown("---")

# --------------------------------------------------------------------------
# TEXTO DE LA DEDICATORIA
# --------------------------------------------------------------------------
parrafos = [
    "Desde las tierras altas de Apurímac hasta el suelo de Chilca, tu camino estuvo trazado por la valentía y la determinación. Llegaste buscando a un hermano y encontraste un hogar, una vida y un destino. Fue aquí donde conociste a nuestra abuela Elena y, juntos, sembraron la semilla de una gran familia que floreció en 12 hijos, convirtiéndose en el pilar más firme de tu vida.",
    "Como hombre, nos enseñaste el verdadero significado de la palabra lealtad y trabajo duro. Enfrentaste adversidades sin doblarte: defendiste con coraje y dignidad lo que con esfuerzo y justicia te correspondía, demostrando que a ti nada te regaló la vida sin que lo lucharas hasta el final. Sin embargo, aun en los momentos de mayor escasez, tu corazón nunca supo de egoísmo. Jamás le negaste la mano a un amigo ni le dijiste \"no\" a quien te pidió ayuda.",
    "La prosperidad llegó a tu vida como fruto de tu perseverancia. Con paciencia y visión, transformaste el trabajo en logros: fundaste el barrio Mayta Cápac, viste nacer tu anhelado Centro Recreacional que lleva ese mismo nombre, y pudiste vivir una de tus grandes pasiones en el fútbol y los torneos interbarrios. Tu esfuerzo dio frutos y compartiste ese éxito con los tuyos.",
    "Como padre, tu presencia fue incondicional. Caminaste al lado de cada uno de tus hijos en sus triunfos y los sostuviste en sus momentos difíciles. Seguiste adelante, de pie, con la mirada puesta en tus hijos y con el abrazo listo para recibir a tus primeros nietos y bisnietos."
]
for p in parrafos:
    st.markdown(f'<p class="texto-dedicatoria">{p}</p>', unsafe_allow_html=True)

st.markdown('<p class="cita-destacada">Hoy honramos al hombre que abrió el camino, al esposo compañero, al padre presente, al abuelo generoso y al bisabuelo sabio. Tu historia de superación y tu legado viven en cada uno de nosotros.</p>', unsafe_allow_html=True)
st.markdown('<p class="cita-destacada" style="margin-top:24px;">Gracias por tu fuerza, por tu generosidad sin límites y por enseñarnos a luchar siempre por lo nuestro.</p>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# DEDICA UNAS PALABRAS (Persistente con Supabase)
# --------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("💛 Dedica unas palabras")
st.caption("Escribe tu propio mensaje para el abuelo; se guardará de forma permanente y toda la familia lo podrá leer.")

with st.form("agregar_dedicatoria", clear_on_submit=True):
    nombre_dedicante = st.text_input("Tu nombre (opcional):", value="")
    mensaje_dedicatoria = st.text_area("Tu dedicatoria:", value="", height=100)
    enviar_dedicatoria = st.form_submit_button("Agregar mi dedicatoria")
    if enviar_dedicatoria and mensaje_dedicatoria.strip():
        texto_final = mensaje_dedicatoria.strip()
        if nombre_dedicante.strip(): 
            texto_final += f" — {nombre_dedicante.strip()}"
        guardar_dedicatoria(texto_final)
        st.success("¡Gracias! Tu dedicatoria fue guardada para toda la familia.")
        lluvia_corazones()

# Cargar mensajes guardados en la base de datos
mensajes_guardados = cargar_dedicatorias()
for mensaje in mensajes_guardados:
    st.markdown(f'<p class="cita-destacada" style="margin-top:16px;">{mensaje}</p>', unsafe_allow_html=True)

st.markdown('<p class="firma-familia">Con amor eterno, tu familia</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# ABRAZO VIRTUAL
# --------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("❤️ Enviar un Abrazo Virtual", use_container_width=True):
        lluvia_corazones()
st.markdown("---")

# --------------------------------------------------------------------------
# GALERÍA DE RECUERDOS FAMILIARES
# --------------------------------------------------------------------------
st.subheader("📷 Galería de Recuerdos Familiares")
st.caption("Las fotos que agregues aparecerán tenues, de fondo, como recuerdos flotando por toda la página.")

with st.form("agregar_foto", clear_on_submit=True):
    nueva_foto = st.file_uploader("Agregar foto familiar", type=["png", "jpg", "jpeg"])
    nota = st.text_input("Escribe una nota para esta foto:", value="Recuerdo especial")
    enviado = st.form_submit_button("Agregar a la galería")
    if enviado and nueva_foto is not None:
        _, ext = os.path.splitext(nueva_foto.name.lower())
        mime = MIME_POR_EXTENSION.get(ext, "image/jpeg")
        st.session_state.galeria.insert(0, (nueva_foto.getvalue(), nota, mime))
        st.success("¡Foto agregada como recuerdo de fondo!")
        lluvia_corazones()

if st.session_state.galeria:
    notas = " · ".join(nota for _foto, nota, _mime in st.session_state.galeria)
    st.markdown(f'<p class="lista-recuerdos">🕊️ {notas}</p>', unsafe_allow_html=True)
else:
    st.info("Aún no hay recuerdos agregados a la galería.")

st.markdown("---")
st.caption("Página de Homenaje Especial dedicada a nuestro querido abuelo ❤️")
