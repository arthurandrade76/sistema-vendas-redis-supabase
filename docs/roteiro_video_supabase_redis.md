# Roteiro do Vídeo — Trabalho Prático: Supabase e Redis (Atualizado)

> ⏱️ **Duração ideal:** 2 a 3 minutos  
> 🎬 = O que você mostra na tela / onde clica  
> 🗣️ = O que você fala (direto ao ponto)

---

## 1. Apresentação e Proposta (30 segundos)
🎬 *Deixe o VS Code aberto no arquivo `banco.py`.*

🗣️ *"Olá, professor! Sou o Arthur Andrade Lima, da disciplina Projeto de Banco de Dados. Este é o Trabalho Prático de Integração com Supabase e Redis.*

*A proposta do projeto é uma aplicação de gerenciamento de produtos e clientes que une duas tecnologias: o **Supabase**, responsável pela persistência permanente dos dados na nuvem, e o **Redis**, utilizado como cache em memória para acelerar as consultas e reduzir o tráfego no banco principal."*

---

## 2. Explicação do Código (`banco.py`) (45 segundos)
🎬 *No VS Code, aponte para o arquivo `banco.py` com o mouse:*

🗣️ *"No código, a integração é muito direta:*
* *No início, conectamos ao Supabase usando o `create_client` e ao Redis na nuvem usando o `redis.Redis`.*
* *Na função `listar_produtos()`, aplicamos o padrão **Cache-Aside**: primeiro o sistema verifica no Redis com `r.get('produtos')`. Se o dado já estiver em memória, ele retorna direto do cache.*
* *Se não estiver, o sistema busca no Supabase com `supabase.table('produtos').select('*')`, e em seguida grava o resultado no Redis com validade de 60 segundos usando o `r.set(..., ex=60)`.*
* *E nas funções `criar_produto()` e `apagar_produto()`, sempre que inserimos ou apagamos no Supabase, executamos `r.delete('produtos')` para invalidar o cache antigo e garantir que o usuário não veja dados desatualizados."*

---

## 3. Demonstração Prática da Aplicação (1 minuto e 15 segundos)
🎬 *Abra a janela do sistema (`python main.py` ou dois cliques no `executar.bat`).*

🗣️ *"Agora vou demonstrar o sistema funcionando na prática."*

🎬 **Passo 1: Demonstrar o Cache MISS (Supabase)**
* Clique no botão **"🧹 Limpar Cache Redis"** e em seguida em **"🔄 Recarregar"**.
* Aponte para o banner no topo da tela: `Fonte: 🟡 SUPABASE (Consultado do Supabase na Nuvem)`.

🗣️ *"Limpei o cache do Redis e cliquei em recarregar. Reparem que o banner no topo indica **Fonte: SUPABASE**. Como o cache estava vazio, a consulta precisou ir até a nuvem para trazer os produtos."*

🎬 **Passo 2: Demonstrar o Cache HIT (Redis)**
* Clique imediatamente no botão **"🔄 Recarregar"** de novo.
* Aponte para o banner no topo da tela: `Fonte: 🟢 REDIS (Memória RAM instantânea)`.

🗣️ *"Agora, ao recarregar novamente, a fonte muda imediatamente para **🟢 REDIS**. O dado foi recuperado da memória RAM em milissegundos, sem fazer nenhuma requisição ao Supabase."*

🎬 **Passo 3: Demonstrar a Invalidação de Cache ao Cadastrar**
* No formulário abaixo, digite:
  * Nome: `Mousepad Gamer`
  * Preço: `45.00`
  * Quantidade: `15`
* Clique em **"➕ Salvar"**.

🗣️ *"Quando eu cadastro um novo item, o sistema salva no Supabase e apaga a chave do Redis. Dessa forma, a próxima leitura trará os dados atualizados com o novo produto."*

🎬 **Passo 4: Mostrar a Aba de Clientes**
* Clique no botão **"👥 Ver Clientes"**.

🗣️ *"A mesma lógica de persistência no Supabase e cache no Redis também está aplicada para a listagem e cadastro de clientes."*

---

## 4. Conclusão e Benefícios do Redis (20 segundos)
🎬 *Volte para o VS Code ou encerre mostrando a tela do app.*

🗣️ *"Em resumo, o Redis foi escolhido pela sua altíssima velocidade por operar em memória e suporte nativo a expiração de chaves com TTL. Ele proporciona redução de latência de rede, alívio de carga no banco Supabase e uma experiência instantânea para o usuário.*

*Muito obrigado!"*
