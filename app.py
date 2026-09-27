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
import random
import textwrap
 
import streamlit as st
import streamlit.components.v1 as components
 
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

# Estado de la galería de recuerdos (se necesita desde el principio del script
# porque las fotos se usan como fondo antes de llegar al formulario)
if "galeria" not in st.session_state:
    st.session_state.galeria = []  # lista de (bytes_foto, nota, mime_type)

if "mensajes_dedicatoria" not in st.session_state:
    st.session_state.mensajes_dedicatoria = []  # lista de strings escritos por la familia

MIME_POR_EXTENSION = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


def html(texto: str) -> str:
    """Quita la indentación común de un bloque HTML/CSS multilínea.

    Streamlit usa Markdown para renderizar st.markdown(unsafe_allow_html=True).
    Si el texto tiene 4 o más espacios de indentación al inicio de cada línea,
    Markdown lo interpreta como un BLOQUE DE CÓDIGO y lo muestra como texto
    plano en vez de renderizarlo como HTML real (por eso, por ejemplo, la
    etiqueta <audio> aparecía literalmente escrita en la página). Esta función
    evita ese problema siempre que construyamos HTML con f-strings indentados.
    """
    return textwrap.dedent(texto).strip()

 
# --------------------------------------------------------------------------
# ESTILOS (recreando la paleta dorada / crema del HTML original)
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

        /* Ocultamos el header/menú/footer nativos de Streamlit: los reemplazamos
           por nuestra propia barra superior. Usamos visibility: hidden en el header
           para evitar el bug de Streamlit que bloquea el scroll al usar display: none. */
        header[data-testid="stHeader"] {
            visibility: hidden !important;
            height: 0px !important;
            min-height: 0px !important;
            padding: 0px !important;
        }
        #MainMenu,
        footer {
            display: none !important;
        }
        
        /* Aseguramos que la página principal pueda desplazarse (solución al bug de scroll) */
        [data-testid="stAppViewContainer"], 
        .stApp, 
        .main {
            overflow-y: auto !important;
            overflow-x: hidden !important;
        }

        .stApp {
            background-color: var(--bg-crema) !important;
            background-image:
                radial-gradient(rgba(212, 175, 55, 0.12) 1px, transparent 0),
                radial-gradient(rgba(17, 29, 51, 0.05) 1px, #faf6f0 1px) !important;
            background-size: 30px 30px;
            background-position: 0 0, 15px 15px;
        }

        /* -------- Barra superior fija (música / imprimir) -------- */
        .barra-superior {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 999999;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 24px;
            background: rgba(250, 246, 240, 0.95);
            backdrop-filter: blur(6px);
            border-bottom: 1px solid rgba(212, 175, 55, 0.25);
        }
        .pastilla-boton {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #fff !important;
            border: 1px solid rgba(212, 175, 55, 0.5);
            border-radius: 999px;
            padding: 8px 16px;
            font-family: 'Cormorant Garamond', serif;
            font-weight: 600;
            font-size: .95rem;
            color: #333 !important;
            cursor: pointer;
            text-decoration: none;
        }
        .pastilla-boton.imprimir {
            background: #c1770f !important;
            color: #fff !important;
            border: none;
        }

        /* Espacio para que la barra fija no tape el contenido */
        .main .block-container {
            position: relative;
            z-index: 1;
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
            .fondo-recuerdos { display: none !important; }
        }

        /* -------- Fotos de la galería usadas como fondo transparente -------- */
        .fondo-recuerdos {
            position: fixed;
            inset: 0;
            z-index: 0;
            overflow: hidden;
            pointer-events: none;
        }
        .fondo-recuerdos img {
            position: absolute;
            opacity: 0.16;
            filter: sepia(0.35) contrast(0.9);
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(17,29,51,0.15);
            object-fit: cover;
        }
        .lista-recuerdos {
            font-family: 'Cormorant Garamond', serif;
            font-size: 1rem;
            color: #6b6b6b !important;
            text-align: center;
            line-height: 1.9;
        }

        /* -------- Lluvia de corazones (reemplaza el confeti) -------- */
        .lluvia-corazones {
            position: fixed;
            inset: 0;
            z-index: 1000000;
            overflow: hidden;
            pointer-events: none;
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

        /* -------- Marco dorado de la foto principal -------- */
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

        /* -------- Forzamos color oscuro en los elementos NATIVOS de Streamlit
           (subtítulos, captions, labels, uploader, alertas). Si el tema del
           navegador/Streamlit es oscuro, estos elementos salen en texto claro
           por defecto y se pierden sobre nuestro fondo crema. No tocamos
           nuestras propias clases (texto-dedicatoria, cita-destacada, etc.)
           porque esas ya fijan su color explícitamente más abajo. -------- */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
        [data-testid="stHeading"] * {
            color: #111d33 !important;
        }
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] *,
        .main .stCaption {
            color: #6b6b6b !important;
        }
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] label,
        .main label {
            color: #2b231d !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"],
        [data-testid="stFileUploaderDropzoneInstructions"] * {
            color: #2b231d !important;
        }
        [data-testid="stFileUploaderDropzone"] small,
        [data-testid="stFileUploaderDropzone"] span {
            color: #6b6b6b !important;
        }
        [data-testid="stAlert"],
        [data-testid="stAlert"] * {
            color: #2b231d !important;
        }
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
    """Dibuja las fotos de la galería como recuerdos translúcidos de fondo."""
    if not st.session_state.galeria:
        return
    # Se limita para no saturar la pantalla si hay muchísimas fotos
    fotos = st.session_state.galeria[:14]
    piezas = ['<div class="fondo-recuerdos">']
    for i, (foto_bytes, _nota, mime) in enumerate(fotos):
        b64 = base64.b64encode(foto_bytes).decode()
        # posiciones/rotación pseudo-aleatorias pero estables (semilla fija por foto)
        rnd = random.Random(i * 97 + 13)
        top = rnd.randint(-5, 85)
        left = rnd.randint(-5, 85)
        rot = rnd.randint(-18, 18)
        ancho = rnd.randint(150, 230)
        piezas.append(
            f'<img src="data:{mime};base64,{b64}" '
            f'style="top:{top}%; left:{left}%; width:{ancho}px; '
            f'transform: rotate({rot}deg);">'
        )
    piezas.append("</div>")
    st.markdown("".join(piezas), unsafe_allow_html=True)


def lluvia_corazones(cantidad: int = 18):
    """Animación de corazones subiendo y desvaneciéndose (reemplaza st.balloons())."""
    simbolos = ["❤️", "🕊️", "✨", "🤍"]
    spans = []
    for i in range(cantidad):
        rnd = random.Random()
        izquierda = rnd.uniform(2, 96)
        duracion = rnd.uniform(4.5, 7.5)
        retraso = rnd.uniform(0, 1.4)
        tamano = rnd.uniform(1.3, 2.3)
        simbolo = rnd.choice(simbolos)
        spans.append(
            f'<span style="left:{izquierda:.1f}%; font-size:{tamano:.2f}rem; '
            f'animation-duration:{duracion:.2f}s; animation-delay:{retraso:.2f}s;">'
            f"{simbolo}</span>"
        )
    st.markdown(
        f'<div class="lluvia-corazones">{"".join(spans)}</div>',
        unsafe_allow_html=True,
    )


# Fondo de recuerdos (se pinta ya, para que quede detrás de todo el contenido)
mostrar_fotos_de_fondo()
 
# --------------------------------------------------------------------------
# MÚSICA DE FONDO + BARRA SUPERIOR (música / imprimir)
# --------------------------------------------------------------------------
# IMPORTANTE: st.markdown(unsafe_allow_html=True) renderiza el HTML, pero por
# seguridad Streamlit IGNORA cualquier JavaScript dentro de ese HTML (scripts
# y atributos onclick/onplay/onpause no se ejecutan nunca). Por eso los
# botones no reaccionaban al hacer clic. La única forma de tener JavaScript
# que realmente funcione en Streamlit es con st.components.v1.html(), que
# crea un <iframe> real donde sí se ejecutan los scripts. Por eso movemos el
# audio y los botones ahí adentro.
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
    st.warning(
        f"No se encontró '{AUDIO_FILE}' en la carpeta del proyecto. "
        "Copia el archivo de música ahí para que suene automáticamente."
    )

barra_superior_html = html(
    f"""
    <div id="barra-superior" style="display:flex; justify-content:space-between;
        align-items:center; padding:8px 20px; background:rgba(250,246,240,0.95);
        border-bottom:1px solid rgba(212,175,55,0.25); font-family:'Cormorant Garamond', serif;
        box-sizing:border-box;">
        <button id="btn-musica" style="display:inline-flex; align-items:center; gap:6px;
            background:#fff; border:1px solid rgba(212,175,55,0.5); border-radius:999px;
            padding:8px 16px; font-family:'Cormorant Garamond', serif; font-weight:600;
            font-size:.95rem; color:#333; cursor:pointer;">
            🎵 Música de fondo: Pausada
        </button>
        <button id="btn-imprimir" style="background:#c1770f; color:#fff; border:none;
            border-radius:999px; padding:8px 16px; font-family:'Cormorant Garamond', serif;
            font-weight:600; font-size:.95rem; cursor:pointer;">
            🖨️ Guardar / Imprimir PDF
        </button>
        {audio_tag}
    </div>
    <script>
        // Intentamos fijar esta barra en la parte superior de la ventana real
        // (no solo del iframe), tomando el propio iframe como referencia.
        try {{
            var marco = window.frameElement;
            if (marco) {{
                marco.style.position = "fixed";
                marco.style.top = "0";
                marco.style.left = "0";
                marco.style.right = "0";
                marco.style.width = "100%";
                marco.style.zIndex = "999999";
                marco.style.border = "none";
            }}
        }} catch (e) {{ /* si el navegador bloquea el acceso, seguimos igual */ }}

        var audio = document.getElementById("audio-fondo");
        var btnMusica = document.getElementById("btn-musica");
        var btnImprimir = document.getElementById("btn-imprimir");

        if (btnMusica) {{
            btnMusica.addEventListener("click", function () {{
                if (!audio) return;
                if (audio.paused) {{
                    audio.play();
                    btnMusica.innerText = "🎵 Música de fondo: Reproduciendo";
                }} else {{
                    audio.pause();
                    btnMusica.innerText = "🎵 Música de fondo: Pausada";
                }}
            }});
        }}

        if (btnImprimir) {{
            btnImprimir.addEventListener("click", function () {{
                // Imprimimos la ventana principal (no el iframe) porque ahí
                // está todo el contenido de la dedicatoria.
                try {{ window.parent.print(); }} catch (e) {{ window.print(); }}
            }});
        }}
    </script>
    """
)
components.html(barra_superior_html, height=56)

# Como la barra ahora vive en un iframe fijo, dejamos un espacio equivalente
# arriba del contenido para que no quede tapado.
st.markdown(html("<div style='height:16px;'></div>"), unsafe_allow_html=True)
 
# --------------------------------------------------------------------------
# ENCABEZADO / RETRATO
# (la foto se embebe como <img> dentro del MISMO bloque que el marco dorado,
#  para que el borde realmente la envuelva)
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

# --------------------------------------------------------------------------
# DEDICA UNAS PALABRAS: cada quien de la familia puede dejar su propio
# mensaje, que aparece como una cita destacada más, junto a las de arriba.
# --------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("💛 Dedica unas palabras")
st.caption("Escribe tu propio mensaje para el abuelo; aparecerá aquí mismo, junto a las demás dedicatorias.")

with st.form("agregar_dedicatoria", clear_on_submit=True):
    nombre_dedicante = st.text_input("Tu nombre (opcional):", value="")
    mensaje_dedicatoria = st.text_area("Tu dedicatoria:", value="", height=100)
    enviar_dedicatoria = st.form_submit_button("Agregar mi dedicatoria")
    if enviar_dedicatoria and mensaje_dedicatoria.strip():
        texto_final = mensaje_dedicatoria.strip()
        if nombre_dedicante.strip():
            texto_final += f" — {nombre_dedicante.strip()}"
        st.session_state.mensajes_dedicatoria.append(texto_final)
        st.success("¡Gracias! Tu dedicatoria fue agregada.")
        lluvia_corazones()

for mensaje in st.session_state.mensajes_dedicatoria:
    st.markdown(
        f'<p class="cita-destacada" style="margin-top:16px;">{mensaje}</p>',
        unsafe_allow_html=True,
    )

st.markdown('<p class="firma-familia">Con amor eterno, tu familia</p>', unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# --------------------------------------------------------------------------
# ABRAZO VIRTUAL (ahora con corazones en vez de globos)
# --------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("❤️ Enviar un Abrazo Virtual", use_container_width=True):
        lluvia_corazones()
 
st.markdown("---")
 
# --------------------------------------------------------------------------
# GALERÍA DE RECUERDOS FAMILIARES
# (las fotos se muestran como fondo translúcido; aquí solo se listan las notas)
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
