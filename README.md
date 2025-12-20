## Objetivo
A AAVSO disponibiliza um grande volume de dados de estrelas variáveis coletados por astrônomos amadores
e profissionais. Este projeto tem como objetivo realizar uma análise dos dados de três 
#### Betelgeuse
Localizada na constelação de Órion, bem próxima ao equador celeste. Em determinadas épocas fica bem próxima ao sol.
#### Eta carinae
Estrela supergigante azul localizada na constelação de Carina, conhecida por suas erupções massivas. Fica próxima ao polo sul celeste.
#### Algol
Localizada na constelação de Perseu, é um sistema estelar binário eclipsante, onde uma estrela passa na frente da outra, causando variações periódicas no brilho observado. Fica próxima ao polo norte celeste.
 
> As estrelas foram escolhidas por serem bastante conhecidadas e por estarem localizadas em diferentes regiões do céu, o que pode influenciar na coleta dos dados.

### Perguntas de pesquisa
- Quais são os padrões de variação de brilho dessas estrelas ao longo do tempo?
- Qual a influência do sol nas observações estelares?
- Qual a distribuição das observações ao longo do ano?
- Que agências/astrônomos contribuem mais para os dados dessas estrelas?

## Modelagem
O modelo proposto foi um modelo dimensional estrela onde o fato é a __magnitude observada__ 
e as dimensões são:
- Data
- Estrela
- Observador
- Incerteza

![Figura 1: Modelo dimensional estrela](img/modelo.png)

## Catálogo
| Coluna | Tipo de dado | Descrição | Valores esperados |
|-------------|---------------------|--------------------------------------------------------------------|--------------------------------|
|Magnitude    |Decimal              | Brilho de um objeto no céu. Quanto menor o número, maior o brilho  | de -10.0 até +10.0             |
|Data         |Data                 | Data da observação da estrela. Formato AAAA-MM-DD                  | 2000-01-01 2021-01-01          |
|Estrela      |Texto                | Nome da estrela observada.                                         | Betelgeuse, Eta Carinae, Algol |
|Observado    |Texto                | Nome ou código do observador que fez a medição.                    | Código alfanumérico            |
|Incerteza    |Decimal              | Margem de erro associada à medição da magnitude.                   | de 0.0 até 1.0                 |

### Linhagem
- Coleta manual dos dados em formato csv na AAVSO
- Armazenamento dos dados via upload no Databricks
- Armazenamento dos dados brutos na camada bronze do Data Lake
- Limpeza e transformação dos dados na camada prata
- Transformação dos dados para o modelo dimensional na camada ouro

## Pipeline de dados
### Coleta
A coleta foi feita manualmente através de arquivos csvs disponibilizados pela AAVSO.
Foi feito um upload para o Databricks e armazenado na camada bronze do Data Lake. Como o Databricks
dá a opção de criar a tabela no momento do upload, não foi necessário usar nenhum mecanismo mais
sofisticado de ingestão de dados. Foram criadas 3 tabelas, uma para cada estrela, pois assim na
camada prata ficará mais fácil fazer a limpeza dos dados.

> Nota-se muitas colunas com valores nulos, inclusive valores incorretos para o nome das estrelas.
![Figura 2: Amostragem da tabela de medições de estrelas variáveis na camada bronze](img/bronze.png)

### Limpeza
A limpeza dos dados foi feita na camada prata do Data Lake. 
- Foram removidas colunas desnecessárias
- Foram corrigidos valores incorretos para os nomes das estrelas
- Todas as linhas cujo o valor da magnitude fosse nulo foram removidas
- Todos os registros de incerteza com valores incorretos foram limpos
- A granularidade da incerteza foi padronizada pra uma casa decimal
- As datas foram convertidas para o calendário gregoriano

- [Link para o notebook da camada prata](https://github.com/igorcavalcante/MVP_engenharia_de_dados/refs/heads/main/silver_layer.py)

### Transformação


## Análise
### Qualidade dos dados
### Solução do problema
## Autoavaliação
## Referências
- [AAVSO](https://www.aavso.org)
> "We acknowledge with thanks the variable star observations from the AAVSO International Database oontributed by observers worldwide and used in this research."
