import type { Conjugations } from '../types/verb'

const persons = ['ich', 'du', 'er', 'wir', 'ihr', 'sie'] as const

export default function ConjugationTable({
  conjugations,
}: {
  conjugations?: Conjugations
}) {
  const indikativ = conjugations?.indikativ

  if (!indikativ) {
    return <p>暂无变位信息</p>
  }

  return (
    <table border={1} cellPadding={6} style={{ marginTop: 8 }}>
      <thead>
        <tr>
          <th></th>
          <th>现在时</th>
          <th>过去时</th>
          <th>完成时</th>
        </tr>
      </thead>
      <tbody>
        {persons.map(p => (
          <tr key={p}>
            <td>{p}</td>
            <td>{indikativ.prasens?.[p] || '—'}</td>
            <td>{indikativ.prateritum?.[p] || '—'}</td>
            <td>{indikativ.perfekt?.[p] || '—'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
