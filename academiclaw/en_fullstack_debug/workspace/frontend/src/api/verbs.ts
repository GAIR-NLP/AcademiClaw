import axios from 'axios'
import type { Verb } from '../types/verb'

const BASE_URL = 'http://localhost:8002'

export async function fetchVerbs(): Promise<Verb[]> {
  const res = await axios.get(`${BASE_URL}/verbs`)
  return res.data
}

export async function createVerb(payload: Partial<Verb>): Promise<Verb> {
  const res = await axios.post(`${BASE_URL}/verbs`, payload)
  return res.data
}
