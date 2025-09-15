# painel_futebol.py
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# ---------- CONFIGURAÇÃO DA API ----------
API_KEY = "c73ba88a5db4f998a232b1b9f8a1677a"  # Sua chave API
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

# ---------- FUNÇÕES ----------
def buscar_jogos(competicao, temporada):
    url = f"{BASE_URL}/fixtures?league={competicao}&season={temporada}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get("response", [])

def extrair_estatisticas(jogo):
    stats = {}
    stats["time_mandante"] = jogo["teams"]["home"]["name"]
    stats["time_visitante"] = jogo["teams"]["away"]["name"]
    stats["data"] = jogo["fixture"]["date"]
    # Estatísticas fictícias para demonstração
    stats["gols_mandante"] = 0
    stats["gols_visitante"] = 0
    stats["escanteios_mandante"] = 0
    stats["escanteios_visitante"] = 0
    stats["cartoes_mandante"] = 0
    stats["cartoes_visitante"] = 0
    stats["finalizacoes_mandante"] = 0
    stats["finalizacoes_visitante"] = 0
    stats["chutes_gol_mandante"] = 0
    stats["chutes_gol_visitante"] = 0
    return stats

def calcular_sugestoes(stats):
    # Sugestões fictícias para demonstração
    sugestoes = [
        f"{stats['time_mandante']} vence",
        "Mais de 2.5 gols",
        "Ambos marcam"
    ]
    return sugestoes

# ---------- INTERFACE ----------
st.title("Painel de Futebol - Prévia Interativa")

# Seleção de campeonato
campeonatos = {
    "Brasileirão": 10,  # ID fictício, substituir pela real API-Football
    "Premier League": 39
}

campeonato_selecionado = st.selectbox("Selecione o campeonato:", list(campeonatos.keys()))

# Seleção de temporada
temporada = st.selectbox("Selecione a temporada:", [2023, 2024])

# Buscar jogos
jogos = buscar_jogos(campeonatos[campeonato_selecionado], temporada)

st.subheader(f"Jogos de {campeonato_selecionado} - Temporada {temporada}")

for jogo in jogos[:5]:  # Mostrando só os primeiros 5 jogos como prévia
    stats = extrair_estatisticas(jogo)
    sugestoes = calcular_sugestoes(stats)
    
    # Alternância Tabela ↔ Gráfico
    modo = st.radio(f"Modo de visualização - {stats['time_mandante']} x {stats['time_visitante']}", ["Tabela", "Gráfico"])
    
    if modo == "Tabela":
        tabela = pd.DataFrame({
            "Estatística": ["Gols", "Escanteios", "Cartões", "Finalizações", "Chutes no Gol"],
            stats["time_mandante"]: [stats["gols_mandante"], stats["escanteios_mandante"], stats["cartoes_mandante"], stats["finalizacoes_mandante"], stats["chutes_gol_mandante"]],
            stats["time_visitante"]: [stats["gols_visitante"], stats["escanteios_visitante"], stats["cartoes_visitante"], stats["finalizacoes_visitante"], stats["chutes_gol_visitante"]],
        })
        st.table(tabela)
    
    else:
        categorias = ["Gols", "Escanteios", "Cartões", "Finalizações", "Chutes no Gol"]
        valores_mandante = [stats["gols_mandante"], stats["escanteios_mandante"], stats["cartoes_mandante"], stats["finalizacoes_mandante"], stats["chutes_gol_mandante"]]
        valores_visitante = [stats["gols_visitante"], stats["escanteios_visitante"], stats["cartoes_visitante"], stats["finalizacoes_visitante"], stats["chutes_gol_visitante"]]
        
        x = range(len(categorias))
        plt.barh([i-0.2 for i in x], valores_mandante, height=0.4, label=stats["time_mandante"])
        plt.barh([i+0.2 for i in x], valores_visitante, height=0.4, label=stats["time_visitante"])
        plt.yticks(x, categorias)
        plt.legend()
        st.pyplot(plt)
        plt.clf()
    
    # Campo com 3 sugestões mais prováveis
    st.markdown("*3 Sugestões mais prováveis:*")
    for s in sugestoes:
        st.write(f"- {s}")