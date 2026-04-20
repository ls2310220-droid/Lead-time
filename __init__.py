-- ═══════════════════════════════════════════════════════
-- LEAD TIME — Schema inicial
-- Projeto: https://xypjacdtbkqomeaimmch.supabase.co
-- ═══════════════════════════════════════════════════════

-- Tabela principal de carregamentos
CREATE TABLE IF NOT EXISTS carregamentos (
  id            SERIAL PRIMARY KEY,
  cliente       TEXT NOT NULL,
  pallets       INTEGER,
  local         TEXT DEFAULT 'FLK',
  semana        INTEGER NOT NULL,

  -- Draft
  draft_dt      TEXT,
  draft_tipo    TEXT,

  -- Etapas do ciclo
  pv            TEXT,
  oe            TEXT,
  sep           TEXT,
  aval          TEXT,
  cheg          TEXT,
  enc           TEXT,
  saiu          TEXT,
  nf            TEXT,
  lib           TEXT,

  -- Extras
  obs           TEXT DEFAULT '',
  motivo_status TEXT DEFAULT '',

  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de histórico (audit trail)
CREATE TABLE IF NOT EXISTS historico_carregamento (
  id               SERIAL PRIMARY KEY,
  carregamento_id  INTEGER NOT NULL REFERENCES carregamentos(id) ON DELETE CASCADE,
  dt               TEXT NOT NULL,
  tipo             TEXT NOT NULL,
  descricao        TEXT NOT NULL,
  extra            TEXT DEFAULT '',
  created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_carregamentos_semana ON carregamentos(semana);
CREATE INDEX IF NOT EXISTS idx_historico_carregamento_id ON historico_carregamento(carregamento_id);

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_carregamentos_updated_at
  BEFORE UPDATE ON carregamentos
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ═══════════════════════════════════════════════════════
-- SEED — dados iniciais da semana 16
-- ═══════════════════════════════════════════════════════
INSERT INTO carregamentos (cliente,pallets,local,semana,draft_dt,draft_tipo,pv,oe,sep,aval,cheg,enc,saiu,nf,lib,obs) VALUES
('OTHIL',28,'FLK',16,'13/04/2026 10:20','EMAIL+PLANNER','13/04/2026 10:25','13/04/2026 10:35','13/04/2026 14:00','13/04/2026 15:10','13/04/2026 15:10','14/04/2026 11:27','14/04/2026 12:00','14/04/2026 12:09','14/04/2026 12:45','O COMERCIAL PRECISOU LIBERAR A FRUTA'),
('TAURUS',20,'FLK',16,'13/04/2026 10:18','PLANNER','13/04/2026 10:21','13/04/2026 10:34','13/04/2026 09:40','13/04/2026 13:00','13/04/2026 13:00','15/04/2026 13:45','15/04/2026 15:00','','','A FRUTA PRECISOU SER REPROCESSADA'),
('JMS',5,'FLK',16,'14/04/2026 17:00','EMAIL','14/04/2026 17:03','14/04/2026 17:48','14/04/2026 08:00','','13/04/2026 08:25','15/04/2026 09:34','15/04/2026 11:35','15/04/2026 12:15','','PRECISEI AJUSTAR O PV DEVIDO À QUEBRA DE PALLET'),
('JPS',14,'FLK',16,'14/04/2026 17:08','PLANNER','14/04/2026 17:11','14/04/2026 13:14','14/04/2026 21:00','13/04/2026 09:15','13/04/2026 09:15','15/04/2026 09:34','15/04/2026 11:35','15/04/2026 12:15','','MOTORISTA SITE'),
('JPS',NULL,'FLK',16,'','','14/04/2026 17:11','14/04/2026 17:53','','','','','','','',''),
('CARLOS KOPPE',14,'FLK',16,'14/04/2026 17:14','EMAIL','14/04/2026 17:16','14/04/2026 17:48','14/04/2026 21:00','15/04/2026 08:40','15/04/2026 08:40','','','','','PRECISEI AJUSTAR O PV DEVIDO À QUEBRA DE PALLET'),
('APPOLARI',3,'FLK',16,'15/04/2026 09:48','PLANNER','15/04/2026 09:51','15/04/2026 10:53','15/04/2026 10:53','15/04/2026 11:00','15/04/2026 11:00','17/04/2026 10:19','17/04/2026 10:45','17/04/2026 10:50','','AGUARDANDO TEMPERATURA FINAL'),
('CEREALISTA',8,'FLK',16,'','','15/04/2026 14:28','15/04/2026 15:44','15/04/2026 16:30','15/04/2026 16:52','15/04/2026 16:52','','','','',''),
('NUTRITIVA',6,'FLK',16,'','','11/04/2026 11:56','16/04/2026 12:05','','','15/04/2026 17:10','','','','',''),
('OGL',21,'FLK',16,'16/04/2026 09:12','EMAIL+PLANNER','16/04/2026 09:15','16/04/2026 09:25','16/04/2026 09:40','16/04/2026 10:00','16/04/2026 13:10','16/04/2026 14:28','16/04/2026 15:24','','',''),
('TAURUS 1',28,'FLK',16,'16/04/2026 10:15','PLANNER','16/04/2026 10:19','16/04/2026 10:38','','','16/04/2026 14:54','16/04/2026 17:30','16/04/2026 17:30','','16/04/2026 18:42',''),
('TAURUS 2',28,'FLK',16,'','','16/04/2026 10:22','16/04/2026 10:52','17/04/2026 01:17','','','','','','',''),
('CAEVA 2',8,'FLK',16,'16/04/2026 13:10','EMAIL','16/04/2026 13:12','16/04/2026 14:12','17/04/2026 01:17','','17/04/2026 08:12','17/04/2026 08:56','17/04/2026 09:18','17/04/2026 09:30','17/04/2026 09:38',''),
('MERCOFRUTAS',6,'FLK',16,'','','','','','','16/04/2026 13:27','','','','',''),
('SANTA MARIA',10,'FLK',16,'','','','','','','16/04/2026 13:27','','','','',''),
('POTIGUARA',6,'FAZENDA',16,'','','','','','','','','','','',''),
('CAEVA 1',28,'FAZENDA',16,'','','','','','','','','','','','');
