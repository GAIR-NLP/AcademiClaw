import type { TaskCatalogItem } from '../types/index.ts';
import { Package } from 'lucide-react';

interface TaskCardProps {
  task: TaskCatalogItem;
}

export default function TaskCard({ task }: TaskCardProps) {
  return (
    <div className="task-card card card-hover">
      <div className="task-card__tags">
        <span className="task-card__tag task-card__tag--lang">
          {task.lang === 'en' ? 'English' : 'Chinese'}
        </span>
        {task.category && (
          <span className="task-card__tag task-card__tag--category">
            {task.category}
          </span>
        )}
      </div>

      <h3 className="task-card__title">{task.name}</h3>

      {task.query_snippet && (
        <p className="task-card__snippet">{task.query_snippet}</p>
      )}

      <div className="task-card__footer">
        <Package size={14} />
        <span>{task.deliverables_count} deliverable{task.deliverables_count !== 1 ? 's' : ''}</span>
      </div>
    </div>
  );
}
