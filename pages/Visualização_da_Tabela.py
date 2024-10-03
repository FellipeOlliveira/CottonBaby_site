import streamlit as st
import bd_worker as bw
from PIL import Image

# Logo Cotton Baby.
logo_cotton = Image.open("./src/img/LogoCottonSemFundoSim.png")
st.image(logo_cotton, caption='', width=700, use_column_width=False)

if st.button('Exportar Excel'):
    st.write(bw.exportar_excel())
    