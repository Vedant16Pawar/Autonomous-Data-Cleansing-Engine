import { useState } from 'react';
import './InstructionInput.css';

export default function InstructionInput({ onSubmit, disabled }) {
  const [instruction, setInstruction] = useState('');

  function handleSubmit() {
    if (instruction.trim() && !disabled) {
      onSubmit(instruction.trim());
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }

  return (
    <div className="instruction-input fade-in">
      <textarea
        className="instruction-input__textarea"
        placeholder="e.g. Remove duplicate rows, fill missing ages with the median, normalize email addresses"
        value={instruction}
        onChange={(e) => setInstruction(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        rows={3}
      />
      <div className="instruction-input__footer">
        <span className="instruction-input__hint">Enter to run, Shift + Enter for new line</span>
        <button
          className="btn-primary instruction-input__btn"
          onClick={handleSubmit}
          disabled={disabled || !instruction.trim()}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="5,3 19,12 5,21" />
          </svg>
          Run Cleaning
        </button>
      </div>
    </div>
  );
}
