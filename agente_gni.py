import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# 1. Configuración de la página (Diseño ancho y metadatos)
st.set_page_config(
    page_title="GNI@ - Asistente de Operaciones",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Barra lateral corporativa (Branding y Call to Action)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=70) # Icono representativo
    st.title("GENIUS NETWORK")
    st.subheader("Intelligence")
    st.markdown("---")
    st.markdown("**Especialistas en:**")
    st.markdown("- Automatización de CRM")
    st.markdown("- Integración de Inteligencia Artificial")
    st.markdown("- Refinamiento de Datos y Procesos")
    st.markdown("---")
    # Botón directo al formulario de Google que ya creaste
    st.link_button("📋 Rellenar formulario de diagnóstico", "https://forms.gle/ohf5SKJarXWa8HEP7", use_container_width=True)
    st.markdown("---")
    st.caption("© 2026 GENIUS NETWORK INTELLIGENCE. Todos los derechos reservados.")

# 3. Interfaz Principal del Chat
st.title("GNI@ - Asistente de Operaciones")
st.write("Hola, soy el agente inteligente de GENIUS NETWORK INTELLIGENCE. ¿En qué proceso operativo o reto de CRM te puedo ayudar hoy?")

# Inicializar el historial de mensajes en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de la conversación al recargar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Entrada de texto moderna para el Chat
if prompt_usuario := st.chat_input("Describe el reto de tu empresa..."):
    
    # Guardar y mostrar el mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    # Definir el comportamiento del Agente
    plantilla_gni = """
    Eres un consultor senior experto en CRM y automatización de procesos para la empresa GENIUS NETWORK INTELLIGENCE.
    Tu objetivo es entender el problema del usuario de forma amable y profesional, y sugerir que completen el formulario de diagnóstico o agenden una sesión.
    Responde de manera concisa y con un tono tecnológico y ejecutivo.
    Usuario: {pregunta_usuario}
    """
    prompt = PromptTemplate(input_variables=["pregunta_usuario"], template=plantilla_gni)

    # Inicializar el Modelo con la clave segura de Streamlit
    mi_api_key = st.secrets["GOOGLE_API_KEY"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=mi_api_key
    )

    # Procesar la respuesta con LangChain
    prompt_final = prompt.format(pregunta_usuario=prompt_usuario)
    respuesta = llm.invoke(prompt_final)

    # Limpiar y extraer el texto de la respuesta de forma segura
    texto_respuesta = ""
    if isinstance(respuesta.content, list):
        for bloque in respuesta.content:
            if isinstance(bloque, dict) and 'text' in bloque:
                texto_respuesta += bloque['text']
    else:
        texto_respuesta = str(respuesta.content)

    # Guardar y mostrar la respuesta del asistente
    st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
    with st.chat_message("assistant"):
        st.markdown(texto_respuesta)
