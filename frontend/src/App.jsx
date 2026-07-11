import { useState, useEffect } from 'react';
import './App.css';

// Components
import Header from './components/Header';
import UploadZone from './components/UploadZone';
import InstructionInput from './components/InstructionInput';
import ProgressStepper from './components/ProgressStepper';
import SummaryMetrics from './components/SummaryMetrics';
import DataPreview from './components/DataPreview';
import Explanation from './components/Explanation';
import CodeViewer from './components/CodeViewer';
import Warnings from './components/Warnings';
import ActionBar from './components/ActionBar';

// API Client
import { uploadCSV, previewCSV, cleanCSV, getDownloadURL } from './api/client';

function App() {
  const [status, setStatus] = useState('idle'); // 'idle' | 'uploading' | 'uploaded' | 'processing' | 'done' | 'error'
  const [fileId, setFileId] = useState(null);
  const [fileName, setFileName] = useState(null);
  const [fileStats, setFileStats] = useState(null);
  
  const [previewBefore, setPreviewBefore] = useState([]);
  const [previewColumns, setPreviewColumns] = useState([]);
  
  const [currentStep, setCurrentStep] = useState(0);
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Stepper simulation timer
  useEffect(() => {
    let timer;
    if (status === 'processing') {
      // Simulate stepper progress every 2.5 seconds
      timer = setInterval(() => {
        setCurrentStep((prev) => (prev < 2 ? prev + 1 : prev));
      }, 2500);
    } else {
      setCurrentStep(0);
    }
    return () => clearInterval(timer);
  }, [status]);

  async function handleUpload(file) {
    setStatus('uploading');
    setErrorMessage(null);
    try {
      // 1. Upload the CSV file
      const uploadRes = await uploadCSV(file);
      const newFileId = uploadRes.file_id;
      
      // 2. Fetch the CSV preview
      const previewRes = await previewCSV(newFileId);
      
      setFileId(newFileId);
      setFileName(file.name);
      setFileStats({
        totalRows: previewRes.total_rows,
        totalColumns: previewRes.total_columns
      });
      setPreviewColumns(previewRes.columns);
      setPreviewBefore(previewRes.rows);
      setStatus('uploaded');
    } catch (err) {
      console.error(err);
      setErrorMessage(err.message || 'Failed to upload or preview file.');
      setStatus('error');
    }
  }

  async function handleClean(instruction) {
    setStatus('processing');
    setErrorMessage(null);
    setCurrentStep(0); // Start at Inspecting

    try {
      // Trigger cleaning
      const cleanRes = await cleanCSV(fileId, instruction);
      
      // Wait a tiny bit if execution is extremely fast to ensure they see the flow transition
      await new Promise((resolve) => setTimeout(resolve, 800));

      // Force stepper to final validating step just before displaying
      setCurrentStep(3);
      await new Promise((resolve) => setTimeout(resolve, 600));

      setResult(cleanRes);
      setStatus('done');
    } catch (err) {
      console.error(err);
      setErrorMessage(err.message || 'Cleaning execution failed. Please verify the instruction or try again.');
      setStatus('error');
    }
  }

  function handleReset() {
    setResult(null);
    setStatus('uploaded');
  }

  function handleFullReset() {
    setFileId(null);
    setFileName(null);
    setFileStats(null);
    setPreviewBefore([]);
    setPreviewColumns([]);
    setResult(null);
    setStatus('idle');
  }

  return (
    <div className="app-container">
      <Header />

      {/* Upload Zone */}
      <UploadZone
        onUpload={handleUpload}
        fileInfo={fileName ? {
          fileName,
          totalRows: fileStats?.totalRows || 0,
          totalColumns: fileStats?.totalColumns || 0
        } : null}
        disabled={status === 'uploading' || status === 'processing'}
      />


      {/* Error Message */}
      {status === 'error' && errorMessage && (
        <div className="error-message fade-in">
          <span>⚠️</span>
          <div>
            <strong>Error:</strong> {errorMessage}
          </div>
        </div>
      )}

      {/* Instruction Input */}
      {status === 'uploaded' && (
        <InstructionInput
          onSubmit={handleClean}
          disabled={status === 'processing'}
        />
      )}

      {/* Progress Stepper */}
      {status === 'processing' && (
        <ProgressStepper currentStep={currentStep} />
      )}

      {/* Results View */}
      {status === 'done' && result && (
        <div className="results-container">
          {/* Summary Stats Grid */}
          <SummaryMetrics
            inputRows={fileStats?.totalRows || 0}
            outputRows={result.output_row_count}
            validationWarnings={result.validation_warnings}
          />

          {/* Before / After Preview tables */}
          <DataPreview
            beforeRows={previewBefore}
            afterRows={result.output_preview_rows}
            columns={previewColumns}
          />

          {/* Explanation Text */}
          <Explanation text={result.explanation} />

          {/* Validation Warnings */}
          <Warnings warnings={result.validation_warnings} />

          {/* Generated Code */}
          <CodeViewer code={result.generated_code} />

          {/* Actions */}
          <ActionBar
            downloadUrl={getDownloadURL(result.output_path)}
            onReset={handleReset}
          />
        </div>
      )}

      {/* Back button to go back to upload if needed */}
      {(status === 'uploaded' || status === 'error' || status === 'done') && (
        <div style={{ textAlign: 'center', marginTop: '24px' }}>
          <button
            className="btn-secondary"
            onClick={handleFullReset}
            style={{ padding: '8px 16px', fontSize: '0.85rem' }}
          >
            ← Upload Different File
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
