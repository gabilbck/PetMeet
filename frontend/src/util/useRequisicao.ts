/** Busca dados da API com estados de carregamento, erro e recarga manual. */

import { useCallback, useEffect, useRef, useState } from 'react'
import { ErroApi } from '../api/cliente'

interface Resultado<T> {
  dados: T | null
  carregando: boolean
  erro: string | null
  recarregar: () => void
}

export function useRequisicao<T>(buscar: () => Promise<T>, dependencias: unknown[]): Resultado<T> {
  const [dados, setDados] = useState<T | null>(null)
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState<string | null>(null)
  const [tentativa, setTentativa] = useState(0)

  // A funcao muda de identidade a cada render; guardamos a ultima versao e
  // reexecutamos apenas quando as dependencias declaradas mudarem.
  const buscarRef = useRef(buscar)
  buscarRef.current = buscar

  useEffect(() => {
    let ativo = true
    setCarregando(true)
    setErro(null)

    buscarRef
      .current()
      .then((resposta) => {
        if (ativo) setDados(resposta)
      })
      .catch((problema: unknown) => {
        if (!ativo) return
        // 401 ja derruba a sessao no cliente; nao vale poluir a tela com erro.
        if (problema instanceof ErroApi && problema.status === 401) return
        setErro(problema instanceof Error ? problema.message : 'Erro inesperado.')
      })
      .finally(() => {
        if (ativo) setCarregando(false)
      })

    return () => {
      ativo = false
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...dependencias, tentativa])

  const recarregar = useCallback(() => setTentativa((valor) => valor + 1), [])

  return { dados, carregando, erro, recarregar }
}
