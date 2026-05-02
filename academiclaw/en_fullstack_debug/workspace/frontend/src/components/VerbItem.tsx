import { useState } from 'react'
import type { Verb } from '../types/verb'
import ConjugationTable from './ConjugationTable'

export default function VerbItem({ verb }: { verb: Verb }) {
  const [open, setOpen] = useState(false)

  return (
    <li style={{ marginBottom: 12 }}>
      <strong>{verb.word}</strong> — {verb.meaning}
      <br />
      <button onClick={() => setOpen(o => !o)}>
        {open ? '隐藏变位' : '查看变位'}
      </button>

      {open && <ConjugationTable conjugations={verb.conjugations} />}
    </li>
  )
}
