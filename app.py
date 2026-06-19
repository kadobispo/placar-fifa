import streamlit as st
import pandas as pd
import os
import base64
import altair as alt
import gspread # Biblioteca para o Google Planilhas
from datetime import date

# ==========================================
# 1. CONFIGURAÇÃO INICIAL E CONEXÃO GOOGLE
# ==========================================
st.set_page_config(page_title="Placar FIFA", page_icon="🎮", layout="centered")

# ⚠️ ATENÇÃO: Substitua o link abaixo pelo LINK DE EDIÇÃO da sua planilha do Google!
# Certifique-se de que nas configurações de compartilhamento da planilha está como "Qualquer pessoa com o link pode editar"
URL_DA_PLANILHA = "https://docs.google.com/spreadsheets/d/18xnRj6LmMJlik7zRqBuIiG0GHwWFF6x1ecL75LQEsUk/edit"

# Função para conectar ao Google Sheets usando o link público de edição
@st.cache_data(ttl=5) # Atualiza os dados a cada 5 segundos
def load_data_from_google():
    try:
        # CONEXÃO PÚBLICA (Sem necessidade de arquivos JSON complexos)
        url_csv = URL_DA_PLANILHA.replace("/edit", "/export?format=csv")
        df_sheets = pd.read_csv(url_csv)
        df_sheets["Data"] = df_sheets["Data"].astype(str)
        return df_sheets
    except:
        return pd.DataFrame(columns=["Data", "Ricardo", "Dinho", "Vencedor"])

df = load_data_from_google()

# Função para converter a imagem em formato Base64
def obter_base64_da_imagem(caminho_da_imagem):
    try:
        with open(caminho_da_imagem, "rb") as f:
            dados = f.read()
        return base64.b64encode(dados).decode()
    except:
        return None

# Aplica a imagem do campo de futebol no fundo
img_base64_fundo = obter_base64_da_imagem("campo_futebol.jpg")
if img_base64_fundo:
    st.markdown(
        f"""
        <style>
        /* Fundo do campo de futebol */
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), url("data:image/jpeg;base64,{img_base64_fundo}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        h1, h2, h3, h4, p, label, .stMarkdown {{
            color: #ffffff !important;
        }}
        
        /* Centraliza a caixa de números (os botões de - e +) no meio da tela */
        div[data-testid="stNumberInput"] {{
            max-width: 250px; /* Impede que a caixa fique gigante de uma ponta a outra */
            margin: 0 auto !important; /* Centraliza perfeitamente */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Função para desenhar os avatares centralizados
def renderizar_avatar(caminho_imagem, emoji, nome):
    img_b64 = obter_base64_da_imagem(caminho_imagem)
    if img_b64:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                <img src="data:image/png;base64,{img_b64}" style="width: 90px; height: 90px; border-radius: 50%; border: 3px solid white; object-fit: cover; box-shadow: 0 4px 8px rgba(0,0,0,0.5); margin-bottom: 8px;">
                <h4 style="margin: 0 0 10px 0; text-align: center; color: white; font-size: 1.2rem;">{nome}</h4>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                <div style="font-size: 60px; line-height: 1.2;">{emoji}</div>
                <h4 style="margin: 0 0 10px 0; text-align: center; color: white; font-size: 1.2rem;">{nome}</h4>
            </div>
            """, unsafe_allow_html=True
        )

# ==========================================
# 2. CABEÇALHO DA APLICAÇÃO
# ==========================================
st.markdown("<h1 style='text-align: center;'>🎮 Confronto FIFA 🎮</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #b0b0b0;'>Ricardo vs Dinho</h3>", unsafe_allow_html=True)
st.divider()

aba1, aba2 = st.tabs(["📝 Registrar Placar", "📊 Resultados do Mês"])

# ==========================================
# 3. ABA 1: REGISTRAR / CONSULTAR PLACAR
# ==========================================
with aba1:
    st.subheader("Como foi o jogo hoje?")
    
    hoje = st.date_input("Data do jogo", date.today(), format="DD/MM/YYYY")
    data_selecionada_str = hoje.strftime("%d/%m/%Y")
    
    jogo_existente = df[df["Data"] == data_selecionada_str]
    
    val_ricardo = 0
    val_dinho = 0
    ja_existe_jogo = False
    
    if not jogo_existente.empty:
        val_ricardo = int(jogo_existente.iloc[0]["Ricardo"])
        val_dinho = int(jogo_existente.iloc[0]["Dinho"])
        st.info(f"ℹ️ Já existe um jogo registrado nesta data! Placar: **Ricardo {val_ricardo} x {val_dinho} Dinho**")
        ja_existe_jogo = True
    
    # Colunas (vão empilhar automaticamente no celular para ficar perfeito)
    col1, col2 = st.columns(2)
    
    # --- Lado do Ricardo ---
    with col1:
        renderizar_avatar("foto_ricardo.png", "👨🏻", "Ricardo")
        vit_ricardo = st.number_input("Ricardo", min_value=0, step=1, value=val_ricardo, key="input_ricardo", label_visibility="collapsed")
        
        # Espaço extra no celular para não ficar colado no jogador de baixo
        st.markdown("<br>", unsafe_allow_html=True) 
        
    # --- Lado do Dinho ---
    with col2:
        renderizar_avatar("foto_dinho.png", "👴🏼", "Dinho")
        vit_dinho = st.number_input("Dinho", min_value=0, step=1, value=val_dinho, key="input_dinho", label_visibility="collapsed")

    st.write("") 
    st.write("") 
    
    texto_botao = "🔄 Atualizar Resultado do Dia" if ja_existe_jogo else "💾 Gravar Resultado de Hoje"
    
    if st.button(texto_botao, use_container_width=True, type="primary"):
        if vit_ricardo > vit_dinho:
            vencedor = "Ricardo"
            st.balloons() 
        elif vit_dinho > vit_ricardo:
            vencedor = "Dinho"
            st.balloons() 
        else:
            vencedor = "Empate"
            
        # GRAVAÇÃO DIRETA NO GOOGLE PLANILHAS
        try:
            gc = gspread.public_link_client()
            sh = gc.open_by_url(URL_DA_PLANILHA)
            worksheet = sh.get_worksheet(0)
            
            if ja_existe_jogo:
                # Se já existe, localiza a linha e atualiza
                celula = worksheet.find(data_selecionada_str)
                linha = celula.row
                worksheet.update_cell(linha, 2, vit_ricardo)
                worksheet.update_cell(linha, 3, vit_dinho)
                worksheet.update_cell(linha, 4, vencedor)
            else:
                # Se é novo, adiciona uma linha no final
                worksheet.append_row([data_selecionada_str, vit_ricardo, vit_dinho, vencedor])
                
            st.success(f"Feito! Gravado no Google Planilhas. Vencedor: **{vencedor}** 🏆")
            st.cache_data.clear() # Força o app a reler a planilha atualizada
            
        except Exception as e:
            st.error("Erro ao conectar ao Google Planilhas. Verifique se configurou para 'Qualquer pessoa com o link pode editar'.")

# ==========================================
# 4. ABA 2: VER QUEM ESTÁ GANHANDO NO MÊS
# ==========================================
with aba2:
    if not df.empty:
        st.subheader("Quem manda no videogame?")
        
        vitorias_dias = df[df["Vencedor"] != "Empate"]["Vencedor"].value_counts()
        ricardo_dias = vitorias_dias.get("Ricardo", 0)
        dinho_dias = vitorias_dias.get("Dinho", 0)
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric(label="🏆 Dias Ganhos - Ricardo", value=ricardo_dias)
        col_res2.metric(label="🏆 Dias Ganhos - Dinho", value=dinho_dias)
        
        st.divider()
        st.write("**Gráfico de Domínio:**")
        
        df_grafico = pd.DataFrame({
            "Jogador": ["Ricardo", "Dinho"],
            "Vitórias": [ricardo_dias, dinho_dias]
        })
        
        grafico = alt.Chart(df_grafico).mark_bar(
            color='#1E90FF', 
            size=60,         
            cornerRadiusTopLeft=8,  
            cornerRadiusTopRight=8
        ).encode(
            x=alt.X('Jogador', axis=alt.Axis(labelColor='white', titleColor='white', labelAngle=0, labelFontSize=14)),
            y=alt.Y('Vitórias', axis=alt.Axis(labelColor='white', titleColor='white', tickMinStep=1, labelFontSize=14))
        ).properties(
            background='transparent' 
        ).configure_view(
            strokeWidth=0 
        )
        
        st.altair_chart(grafico, use_container_width=True)
        
        with st.expander("Ver histórico completo das partidas"):
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    else:
        st.info("Ainda não há nada aqui. Liguem o videogame!")
