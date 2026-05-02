interface NavbarProps {
  activePage?: 'leaderboard' | 'tasks';
}

export default function Navbar({ activePage = 'leaderboard' }: NavbarProps) {
  return (
    <nav className="navbar">
      <div className="navbar__inner">
        <a href="#leaderboard" className="navbar__brand">
          <img
            src={`${import.meta.env.BASE_URL}icon-512.png`}
            alt=""
            width={28}
            height={28}
            className="navbar__brand-icon"
          />
          AcademiClaw
        </a>
        <ul className="navbar__links">
          <li>
            <a
              href="#leaderboard"
              className={activePage === 'leaderboard' ? 'navbar__link--active' : ''}
            >
              Leaderboard
            </a>
          </li>
          <li>
            <a
              href="#tasks"
              className={activePage === 'tasks' ? 'navbar__link--active' : ''}
            >
              Tasks
            </a>
          </li>
          <li>
            <a href="#" aria-disabled="true" title="Paper link coming soon">
              Paper
            </a>
          </li>
          <li>
            <a
              href="https://github.com/GAIR-NLP/AcademiClaw"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
}
