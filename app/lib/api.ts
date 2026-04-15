import { DatabaseConnection } from '@/app/types';

export const API_URL = 'http://localhost:8001/api';

const fetchOptions = {
  credentials: 'include' as const,
};

// Helper function to get CSRF token
async function getCsrfToken(): Promise<string> {
  const response = await fetch(`${API_URL}/csrf-token/`, fetchOptions);
  const data = await response.json();
  return data.csrfToken;
}

export async function getConnections(): Promise<DatabaseConnection[]> {
  const response = await fetch(`${API_URL}/connections/`, fetchOptions);
  if (!response.ok) {
    throw new Error('Failed to fetch connections');
  }
  return response.json();
}

export async function createConnection(connection: Omit<DatabaseConnection, 'id' | 'created_at'>): Promise<DatabaseConnection> {
  const csrfToken = await getCsrfToken();
  
  const response = await fetch(`${API_URL}/connections/`, {
    ...fetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(connection),
  });
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.error || errorData.detail || 'Failed to create connection');
    } catch (e) {
      if (e instanceof Error && e.message !== 'Failed to create connection') {
        throw e;
      }
      throw new Error(`Failed to create connection (HTTP ${response.status})`);
    }
  }
  return response.json();
}

export async function extractData(
  connectionId: number, 
  tableName: string,
  batchSize: number = 1000,
  format: 'json' | 'csv' = 'json'
): Promise<any[]> {
  const csrfToken = await getCsrfToken();
  
  const response = await fetch(`${API_URL}/connections/${connectionId}/extract_data/`, {
    ...fetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ 
      table_name: tableName,
      batch_size: batchSize,
      format: format
    }),
  });
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.error || errorData.detail || 'Failed to extract data');
    } catch (e) {
      if (e instanceof Error && e.message !== 'Failed to extract data') {
        throw e;
      }
      throw new Error('Failed to extract data');
    }
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
    const csrfToken = await getCsrfToken();
    
    const response = await fetch(`${API_URL}/files/${fileId}/submit_data/`, {
        ...fetchOptions,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ data }),
    });
    if (!response.ok) {
        throw new Error('Failed to submit data');
    }
}

export async function shareFile(fileId: number, userIds: number[]): Promise<any> {
    const csrfToken = await getCsrfToken();
    
    const response = await fetch(`${API_URL}/files/${fileId}/share/`, {
        ...fetchOptions,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ user_ids: userIds }),
    });
    if (!response.ok) {
        throw new Error('Failed to share file');
    }
    return response.json();
}

export async function deleteFile(fileId: number): Promise<void> {
    const csrfToken = await getCsrfToken();
    
    const response = await fetch(`${API_URL}/files/${fileId}/`, {
        ...fetchOptions,
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken,
        },
    });
    if (!response.ok) {
        throw new Error('Failed to delete file');
    }
}

export async function getTables(connectionId: number): Promise<string[]> {
    const response = await fetch(`${API_URL}/connections/${connectionId}/get_tables/`, fetchOptions);
    if (!response.ok) {
        throw new Error('Failed to fetch tables');
    }
    return response.json();
}

export async function getExtractedDataByTable(connectionId: number, tableName: string): Promise<any> {
    const url = `${API_URL}/extracted_data/by_table/?connection_id=${connectionId}&table_name=${tableName}`;
    console.log('📨 Fetching data:', { url });
    
    try {
        const response = await fetch(url, fetchOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: Failed to fetch extracted data`);
        }
        
        const responseData = await response.json();
        console.log('✅ Data fetched successfully:', {
            id: responseData.id,
            dataLength: Array.isArray(responseData.data) ? responseData.data.length : 0,
        });
        
        return responseData;
    } catch (error) {
        console.error('❌ Fetch failed:', error);
        throw error;
    }
}

export async function updateExtractedData(id: number, data: any): Promise<any> {
    console.log('📤 Sending PATCH request to update extracted data:', {
        endpoint: `${API_URL}/extracted_data/${id}/`,
        payload: { data }
    });
    
    try {
        const csrfToken = await getCsrfToken();
        
        const response = await fetch(`${API_URL}/extracted_data/${id}/`, {
            ...fetchOptions,
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ data }),
        });
        
        const responseData = await response.json();
        console.log('📥 Response from PATCH:', {
            status: response.status,
            ok: response.ok,
            data: responseData
        });

        if (!response.ok) {
            const errorMsg = responseData.error || responseData.details || 'Failed to update extracted data';
            throw new Error(`${response.status}: ${errorMsg}`);
        }
        
        console.log('✅ Update successful');
        return responseData;
    } catch (error) {
        console.error('❌ Update failed:', error);
        throw error;
    }
}
