export type Person = 'ich' | 'du' | 'er' | 'wir' | 'ihr' | 'sie'

export interface Tense {
  ich?: string
  du?: string
  er?: string
  wir?: string
  ihr?: string
  sie?: string
}

export interface Indikativ {
  prasens?: Tense
  prateritum?: Tense
  perfekt?: Tense
}

export interface Conjugations {
  indikativ?: Indikativ
}

export interface Verb {
  id: number
  word: string
  meaning: string
  conjugations?: Conjugations
}
