import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Função para carregar dados de um quadrimestre, corrigir nomes e formatar

def gerar_quadrimestre(caminho, q):
    quadrimestre = pd.read_csv(f'{str(caminho)}', sep=';', encoding='latin1')
    # Corrigindo nome da UBS que pode vir truncado
    quadrimestre.loc[4, 'Nome UBS'] = 'PROGRAMA SAUDE DA FAMILIA EQUIPE F POTIM'
    # Removendo coluna desnecessária
    quadrimestre.drop('Sigla', axis=1, inplace=True)
    # Adicionando coluna que identifica o quadrimestre
    quadrimestre['Quadrimestre'] = str(f'{q}')
    return quadrimestre

# Carregando os dados de cada quadrimestre de_2023
primeiro_quadrimestre = gerar_quadrimestre(
    '/content/drive/MyDrive/Aulas Python /Pandas/Indicadores de desempenho Potim/indicadores/2023/1Q_2023.csv',
    '1° Quadrimestre')

segundo_quadrimestre = gerar_quadrimestre(
    '/content/drive/MyDrive/Aulas Python /Pandas/Indicadores de desempenho Potim/indicadores/2023/2Q_2023.csv',
    '2° Quadrimestre')

terceiro_quadrimestre = gerar_quadrimestre(
    '/content/drive/MyDrive/Aulas Python /Pandas/Indicadores de desempenho Potim/indicadores/2023/3Q_2023.csv',
    '3° Quadrimestre')

# Agrupando os dados do ano inteiro
indicadores_2023 = pd.concat([primeiro_quadrimestre, segundo_quadrimestre, terceiro_quadrimestre], axis=0, join='outer')

# Função para gerar um gráfico horizontal por UBS para um quadrimestre

def gerar_grafico_por_quadrimestre(df):
    indicadores = df.columns[3:-1]
    lista_esf = sorted(df['Nome UBS'].unique())

    for esf in lista_esf:
        dados = df.loc[df['Nome UBS'] == esf, indicadores]
        valores = dados.values.flatten()

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(indicadores, valores)

        ax.set_title(f'Indicadores de Desempenho - 1° Quadrimestre\n{esf}', fontsize=16, loc='left')
        ax.set_xlim(0, 100)
        ax.set_xlabel('Percentual (%)')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 1,
                bar.get_y() + bar.get_height() / 2,
                f'{width:.1f}%',
                va='center', ha='left')

        plt.tight_layout()
        plt.show()

# Função para gerar gráficos comparativos por UBS ao longo dos quadrimestres do ano

def gerar_grafico_ano(df):
    indicadores = df.columns[3:-1]
    lista_esf = sorted(df['Nome UBS'].unique())
    quadrimestres = sorted(df['Quadrimestre'].unique())
    n_quadrimestres = len(quadrimestres)

    cores = ['#4B8BBE', '#306998', '#FFDD57', '#FFD43B', '#646464']

    for esf in lista_esf:
        dados = df[df['Nome UBS'] == esf]
        fig, ax = plt.subplots(figsize=(12, 7))
        x = np.arange(len(indicadores))
        largura = 0.15

        for i, quadrimestre in enumerate(quadrimestres):
            valores = dados[dados['Quadrimestre'] == quadrimestre][indicadores].values.flatten()
            posicoes = x + (i - n_quadrimestres / 2) * largura + largura / 2
            bars = ax.bar(posicoes, valores, width=largura, label=f'{quadrimestre}', color=cores[i % len(cores)])

            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 1,
                    f'{height:.1f}',
                    ha='center',
                    va='bottom'
                )

        ax.set_title(f'Indicadores de desempenho 2023\n{esf}', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylim(0, 100)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xticks(x)
        ax.set_xticklabels(indicadores, rotation=45, ha='right')
        ax.set_ylabel('Percentual (%)')
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.legend(title='Quadrimestre')
        plt.tight_layout()
        plt.show()
