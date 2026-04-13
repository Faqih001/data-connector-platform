import { DatabaseConnection } from '@/app/types';

const API_URL = 'http://localhost:8001/api';

export async function getConnections(): Promise<DatabaseConnection[]> {
  const response = await fetch(`${API_URL}/connections/`);
  if (!response.ok) {
    throw new Error('Failed to fetch connections');
  }
  return response.json();
}

export async function createConnection(connection: Omit<DatabaseConnection, 'id' | 'created_at'>): Promise<DatabaseConnection> {
  const response = await fetch(`${API_URL}/connections/`, {
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

export async function extractData(connectionId: number, tableName: string): Promise<any[]> {
  const response = await fetch(`${API_URL}/connections/${connectionId}/extract_data/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ table_name: tableName }),
  });
  if (!response.ok) {
    throw new Error('Failed to extract data');
  }
  return response.json();
}

export async function getFiles(): Promise<any[]> {
    const response = await fetch(`${API_URL}/files/`);
    if (!response.ok) {
        throw new Error('Failed to fetch files');
    }
    const responseData = response.json();
    // Handle both paginated and direct array responses
    return responseData instanceof Promise ? await responseData : responseData;
}

export async function getFileData(filePath: string): Promise<any[]> {
    const response = await fetch(`${API_URL}/files/download/?filepath=${encodeURIComponent(filePath)}`);
    if (!response.ok) {
        throw new Error('Failed to fetch file data');
    }
    return response.json();
}

export async function submitData(fileId: number, data: any[]): Promise<void> {
    const response = await fetch(`${API_URL}/files/${fileId}/submit_data/`, {
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
