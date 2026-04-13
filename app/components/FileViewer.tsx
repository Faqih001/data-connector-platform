'use client';

import { useState, useEffect } from 'react';
import { StoredFile } from '@/app/types';

interface FileViewerProps {
  files: StoredFile[];
  onFileSelect?: (file: StoredFile | null) => void;
}

interface DeletedFile {
  file: StoredFile;
  deletedAt: number; // timestamp
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
  const [selectedFiles, setSelectedFiles] = useState<Set<number>>(new Set());
  const [deletedFiles, setDeletedFiles] = useState<DeletedFile[]>([]);
  const [visibleFiles, setVisibleFiles] = useState<StoredFile[]>(files);

  // Update visible files when input files change
  useEffect(() => {
    setVisibleFiles(files);
  }, [files]);

  // Clean up expired deleted files (5 minute window)
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setDeletedFiles(prev => 
        prev.filter(item => now - item.deletedAt < 5 * 60 * 1000)
      );
    }, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const getFileNameFromPath = (filepath: string) => {
    return filepath.split('/').pop() || 'file';
  };

  const handleSelectFile = (fileId: number) => {
    const newSelected = new Set(selectedFiles);
    if (newSelected.has(fileId)) {
      newSelected.delete(fileId);
    } else {
      newSelected.add(fileId);
    }
    setSelectedFiles(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedFiles.size === visibleFiles.length) {
      setSelectedFiles(new Set());
    } else {
      setSelectedFiles(new Set(visibleFiles.map(f => f.id)));
    }
  };

  const handleDeleteFiles = () => {
    if (selectedFiles.size === 0) return;
    
    const filesToDelete = visibleFiles.filter(f => selectedFiles.has(f.id));
    
    // Move to deleted files with timestamp
    setDeletedFiles(prev => [
      ...prev,
      ...filesToDelete.map(file => ({
        file,
        deletedAt: Date.now()
      }))
    ]);

    // Remove from visible files
    setVisibleFiles(prev => 
      prev.filter(f => !selectedFiles.has(f.id))
    );

    // Clear selection
    setSelectedFiles(new Set());
  };

  const handleRestoreFile = (deletedFile: DeletedFile) => {
    // Add back to visible files
    setVisibleFiles(prev => [...prev, deletedFile.file]);
    
    // Remove from deleted files
    setDeletedFiles(prev => 
      prev.filter(item => item.file.id !== deletedFile.file.id)
    );
  };

  const getTimeRemaining = (deletedAt: number): string => {
    const elapsed = Date.now() - deletedAt;
    const remaining = Math.max(0, 5 * 60 * 1000 - elapsed);
    const seconds = Math.ceil(remaining / 1000);
    return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
  };

  const handleDownload = async (file: StoredFile, format: 'json' | 'csv') => {
    try {
      const fileName = getFileNameFromPath(file.filepath);
      const fileUrl = `http://localhost:8001/api/files/${file.id}/download/`;
      
      const response = await fetch(fileUrl);
      if (!response.ok) throw new Error('Failed to fetch file');
      
      const jsonData = await response.json();
      
      let data: string;
      let mimeType: string;
      let extension: string;
      
      if (format === 'csv') {
        data = jsonToCsv(jsonData);
        mimeType = 'text/csv';
        extension = 'csv';
      } else {
        data = JSON.stringify(jsonData, null, 2);
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
      <h2 className="text-lg font-bold mb-4">Stored Files</h2>
      
      {visibleFiles.length === 0 && deletedFiles.length === 0 ? (
        <p className="text-gray-500">No files yet</p>
      ) : (
        <>
          {/* Active Files Section */}
          {visibleFiles.length > 0 && (
            <div className="mb-6">
              <div className="flex items-center gap-3 mb-3 p-3 bg-gray-50 rounded">
                <input
                  type="checkbox"
                  checked={selectedFiles.size === visibleFiles.length && visibleFiles.length > 0}
                  onChange={handleSelectAll}
                  className="w-4 h-4"
                  title="Select all files"
                />
                <span className="text-sm font-medium">
                  {selectedFiles.size > 0 
                    ? `${selectedFiles.size} selected` 
                    : `${visibleFiles.length} file${visibleFiles.length !== 1 ? 's' : ''}`}
                </span>
                {selectedFiles.size > 0 && (
                  <button
                    onClick={handleDeleteFiles}
                    className="ml-auto px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
                  >
                    Delete Selected ({selectedFiles.size})
                  </button>
                )}
              </div>

              <ul className="space-y-2">
                {visibleFiles.map((file) => {
                  const fileName = getFileNameFromPath(file.filepath);
                  const isExpanded = expandedFileId === file.id;
                  const isSelected = selectedFiles.has(file.id);
                  
                  return (
                    <li key={file.id} className={`border rounded p-3 ${isSelected ? 'bg-blue-50 border-blue-300' : ''}`}>
                      <div className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => handleSelectFile(file.id)}
                          className="w-4 h-4 mt-1"
                        />
                        <div className="flex-1">
                          <button
                            onClick={() => {
                              setExpandedFileId(isExpanded ? null : file.id);
                              if (onFileSelect) onFileSelect(isExpanded ? null : file);
                            }}
                            className="text-left text-sm font-medium hover:underline"
                          >
                            {fileName}
                          </button>
                          <div className="text-xs text-gray-500 mt-1">
                            Format: <span className="font-medium uppercase">{file.format_type || 'json'}</span>
                          </div>
                        </div>
                      </div>
                      {isExpanded && (
                        <div className="mt-3 pt-3 border-t space-y-2 ml-7">
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
            </div>
          )}

          {/* Deleted Files Section (5-minute restoration window) */}
          {deletedFiles.length > 0 && (
            <div className="mt-6 pt-6 border-t">
              <h3 className="text-sm font-bold mb-3 text-orange-600">🗑️ Recently Deleted (Restore within 5 minutes)</h3>
              <ul className="space-y-2">
                {deletedFiles.map((item) => {
                  const fileName = getFileNameFromPath(item.file.filepath);
                  const timeReading = getTimeRemaining(item.deletedAt);
                  
                  return (
                    <li key={`deleted-${item.file.id}`} className="border border-orange-200 rounded p-2 bg-orange-50 flex items-center justify-between">
                      <div className="flex-1">
                        <p className="text-sm text-gray-600">{fileName}</p>
                        <p className="text-xs text-orange-600 font-medium">Time remaining: {timeReading}</p>
                      </div>
                      <button
                        onClick={() => handleRestoreFile(item)}
                        className="ml-3 px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600 whitespace-nowrap"
                      >
                        Restore
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
}
