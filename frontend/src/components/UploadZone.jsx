import { useRef, useState } from 'react';
import './UploadZone.css';

export default function UploadZone({ onUpload, fileInfo, disabled }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  function handleDragOver(e) {
    e.preventDefault();
    setIsDragging(true);
  }

  function handleDragLeave() {
    setIsDragging(false);
  }

  function handleDrop(e) {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.name.toLowerCase().endsWith('.csv')) {
      onUpload(file);
    }
  }

  function handleClick() {
    if (!disabled) inputRef.current?.click();
  }

  function handleFileChange(e) {
    const file = e.target.files[0];
    if (file) onUpload(file);
  }

  return (
    <div className="upload-zone fade-in">
      <div
        className={`upload-zone__droparea glass-card ${isDragging ? 'upload-zone__droparea--active' : ''} ${fileInfo ? 'upload-zone__droparea--uploaded' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="upload-zone__input"
          disabled={disabled}
        />

        {fileInfo ? (
          <div className="upload-zone__file-info">
            <div className="upload-zone__file-icon">📄</div>
            <div className="upload-zone__file-name">{fileInfo.fileName}</div>
            <div className="upload-zone__file-stats">
              {fileInfo.totalRows.toLocaleString()} rows · {fileInfo.totalColumns} columns
            </div>
          </div>
        ) : (
          <div className="upload-zone__placeholder">
            <div className="upload-zone__upload-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
            </div>
            <div className="upload-zone__text">
              Drop your CSV here or <span className="upload-zone__browse">browse</span>
            </div>
            <div className="upload-zone__hint">Supports .csv files</div>
          </div>
        )}
      </div>
    </div>
  );
}
