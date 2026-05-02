function LobsterIcon({ size = 22 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      {/* Left claw */}
      <path
        d="M8 12 C4 8, 2 14, 6 18 L14 26"
        stroke="currentColor"
        strokeWidth="3.5"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M6 18 C2 16, 0 22, 5 24 L14 26"
        stroke="currentColor"
        strokeWidth="3.5"
        strokeLinecap="round"
        fill="none"
      />
      {/* Left arm */}
      <path
        d="M14 26 L22 32"
        stroke="currentColor"
        strokeWidth="3.5"
        strokeLinecap="round"
      />
      {/* Right claw */}
      <path
        d="M56 12 C60 8, 62 14, 58 18 L50 26"
        stroke="currentColor"
        strokeWidth="3.5"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M58 18 C62 16, 64 22, 59 24 L50 26"
        stroke="currentColor"
        strokeWidth="3.5"
        strokeLinecap="round"
        fill="none"
      />
      {/* Right arm */}
      <path
        d="M50 26 L42 32"
        stroke="currentColor"
        strokeWidth="3.5"
        strokeLinecap="round"
      />
      {/* Body */}
      <ellipse cx="32" cy="38" rx="12" ry="10" fill="currentColor" opacity="0.15" />
      <ellipse cx="32" cy="38" rx="12" ry="10" stroke="currentColor" strokeWidth="3" fill="none" />
      {/* Head */}
      <circle cx="32" cy="27" r="5" fill="currentColor" opacity="0.2" />
      <circle cx="32" cy="27" r="5" stroke="currentColor" strokeWidth="2.5" fill="none" />
      {/* Eyes */}
      <circle cx="30" cy="25.5" r="1.2" fill="currentColor" />
      <circle cx="34" cy="25.5" r="1.2" fill="currentColor" />
      {/* Tail segments */}
      <path
        d="M32 48 L32 52 M28 53 L32 56 L36 53"
        stroke="currentColor"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Legs */}
      <path d="M24 40 L16 46" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <path d="M25 44 L18 50" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <path d="M40 40 L48 46" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <path d="M39 44 L46 50" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

interface NavbarProps {
  activePage?: 'leaderboard' | 'tasks';
}

export default function Navbar({ activePage = 'leaderboard' }: NavbarProps) {
  return (
    <nav className="navbar">
      <div className="navbar__inner">
        <a href="#leaderboard" className="navbar__brand">
          <LobsterIcon size={22} />
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
