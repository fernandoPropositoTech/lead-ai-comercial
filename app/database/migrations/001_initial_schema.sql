/*
--------------------------------------------------

SIGNALIA DATABASE

Version: 1.0

Tabela: leads

--------------------------------------------------
*/

--------------------------------------------------
-- SCORES
--------------------------------------------------

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS score integer DEFAULT 0;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS score_digital integer DEFAULT 0;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS score_comercial integer DEFAULT 0;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS ranking_comercial integer DEFAULT 0;

--------------------------------------------------
-- OPPORTUNITY
--------------------------------------------------

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS opportunity_score integer DEFAULT 0;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS opportunity_explanation text;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS diagnostico jsonb;

--------------------------------------------------
-- IA
--------------------------------------------------

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS score_oportunidade integer DEFAULT 0;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS problema_principal text;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS abordagem text;

--------------------------------------------------
-- RECOMMENDATION
--------------------------------------------------

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS servico_recomendado text;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS prioridade text;

--------------------------------------------------
-- RELATÓRIO
--------------------------------------------------

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS resumo_comercial text;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS motivo_indicacao text;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS evidencias text;

--------------------------------------------------
-- QUALIFICATION
--------------------------------------------------

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS qualificado boolean DEFAULT false;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS status text;

--------------------------------------------------
-- AUDITORIA
--------------------------------------------------

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS updated_at timestamp;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS created_at timestamp DEFAULT now();



--------------------------------------------------
-- SOCIAL NETWORKS
--------------------------------------------------

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS facebook text;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS linkedin text;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS youtube text;

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS tiktok text;