import streamlit as st
import bd_worker as bw
from PIL import Image

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

# CSS personalizado para estilização
with open("styles.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Logo Cotton Baby.
logo_cotton = Image.open("./src/img/LogoCottonSemFundoSim.png")
st.image(logo_cotton, caption='', width=700, use_column_width=False)

# Título principal com estilo
st.markdown('<p class="titulo">Qual sua agência?</p>', unsafe_allow_html=True)

# Lista de opções padrão
default = "----"
placeholder = [default]
opcoesAg = bw.bd_lista_agencia()  # Função que lista todas as agências
exibAg = placeholder + opcoesAg

def botao():
    if st.button('Submit'):  # Aqui deve estar o botão final de envio
        # Validação: Verifica se algo foi selecionado antes de enviar
        if selecaoAg and selecaoRede and selecaoEst and selecaoCid is not None:
            st.success(f'Sucesso')

        else:
            st.error('Por favor, insira todas as opções corretamente.')

# Caixa de seleção da agência
selecaoAg = st.selectbox(
    'Escolha uma agência:', 
    exibAg,key='selecaoAg'
)

# Se uma agência for selecionada, carrega as redes associadas
if selecaoAg != default:
    st.markdown('<p class="subtitulo">Selecione a rede associada à agência.</p>', unsafe_allow_html=True)
    opcoesRede = bw.bd_pesquisa_rede(selecaoAg)  # Consulta filtrada pela agência
    exibRede = placeholder + opcoesRede
    selecaoRede = st.selectbox('Escolha uma rede:', exibRede,key='selecaoRede')

    # Se uma rede for selecionada, carrega os estados associados
    if selecaoRede != default:
        st.markdown('<p class="subtitulo">Selecione o estado associado à rede.</p>', unsafe_allow_html=True)
        opcoesEst = bw.bd_pesquisa_uf(selecaoAg, selecaoRede)  # Consulta filtrada pela agência e rede
        exibEst = placeholder + opcoesEst
        selecaoEst = st.selectbox('Escolha um estado:', exibEst,key='selecaoEst')

        # Se um estado for selecionado, carrega as cidades associadas
        if selecaoEst != default:
            st.markdown('<p class="subtitulo">Selecione a cidade associada ao estado.</p>', unsafe_allow_html=True)
            opcoesCid = bw.bd_pesquisa_cidade(selecaoAg, selecaoRede, selecaoEst)  # Consulta filtrada pela agência, rede e estado
            exibCid = placeholder + opcoesCid
            selecaoCid = st.selectbox('Escolha uma cidade:', exibCid,key='selecaoCid')

            # Se uma cidade for selecionada, carrega os endereços associados
            if selecaoCid != default:
                st.markdown('<p class="subtitulo">Selecione o endereço associado à cidade.</p>', unsafe_allow_html=True)
                opcoesEnd = bw.bd_pesquisa_endereco(selecaoAg, selecaoRede, selecaoEst, selecaoCid)  # Consulta filtrada pela agência, rede, estado e cidade
                exibEnd = opcoesEnd.values()

                selecaoEnd = st.selectbox('Escolha um endereço:',exibEnd,key='selecaoEnd')
                cod_loja = None

                for chave, valor in opcoesEnd.items():
                    if valor == selecaoEnd:
                        cod_loja = chave
                        break

                page_2 = st.button("Ir para pesquisa de preço")
                if page_2:
                    st.switch_page("pages/CadastramentoProdutopag.py")


#Dicionarios
#cod_produto
#loja_cod