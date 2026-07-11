import './SummaryMetrics.css';

/**
 * Row of three summary metric cards.
 * @param {{
 *   inputRows: number,
 *   outputRows: number,
 *   validationWarnings: string[]
 * }} props
 */
export default function SummaryMetrics({
  inputRows = 0,
  outputRows = 0,
  validationWarnings = [],
}) {
  const rowDiff = inputRows - outputRows;
  const warningCount = validationWarnings.length;

  return (
    <div className="metrics-grid fade-in">
      {/* ---- Original Rows ---- */}
      <div className="summary-metric glass-card">
        <span className="summary-metric__icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        </span>
        <div className="summary-metric__body">
          <span className="summary-metric__label">Original Rows</span>
          <span className="summary-metric__value">
            {inputRows.toLocaleString()}
          </span>
        </div>
      </div>

      {/* ---- Cleaned Rows ---- */}
      <div className="summary-metric glass-card">
        <span className="summary-metric__icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="18" cy="18" r="3" />
            <circle cx="6" cy="6" r="3" />
            <circle cx="6" cy="18" r="3" />
            <path d="M18 15V9a4 4 0 0 0-4-4H9" />
            <line x1="6" y1="9" x2="6" y2="15" />
          </svg>
        </span>
        <div className="summary-metric__body">
          <span className="summary-metric__label">Cleaned Rows</span>
          <span className="summary-metric__value">
            {outputRows.toLocaleString()}
          </span>
          {rowDiff > 0 && (
            <span className="summary-metric__badge summary-metric__badge--error">
              ↓ {rowDiff.toLocaleString()} removed
            </span>
          )}
        </div>
      </div>

      {/* ---- Warnings ---- */}
      <div className="summary-metric glass-card">
        <span className="summary-metric__icon" aria-hidden="true">
          {warningCount === 0 ? (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--color-success)' }}>
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--color-warning)' }}>
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
              <line x1="12" y1="9" x2="12" y2="13" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
          )}
        </span>
        <div className="summary-metric__body">
          <span className="summary-metric__label">Warnings</span>
          <span className="summary-metric__value">{warningCount}</span>
          {warningCount === 0 ? (
            <span className="summary-metric__badge summary-metric__badge--success">
              All checks passed
            </span>
          ) : (
            <span className="summary-metric__badge summary-metric__badge--warning">
              {warningCount} warning{warningCount !== 1 ? 's' : ''} found
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
