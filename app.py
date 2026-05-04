import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(page_title="Volt Aries - Gráfica", page_icon="🎨")
st.title("🎨 Volt Aries: Herramienta de Sublimación")

st.write("Sube tu diseño y prepáralo para imprimir de una vez.")

archivo = st.file_uploader("Sube tu imagen (PNG o JPG)", type=["png", "jpg", "jpeg"])

if archivo:
    img = Image.open(archivo)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original")
        st.image(img, use_container_width=True)
        
    with col2:
        st.subheader("Modo Sublimación")
        # Aquí aplicamos el efecto espejo automáticamente
        img_espejo = ImageOps.mirror(img)
        st.image(img_espejo, caption="¡Lista para transfer!", use_container_width=True)

    st.sidebar.header("Ajustes Rápidos")
    if st.sidebar.button("Invertir Colores"):
        img = ImageOps.invert(img.convert("RGB"))
        st.image(img, caption="Colores Invertidos")
