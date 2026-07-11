import './Warnings.css';

/**
 * Amber validation-warnings banner.
 * Renders nothing when there are no warnings.
 * @param {{ warnings: string[] }} props
 */
export default function Warnings({ warnings = [] }) {
  if (!warnings.length) return null;

  return (
    <div className="warnings fade-in">
      <div className="warnings__header">
        <span className="warnings__header-icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
        </span>
        <span className="warnings__header-title">Validation Warnings</span>
      </div>
      <ul className="warnings__list">
        {warnings.map((msg, index) => (
          <li className="warnings__item" key={index}>
            {msg}
          </li>
        ))}
      </ul>
    </div>
  );
}
