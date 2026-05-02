import { useMemo, useState } from 'react'
import { createVerb } from '../api/verbs'
import type { Verb, Conjugations, Tense } from '../types/verb'

interface Props {
  onClose: () => void
  onCreated: (verb: Verb) => void
}

type TenseKey = 'prasens' | 'prateritum' | 'perfekt'
type PersonKey = 'ich' | 'du' | 'er' | 'wir' | 'ihr' | 'sie'

const PERSONS: PersonKey[] = ['ich', 'du', 'er', 'wir', 'ihr', 'sie']
const TENSES: { key: TenseKey; label: string }[] = [
  { key: 'prasens', label: '现在时' },
  { key: 'prateritum', label: '过去时' },
  { key: 'perfekt', label: '完成时' },
]

function makeEmptyTense(): Tense {
  return { ich: '', du: '', er: '', wir: '', ihr: '', sie: '' }
}

export default function AddVerbModal({ onClose, onCreated }: Props) {
  const [word, setWord] = useState('')
  const [meaning, setMeaning] = useState('')

  // 18 个输入框：3 个时态 * 6 个人称
  const [forms, setForms] = useState<Record<TenseKey, Tense>>({
    prasens: makeEmptyTense(),
    prateritum: makeEmptyTense(),
    perfekt: makeEmptyTense(),
  })

  const canSubmit = useMemo(() => word.trim() !== '' && meaning.trim() !== '', [word, meaning])

  function setFormValue(tense: TenseKey, person: PersonKey, value: string) {
    setForms(prev => ({
      ...prev,
      [tense]: {
        ...prev[tense],
        [person]: value,
      },
    }))
  }

  function toOptionalTense(t: Tense): Tense | undefined {
    // 全空则不传（保持可选）
    const cleaned: Tense = {
      ich: t.ich?.trim() || undefined,
      du: t.du?.trim() || undefined,
      er: t.er?.trim() || undefined,
      wir: t.wir?.trim() || undefined,
      ihr: t.ihr?.trim() || undefined,
      sie: t.sie?.trim() || undefined,
    }
    const hasAny = Object.values(cleaned).some(v => v && v.length > 0)
    return hasAny ? cleaned : undefined
  }

  async function submit() {
    if (!canSubmit) return

    const prasens = toOptionalTense(forms.prasens)
    const prateritum = toOptionalTense(forms.prateritum)
    const perfekt = toOptionalTense(forms.perfekt)

    let conjugations: Conjugations | undefined = undefined
    if (prasens || prateritum || perfekt) {
      conjugations = {
        indikativ: {
          prasens,
          prateritum,
          perfekt,
        },
      }
    }

    const verb = await createVerb({
      word: word.trim(),
      meaning: meaning.trim(),
      conjugations,
    })

    onCreated(verb)
    onClose()
  }

  return (
    <div style={{ border: '1px solid #ccc', padding: 12, marginTop: 12 }}>
      <h3>新增动词</h3>

      <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
        <input
          placeholder="动词（必填）"
          value={word}
          onChange={e => setWord(e.target.value)}
          style={{ flex: 1 }}
        />
        <input
          placeholder="中文（必填）"
          value={meaning}
          onChange={e => setMeaning(e.target.value)}
          style={{ flex: 1 }}
        />
      </div>

      <div style={{ marginTop: 8 }}>
        <div style={{ fontWeight: 600, marginBottom: 6 }}>动词变位（可选）</div>

        <table border={1} cellPadding={6} style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ width: 80 }}></th>
              {TENSES.map(t => (
                <th key={t.key}>{t.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {PERSONS.map(p => (
              <tr key={p}>
                <td style={{ fontWeight: 600 }}>{p}</td>
                {TENSES.map(t => (
                  <td key={t.key}>
                    <input
                      value={forms[t.key][p] ?? ''}
                      onChange={e => setFormValue(t.key, p, e.target.value)}
                      placeholder="—"
                      style={{ width: '100%' }}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ marginTop: 10, display: 'flex', gap: 8 }}>
        <button onClick={submit} disabled={!canSubmit}>
          提交
        </button>
        <button onClick={onClose}>取消</button>
      </div>

      {!canSubmit && (
        <div style={{ marginTop: 6, fontSize: 12 }}>
          提示：动词和中文为必填；变位可留空。
        </div>
      )}
    </div>
  )
}
