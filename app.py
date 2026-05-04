import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
from rembg import remove
import io

# Configuración de página
st.set_page_config(page_title="Volt Aries PRO", page_icon="⚡", layout="wide")

# Título con estilo (Luego pondremos tu logo aquí)
st.title("⚡ VOLT ARIES | Control de Ingeniería Gráfica")
st.markdown("---")

# --- BARRA LATERAL: AJUSTES DE PRE-PRENSA ---
st.sidebar.header("🎨 Ajustes de Color y Niveles")
brillo = st.sidebar.slider("Brillo (Exposición)", 0.0, 2.0, 1.0)
contraste = st.sidebar.slider("Contraste", 0.0, 2.0, 1.0)
saturacion = st.sidebar.slider("Saturación", 0.0, 2.0, 1.0)
nitidez = st.sidebar.slider("Nitidez (Sharpen)", 1.0, 5.0, 1.0)

st.sidebar.header("📐 Configuración de Impresión")
espacio_color = st.sidebar.radio("Perfil de Color:", ["RGB (Digital/Sublimación)", "CMYK (Prensa/Láser)"])
dpi_valor = st.sidebar.number_input("Resolución (DPI):", value=300)
modo_impresion = st.sidebar.selectbox("Lógica de Salida:", ["Directo (Canon/Láser)", "Espejo (Epson/Sublimación)"])

# --- ÁREA DE TRABAJO ---
archivo = st.file_uploader("Arrastra el archivo para procesar (PNG, JPG)", type=["png", "jpg", "jpeg"])

if archivo:
    # Cargar imagen original
    img_original = Image.open(archivo)
    
    # Procesar ajustes
    img_proc = ImageEnhance.Brightness(img_original).enhance(brillo)
    img_proc = ImageEnhance.Contrast(img_proc).enhance(contraste)
    img_proc = ImageEnhance.Color(img_proc).enhance(saturacion)
    img_proc = ImageEnhance.Sharpness(img_proc).enhance(nitidez)

    # Columnas para comparar
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Entrada (Original)")
        st.image(img_original, use_container_width=True)
        
    with col2:
        st.subheader("Salida Técnica")
        
        # Aplicar Espejo si es necesario
        img_final = ImageOps.mirror(img_proc) if "Espejo" in modo_impresion else img_proc
        st.image(img_final, use_container_width=True)

        # Botón para Remover Fondo (Solo si se solicita)
        if st.button("🚀 REMOVER FONDO (Alpha Channel)"):
            with st.spinner("Limpiando..."):
                img_final = remove(img_final)
                st.image(img_final, caption="Fondo Eliminado")

        # --- EXPORTACIÓN ---
        st.markdown("### Generar Archivo de Imprenta")
        buf = io.BytesIO()
        
        # Lógica de conversión de perfil
        if espacio_color == "CMYK (Prensa/Láser)":
            export_img = img_final.convert("CMYK")
        else:
            export_img = img_final.convert("RGB")
            
        # Guardar como PDF con DPI específico
        export_img.save(buf, format="PDF", resolution=float(dpi_valor))
        
        st.download_button(
            label=f"📥 DESCARGAR PDF ({espacio_color} @ {dpi_valor} DPI)",
            data=buf.getvalue(),
            file_name="volt_aries_listo.pdf",
            mime="application/pdf"
        )
