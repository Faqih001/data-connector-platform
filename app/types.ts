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
    user?: number | null;
    shared_with?: number[];
    created_at?: string;
  }
  