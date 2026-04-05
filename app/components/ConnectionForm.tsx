'use client';

import { useState } from 'react';
import { DatabaseConnection } from '@/app/types';

interface ConnectionFormProps {
  onSubmit: (connection: Omit<DatabaseConnection, 'id' | 'created_at'>) => void;
  isLoading: boolean;
}

export function ConnectionForm({ onSubmit, isLoading }: ConnectionFormProps) {
  const [name, setName] = useState('');
  const [db_type, setDbType] = useState<'postgresql' | 'mysql' | 'mongodb' | 'clickhouse'>('postgresql');
  const [host, setHost] = useState('');
  const [port, setPort] = useState(5432);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [database_name, setDatabaseName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ name, db_type, host, port, username, password, database_name });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-lg">
      <div>
        <label className="block text-sm font-medium">Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Database Type</label>
        <select
          value={db_type}
          onChange={(e) => setDbType(e.target.value as any)}
          className="w-full p-2 border rounded"
        >
          <option value="postgresql">PostgreSQL</option>
          <option value="mysql">MySQL</option>
          <option value="mongodb">MongoDB</option>
          <option value="clickhouse">ClickHouse</option>
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium">Host</label>
        <input
          type="text"
          value={host}
          onChange={(e) => setHost(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Port</label>
        <input
          type="number"
          value={port}
          onChange={(e) => setPort(parseInt(e.target.value))}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 border rounded"
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Database Name</label>
        <input
          type="text"
          value={database_name}
          onChange={(e) => setDatabaseName(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <button
        type="submit"
        className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        disabled={isLoading}
      >
        {isLoading ? 'Connecting...' : 'Create Connection'}
      </button>
    </form>
  );
}
