import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { App } from './App'
import { ProvedorAuth } from './auth/ContextoAuth'
import './estilos/base.css'
import './estilos/componentes.css'

const raiz = document.getElementById('raiz')
if (!raiz) throw new Error('Elemento #raiz nao encontrado em index.html')

createRoot(raiz).render(
  <StrictMode>
    <BrowserRouter>
      <ProvedorAuth>
        <App />
      </ProvedorAuth>
    </BrowserRouter>
  </StrictMode>,
)
