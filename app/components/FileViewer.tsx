'use client';

import { useState } from 'react';
import { StoredFile } from '@/app/types';

interface FileViewerProps {
  files: StoredFile[];
  onFileSelect?: (file: StoredFile | null) => void;
}

function jsonToCsv(jsonData: any[]): string {
  if (jsonData.length === 0) return '';
  
  const headers = Object.keys(jsonData[0]);
  const csvHeaders = headers.map(h => `"${h}"`).join(',');
  
  const csvRows = jsonData.map(row =>
    headers.map(header => {
      const value = row[header];
      if (value === null || value === undefined) return '';
      const stringValue = String(value).replace(/"/g, '""');
      return `"${stringValue}"`;
    }).join(',')
  );
  
  return [csvHeaders, ...csvRows].join('\n');
}

export function FileViewer({ files, onFileSelect }: FileViewerProps) {
  const [expandedFileId, setExpandedFileId] = useState<number | null>(null);
  const [downloadFormat, setDownloadFormat] = useState<'json' | 'csv'>('json');

  const getFileNameFromPath = (filepath: string) => {
    return filepath.split('/').pop() || 'file';
  };

  const handleDownload = async (file: StoredFile, format: 'json' | 'csv') => {
    try {
      const fileName = getFileNameFromPath(file.filepath);
      const fileUrl = `http://localhost:8001/api/media/${fileName}`;
      
      const response = await fetch(fileUrl);
      if (!response.ok) throw new Error('Failed to fetch file');
      
      let data: string;
      let mimeType: string;
      let extension: string;
      
      if (format === 'csv') {
        const jsonData = await response.json();
        data = jsonToCsv(jsonData);
        mimeType = 'text/csv';
        extension = 'csv';
      } else {
        data = await response.text();
        mimeType = 'application/json';
        extension = 'json';
      }
      
      const blob = new Blob([data], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${fileName.replace('.json', '')}.${extension}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
      alert(`Failed to download file: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  return (
    <div className="p-4 border rounded-lg">
      <h2 className="text-lg font-bold mb-2">Stored Files</h2>
      {files.length === 0 ? (
        <p className="text-gray-500">No files yet</p>
      ) : (
        <ul className="space-y-2">
          {files.map((file) => {
            const fileName = getFileNameFromPath(file.filepath);
            const isExpanded = expandedFileId === file.id;
            
            return (
              <li key={file.id} className="border rounded p-2">
                <div className="flex justify-between items-center">
                  <button
                    onClick={() => {
                      setExpandedFileId(isExpanded ? null : file.id);
                      if (onFileSelect) onFileSelect(isExpanded ? null : file);
                    }}
                    className="flex-1 text-left text-sm font-medium hover:underline"
                  >
                    {fileName}
                  </button>
                </div>
                {isExpanded && (
                  <div className="mt-2 pt-2 border-t space-y-2">
                    <div className="flex gap-2 items-center">
                      <select
                        value={downloadFormat}
                        onChange={(e) => setDownloadFormat(e.target.value as 'json' | 'csv')}
                        className="px-2 py-1 border rounded text-sm"
                      >
                        <option value="json">JSON</option>
                        <option value="csv">CSV</option>
                      </select>
                      <button
                        onClick={() => handleDownload(file, downloadFormat)}
                        className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
                      >
                        Download
                      </button>
                    </div>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
