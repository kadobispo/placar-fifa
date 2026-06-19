import streamlit as st
import pandas as pd
import os
import base64
import altair as alt
from datetime import date

# ==========================================
# 1. CONFIGURAÇÃO INICIAL E ESTILOS (CSS)
# ==========================================
st.set_page_config(page_title="Placar FIFA", page_icon="🎮", layout="centered")

DATA_FILE = "historico_fifa.csv"

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
        h1, h2, h3, p, label, .stMarkdown {{
            color: #ffffff !important;
        }}
        
        /* ==========================================
           A OPÇÃO NUCLEAR PARA O TELEMÓVEL (CSS com Especificidade Máxima)
           ========================================== */
        html body div[data-testid="stHorizontalBlock"] {{
            display: flex !important;
            flex-direction: row !important; /* FORÇA LADO A LADO */
            flex-wrap: nowrap !important;   /* PROÍBE EMPILHAR */
            gap: 15px !important;           /* ESPAÇO NO MEIO */
            padding: 0 5px !important;
        }}
        
        html body div[data-testid="column"] {{
            width: 50% !important;          /* 50% EXATO PARA CADA UM */
            flex: 1 1 50% !important;
            min-width: 0 !important;        /* PERMITE ENCOLHER */
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }}
        
        /* Força a caixa de números a caber nos 50% */
        html body div[data-testid="stNumberInput"] {{
            min-width: 0 !important;
            width: 100% !important;
        }}
        
        /* Ajuste fino dos botões de - e + para não ficarem escondidos */
        html body div[data-baseweb="input"] {{
            font-size: 14px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Função para desenhar os avatares (tamanho ajustado para caber perfeito no telemóvel)
def renderizar_avatar(caminho_imagem, emoji, nome):
    img_b64 = obter_base64_da_imagem(caminho_imagem)
    if img_b64:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                <img src="data:image/png;base64,{img_b64}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid white; object-fit: cover; box-shadow: 0 4px 8px rgba(0,0,0,0.5); margin-bottom: 8px;">
                <h4 style="margin: 0 0 10px 0; text-align: center; color: white; font-size: 1.1rem;">{nome}</h4>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                <div style="font-size: 60px; line-height: 1.2;">{emoji}</div>
                <h4 style="margin: 0 0 10px 0; text-align: center; color: white; font-size: 1.1rem;">{nome}</h4>
            </div>
            """, unsafe_allow_html=True
        )

# Função para carregar a base de dados
def load_data():
    if os.path.exists(DATA_FILE):
        df_carregado = pd.read_csv(DATA_FILE)
        df_carregado["Data"] = df_carregado["Data"].astype(str)
        return df_carregado
    else:
        return pd.DataFrame(columns=["Data", "Ricardo", "Dinho", "Vencedor"])

df = load_data()

# ==========================================
# 2. CABEÇALHO DA APLICAÇÃO
# ==========================================
st.markdown("<h1 style='text-align: center;'>🎮 Confronto FIFA 🎮</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #b0b0b0;'>Ricardo vs Dinho</h3>", unsafe_allow_html=True)
st.divider()

aba1, aba2 = st.tabs(["📝 Registar Placar", "📊 Resultados do Mês"])

# ==========================================
# 3. ABA 1: REGISTAR / CONSULTAR PLACAR
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
        vencedor_salvo = jogo_existente.iloc[0]["Vencedor"]
        st.info(f"ℹ️ Já existe um jogo registado nesta data! Placar: **Ricardo {val_ricardo} x {val_dinho} Dinho**")
        ja_existe_jogo = True
    
    # Colunas
    col1, col2 = st.columns(2)
    
    # --- Lado do Ricardo ---
    with col1:
        renderizar_avatar("foto_ricardo.png", "👨🏻", "Ricardo")
        vit_ricardo = st.number_input("Ricardo", min_value=0, step=1, value=val_ricardo, key="input_ricardo", label_visibility="collapsed")
        
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
            
        novo_dado = pd.DataFrame({
            "Data": [data_selecionada_str],
            "Ricardo": [vit_ricardo],
            "Dinho": [vit_dinho],
            "Vencedor": [vencedor]
        })
        
        if ja_existe_jogo:
            df = df[df["Data"] != data_selecionada_str]
            
        df = pd.concat([df, novo_dado], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Feito! Placar guardado com sucesso. Vencedor: **{vencedor}** 🏆")

# ==========================================
# 4. ABA 2: VER QUEM ESTÁ A GANHAR NO MÊS
# ==========================================
with aba2:
    if not df.empty:
        st.subheader("Quem manda na consola?")
        
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
        st.info("Ainda não há nada aqui. Liguem a consola!")
