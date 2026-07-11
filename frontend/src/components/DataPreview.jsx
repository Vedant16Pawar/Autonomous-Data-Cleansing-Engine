import './DataPreview.css';

export default function DataPreview({ beforeRows, afterRows, columns }) {
  if (!beforeRows || beforeRows.length === 0) return null;

  // Detect which cells changed between before and after
  function getCellClass(rowIdx, col, side) {
    if (side === 'before') {
      const val = beforeRows[rowIdx]?.[col];
      // Highlight nulls/empty in before
      if (val === '' || val === null || val === undefined) {
        return 'data-preview__cell--null';
      }
      return '';
    }

    if (side === 'after') {
      if (rowIdx >= (afterRows?.length || 0)) return '';
      
      const afterRow = afterRows[rowIdx];
      const afterVal = afterRow?.[col];
      
      // Align row with original dataset using ID columns if present
      const idCol = columns.find(c => ['id', 'userid', 'user_id', 'index'].includes(c.toLowerCase()));
      let beforeRow = beforeRows[rowIdx];
      
      if (idCol && afterRow) {
        const afterId = afterRow[idCol];
        const match = beforeRows.find(r => String(r[idCol]) === String(afterId));
        if (match) beforeRow = match;
      }
      
      const beforeVal = beforeRow?.[col];

      // Highlight cells that changed
      if (beforeVal !== afterVal && afterVal !== '' && afterVal !== null && beforeVal !== undefined) {
        return 'data-preview__cell--changed';
      }
      return '';
    }

    return '';
  }

  return (
    <div className="data-preview fade-in">
      {/* Before Table */}
      <div className="data-preview__panel">
        <div className="data-preview__header data-preview__header--before">
          <div className="data-preview__window-controls">
            <span className="data-preview__window-dot"></span>
          </div>
          <span className="data-preview__header-title">Before (Original Dataset)</span>
        </div>
        <div className="data-preview__table-wrap">
          <table className="data-preview__table">
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {beforeRows.map((row, rowIdx) => (
                <tr key={rowIdx}>
                  {columns.map((col) => (
                    <td
                      key={col}
                      className={getCellClass(rowIdx, col, 'before')}
                    >
                      {row[col] === '' || row[col] === null || row[col] === undefined
                        ? <span className="data-preview__null-tag">Ø NULL</span>
                        : String(row[col])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Arrow */}
      <div className="data-preview__arrow">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <line x1="5" y1="12" x2="19" y2="12" />
          <polyline points="12 5 19 12 12 19" />
        </svg>
      </div>

      {/* After Table */}
      <div className="data-preview__panel">
        <div className="data-preview__header data-preview__header--after">
          <div className="data-preview__window-controls">
            <span className="data-preview__window-dot"></span>
          </div>
          <span className="data-preview__header-title">After (Cleaned Dataset)</span>
        </div>
        <div className="data-preview__table-wrap">
          <table className="data-preview__table">
            <thead>
              <tr>
                {columns.map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(afterRows || []).map((row, rowIdx) => (
                <tr key={rowIdx}>
                  {columns.map((col) => (
                    <td
                      key={col}
                      className={getCellClass(rowIdx, col, 'after')}
                    >
                      {String(row[col] ?? '')}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
