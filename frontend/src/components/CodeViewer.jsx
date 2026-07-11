import { useState } from 'react';
import './CodeViewer.css';

export default function CodeViewer({ code }) {
  const [copied, setCopied] = useState(false);

  if (!code) return null;

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = code;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }

  return (
    <div className="code-viewer glass-card fade-in">
      <div className="code-viewer__header">
        <div className="code-viewer__title-area">
          <div className="code-viewer__window-controls">
            <span className="code-viewer__window-dot code-viewer__window-dot--red"></span>
            <span className="code-viewer__window-dot code-viewer__window-dot--yellow"></span>
            <span className="code-viewer__window-dot code-viewer__window-dot--green"></span>
          </div>
          <span className="code-viewer__title">Generated Code</span>
        </div>
        <button className="code-viewer__copy-btn" onClick={handleCopy}>
          {copied ? (
            <>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              Copied
            </>
          ) : (
            <>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
              </svg>
              Copy
            </>
          )}
        </button>
      </div>
      <div className="code-viewer__body">
        <pre className="code-viewer__pre">
          <code>{code}</code>
        </pre>
      </div>
    </div>
  );
}
