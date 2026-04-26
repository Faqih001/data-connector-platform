'use client';

import { useState } from 'react';
import { DatabaseConnection } from '@/app/types';

interface ConnectionFormProps {
  onSubmit: (connection: Omit<DatabaseConnection, 'id' | 'created_at'>) => void;
  isLoading: boolean;
}

// Docker-aware host and port defaults
const isDocker = typeof window === 'undefined' || process.env.NEXT_PUBLIC_DOCKER_ENV === '1';

const DEFAULT_PORTS = {
  postgresql: 5432,
  mysql: 3306,
  mongodb: 27017,
  clickhouse: 9000,
} as const;

// Docker service names for each database type
const DOCKER_SERVICE_NAMES = {
  postgresql: 'db',
  mysql: 'mysql',
  mongodb: 'mongo',
  clickhouse: 'clickhouse',
} as const;

// Default credentials for each database type
const DEFAULT_CREDENTIALS = {
  postgresql: { username: 'user', password: 'password' },
  mysql: { username: 'user', password: 'password' },
  mongodb: { username: '', password: '' },
  clickhouse: { username: 'default', password: '' },
} as const;

// Default database names
const DEFAULT_DATABASES = {
  postgresql: 'dataconnector',
  mysql: 'testdb',
  mongodb: 'test_db',
  clickhouse: 'default',
} as const;

// Get default host based on environment and database type
const getDefaultHost = (dbType: keyof typeof DEFAULT_PORTS = 'postgresql') => {
  if (!isDocker) return 'localhost';
  return DOCKER_SERVICE_NAMES[dbType];
};

const DEFAULT_HOST = getDefaultHost('postgresql');

export function ConnectionForm({ onSubmit, isLoading }: ConnectionFormProps) {
  const [name, setName] = useState('');
  const [db_type, setDbType] = useState<'postgresql' | 'mysql' | 'mongodb' | 'clickhouse'>('postgresql');
  const [host, setHost] = useState<string>(DEFAULT_HOST);
  const [port, setPort] = useState<number>(DEFAULT_PORTS.postgresql);
  const [username, setUsername] = useState<string>(DEFAULT_CREDENTIALS.postgresql.username);
  const [password, setPassword] = useState<string>(DEFAULT_CREDENTIALS.postgresql.password);
  const [database_name, setDatabaseName] = useState<string>(DEFAULT_DATABASES.postgresql);
  const [showPassword, setShowPassword] = useState(false);

  // Handle database type change - auto-update host, port, username, password, and database name
  const handleDbTypeChange = (newType: 'postgresql' | 'mysql' | 'mongodb' | 'clickhouse') => {
    setDbType(newType);
    setHost(getDefaultHost(newType));
    setPort(DEFAULT_PORTS[newType]);
    setUsername(DEFAULT_CREDENTIALS[newType].username as string);
    setPassword(DEFAULT_CREDENTIALS[newType].password as string);
    setDatabaseName(DEFAULT_DATABASES[newType]);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ name, db_type, host, port, username, password, database_name });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3 p-4 border rounded-lg bg-white shadow-sm">
      <h2 className="text-base sm:text-lg font-bold">Create Connection</h2>
      <div>
        <label className="block text-xs sm:text-sm font-medium mb-1">Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g., My PostgreSQL DB"
          className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      <div>
        <label className="block text-xs sm:text-sm font-medium mb-1">Database Type</label>
        <select
          value={db_type}
          onChange={(e) => handleDbTypeChange(e.target.value as any)}
          className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="postgresql">PostgreSQL (Default: localhost:5432)</option>
          <option value="mysql">MySQL (Default: localhost:3306)</option>
          <option value="mongodb">MongoDB (Default: localhost:27017)</option>
          <option value="clickhouse">ClickHouse (Default: localhost:9000)</option>
        </select>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <div>
          <label className="block text-xs sm:text-sm font-medium mb-1">Host</label>
          <input
            type="text"
            value={host}
            onChange={(e) => setHost(e.target.value)}
            placeholder={DEFAULT_HOST}
            className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-xs sm:text-sm font-medium mb-1">Port</label>
          <input
            type="number"
            value={port}
            onChange={(e) => setPort(parseInt(e.target.value))}
            placeholder={DEFAULT_PORTS[db_type].toString()}
            className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
      </div>
      <div>
        <label className="block text-xs sm:text-sm font-medium mb-1">Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="e.g., user"
          className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      <div>
        <label className="block text-xs sm:text-sm font-medium mb-1">Password</label>
        <div className="flex items-center gap-2">
          <input
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password"
            className="flex-1 p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="px-3 py-2 bg-gray-100 hover:bg-gray-200 border border-gray-300 rounded text-xs font-medium transition"
            title={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? '🙈' : '👁️'}
          </button>
        </div>
      </div>
      <div>
        <label className="block text-xs sm:text-sm font-medium mb-1">Database Name</label>
        <input
          type="text"
          value={database_name}
          onChange={(e) => setDatabaseName(e.target.value)}
          placeholder="e.g., dataconnector"
          className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      <button
        type="submit"
        className="w-full p-2 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600 disabled:bg-gray-400 transition text-sm sm:text-base"
        disabled={isLoading}
      >
        {isLoading ? 'Connecting...' : 'Create Connection'}
      </button>
    </form>
  );
}
