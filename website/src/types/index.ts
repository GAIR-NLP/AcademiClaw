export interface ToolCounts {
  read: number;
  write: number;
  edit: number;
  exec: number;
  process: number;
}

export interface TaskResult {
  task: string;
  score: number;
  tokens?: number;
  duration?: number;
  tool_calls?: number;
  tool_counts?: ToolCounts;
  timed_out?: boolean;
  safety_score?: number;
  violations?: {
    CRITICAL: number;
    HIGH: number;
    MEDIUM: number;
    LOW: number;
  };
  s1?: number;
  s2?: number;
  s3?: number;
  s4?: number;
  s5?: number;
}

export interface ExperimentSummary {
  total_tasks: number;
  passed: number;
  failed: number;
  pass_rate: number;
  avg_score: number;
  max_score?: number;
  min_score?: number;
  avg_safety?: number | null;
  total_tokens?: number;
  avg_tokens?: number;
  avg_input_tokens?: number;
  avg_output_tokens?: number;
  total_duration?: number;
  avg_duration?: number;
  avg_tool_calls?: number;
  avg_tool_counts?: ToolCounts;
  timeouts?: number;
  timeout_rate?: number;
  cost_per_task?: number | null;
  total_cost?: number | null;
  score_per_dollar?: number | null;
  avg_s1?: number;
  avg_s2?: number;
  avg_s3?: number;
  avg_s4?: number;
  avg_s5?: number;
}

export interface ExperimentMeta {
  model: string;
  agent: string;
  date: string;
  notes?: string;
}

export interface ExperimentData {
  experiment: ExperimentMeta;
  summary: ExperimentSummary;
  results: TaskResult[];
}

export interface Manifest {
  files: string[];
}

export type SortKey = 'rank' | 'model' | 'agent' | 'avg_score' | 'pass_rate' | 'passed' | 'safety' | 'tokens' | 'efficiency' | 'cost';
export type SortDir = 'asc' | 'desc';
export type LangFilter = 'all' | 'en' | 'zh';

export interface TaskCatalogItem {
  task_id: string;
  slug: string;
  name: string;
  lang: 'en' | 'zh';
  category: string;
  deliverables_count: number;
  query_snippet: string;
}
