'use client';

import { useState, useEffect } from 'react';
import { getFiles } from '@/app/lib/api';

interface StoredFile {
  id: number;
  filepath: string;
  user: number;
  shared_with: number[];
}

export function FileViewer() {
  const [files, setFiles] = useState<StoredFile[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadFiles() {
      try {
        setIsLoading(true);
        const fetchedFiles = await getFiles();
        setFiles(fetchedFiles);
      } catch (err) {
        setError('Failed to load files.');
      } finally {
        setIsLoading(false);
      }
    }
    loadFiles();
  }, []);

  if (isLoading) return <div>Loading files...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="p-4 border rounded-lg">
      <h2 className="text-lg font-bold mb-2">Stored Files</h2>
      <ul>
        {files.map((file) => (
          <li key={file.id} className="flex justify-between items-center p-2 border-b">
            <span>{file.filepath.split('/').pop()}</span>
            <a
              href={`http://localhost:8000/media/${file.filepath.split('/').pop()}`}
              download
              className="text-blue-500 hover:underline"
            >
              Download
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
