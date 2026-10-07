-- ====================================================================
-- MIGRAÇÃO DATE HACK v2: Nuvem, Privacidade RLS e Dashboard de Gestão
-- Execute este script no SQL Editor do Supabase (qqxjrfrtomyaozzfbqcc)
-- ====================================================================

-- 1. NOVAS COLUNAS NA TABELA public.usuarios_licenciados
ALTER TABLE public.usuarios_licenciados
  ADD COLUMN IF NOT EXISTS plano TEXT DEFAULT 'vitalicio',
  ADD COLUMN IF NOT EXISTS limite_convites INTEGER DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS data_expiracao TIMESTAMPTZ DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS valor_pago NUMERIC(10,2) DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS origem_venda TEXT DEFAULT 'manual',
  ADD COLUMN IF NOT EXISTS ultimo_acesso TIMESTAMPTZ DEFAULT NOW();

-- 2. NOVA TABELA public.convites
CREATE TABLE IF NOT EXISTS public.convites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  titulo TEXT NOT NULL,
  dados TEXT NOT NULL,
  link_gerado TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_convites_user_id ON public.convites(user_id);
CREATE INDEX IF NOT EXISTS idx_convites_created_at ON public.convites(created_at);

-- 3. FUNÇÃO AUXILIAR is_admin() (SECURITY DEFINER)
-- Evita recursão infinita nas policies RLS
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
STABLE
AS $$
  SELECT COALESCE(
    (SELECT is_admin FROM public.usuarios_licenciados WHERE auth_user_id = auth.uid() LIMIT 1),
    false
  );
$$;

-- 4. POLÍTICAS RLS PARA public.convites
-- PRIVACIDADE TOTAL: Cada usuário só manipula e vê seus próprios convites.
-- O Admin NÃO TEM policy para visualizar os convites de outros clientes!
ALTER TABLE public.convites ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "convites_user_isolation" ON public.convites;

CREATE POLICY "convites_user_isolation"
ON public.convites
FOR ALL
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

-- 5. POLÍTICAS RLS PARA public.usuarios_licenciados
ALTER TABLE public.usuarios_licenciados ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "licenciados_select_policy" ON public.usuarios_licenciados;
DROP POLICY IF EXISTS "licenciados_admin_insert" ON public.usuarios_licenciados;
DROP POLICY IF EXISTS "licenciados_admin_update" ON public.usuarios_licenciados;
DROP POLICY IF EXISTS "licenciados_admin_delete" ON public.usuarios_licenciados;
DROP POLICY IF EXISTS "licenciados_user_update_ultimo_acesso" ON public.usuarios_licenciados;

-- Cliente comum lê apenas sua própria linha; Admin lê todas
CREATE POLICY "licenciados_select_policy"
ON public.usuarios_licenciados
FOR SELECT
TO authenticated
USING (auth_user_id = auth.uid() OR public.is_admin());

-- Somente admin insere
CREATE POLICY "licenciados_admin_insert"
ON public.usuarios_licenciados
FOR INSERT
TO authenticated
WITH CHECK (public.is_admin());

-- Somente admin altera campos cadastrais/administrativos
CREATE POLICY "licenciados_admin_update"
ON public.usuarios_licenciados
FOR UPDATE
TO authenticated
USING (public.is_admin())
WITH CHECK (public.is_admin());

-- Próprio usuário atualiza apenas o seu próprio ultimo_acesso
CREATE POLICY "licenciados_user_update_ultimo_acesso"
ON public.usuarios_licenciados
FOR UPDATE
TO authenticated
USING (auth_user_id = auth.uid())
WITH CHECK (auth_user_id = auth.uid());

-- Somente admin pode deletar licenças
CREATE POLICY "licenciados_admin_delete"
ON public.usuarios_licenciados
FOR DELETE
TO authenticated
USING (public.is_admin());

-- 6. RPCs DE AGREGAÇÃO PARA O ADMIN (NUNCA EXPÕEM DADOS NEM LINKS DE CLIENTES)

-- RPC 6.1: Métricas Gerais (KPIs)
CREATE OR REPLACE FUNCTION public.admin_get_metrics(p_days INTEGER DEFAULT 30)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_is_adm BOOLEAN;
  v_total_clientes INT;
  v_ativos INT;
  v_suspensos INT;
  v_expirando_7d INT;
  v_novos_7d INT;
  v_novos_30d INT;
  v_faturamento NUMERIC(10,2);
  v_ticket_medio NUMERIC(10,2);
  v_convites_geral INT;
  v_convites_hoje INT;
  v_convites_7d INT;
  v_convites_30d INT;
  v_media_convites NUMERIC(10,2);
BEGIN
  -- Validar se o requisitante é admin
  SELECT public.is_admin() INTO v_is_adm;
  IF NOT v_is_adm THEN
    RAISE EXCEPTION 'Acesso negado: apenas administradores podem visualizar metricas.';
  END IF;

  -- Clientes
  SELECT COUNT(*) INTO v_total_clientes FROM public.usuarios_licenciados;
  SELECT COUNT(*) INTO v_ativos FROM public.usuarios_licenciados WHERE ativo = true;
  SELECT COUNT(*) INTO v_suspensos FROM public.usuarios_licenciados WHERE ativo = false;
  SELECT COUNT(*) INTO v_expirando_7d FROM public.usuarios_licenciados
    WHERE data_expiracao IS NOT NULL
      AND data_expiracao >= NOW()
      AND data_expiracao <= NOW() + INTERVAL '7 days';
  SELECT COUNT(*) INTO v_novos_7d FROM public.usuarios_licenciados WHERE data_liberacao >= NOW() - INTERVAL '7 days';
  SELECT COUNT(*) INTO v_novos_30d FROM public.usuarios_licenciados WHERE data_liberacao >= NOW() - INTERVAL '30 days';

  -- Financeiro
  SELECT COALESCE(SUM(valor_pago), 0) INTO v_faturamento FROM public.usuarios_licenciados;
  IF v_total_clientes > 0 THEN
    v_ticket_medio := ROUND(v_faturamento / v_total_clientes, 2);
  ELSE
    v_ticket_medio := 0;
  END IF;

  -- Convites (apenas contagens numéricas agregadas!)
  SELECT COUNT(*) INTO v_convites_geral FROM public.convites;
  SELECT COUNT(*) INTO v_convites_hoje FROM public.convites WHERE created_at >= date_trunc('day', NOW());
  SELECT COUNT(*) INTO v_convites_7d FROM public.convites WHERE created_at >= NOW() - INTERVAL '7 days';
  SELECT COUNT(*) INTO v_convites_30d FROM public.convites WHERE created_at >= NOW() - INTERVAL '30 days';

  IF v_total_clientes > 0 THEN
    v_media_convites := ROUND(v_convites_geral::NUMERIC / v_total_clientes, 2);
  ELSE
    v_media_convites := 0;
  END IF;

  RETURN jsonb_build_object(
    'total_clientes', v_total_clientes,
    'clientes_ativos', v_ativos,
    'clientes_suspensos', v_suspensos,
    'clientes_expirando_7d', v_expirando_7d,
    'novos_clientes_7d', v_novos_7d,
    'novos_clientes_30d', v_novos_30d,
    'faturamento_total', v_faturamento,
    'ticket_medio', v_ticket_medio,
    'total_convites_geral', v_convites_geral,
    'total_convites_hoje', v_convites_hoje,
    'total_convites_7d', v_convites_7d,
    'total_convites_30d', v_convites_30d,
    'media_convites_por_cliente', v_media_convites
  );
END;
$$;

-- RPC 6.2: Dados dos Gráficos (Agregações numéricas por período)
CREATE OR REPLACE FUNCTION public.admin_get_chart_data(p_days INTEGER DEFAULT 30)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_is_adm BOOLEAN;
  v_convites_dia JSONB;
  v_clientes_semana JSONB;
  v_faturamento_mes JSONB;
  v_top_clientes JSONB;
BEGIN
  SELECT public.is_admin() INTO v_is_adm;
  IF NOT v_is_adm THEN
    RAISE EXCEPTION 'Acesso negado.';
  END IF;

  -- Convites por dia (últimos p_days dias)
  SELECT COALESCE(jsonb_agg(d), '[]'::jsonb) INTO v_convites_dia
  FROM (
    SELECT
      to_char(day::date, 'DD/MM') AS label,
      to_char(day::date, 'YYYY-MM-DD') AS date_key,
      COUNT(c.id)::INT AS count
    FROM generate_series(
      (NOW() - (p_days || ' days')::INTERVAL)::date,
      NOW()::date,
      '1 day'::interval
    ) AS day
    LEFT JOIN public.convites c ON date_trunc('day', c.created_at) = day
    GROUP BY day
    ORDER BY day ASC
  ) d;

  -- Novos clientes por semana (últimas 6 semanas)
  SELECT COALESCE(jsonb_agg(s), '[]'::jsonb) INTO v_clientes_semana
  FROM (
    SELECT
      to_char(date_trunc('week', u.data_liberacao), 'DD/MM') AS label,
      COUNT(*)::INT AS count
    FROM public.usuarios_licenciados u
    WHERE u.data_liberacao >= NOW() - INTERVAL '6 weeks'
    GROUP BY date_trunc('week', u.data_liberacao)
    ORDER BY date_trunc('week', u.data_liberacao) ASC
  ) s;

  -- Faturamento por mês (últimos 6 meses)
  SELECT COALESCE(jsonb_agg(m), '[]'::jsonb) INTO v_faturamento_mes
  FROM (
    SELECT
      to_char(date_trunc('month', u.data_liberacao), 'Mon/YY') AS label,
      COALESCE(SUM(u.valor_pago), 0)::NUMERIC AS total
    FROM public.usuarios_licenciados u
    WHERE u.data_liberacao >= NOW() - INTERVAL '6 months'
    GROUP BY date_trunc('month', u.data_liberacao)
    ORDER BY date_trunc('month', u.data_liberacao) ASC
  ) m;

  -- Top 10 clientes por volume de convites (apenas nomes/iniciais e contagem)
  SELECT COALESCE(jsonb_agg(t), '[]'::jsonb) INTO v_top_clientes
  FROM (
    SELECT
      COALESCE(u.nome, split_part(u.email, '@', 1)) AS nome,
      COUNT(c.id)::INT AS total
    FROM public.convites c
    JOIN public.usuarios_licenciados u ON u.auth_user_id = c.user_id
    GROUP BY u.nome, u.email
    ORDER BY total DESC
    LIMIT 10
  ) t;

  RETURN jsonb_build_object(
    'convites_dia', v_convites_dia,
    'clientes_semana', v_clientes_semana,
    'faturamento_mes', v_faturamento_mes,
    'top_clientes', v_top_clientes
  );
END;
$$;

-- RPC 6.3: Contagem de convites por usuário (para a tabela de clientes)
CREATE OR REPLACE FUNCTION public.admin_get_user_invite_counts()
RETURNS TABLE (
  auth_user_id UUID,
  total_convites BIGINT
)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  IF NOT public.is_admin() THEN
    RAISE EXCEPTION 'Acesso negado.';
  END IF;

  RETURN QUERY
    SELECT c.user_id AS auth_user_id, COUNT(c.id) AS total_convites
    FROM public.convites c
    GROUP BY c.user_id;
END;
$$;

-- RPC 6.4: Listas Rápidas do Dashboard Executivo
CREATE OR REPLACE FUNCTION public.admin_get_quick_lists()
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_sem_convites JSONB;
  v_inativos_14d JSONB;
  v_expirando_breve JSONB;
BEGIN
  IF NOT public.is_admin() THEN
    RAISE EXCEPTION 'Acesso negado.';
  END IF;

  -- Clientes sem convites criados (nunca usaram)
  SELECT COALESCE(jsonb_agg(x), '[]'::jsonb) INTO v_sem_convites
  FROM (
    SELECT u.id, u.nome, u.email, u.data_liberacao
    FROM public.usuarios_licenciados u
    LEFT JOIN public.convites c ON c.user_id = u.auth_user_id
    WHERE c.id IS NULL
    ORDER BY u.data_liberacao DESC
    LIMIT 6
  ) x;

  -- Clientes inativos há mais de 14 dias
  SELECT COALESCE(jsonb_agg(x), '[]'::jsonb) INTO v_inativos_14d
  FROM (
    SELECT u.id, u.nome, u.email, u.ultimo_acesso
    FROM public.usuarios_licenciados u
    WHERE u.ultimo_acesso < NOW() - INTERVAL '14 days'
    ORDER BY u.ultimo_acesso ASC
    LIMIT 6
  ) x;

  -- Acessos perto de expirar (próximos 7 dias)
  SELECT COALESCE(jsonb_agg(x), '[]'::jsonb) INTO v_expirando_breve
  FROM (
    SELECT u.id, u.nome, u.email, u.data_expiracao
    FROM public.usuarios_licenciados u
    WHERE u.data_expiracao IS NOT NULL
      AND u.data_expiracao >= NOW()
      AND u.data_expiracao <= NOW() + INTERVAL '7 days'
    ORDER BY u.data_expiracao ASC
    LIMIT 6
  ) x;

  RETURN jsonb_build_object(
    'sem_convites', v_sem_convites,
    'inativos_14d', v_inativos_14d,
    'expirando_breve', v_expirando_breve
  );
END;
$$;

-- 7. TRIGGER PARA ATUALIZAR updated_at EM convites
CREATE OR REPLACE FUNCTION public.trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_convites_updated_at ON public.convites;
CREATE TRIGGER set_convites_updated_at
BEFORE UPDATE ON public.convites
FOR EACH ROW
EXECUTE FUNCTION public.trigger_set_timestamp();
