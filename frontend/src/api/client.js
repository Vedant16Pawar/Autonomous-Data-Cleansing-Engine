const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function uploadCSV(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Upload failed");
  }

  return response.json();
}

export async function previewCSV(fileId) {
  const response = await fetch(`${API_BASE}/preview/${fileId}`);

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Preview failed");
  }

  return response.json();
}

export async function cleanCSV(fileId, instruction) {
  const response = await fetch(`${API_BASE}/clean`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      file_id: fileId,
      instruction: instruction,
    }),
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Cleaning failed");
  }

  return response.json();
}

export function getDownloadURL(outputPath) {
  return `${API_BASE}/download?path=${encodeURIComponent(outputPath)}`;
}
