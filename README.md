# Sistema de Gestão de Vendas — Integração com Supabase e Redis

## Identificação

| Campo | Detalhe |
|---|---|
| **Integrante** | Arthur Andrade Lima |
| **Disciplina** | Projeto de Banco de Dados |
| **Professor** | Anderson Soares Costa |
| **Trabalho** | Trabalho Prático — Integração com Supabase e Redis |

---

## 1. Sobre o Projeto e Problema que Resolve

O **Sistema de Gestão de Vendas** é uma aplicação desktop desenvolvida em Python para gerenciar produtos e clientes de forma ágil e eficiente.

Em sistemas baseados exclusivamente em bancos de dados na nuvem, consultas repetitivas (como listagem de estoque ou clientes) enfrentam latência de rede a cada requisição. Para resolver esse problema, a aplicação combina:
1. **Supabase (PostgreSQL na Nuvem):** Como banco de dados relacional permanente, garantindo a integridade e persistência de longo prazo.
2. **Redis Cloud:** Como banco em memória (*in-memory*) atuando como camada de **Cache**, entregando dados instantaneamente em milissegundos e reduzindo requisições desnecessárias à nuvem.

---

## 2. Objetivo e Principais Funcionalidades

* **Cadastro e Listagem de Produtos:** Inclusão, listagem e remoção de produtos com atualização automática.
* **Cadastro e Listagem de Clientes:** Gerenciamento dos dados cadastrais de clientes.
* **Cache Inteligente com Redis (Padrão Cache-Aside):**
  * Na primeira consulta, busca os dados no Supabase e armazena no Redis por 60 segundos com tempo de expiração (`TTL`).
  * Em consultas subsequentes, os dados são entregues diretamente da memória RAM pelo Redis (Cache HIT).
* **Invalidação Reativa de Cache:** Sempre que um produto ou cliente é cadastrado ou apagado, a chave no Redis é removida (`r.delete`) para evitar inconsistências e garantir dados sempre atualizados.
* **Indicador Visual na Interface:** A tela informa em tempo real se os dados exibidos vieram do `🟢 REDIS (Cache HIT)` ou do `🟡 SUPABASE (Cache MISS)`.
* **Botão de Limpeza Manual de Cache:** Permite demonstrar na prática a alternância entre a busca em nuvem e a entrega em cache.

---

## 3. Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Interface Gráfica:** Tkinter (Interface nativa e leve)
* **Banco de Dados Relacional:** Supabase (PostgreSQL na nuvem via biblioteca oficial `supabase`)
* **Banco em Memória / Cache:** Redis Cloud (via biblioteca `redis`)
* **Serialização de Dados:** `json`

---

## 4. Integração com o Supabase

O Supabase atua como a fonte principal e permanente dos dados. A comunicação é realizada por meio do client Python oficial:

```python
# Consulta de produtos
produtos = supabase.table("produtos").select("*").order("id").execute().data

# Inserção de novo produto
supabase.table("produtos").insert({"nome": nome, "preco_unitario": preco, "quantidade_estoque": quantidade}).execute().data

# Remoção de produto
supabase.table("produtos").delete().eq("id", id_prod).execute().data
```

---

## 5. Integração com o Redis

### Por que o Redis foi escolhido?
O Redis opera em memória RAM, o que o torna uma das ferramentas mais rápidas do mundo para leitura e escrita de dados chave-valor. Ele evita requisições redundantes pela internet ao Supabase, diminui a latência percebida pelo usuário e protege o banco principal contra sobrecargas.

### Onde e como foi aplicado:
* **Leitura com Cache (`r.get`):** Antes de consultar o Supabase, o sistema verifica se a chave existe no Redis. Se existir, os dados em formato JSON são carregados instantaneamente da memória.
* **Armazenamento com TTL (`r.set(..., ex=60)`):** Ao buscar no Supabase, a resposta é armazenada no Redis com prazo de validade de 60 segundos.
* **Invalidação de Cache (`r.delete`):** Ao criar ou apagar registros, a chave correspondente no Redis é imediatamente apagada para manter a consistência dos dados.

---

## 6. Como Executar a Aplicação

### Pré-requisitos
* Python 3.10 ou superior instalado.
* Conexão com a internet para acesso ao Supabase e Redis.

### 1. Instalar as dependências
Abra o terminal na pasta do projeto e execute:
```bash
pip install supabase redis
```

### 2. Executar o sistema
Execute o comando:
```bash
python main.py
```
*(Ou dê dois cliques no arquivo `executar.bat` no Windows).*

---

## 7. Estrutura dos Arquivos

```
sistema-vendas-supabase-redis/
├── banco.py          # Conexões diretas e funções CRUD integradas com Supabase e Redis
├── main.py           # Interface gráfica para interação do usuário e visualização de cache
├── executar.bat      # Inicializador rápido para Windows
├── docs/             # Roteiro do vídeo explicativo
└── README.md         # Documentação do projeto
```
