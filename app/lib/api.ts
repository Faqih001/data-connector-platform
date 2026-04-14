import { DatabaseConnection } from '@/app/types';

export const API_URL = 'http://localhost:8001/api';

const fetchOptions = {
  credentials: 'include' as const,
};

export async function getConnections(): Promise<DatabaseConnection[]> {
  const response = await fetch(`${API_URL}/connections/`, fetchOptions);
  if (!response.ok) {
    throw new Error('Failed to fetch connections');
  }
  return response.json();
}

export async function createConnection(connection: Omit<DatabaseConnection, 'id' | 'created_at'>): Promise<DatabaseConnection> {
  const response = await fetch(`${API_URL}/connections/`, {
    ...fetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(connection),
  });
  if (!response.ok) {
    throw new Error('Failed to create connection');
  }
  return response.json();
}

export async function extractData(
  connectionId: number, 
  tableName: string,
  batchSize: number = 1000,
  format: 'json' | 'csv' = 'json'
): Promise<any[]> {
  const response = await fetch(`${API_URL}/connections/${connectionId}/extract_data/`, {
    ...fetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      table_name: tableName,
      batch_size: batchSize,
      format: format
    }),
  });
  if (!response.ok) {
    throw new Error('Failed to extract data');
  }
  const result = await response.json();
  return result.data || result;
}

export async function getFiles(): Promise<any[]> {
    const response = await fetch(`${API_URL}/files/`, fetchOptions);
    if (!response.ok) {
        throw new Error('Failed to fetch files');
    }
    return response.json();
}

export async function submitData(fileId: number, data: any[]): Promise<void> {
    const response = await fetch(`${API_URL}/files/${fileId}/submit_data/`, {
        ...fetchOptions,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data }),
    });
    if (!response.ok) {
        throw new Error('Failed to submit data');
    }
}

export async function shareFile(fileId: number, userIds: number[]): Promise<any> {
    const response = await fetch(`${API_URL}/files/${fileId}/share/`, {
        ...fetchOptions,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_ids: userIds }),
    });
    if (!response.ok) {
        throw new Error('Failed to share file');
    }
    return response.json();
}

export async function deleteFile(fileId: number): Promise<void> {
    const response = await fetch(`${API_URL}/files/${fileId}/`, {
        ...fetchOptions,
        method: 'DELETE',
    });
    if (!response.ok) {
        throw new Error('Failed to delete file');
    }
}
