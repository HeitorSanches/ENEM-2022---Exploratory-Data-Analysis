#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


# In[2]:


file_path = "ITENS_PROVA_2022.csv"

# Tente abrir o arquivo especificando uma codificação diferente
try:
    itensprova = pd.read_csv(file_path, encoding='latin1' , sep = ";")
except UnicodeDecodeError:
    try:
        itensprova = pd.read_csv(file_path, encoding='iso-8859-1', sep = ";")
    except UnicodeDecodeError:
        itensprova = pd.read_csv(file_path, encoding='cp1252', sep = ";")


# In[3]:


file_path = "MICRODADOS_ENEM_2022.csv"

# Tente abrir o arquivo especificando uma codificação diferente
try:
    microdados = pd.read_csv(file_path, encoding='latin1' , sep = ";")
except UnicodeDecodeError:
    try:
        microdados = pd.read_csv(file_path, encoding='iso-8859-1', sep = ";")
    except UnicodeDecodeError:
        microdados = pd.read_csv(file_path, encoding='cp1252', sep = ";")


# In[4]:


microdados.head()


# In[5]:


microdados.describe()


# In[6]:


# Tipo faixa etária:
# 1	Menor de 17 anos
# 2	17 anos
# 3	18 anos
# 4	19 anos
# 5	20 anos
# 6	21 anos
# 7	22 anos
# 8	23 anos
# 9	24 anos
# 10	25 anos
# 11	Entre 26 e 30 anos
# 12	Entre 31 e 35 anos
# 13	Entre 36 e 40 anos
# 14	Entre 41 e 45 anos
# 15	Entre 46 e 50 anos
# 16	Entre 51 e 55 anos
# 17	Entre 56 e 60 anos
# 18	Entre 61 e 65 anos
# 19	Entre 66 e 70 anos
# 20	Maior de 70 anos


# In[7]:


faixaetaria1 = microdados["TP_FAIXA_ETARIA"].sample(n= 100,random_state = 12) #pegando uma amostra

index = faixaetaria1.index

notaredacao1 = microdados["NU_NOTA_REDACAO"].loc[index]
notamatematica1 = microdados["NU_NOTA_MT"].loc[index]
notanatureza1 = microdados["NU_NOTA_CN"].loc[index]
notahumanas1 = microdados["NU_NOTA_CH"].loc[index]
notalinguagem1= microdados["NU_NOTA_LC"].loc[index]


df1 = pd.DataFrame([faixaetaria1,notaredacao1,notamatematica1,notanatureza1,notahumanas1,notalinguagem1])
df1 = df1.T


# In[8]:


def amostra(df): # função para pegar várias amostras
    amostras = {}
    for i in range(40):
        
        faixaetaria  = df["TP_FAIXA_ETARIA"].sample(n = 100, random_state = i)
        
        index = faixaetaria.index
        
        notaredacao = df["NU_NOTA_REDACAO"].loc[index]
        notamatematica = df["NU_NOTA_MT"].loc[index]
        notanatureza = df["NU_NOTA_CN"].loc[index]
        notahumanas = df["NU_NOTA_CH"].loc[index]
        notalinguagem= df["NU_NOTA_LC"].loc[index]


        amostra_df = pd.DataFrame([faixaetaria,notaredacao,notamatematica,notanatureza,notahumanas,notalinguagem])
        amostra_df = amostra_df.T
        
        
        amostras[f"amostra_{i}"] = amostra_df 
        
    return amostras
        
        
        
        
    
    


# In[9]:


amostra_microdados = amostra(microdados) #passando a função amostra no dataset microdados ( criando amostras )


# # Verificando média das redações da amostra 1 

# In[10]:


amostra1 = amostra_microdados["amostra_0"]
amostra1 = amostra1.dropna()
amostra1["NU_NOTA_REDACAO"]


# In[11]:


amostra1


# In[12]:


amostra1["NU_NOTA_REDACAO"].mean()


# # Verificando a média das amostras 2 

# In[13]:


amostra2 = amostra_microdados["amostra_1"]
amostra2 = amostra2.dropna()
amostra2["NU_NOTA_REDACAO"]


# In[14]:


amostra2["NU_NOTA_REDACAO"].mean()


# # Limpando os dados!

# In[15]:


microdados.columns


# # Removendo colunas não relevantes para análise

# In[16]:


microdados.drop(["NU_ANO", "TP_SIT_FUNC_ESC","CO_MUNICIPIO_PROVA",
                "NO_MUNICIPIO_PROVA","CO_UF_PROVA","SG_UF_PROVA",
                "CO_PROVA_CN","CO_PROVA_CH","CO_PROVA_LC","CO_PROVA_MT",
                "TX_RESPOSTAS_CN","TX_RESPOSTAS_CH","TX_RESPOSTAS_LC",
                "TX_RESPOSTAS_MT","TX_GABARITO_CN","TX_GABARITO_CH",
                "TX_GABARITO_LC","TX_GABARITO_MT"],axis = 1 ,inplace = True)


# In[17]:


microdados.drop(["NU_INSCRICAO"],axis = 1, inplace = True)


# In[18]:


microdados.columns


# # Removendo os participantes que foram ausentes em alguma prova

# In[19]:


indices_to_drop = microdados.query("TP_PRESENCA_CN != 1 & TP_PRESENCA_CH != 1 & TP_PRESENCA_LC != 1 &"
                "TP_PRESENCA_MT != 1").index


# In[20]:


microdados.drop(indices_to_drop)


# # Removendo valores nulos

# In[21]:


microdados.isnull().sum()


# In[22]:


microdados = microdados.dropna()


# In[23]:


microdados.isnull().sum()


# In[24]:


microdados


# In[25]:


microdados["NOTA MÉDIA"] = (microdados["NU_NOTA_CN"] + microdados["NU_NOTA_CH"] + microdados["NU_NOTA_LC"] + microdados["NU_NOTA_MT"] + microdados["NU_NOTA_REDACAO"])/5


# In[26]:


microdados


# In[27]:


import seaborn as sns 

sns.displot(microdados["NOTA MÉDIA"])

print("Distribuição Normal")


# In[28]:


sns.displot(microdados["NOTA MÉDIA"] , kind = "ecdf")

media = microdados["NOTA MÉDIA"].mean()
median = microdados["NOTA MÉDIA"].median()
std = microdados["NOTA MÉDIA"].std()


twenty = microdados["NOTA MÉDIA"].quantile(0.2)
fourty = microdados["NOTA MÉDIA"].quantile(0.4)
sixty = microdados["NOTA MÉDIA"].quantile(0.6)
eity = microdados["NOTA MÉDIA"].quantile(0.8)

print(f"A média das notas médias é de {media:.2f}")
print(f"O valor central das notas médias é de  {median:.2f}")
print(f"As notas variam em média  {std:.2f} pontos em relação a média ({media:.2f})")

print("****************************************************************************************************")
print(f"80% dos candidatos tiraram pelo menos {twenty:.2f} ,cuja nota está  apenas 20% acima  dos outros")
print(f"Apenas 60% tiraram pelo menos {fourty:.2f} ,cuja nota está apenas 40% acima a dos outros")
print(f"Apenas 40% tiraram pelo menos {sixty:.2f} ,cuja nota está  60% acima dos outros")
print(f"Somente 20 % tiraram pelo menos {eity:.2f} ,cuja nota está acima de 80% dos outros")
print("****************************************************************************************************")


# In[29]:


sns.boxplot(microdados["NOTA MÉDIA"].values, orient ="h")


# In[ ]:





# # Quem são os que tiraram as melhores notas?

# In[30]:


ax = sns.scatterplot(microdados , x = "TP_FAIXA_ETARIA" , y = "NOTA MÉDIA" , hue = "TP_ESCOLA" )
ax.figure.set_size_inches(12,8)
handles, labels = ax.get_legend_handles_labels()
new_labels = ['Escola Pública', 'Escola Particular']
ax.legend(handles=handles, labels=new_labels, title='Categoria', title_fontsize='13', fontsize='12', loc='best')


# Os que tiraram as melhores notas, estatísticamente falando, foram jovens na faixa de 17 a 20 anos\
# que estudaram em escolas particulares.
# É possível ver a predominância de participantes provindos de uma escola particular nesta faixa de idade, também \
# como é possível notar a queda de particpantes provindos de uma escola particular, conforme a idade aumenta.

# Devido a sua nota mais alta, jovens provindos de escolas particulares adentram a faculdade mais rapidamente.
# A grande maioria das pessoas mais velhas que prestaram o vestibular são de escolas públicas.


# In[31]:


ax = sns.scatterplot(microdados , x = "TP_FAIXA_ETARIA" , y = "NOTA MÉDIA" , hue = "TP_SEXO" )
ax.figure.set_size_inches(12,8)
handles, labels = ax.get_legend_handles_labels()
new_labels = ['Feminino', 'Masculino']
ax.legend(handles = handles , labels = new_labels,title='Sexo', title_fontsize='13', fontsize='12', loc='best')

#Ao que parece,visualmente, muitas das notas mais altas são de pessoas jovens do gênero masculino,
# mas isto não é um veredicto estatístico, visto que as notas mais baixas também são de jovens do gênero masculino.
#Também é possível notar a diminuição de participantes mais velhos, do sexo masculino, conforme a idade aumenta.


# In[32]:


microdados.columns


# In[33]:


ax = sns.scatterplot(microdados , x = "TP_FAIXA_ETARIA" , y = "NOTA MÉDIA" , hue = "TP_ESTADO_CIVIL", palette="deep" )
ax.figure.set_size_inches(12,8)
handles, labels = ax.get_legend_handles_labels()
new_labels = ['Não Informado', 'Solteiro' , 'Casado','Divorciado','Viúvo']
ax.legend(handles=handles, labels=new_labels, title='Estado Civil', title_fontsize='13', fontsize='12', loc='best')

# Ao que parece,visualmente,as maiores notas provém de jovens solteiros.
# Nota-se que , ao aumentar da idade, aumenta-se o número de participantes casados e/ou divorciados.


# In[34]:


ax = sns.scatterplot(microdados , x = "TP_FAIXA_ETARIA" , y = "NOTA MÉDIA" , hue = "TP_COR_RACA" , palette = "tab10")
ax.figure.set_size_inches(12,8)
handles, labels = ax.get_legend_handles_labels()
new_labels = ['Não declarado','Branca', 'Preta' , 'Parda','Amarela','Indígena','Não dispõe da informação']
ax.legend(handles=handles, labels=new_labels, title='Cor Declarada', title_fontsize='13', fontsize='12', loc='best')

# É possível notar, nas maiores notas, a relevância do aparecimento das cor de pele branca nos jovens, e também, com menos predominância\
# a cor parda. Como no caso da análise do sexo dos participantes, também não um veredicto estatístico, visto que as menores notas \
# também provém de jovens de pele branca.
# É notório também o pouco aparecimento de participantes de cor amarela, ou indígenas.


# In[35]:


microdados.groupby("TP_FAIXA_ETARIA")["NOTA MÉDIA"].mean()
microdados.groupby("TP_ESCOLA")["NOTA MÉDIA"].mean()
microdados.groupby("TP_SEXO")["NOTA MÉDIA"].mean()
microdados.groupby("TP_COR_RACA")["NOTA MÉDIA"].mean()
microdados.groupby("TP_ESTADO_CIVIL")["NOTA MÉDIA"].mean()


# # Verificando o quadro social dos participantes de acordo com a respostas dos questionarios
# 

# In[36]:


questoes = {
    "Q001": {
        "pergunta": "Até que série seu pai, ou o homem responsável por você, estudou?",
        "respostas": {
            "A": "Nunca estudou",
            "B": "Não completou a 4ª série/5º ano do Ensino Fundamental.",
            "C": "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.",
            "D": "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.",
            "E": "Completou o Ensino Médio, mas não completou a Faculdade.",
            "F": "Completou a Faculdade, mas não completou a Pós-graduação.",
            "G": "Completou a Pós-graduação.",
            "H": "Não sei"
        }
    },
    "Q002": {
        "pergunta": "Até que série sua mãe, ou a mulher responsável por você, estudou?",
        "respostas": {
            "A": "Nunca estudou",
            "B": "Não completou a 4ª série/5º ano do Ensino Fundamental.",
            "C": "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.",
            "D": "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.",
            "E": "Completou o Ensino Médio, mas não completou a Faculdade.",
            "F": "Completou a Faculdade, mas não completou a Pós-graduação.",
            "G": "Completou a Pós-graduação.",
            "H": "Não sei"
        }
    },
    "Q003": {
        "pergunta": "A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação do seu pai ou do homem responsável por você. (Se ele não estiver trabalhando, escolha uma ocupação pensando no último trabalho dele).",
        "respostas": {
            "A": "Grupo 1: Lavrador, agricultor sem empregados, bóia fria, criador de animais (gado, porcos, galinhas, ovelhas, cavalos etc.), apicultor, pescador, lenhador, seringueiro, extrativista.",
            "B": "Grupo 2: Diarista, empregado doméstico, cuidador de idosos, babá, cozinheiro (em casas particulares), motorista particular, jardineiro, faxineiro de empresas e prédios, vigilante, porteiro, carteiro, office-boy, vendedor, caixa, atendente de loja, auxiliar administrativo, recepcionista, servente de pedreiro, repositor de mercadoria.",
            "C": "Grupo 3: Padeiro, cozinheiro industrial ou em restaurantes, sapateiro, costureiro, joalheiro, torneiro mecânico, operador de máquinas, soldador, operário de fábrica, trabalhador da mineração, pedreiro, pintor, eletricista, encanador, motorista, caminhoneiro, taxista.",
            "D": "Grupo 4: Professor (de ensino fundamental ou médio, idioma, música, artes etc.), técnico (de enfermagem, contabilidade, eletrônica etc.), policial, militar de baixa patente (soldado, cabo, sargento), corretor de imóveis, supervisor, gerente, mestre de obras, pastor, microempresário (proprietário de empresa com menos de 10 empregados), pequeno comerciante, pequeno proprietário de terras, trabalhador autônomo ou por conta própria.",
            "E": "Grupo 5: Médico, engenheiro, dentista, psicólogo, economista, advogado, juiz, promotor, defensor, delegado, tenente, capitão, coronel, professor universitário, diretor em empresas públicas ou privadas, político, proprietário de empresas com mais de 10 empregados.",
            "F": "Não sei"
        }
    },
    "Q004": {
        "pergunta": "A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação da sua mãe ou da mulher responsável por você. (Se ela não estiver trabalhando, escolha uma ocupação pensando no último trabalho dela).",
        "respostas": {
            "A": "Grupo 1: Lavradora, agricultora sem empregados, bóia fria, criadora de animais (gado, porcos, galinhas, ovelhas, cavalos etc.), apicultora, pescadora, lenhadora, seringueira, extrativista.",
            "B": "Grupo 2: Diarista, empregada doméstica, cuidadora de idosos, babá, cozinheira (em casas particulares), motorista particular, jardineira, faxineira de empresas e prédios, vigilante, porteira, carteira, office-boy, vendedora, caixa, atendente de loja, auxiliar administrativa, recepcionista, servente de pedreiro, repositora de mercadoria.",
            "C": "Grupo 3: Padeira, cozinheira industrial ou em restaurantes, sapateira, costureira, joalheira, torneira mecânica, operadora de máquinas, soldadora, operária de fábrica, trabalhadora da mineração, pedreira, pintora, eletricista, encanadora, motorista, caminhoneira, taxista.",
            "D": "Grupo 4: Professora (de ensino fundamental ou médio, idioma, música, artes etc.), técnica (de enfermagem, contabilidade, eletrônica etc.), policial, militar de baixa patente (soldado, cabo, sargento), corretora de imóveis, supervisora, gerente, mestre de obras, pastora, microempresária (proprietária de empresa com menos de 10 empregados), pequena comerciante, pequena proprietária de terras, trabalhadora autônoma ou por conta própria.",
            "E": "Grupo 5: Médica, engenheira, dentista, psicóloga, economista, advogada, juíza, promotora, defensora, delegada, tenente, capitã, coronel, professora universitária, diretora em empresas públicas ou privadas, política, proprietária de empresas com mais de 10 empregados.",
            "F": "Não sei"
        }
    },
    "Q005": {
        "pergunta": "Incluindo você, quantas pessoas moram atualmente em sua residência?",
        "respostas": {
            "1": "1 , pois moro sozinho(a)",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "10": "10",
            "11": "11",
            "12": "12",
            "13": "13",
            "14": "14",
            "15": "15",
            "16": "16",
            "17": "17",
            "18": "18",
            "19": "19",
            "20": "20"
        }
    },
    "Q006": {
        "pergunta": "Qual é a renda mensal de sua família? (Some a sua renda com a dos seus familiares.)",
        "respostas": {
            "A": "Nenhuma Renda",
            "B": "Até R$ 1.212,00",
            "C": "De R$ 1.212,01 até R$ 1.818,00.",
            "D": "De R$ 1.818,01 até R$ 2.424,00.",
            "E": "De R$ 2.424,01 até R$ 3.030,00.",
            "F": "De R$ 3.030,01 até R$ 3.636,00.",
            "G": "De R$ 3.636,01 até R$ 4.848,00.",
            "H": "De R$ 4.848,01 até R$ 6.060,00.",
            "I": "De R$ 6.060,01 até R$ 7.272,00.",
            "J": "De R$ 7.272,01 até R$ 8.484,00.",
            "K": "De R$ 8.484,01 até R$ 9.696,00.",
            "L": "De R$ 9.696,01 até R$ 10.908,00.",
            "M": "De R$ 10.908,01 até R$ 12.120,00.",
            "N": "De R$ 12.120,01 até R$ 14.544,00.",
            "O": "De R$ 14.544,01 até R$ 18.180,00.",
            "P": "De R$ 18.180,01 até R$ 24.240,00.",
            "Q": "Acima de R$ 24.240,00."

            
        }
    },
    "Q007": {
        "pergunta": "Em sua residência trabalha empregado(a) doméstico(a)?",
        "respostas": {
            "A": "Não.",
            "B": "Sim,um ou dois dias por semana.",
            "C": "Sim, três ou quatro dias por semana.",
            "D": "Sim, pelo menos cinco dias por semana.",
        }
    },
    "Q008": {
        "pergunta": "Na sua residência tem banheiro?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q009": {
        "pergunta": "Na sua residência tem quartos para dormir?",
        "respostas": {
            "A": "Não",
            "B": "Sim , um",
            "C": "Sim, dois",
            "D": "Sim , três",
            "E": "Sim , quatro ou mais"
        }
    },
    "Q010": {
        "pergunta": "Na sua residência tem carro?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q011": {
        "pergunta": "Na sua residência tem motocicleta?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q012": {
        "pergunta": "Na sua residência tem geladeira?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q013": {
        "pergunta": "Na sua residência tem freezer (independente ou segunda porta da geladeira)?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q014": {
        "pergunta": "Na sua residência tem máquina de lavar roupa? (o tanquinho NÃO deve ser considerado)",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q015": {
        "pergunta": "Na sua residência tem máquina de secar roupa (independente ou em conjunto com a máquina de lavar roupa)?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q016": {
        "pergunta": "Na sua residência tem forno micro-ondas?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q017": {
        "pergunta": "Na sua residência tem máquina de lavar louça?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q018": {
        "pergunta": "Na sua residência tem aspirador de pó?",
        "respostas": {
            "A": "Não",
            "B": "Sim"
        }
    },
    "Q019": {
        "pergunta": "Na sua residência tem televisão em cores?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q020": {
        "pergunta": "Na sua residência tem aparelho de DVD?",
        "respostas": {
            "A": "Não",
            "B": "Sim"
        }
    },
    "Q021": {
        "pergunta": "Na sua residência tem TV por assinatura?",
        "respostas": {
            "A": "Não",
            "B": "Sim"
        }
    },
    "Q022": {
        "pergunta": "Na sua residência tem telefone celular?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q023": {
        "pergunta": "Na sua residência tem telefone fixo?",
        "respostas": {
            "A": "Não",
            "B": "Sim"
        }
    },
    "Q024": {
        "pergunta": "Na sua residência tem computador?",
        "respostas": {
            "A": "Não",
            "B": "Sim,um",
            "C": "Sim,dois",
            "D": "Sim,três",
            "E": "Sim,quatro ou mais"
        }
    },
    "Q025": {
        "pergunta": "Na sua residência tem acesso à Internet?",
        "respostas": {
            "A": "Não",
            "B": "Sim"
        }
    }
}


# #  Desenvolvendo uma função  para facilitar as análises

# In[37]:


def questionario(quest):
    respostas = microdados[quest].unique()
    respostas = sorted(respostas)
    vetor = []
    for resposta in respostas:
        resposta = microdados[microdados[quest] == resposta]
        
        vetor.append(resposta)
        
    for numero,pergunta in questoes.items():
        if numero == quest:
            print(f"{numero} : {questoes[quest]['pergunta']} \n")
            for opcao,conteudo in questoes[quest]["respostas"].items():
                print(f"{opcao} : {conteudo}\n")
    
    for resposta in vetor:
        print(f"A média  das notas dos participantes que  responderam {resposta[quest].unique()}({resposta.shape[0]} participantes) foi de {resposta['NOTA MÉDIA'].mean():.2f}, com um desvio padrão de {resposta['NOTA MÉDIA'].std():.2f}\n")
    
    ax = sns.catplot(data = microdados.sort_values(by=quest , ascending = True) , x = "NOTA MÉDIA",y = quest , kind = "bar" , palette = 'mako')
    ax.set(title = (f"Distribuição das Notas Médias conforme a resposta do questionário {quest}"))
    ax.figure.set_size_inches(12,8)
        
    ax.savefig(f"{quest}.png" , bbox_inches = "tight")


# In[38]:


questionario("Q001")


# In[ ]:




