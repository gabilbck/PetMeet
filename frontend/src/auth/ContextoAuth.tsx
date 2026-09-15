/**
 * Sessao do usuario.
 *
 * O token emitido pelo backend carrega apenas {"sub": email, "exp": ...}
 * (app/core/seguranca.py). Nao ha rota /auth/me nem o perfil dentro do token,
 * entao o front sabe quem esta logado, mas nao se a pessoa e admin ou
 * voluntaria: as telas restritas tratam o 403 da API como a resposta.
 */

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import { EVENTO_SESSAO_EXPIRADA, apagarToken, gravarToken, lerToken } from '../api/cliente'
import { autenticacao } from '../api/recursos'

interface Sessao {
  email: string | null
  autenticado: boolean
  entrar: (email: string, senha: string) => Promise<void>
  sair: () => void
}

const ContextoAuth = createContext<Sessao | null>(null)

interface CargaToken {
  sub?: string
  exp?: number
}

function lerCargaDoToken(token: string): CargaToken | null {
  const partes = token.split('.')
  if (partes.length !== 3) return null
  try {
    const base64 = partes[1].replace(/-/g, '+').replace(/_/g, '/')
    const preenchido = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), '=')
    const bytes = Uint8Array.from(atob(preenchido), (caractere) => caractere.charCodeAt(0))
    return JSON.parse(new TextDecoder().decode(bytes)) as CargaToken
  } catch {
    return null
  }
}

function emailDeTokenValido(token: string | null): string | null {
  if (!token) return null
  const carga = lerCargaDoToken(token)
  if (!carga?.sub) return null
  // Token ja vencido: nem tenta usar, vai direto para o login.
  if (carga.exp && carga.exp * 1000 <= Date.now()) return null
  return carga.sub
}

export function ProvedorAuth({ children }: { children: ReactNode }) {
  const [email, setEmail] = useState<string | null>(() => emailDeTokenValido(lerToken()))

  useEffect(() => {
    if (!email) apagarToken()
  }, [email])

  useEffect(() => {
    const aoExpirar = () => setEmail(null)
    window.addEventListener(EVENTO_SESSAO_EXPIRADA, aoExpirar)
    return () => window.removeEventListener(EVENTO_SESSAO_EXPIRADA, aoExpirar)
  }, [])

  const entrar = useCallback(async (usuario: string, senha: string) => {
    const resposta = await autenticacao.entrar(usuario, senha)
    gravarToken(resposta.access_token)
    setEmail(emailDeTokenValido(resposta.access_token) ?? usuario)
  }, [])

  const sair = useCallback(() => {
    apagarToken()
    setEmail(null)
  }, [])

  const valor = useMemo<Sessao>(
    () => ({ email, autenticado: email !== null, entrar, sair }),
    [email, entrar, sair],
  )

  return <ContextoAuth.Provider value={valor}>{children}</ContextoAuth.Provider>
}

// O hook mora junto do provedor de proposito: sao a mesma peca. O aviso abaixo
// e so sobre recarga a quente durante o desenvolvimento.
// eslint-disable-next-line react-refresh/only-export-components
export function useAuth(): Sessao {
  const sessao = useContext(ContextoAuth)
  if (!sessao) throw new Error('useAuth precisa estar dentro de ProvedorAuth')
  return sessao
}
