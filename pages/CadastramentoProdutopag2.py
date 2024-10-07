import streamlit as st
import bd_worker as bw
from PIL import Image
import EscolhaAgenciaFinal as EAR

#st.set_page_config(initial_sidebar_state="collapsed")

if 'selecaoAg' in st.session_state:
    st.session_state.selecaoAg = st.session_state.selecaoAg
if 'selecaoRede' in st.session_state:
    st.session_state.selecaoRede = st.session_state.selecaoRede
if 'selecaoEst' in st.session_state:
    st.session_state.selecaoEst = st.session_state.selecaoEst
if 'selecaoCid' in st.session_state:
    st.session_state.selecaoCid = st.session_state.selecaoCid
if 'selecaoEnd' in st.session_state:
    st.session_state.selecaoEnd = st.session_state.selecaoEnd
if 'precos_enviados' not in st.session_state:
    st.session_state.precos_enviados = False

def voltar():
    if st.button('Voltar'):
        st.session_state['selecaoAg'] = None
        st.session_state['selecaoRede'] = None
        st.session_state['selecaoEst'] = None
        st.session_state['selecaoCid'] = None
        st.session_state['selecaoEnd'] = None
        st.switch_page("Escolha_de_Agência_e_Rede.py")



st.write('O valor de selecaoEnd é:', st.session_state.get('selecaoEnd', 'Valor não definido'))

# CSS personalizado para estilização
with open("../styles.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Logo Cotton Baby.
logo_cotton = Image.open("../src/img/LogoCottonSemFundoSim.png")
st.image(logo_cotton, caption='', width=700, use_column_width=False)

st.markdown('<p class="subtitulo">Selecione o produto associado ao endereço.</p>', unsafe_allow_html=True)
opcoesPrd = bw.bd_produto()  # Consulta filtrada pela agência, rede, estado, cidade e endereço
exibPrd = EAR.placeholder + list(opcoesPrd.values())

selecaoPrd = st.selectbox('Escolha um produto:', exibPrd)

cod_produto = None

for chave, valor in opcoesPrd.items():
    if valor == selecaoPrd:
        cod_produto = chave
        break

# Se um produto for selecionado, carrega os concorrentes associados
if selecaoPrd != EAR.default:
    st.markdown('<p class="subtitulo">Selecione 2 concorrentes associados ao produto.</p>', unsafe_allow_html=True)
    opcoesConc = bw.bd_concorrentes(selecaoPrd)  # Consulta filtrada pela agência, rede, estado, cidade, endereço e produto.

    selecaoConc1 = st.selectbox('Selecione o concorrente 1:', ["----"] + list(opcoesConc.values()))
    selecaoConc2 = st.selectbox('Selecione o concorrente 2:', ["----"] + list(opcoesConc.values()))

    cod_concorrente1 = None
    cod_concorrente2 = None
    for chave, valor in opcoesConc.items():
        if valor == selecaoConc1:
            cod_concorrente1 = chave
        if valor == selecaoConc2:
            cod_concorrente2 = chave

        # Digite os preços dos produtos. Se concorrente selecionados.
    if selecaoConc1 != "----" and selecaoConc2 != "----" and selecaoConc1 != selecaoConc2:
            st.markdown('<p class="subtitulo">Preço Cottonbaby.</p>', unsafe_allow_html=True)
            precoCotton = st.number_input('Digite o preço do produto de Cottonbaby',key='Cotton', placeholder='0,00')
            st.markdown(f'<p class="subtitulo">Preço {selecaoConc1}.</p>', unsafe_allow_html=True)
            precoConc1 = st.number_input(f'Digite o preço do produto de {selecaoConc1}',key='conc1', placeholder='0,00')
            st.markdown(f'<p class="subtitulo">Preço {selecaoConc2}.</p>', unsafe_allow_html=True)
            precoConc2 = st.number_input(f'Digite o preço do produto de {selecaoConc2}',key='conc2', placeholder='0,00')

            # Se preços diferentes de 0.
            if precoCotton != 0 and precoConc1 != 0 and precoConc2 != 0:
                                    
                # Aviso!!!
                st.warning("Lembre-se de verificar se todos os dados estão preenchidos corretamente")

                
            if st.button('Enviar preços'):
                    
                    try:
                        precos = {
                            0 : precoCotton,
                            cod_concorrente1: precoConc1,
                            cod_concorrente2: precoConc2
                        }
                        empresas = {
                            0 : 'Cotton',
                            cod_concorrente1:selecaoConc1,
                            cod_concorrente2:selecaoConc2
                        }
                        bw.bd_insert_precos(
                                                    cod_loja=EAR.cod_loja,
                                                    loja_rede=EAR.selecaoRede,
                                                    loja_agencia=EAR.selecaoAg,
                                                    cod_produto=cod_produto,
                                                    uf=EAR.selecaoEst,
                                                    cidade=EAR.selecaoCid,
                                                    empresas=empresas,
                                                    produto_nome=selecaoPrd,
                                                    preco=precos
                                                    )
                    
                                        
                    except Exception as e:
                        pass

                    st.success('Preços registrados com sucesso.')
                    st.session_state.precos_enviados = True
                    
            if st.session_state.precos_enviados:
              
                if st.button('Próximo'):
                        
                        st.switch_page('pages/CadastramentoProdutopag.py')
                    
    
    else:
        st.warning("Os concorrentes não podem ser iguais!")

# Botão voltar
voltar()

