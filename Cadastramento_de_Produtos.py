import streamlit as st
import bd_worker as bw
from PIL import Image

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

def botao(selecaoConc, selecaoPrd, preco):
    if st.button('Submit'):  # Aqui deve estar o botão final de envio
        # Validação: Verifica se algo foi selecionado antes de enviar
        if preco is not None:
            st.success(f'Você definiu o produto ( {selecaoPrd} ) da marca ( {selecaoConc} ) com o preço: ( {preco} )')
        else:
            st.error('Por favor, insira todas as opções corretamente.')

# Caixa de seleção da agência
selecaoAg = st.selectbox(
    'Escolha uma agência:', 
    exibAg
)

# Se uma agência for selecionada, carrega as redes associadas
if selecaoAg != default:
    st.markdown('<p class="subtitulo">Selecione a rede associada à agência.</p>', unsafe_allow_html=True)
    opcoesRede = bw.bd_pesquisa_rede(selecaoAg)  # Consulta filtrada pela agência
    exibRede = placeholder + opcoesRede
    selecaoRede = st.selectbox('Escolha uma rede:', exibRede)

    # Se uma rede for selecionada, carrega os estados associados
    if selecaoRede != default:
        st.markdown('<p class="subtitulo">Selecione o estado associado à rede.</p>', unsafe_allow_html=True)
        opcoesEst = bw.bd_pesquisa_uf(selecaoAg, selecaoRede)  # Consulta filtrada pela agência e rede
        exibEst = placeholder + opcoesEst
        selecaoEst = st.selectbox('Escolha um estado:', exibEst)

        # Se um estado for selecionado, carrega as cidades associadas
        if selecaoEst != default:
            st.markdown('<p class="subtitulo">Selecione a cidade associada ao estado.</p>', unsafe_allow_html=True)
            opcoesCid = bw.bd_pesquisa_cidade(selecaoAg, selecaoRede, selecaoEst)  # Consulta filtrada pela agência, rede e estado
            exibCid = placeholder + opcoesCid
            selecaoCid = st.selectbox('Escolha uma cidade:', exibCid)

            # Se uma cidade for selecionada, carrega os endereços associados
            if selecaoCid != default:
                st.markdown('<p class="subtitulo">Selecione o endereço associado à cidade.</p>', unsafe_allow_html=True)
                opcoesEnd = bw.bd_pesquisa_endereco(selecaoAg, selecaoRede, selecaoEst, selecaoCid)  # Consulta filtrada pela agência, rede, estado e cidade
                exibEnd = opcoesEnd.values()

                selecaoEnd = st.selectbox('Escolha um endereço:', exibEnd)
                cod_loja = None

                for chave, valor in opcoesEnd.items():
                    if valor == selecaoEnd:
                        cod_loja = chave
                        break

                # Se um endereço for selecionado, carrega os produtos associados
                if selecaoEnd != default:
                    st.markdown('<p class="subtitulo">Selecione o produto associado ao endereço.</p>', unsafe_allow_html=True)
                    opcoesPrd = bw.bd_produto()  # Consulta filtrada pela agência, rede, estado, cidade e endereço
                    exibPrd = placeholder + list(opcoesPrd.values())

                    selecaoPrd = st.selectbox('Escolha um produto:', exibPrd)

                    cod_produto = None

                    for chave, valor in opcoesPrd.items():
                        if valor == selecaoPrd:
                            cod_produto = chave
                            break

                    # Se um produto for selecionado, carrega os concorrentes associados
                    if selecaoPrd != default:
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
                        if selecaoConc1 != "----" and selecaoConc2 != "----":
                            st.markdown('<p class="subtitulo">Preço Cotton Baby.</p>', unsafe_allow_html=True)
                            precoCotton = st.number_input('Digite o preço do produto de Cotton Baby',key='cotton', placeholder='0,00')
                            st.markdown(f'<p class="subtitulo">Preço {selecaoConc1}.</p>', unsafe_allow_html=True)
                            precoConc1 = st.number_input(f'Digite o preço do produto de {selecaoConc1}',key='conc1', placeholder='0,00')
                            st.markdown(f'<p class="subtitulo">Preço {selecaoConc2}.</p>', unsafe_allow_html=True)
                            precoConc2 = st.number_input(f'Digite o preço do produto de {selecaoConc2}',key='conc2', placeholder='0,00')

                            # Se preços diferentes de 0.
                            if precoCotton != 0 and precoConc1 != 0 and precoConc2 != 0:
                                    
                                # Aviso!!!
                                st.warning("Lembre-se de verificar se todos os dados estão preenchidos corretamente")

                                # Botão voltar
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
                                                                    cod_loja=cod_loja,
                                                                    loja_rede=selecaoRede,
                                                                    loja_agencia=selecaoAg,
                                                                    cod_produto=cod_produto,
                                                                    uf=selecaoEst,
                                                                    cidade=selecaoCid,
                                                                    empresas=empresas,
                                                                    produto_nome=selecaoPrd,
                                                                    preco=precos
                                                                   )
                                        st.success('Preços registrados com sucesso.')
                                    except Exception as e:
                                        pass


#Dicionarios
#cod_produto
#loja_cod