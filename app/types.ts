export interface User {
    id: number;
    username: string;
    email?: string;
    is_staff?: boolean;
}

export interface DatabaseConnection {
    id: number;
    name: string;
    db_type: 'postgresql' | 'mysql' | 'mongodb' | 'clickhouse';
    host: string;
    port: number;
    username: string;
    password?: string;
    database_name: string;
    created_at: string;
}

export interface StoredFile {
    id: number;
    filepath: string;
    format_type?: string; // 'json' or 'csv'
    user?: User | null;
    shared_with?: User[];
    base_filename?: string; // Base filename without timestamp
    table_name?: string; // Original table name
    connection_name?: string; // Database connection name
    extracted_at?: string; // Date when data was extracted
    last_modified_at?: string; // Date when data was last updated
    created_at?: string; // Deprecated
    updated_at?: string; // Deprecated
}

export interface ExtractedData {
    id: number;
    connection_id: number;
    data: any[];
    created_at?: string;
    updated_at?: string;
}
  