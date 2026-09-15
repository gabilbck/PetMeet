/** Pecas visuais reaproveitadas por todas as telas. */

import { useState } from 'react'
import type { ReactNode } from 'react'
import { urlDeMidia } from '../api/cliente'
import { formatarCpf, mascararCpf } from '../util/formato'
import type { Tom } from '../util/formato'

/* --- Selo de estado ---------------------------------------------------- */

export function Selo({ tom = 'neutro', children }: { tom?: Tom; children: ReactNode }) {
  return (
    <span className="selo" data-tom={tom}>
      {children}
    </span>
  )
}

/* --- Aviso ------------------------------------------------------------- */

interface AvisoProps {
  tom?: 'erro' | 'sucesso' | 'atencao'
  children: ReactNode
}

export function Aviso({ tom = 'erro', children }: AvisoProps) {
  return (
    <div className="aviso" data-tom={tom} role={tom === 'erro' ? 'alert' : 'status'}>
      {children}
    </div>
  )
}

/* --- Espaco da foto ----------------------------------------------------- */

interface MolduraProps {
  url: string | null
  nome: string
  formato?: 'grade' | 'retrato'
}

/**
 * Reserva o lugar da imagem mesmo quando ela ainda nao existe: hachura de
 * ficha em branco com a inicial do animal. Uma ficha sem foto continua sendo
 * uma ficha, e fica visivel que falta subir a foto.
 */
export function Moldura({ url, nome, formato = 'grade' }: MolduraProps) {
  const endereco = urlDeMidia(url)
  const classe = `moldura ${formato === 'retrato' ? 'moldura-retrato' : 'moldura-grade'}`

  if (endereco) {
    return (
      <div className={classe}>
        <img src={endereco} alt={`Foto de ${nome}`} loading="lazy" />
      </div>
    )
  }

  return (
    <div className={classe}>
      <div className="moldura-vazia" aria-hidden="true">
        <span className="moldura-inicial">{nome.trim().charAt(0).toUpperCase() || '?'}</span>
      </div>
      <span className="so-leitor-tela">{nome} ainda não tem foto</span>
    </div>
  )
}

/* --- Dado pessoal ------------------------------------------------------- */

/**
 * CPF fica coberto ate alguem precisar dele (RN07/RNF03). Quem confere uma
 * lista na tela raramente precisa do numero inteiro, e ombro alheio le rapido.
 */
export function Cpf({ valor }: { valor: string }) {
  const [revelado, setRevelado] = useState(false)

  return (
    <span className="dado-sigiloso">
      <span className="numero-tabular">{revelado ? formatarCpf(valor) : mascararCpf(valor)}</span>
      <button
        type="button"
        className="botao"
        data-tipo="texto"
        onClick={() => setRevelado((atual) => !atual)}
      >
        {revelado ? 'ocultar' : 'mostrar'}
      </button>
    </span>
  )
}

/* --- Estados de lista --------------------------------------------------- */

export function Carregando({ texto = 'Carregando…' }: { texto?: string }) {
  return (
    <p className="carregando" role="status">
      {texto}
    </p>
  )
}

interface EstadoVazioProps {
  titulo: string
  descricao: string
  acao?: ReactNode
}

/** Tela vazia e convite para agir, nao lamento. */
export function EstadoVazio({ titulo, descricao, acao }: EstadoVazioProps) {
  return (
    <div className="vazio">
      <h3>{titulo}</h3>
      <p>{descricao}</p>
      {acao}
    </div>
  )
}

/* --- Paginacao ---------------------------------------------------------- */

interface PaginacaoProps {
  pagina: number
  tamanhoPagina: number
  total: number
  aoMudar: (pagina: number) => void
}

export function Paginacao({ pagina, tamanhoPagina, total, aoMudar }: PaginacaoProps) {
  const ultimaPagina = Math.max(1, Math.ceil(total / tamanhoPagina))
  if (total === 0) return null

  const primeiro = (pagina - 1) * tamanhoPagina + 1
  const ultimo = Math.min(pagina * tamanhoPagina, total)

  return (
    <div className="paginacao">
      <span className="paginacao-contagem">
        {primeiro}–{ultimo} de {total}
      </span>
      <div className="paginacao-botoes">
        <button
          type="button"
          className="botao"
          data-tipo="contorno"
          onClick={() => aoMudar(pagina - 1)}
          disabled={pagina <= 1}
        >
          Anterior
        </button>
        <button
          type="button"
          className="botao"
          data-tipo="contorno"
          onClick={() => aoMudar(pagina + 1)}
          disabled={pagina >= ultimaPagina}
        >
          Próxima
        </button>
      </div>
    </div>
  )
}

/* --- Cabecalho de pagina ------------------------------------------------ */

interface CabecalhoProps {
  titulo: string
  descricao?: string
  acao?: ReactNode
}

export function CabecalhoPagina({ titulo, descricao, acao }: CabecalhoProps) {
  return (
    <header className="cabecalho-pagina">
      <div>
        <h1>{titulo}</h1>
        {descricao ? <p className="descricao">{descricao}</p> : null}
      </div>
      {acao}
    </header>
  )
}

/* --- Sobreposicao ------------------------------------------------------- */

interface SobreposicaoProps {
  titulo: string
  aoFechar: () => void
  children: ReactNode
}

export function Sobreposicao({ titulo, aoFechar, children }: SobreposicaoProps) {
  return (
    <div
      className="sobreposicao"
      role="dialog"
      aria-modal="true"
      aria-label={titulo}
      onClick={(evento) => {
        if (evento.target === evento.currentTarget) aoFechar()
      }}
    >
      <div className="painel-flutuante">
        <h2>{titulo}</h2>
        {children}
      </div>
    </div>
  )
}
