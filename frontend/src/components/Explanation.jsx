import './Explanation.css';

/**
 * Displays a human-readable explanation of what the cleansing engine did.
 * @param {{ text: string }} props
 */
export default function Explanation({ text }) {
  if (!text) return null;

  return (
    <div className="explanation glass-card fade-in">
      <div className="explanation__header">
        <span className="explanation__header-icon" aria-hidden="true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
            <rect x="8" y="2" width="8" height="4" rx="1" ry="1" />
          </svg>
        </span>
        <span className="explanation__header-title">What was done</span>
      </div>
      <p className="explanation__text">{text}</p>
    </div>
  );
}
