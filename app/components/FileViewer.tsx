'use client';

import { useState, useEffect } from 'react';
import { StoredFile, User } from '@/app/types';
import { API_URL } from '@/app/lib/api';

interface FileViewerProps {
  files: StoredFile[];
  onFileSelect?: (file: StoredFile | null) => void;
  currentUser?: User;
}

interface DeletedFile {
  file: StoredFile;
  deletedAt: number;
}

interface FileAccess {
  is_owner: boolean;
  is_admin: boolean;
  is_shared_with_me: boolean;
  can_modify: boolean;
  can_share: boolean;
  access_level: string;
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

export function FileViewer({ files, onFileSelect, currentUser }: FileViewerProps) {
  const [expandedFileId, setExpandedFileId] = useState<number | null>(null);
  const [downloadFormat, setDownloadFormat] = useState<'json' | 'csv'>('json');
  const [selectedFiles, setSelectedFiles] = useState<Set<number>>(new Set());
  const [deletedFiles, setDeletedFiles] = useState<DeletedFile[]>([]);
  const [visibleFiles, setVisibleFiles] = useState<StoredFile[]>(files);
  const [fileAccess, setFileAccess] = useState<Record<number, FileAccess>>({});
  const [shareModal, setShareModal] = useState<{ open: boolean; fileId: number | null }>({ open: false, fileId: null });
  const [shareEmail, setShareEmail] = useState('');
  const [loadingShare, setLoadingShare] = useState(false);
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [selectedUsers, setSelectedUsers] = useState<Set<number>>(new Set());
  const [searchLoading, setSearchLoading] = useState(false);

  // Update visible files when input files change
  useEffect(() => {
    setVisibleFiles(files);
    // Fetch access levels for all files
    files.forEach(file => {
      fetchFileAccess(file.id);
    });
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

  const fetchFileAccess = async (fileId: number) => {
    try {
      const response = await fetch(`${API_URL}/files/${fileId}/permissions/`, {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setFileAccess(prev => ({
          ...prev,
          [fileId]: data
        }));
      }
    } catch (error) {
      console.error('Failed to fetch file access:', error);
    }
  };

  const getFileNameFromPath = (filepath: string) => {
    return filepath.split('/').pop() || 'file';
  };

  const getAccessBadge = (file: StoredFile) => {
    const access = fileAccess[file.id];
    if (!access) return null;

    if (access.is_admin) {
      return <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">👑 Admin</span>;
    } else if (access.is_owner) {
      return <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">🔒 Owner</span>;
    } else if (access.is_shared_with_me) {
      return <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">📤 Shared</span>;
    }
    return null;
  };

  const handleSelectFile = (fileId: number) => {
    const access = fileAccess[fileId];
    if (access && !access.can_modify) {
      return; // Don't allow selection if can't modify
    }

    const newSelected = new Set(selectedFiles);
    if (newSelected.has(fileId)) {
      newSelected.delete(fileId);
    } else {
      newSelected.add(fileId);
    }
    setSelectedFiles(newSelected);
  };

  const handleSelectAll = () => {
    const modifiableFiles = visibleFiles.filter(f => {
      const access = fileAccess[f.id];
      return access?.can_modify;
    });

    if (selectedFiles.size === modifiableFiles.length) {
      setSelectedFiles(new Set());
    } else {
      setSelectedFiles(new Set(modifiableFiles.map(f => f.id)));
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

  const handleShareClick = (fileId: number) => {
    setShareModal({ open: true, fileId });
    setShareEmail('');
    setSearchResults([]);
    setSelectedUsers(new Set());
  };

  const handleSearchUsers = async (query: string) => {
    setShareEmail(query);
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }

    setSearchLoading(true);
    try {
      const response = await fetch(`${API_URL}/search-users/?q=${encodeURIComponent(query)}`, {
        credentials: 'include'
      });
      const data = await response.json();
      setSearchResults(data.results || []);
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const toggleUserSelection = (userId: number) => {
    const newSelected = new Set(selectedUsers);
    if (newSelected.has(userId)) {
      newSelected.delete(userId);
    } else {
      newSelected.add(userId);
    }
    setSelectedUsers(newSelected);
  };

  const handleShare = async () => {
    if (!shareModal.fileId || selectedUsers.size === 0) {
      alert('Please select at least one user to share with');
      return;
    }

    setLoadingShare(true);
    try {
      const response = await fetch(`${API_URL}/files/${shareModal.fileId}/share/`, {
        credentials: 'include',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_ids: Array.from(selectedUsers) })
      });

      if (response.ok) {
        alert('✅ File shared successfully!');
        setShareModal({ open: false, fileId: null });
        setSearchResults([]);
        setSelectedUsers(new Set());
        setShareEmail('');
        if (shareModal.fileId) {
          fetchFileAccess(shareModal.fileId);
        }
      } else {
        alert('Failed to share file');
      }
    } catch (error) {
      alert('Failed to share file: ' + error);
    } finally {
      setLoadingShare(false);
    }
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
      
      const response = await fetch(fileUrl, {
        credentials: 'include'
      });
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
    <div className="p-4 border rounded-lg bg-white shadow-sm">
      <h2 className="text-base sm:text-lg font-bold mb-3">Stored Files</h2>
      
      {visibleFiles.length === 0 && deletedFiles.length === 0 ? (
        <p className="text-gray-500 text-sm">No files yet</p>
      ) : (
        <>
          {/* Active Files Section */}
          {visibleFiles.length > 0 && (
            <div className="mb-6">
              <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-3 p-2 sm:p-3 bg-gray-50 rounded text-sm">
                <input
                  type="checkbox"
                  checked={selectedFiles.size === visibleFiles.length && visibleFiles.length > 0}
                  onChange={handleSelectAll}
                  className="w-4 h-4"
                  title="Select all files"
                />
                <span className="text-xs sm:text-sm font-medium">
                  {selectedFiles.size > 0 
                    ? `${selectedFiles.size} selected` 
                    : `${visibleFiles.length} file${visibleFiles.length !== 1 ? 's' : ''}`}
                </span>
                {selectedFiles.size > 0 && (
                  <button
                    onClick={handleDeleteFiles}
                    className="sm:ml-auto px-3 py-1 bg-red-500 text-white rounded text-xs hover:bg-red-600 transition"
                  >
                    Delete ({selectedFiles.size})
                  </button>
                )}
              </div>

              <ul className="space-y-2">
                {visibleFiles.map((file) => {
                  const fileName = getFileNameFromPath(file.filepath);
                  const isExpanded = expandedFileId === file.id;
                  const isSelected = selectedFiles.has(file.id);
                  const access = fileAccess[file.id];
                  
                  return (
                    <li key={file.id} className={`border rounded p-2 sm:p-3 text-xs sm:text-sm ${isSelected ? 'bg-blue-50 border-blue-300' : ''}`}>
                      <div className="flex items-start gap-2">
                        {access?.can_modify && (
                          <input
                            type="checkbox"
                            checked={isSelected}
                            onChange={() => handleSelectFile(file.id)}
                            className="w-4 h-4 mt-1 flex-shrink-0"
                          />
                        )}
                        <div className="flex-1 min-w-0">
                          <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2 mb-1 flex-wrap">
                            <button
                              onClick={() => {
                                setExpandedFileId(isExpanded ? null : file.id);
                                if (onFileSelect) onFileSelect(isExpanded ? null : file);
                              }}
                              className="text-left text-xs sm:text-sm font-medium hover:underline break-words"
                            >
                              {fileName}
                            </button>
                            {getAccessBadge(file)}
                          </div>
                          {file.user && (
                            <p className="text-xs text-gray-500">👤 {file.user.username || 'Unknown'}</p>
                          )}
                          {file.shared_with && file.shared_with.length > 0 && (
                            <p className="text-xs text-green-600">📤 Shared with {file.shared_with.length}</p>
                          )}
                          <div className="text-xs text-gray-500 mt-1">
                            Format: <span className="font-medium uppercase">{file.format_type || 'json'}</span>
                          </div>
                        </div>
                        <div className="flex gap-1">
                          {access?.can_share && (
                            <button
                              onClick={() => handleShareClick(file.id)}
                              className="px-2 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600"
                              title="Share file"
                            >
                              📤
                            </button>
                          )}
                        </div>
                      </div>
                      {isExpanded && (
                        <div className="mt-3 pt-3 border-t space-y-2 ml-7">
                          {access && (
                            <div className="text-xs text-gray-600 mb-2 p-2 bg-gray-50 rounded">
                              <p><strong>Access:</strong> {access.access_level.toUpperCase()} | Modify: {access.can_modify ? '✅' : '❌'} | Share: {access.can_share ? '✅' : '❌'}</p>
                            </div>
                          )}
                          <div className="flex gap-2 items-center">
                            <select
                              value={downloadFormat}
                              onChange={(e) => setDownloadFormat(e.target.value as 'json' | 'csv')}
                              className="px-2 py-1 border rounded text-sm"
                              disabled={!access?.can_modify}
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

      {shareModal.open && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 shadow-lg max-h-96 overflow-y-auto">
            <h3 className="text-lg font-bold mb-4">📤 Share File</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-semibold mb-2">Search Users</label>
              <input
                type="text"
                placeholder="Search by email or username..."
                value={shareEmail}
                onChange={(e) => handleSearchUsers(e.target.value)}
                className="w-full border rounded p-2 mb-2"
              />
              
              {searchLoading && (
                <p className="text-sm text-gray-500">Searching...</p>
              )}
              
              {shareEmail.length >= 2 && searchResults.length === 0 && !searchLoading && (
                <p className="text-sm text-gray-500">No users found</p>
              )}
              
              {searchResults.length > 0 && (
                <div className="border rounded p-2 bg-gray-50 max-h-48 overflow-y-auto">
                  {searchResults.map(user => (
                    <label key={user.id} className="flex items-center p-2 hover:bg-gray-100 rounded cursor-pointer">
                      <input
                        type="checkbox"
                        checked={selectedUsers.has(user.id)}
                        onChange={() => toggleUserSelection(user.id)}
                        className="mr-2"
                      />
                      <div className="flex-1">
                        <div className="text-sm font-semibold">{user.username}</div>
                        <div className="text-xs text-gray-500">{user.email}</div>
                      </div>
                    </label>
                  ))}
                </div>
              )}
            </div>
            
            {selectedUsers.size > 0 && (
              <div className="mb-4 p-2 bg-blue-50 rounded border border-blue-200">
                <p className="text-sm font-semibold text-blue-900">
                  Selected: {selectedUsers.size} user{selectedUsers.size !== 1 ? 's' : ''}
                </p>
              </div>
            )}
            
            <div className="flex gap-2">
              <button
                onClick={handleShare}
                disabled={loadingShare || selectedUsers.size === 0}
                className="flex-1 bg-blue-500 text-white rounded p-2 hover:bg-blue-600 disabled:opacity-50"
              >
                {loadingShare ? 'Sharing...' : 'Share'}
              </button>
              <button
                onClick={() => {
                  setShareModal({ open: false, fileId: null });
                  setSearchResults([]);
                  setSelectedUsers(new Set());
                  setShareEmail('');
                }}
                className="flex-1 bg-gray-300 text-gray-800 rounded p-2 hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
