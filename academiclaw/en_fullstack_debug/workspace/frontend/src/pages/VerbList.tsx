import { useEffect, useState } from 'react'
import { fetchVerbs } from '../api/verbs'
import type { Verb } from '../types/verb'
import VerbItem from '../components/VerbItem'
import AddVerbModal from '../components/AddVerbModal'

interface Props {
  onBack: () => void
}

export default function VerbList({ onBack }: Props) {
  const [verbs, setVerbs] = useState<Verb[]>([])
  const [showAdd, setShowAdd] = useState(false)

  useEffect(() => {
    fetchVerbs().then(setVerbs)
  }, [])

  return (
    <div>
      <button onClick={onBack}>← 返回</button>
      <h2>动词列表</h2>

      <button onClick={() => setShowAdd(true)}>＋ 添加动词</button>

      <ul>
        {verbs.map(v => (
          <VerbItem key={v.id} verb={v} />
        ))}
      </ul>

      {showAdd && (
        <AddVerbModal
          onClose={() => setShowAdd(false)}
          onCreated={v => setVerbs(prev => [...prev, v])}
        />
      )}
    </div>
  )
}
