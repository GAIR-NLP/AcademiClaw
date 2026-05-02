import { useState } from 'react'
import Home from './pages/Home'
import VerbList from './pages/VerbList'

export default function App() {
  const [page, setPage] = useState<'home' | 'verbs'>('home')

  return (
    <div style={{ padding: 20 }}>
      {page === 'home' && <Home onEnterVerbs={() => setPage('verbs')} />}
      {page === 'verbs' && <VerbList onBack={() => setPage('home')} />}
    </div>
  )
}
