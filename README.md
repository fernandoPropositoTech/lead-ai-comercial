[README (2).md](https://github.com/user-attachments/files/31286882/README.2.md)
# Signalia

> Inteligência comercial baseada em dados públicos para identificar, qualificar e priorizar oportunidades B2B.

[![Status](https://img.shields.io/badge/status-MVP%20em%20valida%C3%A7%C3%A3o-f59e0b)](#status-do-projeto)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3FCF8E?logo=supabase&logoColor=white)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

## Visão geral

A **Signalia** é uma plataforma em desenvolvimento que transforma dados públicos de empresas em oportunidades comerciais qualificadas e priorizadas.

Em vez de entregar apenas uma lista de contatos, a Signalia procura responder:

- Qual empresa merece ser abordada primeiro?
- Quais sinais justificam essa abordagem?
- Qual problema ou oportunidade foi identificado?
- Que serviço pode ser mais adequado?
- Qual argumento comercial pode iniciar a conversa?

O projeto começou com a validação de oportunidades para agências de marketing, desenvolvimento de sites, tráfego pago, SEO e automação. A arquitetura, entretanto, foi pensada para evoluir para outros mercados B2B por meio de modelos de análise específicos para cada setor e oferta.

## Problema

Equipes comerciais frequentemente trabalham com listas genéricas, dados incompletos e pouca informação sobre o contexto de cada empresa. Isso provoca:

- Tempo desperdiçado em pesquisa manual;
- Abordagens genéricas;
- Priorização baseada em opinião;
- Contato com empresas sem aderência;
- Baixa rastreabilidade sobre a qualidade das oportunidades.

## Proposta da Signalia

```text
Dados públicos
    ↓
Coleta e enriquecimento
    ↓
Validação e qualidade
    ↓
Scores e diagnóstico
    ↓
Priorização de oportunidades
    ↓
Recomendação para abordagem
```

A Signalia não classifica automaticamente uma empresa como um **lead quente**. No estágio atual, ela identifica uma **oportunidade fria, qualificada e priorizada**: uma empresa que ainda não demonstrou interesse, mas apresenta perfil, necessidade provável, canais de contato e evidências que justificam uma abordagem personalizada.

## As três camadas do produto

### 1. Dados

- Coleta de informações públicas;
- Padronização e limpeza;
- Recuperação e validação de websites;
- Extração de telefone, WhatsApp, e-mail e redes sociais;
- Tratamento de duplicidades e dados ausentes;
- Persistência estruturada.

### 2. Inteligência

- Avaliação da presença digital;
- Score técnico e comercial;
- Score de oportunidade;
- Indicador de confiança dos dados;
- Identificação do problema principal;
- Diagnóstico e impacto provável;
- Serviço recomendado;
- Ranking das melhores oportunidades.

### 3. Ação

- Resumo comercial;
- Sugestão de abordagem;
- Exportação dos resultados;
- Geração de planilhas e relatórios;
- Preparação para integração com CRM;
- Registro futuro de respostas, reuniões e vendas.

## Exemplo de oportunidade

```json
{
  "empresa": "Clínica Exemplo",
  "categoria": "Clínica odontológica",
  "cidade": "São Paulo",
  "score_oportunidade": 82,
  "prioridade": "Alta",
  "problema_principal": "Jornada digital com pontos de perda de conversão",
  "evidencias": [
    "site sem chamada clara para agendamento",
    "WhatsApp localizado, mas pouco integrado à jornada",
    "boa avaliação no Google e volume relevante de reviews"
  ],
  "servico_recomendado": "Otimização do site e da conversão pelo WhatsApp",
  "abordagem": "Apresentar as evidências encontradas e propor uma análise objetiva da jornada digital"
}
```

> Os dados acima são fictícios e servem somente para demonstrar o formato da análise.

## Pipeline atual

```mermaid
flowchart LR
    A[Apify] --> B[Pipeline Python]
    B --> C[Validação]
    C --> D[Enriquecimento]
    D --> E[Scoring]
    E --> F[Diagnóstico]
    F --> G[Supabase]
    G --> H[Planilha ou relatório]
```

## Principais funcionalidades

- Busca por nicho e localização;
- Coleta de empresas em fontes públicas;
- Validação e recuperação de websites;
- Descoberta de páginas relevantes do site;
- Extração de contatos e canais digitais;
- Normalização e validação dos dados;
- Detecção de presença digital;
- Cálculo de scores por diferentes critérios;
- Geração de diagnóstico comercial;
- Priorização e ranking;
- Armazenamento no Supabase;
- Exportação para planilha e relatório.

## Arquitetura conceitual

```text
src/
├── collectors/          # Coleta de dados externos
├── processors/          # Orquestração do processamento
├── services/
│   ├── enrichment/      # Enriquecimento de sites e contatos
│   ├── validation/      # Validação e qualidade
│   ├── opportunity/     # Score, diagnóstico e recomendação
│   └── storage/         # Persistência dos resultados
├── models/              # Estruturas e contratos de dados
└── exports/             # Planilhas e relatórios
```

> A estrutura apresentada é conceitual e pode variar conforme a evolução da refatoração do projeto.

## Tecnologias

| Área | Tecnologias |
|---|---|
| Linguagem | Python |
| Coleta | Apify, Requests, Beautiful Soup |
| Processamento | Python e Pandas |
| Banco de dados | Supabase / PostgreSQL |
| Automação | N8N |
| API | FastAPI — evolução planejada |
| Interface de validação | Streamlit — próxima etapa |
| Infraestrutura | Docker |
| Testes | Pytest |
| Versionamento | Git e GitHub |

## Configuração local

### Pré-requisitos

- Python 3.11 ou superior;
- Git;
- Conta e credenciais das fontes externas utilizadas;
- Projeto Supabase configurado;
- Docker, caso a execução conteinerizada seja utilizada.

### Instalação

Clone este repositório pela opção **Code** do GitHub. Depois, abra o terminal na pasta criada e execute:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No Linux ou macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example` e informe somente suas próprias credenciais:

```env
APIFY_API_TOKEN=
SUPABASE_URL=
SUPABASE_KEY=
```

Nunca envie o arquivo `.env`, tokens, chaves ou dados reais de clientes para o GitHub.

### Execução

O comando definitivo depende do ponto de entrada mantido na versão publicada. Exemplo para execução pelo módulo principal:

```bash
python main.py
```

Antes da primeira execução, confira o `.env.example`, a estrutura atual do projeto e as instruções da versão publicada.

## Status do projeto

O projeto está na fase de **estabilização do MVP e preparação para validação controlada com agências**.

O trabalho atual está concentrado em:

- Refatorar o pipeline;
- Separar responsabilidades entre os módulos;
- Melhorar consistência e qualidade dos dados;
- Garantir que scores e diagnósticos sejam rastreáveis;
- Criar testes para os fluxos principais;
- Preparar uma interface Streamlit para validação;
- Medir a utilidade comercial das oportunidades entregues.

Resultados iniciais de conversas e testes não devem ser interpretados como comprovação estatística. A validação será baseada em feedback estruturado e métricas de abordagem, resposta, reunião e venda.

## Roadmap

### Fase 1 — MVP de inteligência comercial

- [x] Coleta inicial de empresas;
- [x] Enriquecimento de websites e contatos;
- [x] Persistência no Supabase;
- [x] Scores e diagnóstico inicial;
- [x] Exportação de resultados;
- [ ] Finalização da estabilização e dos testes.

### Fase 2 — Validação com agências

- [ ] Interface web em Streamlit;
- [ ] Configuração por nicho, cidade e quantidade;
- [ ] Avaliação da qualidade dos dados;
- [ ] Feedback sobre score e diagnóstico;
- [ ] Registro de abordagens e respostas;
- [ ] Ajuste da proposta comercial.

### Fase 3 — Expansão B2B

- [ ] Modelos de oportunidade por setor;
- [ ] ICP e pesos configuráveis;
- [ ] Diagnósticos específicos por oferta;
- [ ] Novas fontes de dados;
- [ ] API para integrações.

### Fase 4 — Inteligência orientada a resultados

- [ ] Integração com CRM;
- [ ] Retorno de respostas, reuniões e vendas;
- [ ] Ajuste dos scores com dados reais;
- [ ] Dashboard comercial;
- [ ] Monitoramento de qualidade e desempenho.

### Fase 5 — Prospecção assistida

- [ ] Cadências personalizadas;
- [ ] Agente de IA ou operação SDR;
- [ ] Qualificação do interesse;
- [ ] Agendamento de reuniões;
- [ ] Evolução de oportunidade qualificada para lead quente.

## Métricas de validação

A evolução do produto será acompanhada por indicadores como:

- Percentual de contatos válidos;
- Precisão dos websites e canais encontrados;
- Percentual de oportunidades consideradas abordáveis;
- Taxa de resposta;
- Taxa de reuniões realizadas;
- Taxa de conversão em vendas;
- Motivos de rejeição dos leads;
- Relação entre score e resultado comercial.

## Diferencial em construção

Ferramentas tradicionais de prospecção ajudam a encontrar empresas e contatos. A proposta da Signalia é avançar uma etapa:

```text
Perfil adequado
+ necessidade provável
+ evidências públicas
+ diagnóstico explicável
+ recomendação comercial
= oportunidade priorizada
```

O diferencial não está apenas no uso de inteligência artificial, mas na construção de modelos que relacionem sinais observáveis a oportunidades específicas e, futuramente, aprendam com resultados comerciais reais.

## Uso responsável dos dados

A Signalia foi projetada para trabalhar com dados empresariais públicos e para apoiar decisões comerciais. A utilização do projeto deve observar:

- Legislação aplicável, incluindo a LGPD;
- Termos de uso das fontes consultadas;
- Limites técnicos e políticas de acesso;
- Transparência e respeito nas abordagens;
- Minimização e proteção dos dados armazenados;
- Possibilidade de correção e remoção quando aplicável.

Este projeto não deve ser usado para spam, assédio, coleta indevida de dados pessoais ou automações que violem regras das plataformas.

## Limitações atuais

- Scores iniciais baseados majoritariamente em regras;
- Necessidade de validação com maior volume de resultados;
- Cobertura dependente das fontes públicas disponíveis;
- Possibilidade de dados ausentes ou desatualizados;
- Diagnósticos representam indícios, não garantias de necessidade ou compra;
- A plataforma ainda não realiza prospecção nem garante reuniões.

## Autor

**Fernando Caruzo Bento**

Profissional com mais de 20 anos de experiência na indústria têxtil, em transição para Engenharia de Dados, Machine Learning e desenvolvimento de produtos orientados por IA.

A Signalia integra estudos e aplicações práticas de:

- Engenharia de dados;
- APIs e automação;
- Qualidade e enriquecimento de dados;
- Inteligência comercial;
- Desenvolvimento de produtos com IA;
- Sistemas de apoio à decisão.

## Contato

- Site: [signalia.com.br](https://signalia.com.br)
- Instagram: [@signalia.ia](https://www.instagram.com/signalia.ia/)
- GitHub: [fernandoPropositoTech](https://github.com/fernandoPropositoTech)

## Licença e propriedade intelectual

Este repositório é disponibilizado para demonstração técnica, estudo e portfólio. O código, os modelos de scoring, as regras comerciais e os demais ativos permanecem sujeitos aos termos definidos pelo autor.

Antes de reutilizar, distribuir ou empregar o projeto comercialmente, entre em contato para obter autorização.

---

**Signalia — não apenas uma lista de leads, mas inteligência para priorizar oportunidades comerciais.**
