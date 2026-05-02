interface Props {
  onEnterVerbs: () => void
}

export default function Home({ onEnterVerbs }: Props) {
  return (
    <div>
      <h1>自定义德语单词本</h1>

      <div style={{ display: 'flex', gap: 12 }}>
        <button onClick={onEnterVerbs}>动词</button>
        <button disabled>名词</button>
        <button disabled>形容词</button>
        <button disabled>介词</button>
        <button disabled>副词</button>
      </div>
    </div>
  )
}
