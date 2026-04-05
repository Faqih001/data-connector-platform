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
  