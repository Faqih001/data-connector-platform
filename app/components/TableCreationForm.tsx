'use client';

import { useState } from 'react';
import { DatabaseConnection } from '@/app/types';
import { useToast } from './ToastContext';
import { createTable } from '@/app/lib/api';

interface TableCreationFormProps {
  connection: DatabaseConnection | null;
  onTableCreated?: () => void;
}

export function TableCreationForm({ connection, onTableCreated }: TableCreationFormProps) {
  const toast = useToast();
  const [isExpanded, setIsExpanded] = useState(false);
  const [tableName, setTableName] = useState('');
  const [sqlStatement, setSqlStatement] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  if (!connection) {
    return null;
  }

  // Provide SQL templates based on database type
  const getSqlTemplate = () => {
    switch (connection.db_type) {
      case 'postgresql':
        return `CREATE TABLE IF NOT EXISTS ${tableName || 'table_name'} (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`;
      case 'mysql':
        return `CREATE TABLE IF NOT EXISTS ${tableName || 'table_name'} (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`;
      case 'mongodb':
        return `// MongoDB creates collections on first insert
// Collection name: ${tableName || 'collection_name'}`;
      case 'clickhouse':
        return `CREATE TABLE IF NOT EXISTS ${tableName || 'table_name'} (
  id UInt32,
  name String,
  created_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY id;`;
      default:
        return '';
    }
  };

  const handleCreateTable = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!tableName.trim()) {
      toast.error('Please enter a table name');
      return;
    }

    if (!sqlStatement.trim()) {
      toast.error('Please enter a SQL statement');
      return;
    }

    setIsLoading(true);
    try {
      await createTable(connection.id, sqlStatement);
      
      // Reset form
      setTableName('');
      setSqlStatement('');
      setIsExpanded(false);
      
      toast.success(`Table "${tableName}" created successfully!`);
      if (onTableCreated) {
        onTableCreated();
      }
    } catch (err) {
      toast.error(`Failed to create table: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg bg-blue-50 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-bold text-blue-900 flex items-center gap-2">
          📋 Create New Table
          {isExpanded && <span className="text-xs bg-blue-200 px-2 py-1 rounded">No tables found</span>}
        </h3>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-xs bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
        >
          {isExpanded ? 'Hide' : 'Show'}
        </button>
      </div>

      {isExpanded && (
        <form onSubmit={handleCreateTable} className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Table Name
            </label>
            <input
              type="text"
              value={tableName}
              onChange={(e) => {
                setTableName(e.target.value);
                if (!sqlStatement) {
                  setSqlStatement(getSqlTemplate());
                }
              }}
              placeholder="Enter table name"
              className="w-full px-2 py-2 border border-gray-300 rounded text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-medium text-gray-700">
                SQL Statement
              </label>
              <button
                type="button"
                onClick={() => setSqlStatement(getSqlTemplate())}
                className="text-xs text-blue-600 hover:text-blue-800 underline"
              >
                Use Template
              </button>
            </div>
            <textarea
              value={sqlStatement}
              onChange={(e) => setSqlStatement(e.target.value)}
              placeholder="Enter SQL CREATE TABLE statement"
              className="w-full px-2 py-2 border border-gray-300 rounded text-xs font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 h-24"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Database: <span className="font-semibold">{connection.db_type.toUpperCase()}</span>
            </p>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full px-3 py-2 bg-blue-500 text-white text-sm font-medium rounded hover:bg-blue-600 disabled:bg-gray-400 transition"
          >
            {isLoading ? 'Creating...' : 'Create Table'}
          </button>
        </form>
      )}

      {!isExpanded && (
        <p className="text-xs text-gray-600">
          Click "Show" to create a new table for this connection
        </p>
      )}
    </div>
  );
}
