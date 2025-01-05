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


file_path = "MICRODADOS_ENEM_2022.csv"


try:
    microdados = pd.read_csv(file_path, encoding='latin1' , sep = ";")
except UnicodeDecodeError:
    try:
        microdados = pd.read_csv(file_path, encoding='iso-8859-1', sep = ";")
    except UnicodeDecodeError:
        microdados = pd.read_csv(file_path, encoding='cp1252', sep = ";")


# In[3]:


microdados.head()


# In[4]:


microdados.describe()


# # Cleaning data!

# In[5]:


microdados.columns


# # Removing irrelevant columns

# In[6]:


# microdados.drop(["NU_ANO", "TP_SIT_FUNC_ESC","CO_MUNICIPIO_PROVA",
#                 "NO_MUNICIPIO_PROVA","CO_UF_PROVA","SG_UF_PROVA",
#                 "CO_PROVA_CN","CO_PROVA_CH","CO_PROVA_LC","CO_PROVA_MT",
#                 "TX_RESPOSTAS_CN","TX_RESPOSTAS_CH","TX_RESPOSTAS_LC",
#                 "TX_RESPOSTAS_MT","TX_GABARITO_CN","TX_GABARITO_CH",
#                 "TX_GABARITO_LC","TX_GABARITO_MT"],axis = 1 ,inplace = True)


# In[7]:


microdados.drop(["NU_INSCRICAO"],axis = 1, inplace = True)


# In[8]:


microdados.columns


# # Removing participants who did not take the test

# In[9]:


indices_to_drop = microdados.query("TP_PRESENCA_CN != 1 & TP_PRESENCA_CH != 1 & TP_PRESENCA_LC != 1 &"
                "TP_PRESENCA_MT != 1").index


# In[10]:


microdados.drop(indices_to_drop)


# # Removing null values

# In[11]:


microdados.isnull().sum()


# In[12]:


microdados = microdados.dropna()


# In[13]:


microdados.isnull().sum()


# # A function to create samples

# In[14]:


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
        
        
        
        
    
    


# In[15]:


amostra_microdados = amostra(microdados) #passando a função amostra no dataset microdados ( criando amostras )


# # Checking the average essay scores of the population

# In[16]:


microdados["NU_NOTA_REDACAO"].mean()


# # Checking the average essay scores of sample 1

# In[17]:


amostra1 = amostra_microdados["amostra_0"]
amostra1 = amostra1.dropna()
amostra1["NU_NOTA_REDACAO"].mean()


# In[18]:


amostra1["NU_NOTA_REDACAO"].mean()


# # Checking the average essay scores of samples 2

# In[19]:


somamedias = 0
for i in range(len(amostra_microdados)):
    mediai = amostra_microdados[f"amostra_{i}"]["NU_NOTA_REDACAO"].mean()
    somamedias += mediai
    
media_das_amostras = somamedias/len(amostra_microdados)
media_das_amostras

print("A média das amostras")


# <hr style="height: 2px; border-width: 0; color: #FF0000;">

# # When it comes to essay scores, the population mean and the mean of the sample means are very similar, which may suggest that reliable conclusions can be drawn from the samples

# <hr style="height: 2px; border-width: 0; color: #FF0000;">

# # Creating a new column : NOTA MÉDIA ( Average score)

# In[20]:


microdados["NOTA MÉDIA"] = (microdados["NU_NOTA_CN"] + microdados["NU_NOTA_CH"] + microdados["NU_NOTA_LC"] + microdados["NU_NOTA_MT"] + microdados["NU_NOTA_REDACAO"])/5


# In[ ]:





# In[21]:


microdados


# In[22]:


import seaborn as sns 

sns.displot(microdados["NOTA MÉDIA"])

print("Distribuição Normal")


# In[23]:


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


# In[24]:


sns.boxplot(microdados["NOTA MÉDIA"].values, orient ="h")


# In[ ]:





# # Who are the ones that got the highest scores?

# In[25]:


ax = sns.scatterplot(microdados , x = "TP_FAIXA_ETARIA" , y = "NOTA MÉDIA", hue = "TP_ESCOLA")
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


# # Conclusion 1: Younger participants who attended private schools predominantly have higher scores. The vast majority of older individuals taking the ENEM come from public schools, which may suggest that younger students from private schools are more likely to gain immediate acceptance into universities.

# In[26]:


ax = sns.scatterplot(microdados , x = "TP_FAIXA_ETARIA" , y = "NOTA MÉDIA" , hue = "TP_SEXO" )
ax.figure.set_size_inches(12,8)
handles, labels = ax.get_legend_handles_labels()
new_labels = ['Feminino', 'Masculino']
ax.legend(handles = handles , labels = new_labels,title='Sexo', title_fontsize='13', fontsize='12', loc='best')

#Ao que parece,visualmente, muitas das notas mais altas são de pessoas jovens do gênero masculino,
# mas isto não é um veredicto estatístico, visto que as notas mais baixas também são de jovens do gênero masculino.
#Também é possível notar a diminuição de participantes mais velhos, do sexo masculino, conforme a idade aumenta.


# In[27]:


participantesM = microdados.query("TP_SEXO == 'M'").shape[0]
participantesF = microdados.query("TP_SEXO =='F'").shape[0]
notasM = microdados.query("TP_SEXO == 'M'")["NOTA MÉDIA"].mean()
notasF = microdados.query("TP_SEXO == 'F'")["NOTA MÉDIA"].mean()

print(f"{participantesM} participantes do sexo masculino realizaram a prova. Sua nota média foi de {notasM}")
print(f"{participantesF} participantes do sexo feminino realizaram a prova. Sua nota média foi de {notasF}")

diferencapercentual = ((participantesF - participantesM))/(participantesM)*100
print(f"Houve {diferencapercentual:.2f} % a mais de participantes do sexo feminino ")

notas_acima_700M =  microdados.query("TP_SEXO == 'M'")
notas_acima_700M = notas_acima_700M[notas_acima_700M["NOTA MÉDIA"] > 700].shape[0]
notas_acima_700F =  microdados.query("TP_SEXO == 'F'")
notas_acima_700F = notas_acima_700F[notas_acima_700F["NOTA MÉDIA"] > 700].shape[0]

print(f"{notas_acima_700M} do sexo masculino tiveram nota média maior que 700")
print(f"{notas_acima_700F} do sexo feminino tiveram nota média maior que 700")


# # Conclusion 2: There seems to be a slightly higher occurrence of high scores among male participants. However, this is not statistically significant, as the numbers are very similar. It can be observed that the number of female participants increases with age, leading to the hypothesis that older men tend not to take the ENEM exam.

# In[28]:


ax = sns.scatterplot(microdados , x = "TP_FAIXA_ETARIA" , y = "NOTA MÉDIA" , hue = "TP_ESTADO_CIVIL", palette="deep" )
ax.figure.set_size_inches(12,8)
handles, labels = ax.get_legend_handles_labels()
new_labels = ['Não Informado', 'Solteiro' , 'Casado','Divorciado','Viúvo']
ax.legend(handles=handles, labels=new_labels, title='Estado Civil', title_fontsize='13', fontsize='12', loc='best')

# Ao que parece,visualmente,as maiores notas provém de jovens solteiros.
# Nota-se que , ao aumentar da idade, aumenta-se o número de participantes casados e/ou divorciados.


# In[29]:


participantes_solteiros = microdados.query("TP_ESTADO_CIVIL == 1").shape[0]
print(f"{participantes_solteiros} se identificaram como solteiros")

participantes_casados = microdados.query("TP_ESTADO_CIVIL == 2").shape[0]
print(f"{participantes_casados} se identificaram como casados")


participantes_divorciados = microdados.query("TP_ESTADO_CIVIL == 3").shape[0]
print(f"{participantes_divorciados} se identificaram como divorciados")

participantes_viuvos = microdados.query("TP_ESTADO_CIVIL == 4").shape[0]
print(f"{participantes_viuvos} se identificaram como viuvos")

participantes_sem_info = microdados.query("TP_ESTADO_CIVIL == 0").shape[0]
print(f"{participantes_sem_info} não informaram")


# # Conclusion 3: The vast majority of participants identified as single. This may be correlated with the age of the participants, as younger people tend to be single in general.

# In[30]:


ax = sns.scatterplot(microdados , x = "TP_FAIXA_ETARIA" , y = "NOTA MÉDIA" , hue = "TP_COR_RACA" , palette = "tab10")
ax.figure.set_size_inches(12,8)
handles, labels = ax.get_legend_handles_labels()
new_labels = ['Não declarado','Branca', 'Preta' , 'Parda','Amarela','Indígena','Não dispõe da informação']
ax.legend(handles=handles, labels=new_labels, title='Cor Declarada', title_fontsize='13', fontsize='12', loc='best')

# É possível notar, nas maiores notas, a relevância do aparecimento das cor de pele branca nos jovens, e também, com menos predominância\
# a cor parda. Como no caso da análise do sexo dos participantes, também não um veredicto estatístico, visto que as menores notas \
# também provém de jovens de pele branca.
# É notório também o pouco aparecimento de participantes de cor amarela, ou indígenas.


# In[31]:


microdados.groupby("TP_FAIXA_ETARIA")["NOTA MÉDIA"].mean()
microdados.groupby("TP_ESCOLA")["NOTA MÉDIA"].mean()
microdados.groupby("TP_SEXO")["NOTA MÉDIA"].mean()
microdados.groupby("TP_COR_RACA")["NOTA MÉDIA"].mean()
microdados.groupby("TP_ESTADO_CIVIL")["NOTA MÉDIA"].mean()


# # Checking the social profile of the participants based on the questionnaire responses.

# In[32]:


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


# # Developing a function to facilitate analyses.

# In[33]:


total = microdados.shape[0]


# In[34]:


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
        print(f"A média  das notas dos participantes que  responderam {resposta[quest].unique()}({resposta.shape[0]} participantes, {resposta.shape[0]/total*100:.2f}%) foi de {resposta['NOTA MÉDIA'].mean():.2f}, com um desvio padrão de {resposta['NOTA MÉDIA'].std():.2f}\n")
    
#     ax = sns.catplot(data = microdados.sort_values(by=quest , ascending = True) , x = "NOTA MÉDIA",y = quest , kind = "bar" , palette = 'mako')
#     ax.set(title = (f"Distribuição das Notas Médias conforme a resposta do questionário {quest}"))
#     ax.figure.set_size_inches(12,8)
    
        
    #ax.savefig(f"{quest}.png" , bbox_inches = "tight")


# In[39]:


for i in range(1, 26):  
    question = f"Q{str(i).zfill(3)}"  
    print(questionario(question))


# # Based on the social analysis and questionnaire responses, it is observed that students with better economic conditions tend to achieve higher grades more frequently compared to those with lower income. This result is likely due to their ability to attend private schools, which typically offer greater investment and development in education, better preparing students for college entrance exams. The hypothesis suggested is that if the government were to increase investments in public education for children and young people, this significant disparity could be reduced.

# In[ ]:




