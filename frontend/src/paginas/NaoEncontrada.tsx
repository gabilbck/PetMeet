import { Link } from 'react-router-dom'
import { CabecalhoPagina, EstadoVazio } from '../componentes/Interface'

export function NaoEncontrada() {
  return (
    <>
      <CabecalhoPagina titulo="Página não encontrada" />
      <EstadoVazio
        titulo="Este endereço não existe no painel"
        descricao="O link pode estar desatualizado. Volte ao painel e siga pelo menu."
        acao={
          <Link to="/" className="botao">
            Ir para o painel
          </Link>
        }
      />
    </>
  )
}
