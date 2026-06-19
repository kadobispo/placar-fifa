import streamlit as st
import pandas as pd
import os
import base64
import altair as alt
from datetime import date
from PIL import Image, ImageOps

# ==========================================
# 1. CONFIGURAÇÃO INICIAL E ESTILOS (CSS)
# ==========================================
st.set_page_config(page_title="Placar FIFA", page_icon="🎮", layout="centered")

DATA_FILE = "historico_fifa.csv"

def obter_base64_da_imagem(caminho_da_imagem):
    with open(caminho_da_imagem, "rb") as f:
        dados = f.read()
    return base64.b64encode(dados).decode()

# Aplica a imagem do campo de futebol no fundo e corrige as fotos e o celular
if os.path.exists("campo_futebol.jpg"):
    img_base64 = obter_base64_da_imagem("campo_futebol.jpg")
    st.markdown(
        f"""
        <style>
        /* Fundo do campo de futebol */
        [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), url("data:image/jpeg;base64,{img_base64}");
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
           MÁGICA PARA AS FOTOS (Deixa redonda e centralizada)
           ========================================== */
        div[data-testid="stImage"] {{
            display: flex;
            justify-content: center;
        }}
        div[data-testid="stImage"] img {{
            max-width: 140px !important; /* Tamanho perfeito para a tela */
            border-radius: 50% !important; /* Deixa a foto perfeitamente redonda */
            border: 3px solid #ffffff; /* Borda branca para destacar no fundo escuro */
            box-shadow: 0 4px 8px rgba(0,0,0,0.5); /* Sombra para dar profundidade */
        }}

        /* ==========================================
           MÁGICA PARA O CELULAR (Impede de estourar)
           ========================================== */
        @media (max-width: 768px) {{
            div[data-testid="stHorizontalBlock"] {{
                flex-direction: row !important;
                flex-wrap: nowrap !important;
            }}
            div[data-testid="column"] {{
                width: 50% !important;
                flex: 1 1 50% !important;
                min-width: 50% !important;
                padding: 0 5px !important;
            }}
            h3 {{
                font-size: 1.1rem !important;
            }}
            /* No celular, a foto fica um pouquinho menor para caber perfeito */
            div[data-testid="stImage"] img {{
                max-width: 100px !important; 
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def load_data():
    if os.path.exists(DATA_FILE):
        df_carregado = pd.read_csv(DATA_FILE)
        df_carregado["Data"] = df_carregado["Data"].astype(str)
        return df_carregado
    else:
        return pd.DataFrame(columns=["Data", "Ricardo", "Dinho", "Vencedor"])

df = load_data()

def obter_foto_padronizada(caminho):
    try:
        img = Image.open(caminho)
        img_redimensionada = ImageOps.fit(img, (300, 300), Image.Resampling.LANCZOS)
        return img_redimensionada
    except:
        return None

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
        vencedor_salvo = jogo_existente.iloc[0]["Vencedor"]
        st.info(f"ℹ️ Já existe um jogo registrado nesta data! Placar: **Ricardo {val_ricardo} x {val_dinho} Dinho** (Vencedor: {vencedor_salvo})")
        ja_existe_jogo = True
    
    col1, col2 = st.columns(2)
    
    # --- Lado do Ricardo ---
    with col1:
        # Repare que retiramos as subcolunas, o CSS agora centraliza sozinho!
        foto_ricardo = obter_foto_padronizada("foto_ricardo.png")
        if foto_ricardo:
            st.image(foto_ricardo, use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center;'>👨🏻</h1>", unsafe_allow_html=True)
                
        st.markdown("<h3 style='text-align: center;'>Ricardo</h3>", unsafe_allow_html=True)
        vit_ricardo = st.number_input("Suas Vitórias", min_value=0, step=1, value=val_ricardo, key="input_ricardo")
        
    # --- Lado do Dinho ---
    with col2:
        foto_dinho = obter_foto_padronizada("foto_dinho.png")
        if foto_dinho:
            st.image(foto_dinho, use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center;'>👴🏼</h1>", unsafe_allow_html=True)
                
        st.markdown("<h3 style='text-align: center;'>Dinho</h3>", unsafe_allow_html=True)
        vit_dinho = st.number_input("Vitórias dele", min_value=0, step=1, value=val_dinho, key="input_dinho")

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
        st.success(f"Feito! Placar gravado com sucesso. Vencedor: **{vencedor}** 🏆")

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
