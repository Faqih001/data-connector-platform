"use client";

import { useState, useEffect, useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { DataGrid } from "./components/DataGrid";
import { ConnectionForm } from "./components/ConnectionForm";
import { FileViewer } from "./components/FileViewer";
import { getConnections, createConnection, extractData, getFiles, submitData } from "./lib/api";
import { DatabaseConnection, StoredFile } from "./types";

const API_URL = 'http://localhost:8001/api';

export default function Home() {
  // All state declarations - MUST come first
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [connections, setConnections] = useState<DatabaseConnection[]>([]);
  const [selectedConnection, setSelectedConnection] = useState<
    DatabaseConnection | null
  >(null);
  const [tableName, setTableName] = useState("");
  const [batchSize, setBatchSize] = useState<number>(1000);
  const [format, setFormat] = useState<'json' | 'csv'>('json');
  const [data, setData] = useState<any[]>([]);
  const [files, setFiles] = useState<StoredFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<StoredFile | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // All effects - MUST come second
  // Check if user is already logged in
  useEffect(() => {
    async function checkAuth() {
      try {
        const response = await fetch(`${API_URL}/user/`, {
          credentials: 'include'
        });
        if (response.ok) {
          const user = await response.json();
          setCurrentUser(user);
          setIsLoggedIn(true);
        }
      } catch (err) {
        console.log('Not logged in');
      }
    }
    checkAuth();
  }, []);

  // Load user data when logged in
  const loadInitialData = async () => {
    try {
      setIsLoading(true);
      const [fetchedConnections, fetchedFiles] = await Promise.all([
        getConnections(),
        getFiles(),
      ]);
      setConnections(fetchedConnections);
      setFiles(fetchedFiles);
    } catch (err) {
      setError("Failed to load initial data.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isLoggedIn) {
      loadInitialData();
    }
  }, [isLoggedIn]);

  // Memos - MUST come third
  const columns = useMemo<ColumnDef<any>[]>(() => {
    if (data.length === 0) return [];
    return Object.keys(data[0]).map((key) => ({
      accessorKey: key,
      header: key,
    }));
  }, [data]);

  // Handler functions - CAN come anywhere but after hooks
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoggingIn(true);
    setLoginError("");
    
    try {
      // Step 1: Get CSRF token
      const csrfResponse = await fetch(`${API_URL}/csrf-token/`, {
        credentials: 'include'
      });
      const csrfData = await csrfResponse.json();
      const csrfToken = csrfData.csrfToken;
      
      // Step 2: Login with CSRF token
      const response = await fetch(`${API_URL}/login/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          username: loginUsername,
          password: loginPassword
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setCurrentUser(data.user);
        setIsLoggedIn(true);
        setLoginUsername("");
        setLoginPassword("");
        setLoginError("");
      } else {
        const errorData = await response.json();
        setLoginError(errorData.error || "❌ Invalid username or password");
      }
    } catch (err) {
      setLoginError("Failed to login: " + (err instanceof Error ? err.message : String(err)));
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleLogout = async () => {
    try {
      // Get CSRF token for logout
      const csrfResponse = await fetch(`${API_URL}/csrf-token/`, {
        credentials: 'include'
      });
      const csrfData = await csrfResponse.json();
      const csrfToken = csrfData.csrfToken;
      
      await fetch(`${API_URL}/logout/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'X-CSRFToken': csrfToken,
        }
      });
      setIsLoggedIn(false);
      setCurrentUser(null);
      setConnections([]);
      setFiles([]);
      setData([]);
      setLoginError("");
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  const handleCreateConnection = async (
    connection: Omit<DatabaseConnection, "id" | "created_at">
  ) => {
    try {
      setIsLoading(true);
      const newConnection = await createConnection(connection);
      setConnections([...connections, newConnection]);
    } catch (err) {
      setError("Failed to create connection.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleExtractData = async () => {
    if (!selectedConnection || !tableName) {
      setError("Please select a connection and enter a table name.");
      return;
    }
    try {
      setIsLoading(true);
      setError(null);
      const extractedData = await extractData(selectedConnection.id, tableName, batchSize, format);
      setData(extractedData);
    } catch (err) {
      setError("Failed to extract data.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveData = async (updatedData: any[]) => {
    if (!selectedFile) {
      setError("Please select a file to save the data.");
      return;
    }
    try {
      setIsLoading(true);
      setError(null);
      await submitData(selectedFile.id, updatedData);
      setData(updatedData);
    } catch (err) {
      setError("Failed to save data.");
    } finally {
      setIsLoading(false);
    }
  };

  // Conditional rendering - MUST come last
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center p-4 sm:p-6">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">Data Connector Platform</h1>
            <p className="text-gray-600 text-sm sm:text-base">Secure authentication required</p>
          </div>
          
          <div className="bg-white rounded-lg border-2 border-gray-200 p-6 sm:p-8 shadow-sm">
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                  Username
                </label>
                <input
                  id="username"
                  type="text"
                  value={loginUsername}
                  onChange={(e) => setLoginUsername(e.target.value)}
                  placeholder="Enter your username"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  disabled={isLoggingIn}
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                  Password
                </label>
                <div className="relative">
                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                    disabled={isLoggingIn}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
                    disabled={isLoggingIn}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? (
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                        <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-4.803m5.596-3.856a3.375 3.375 0 11-4.753 4.753m4.753-4.753L3.596 3.039m10.318 10.318L3.596 3.039M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              {loginError && (
                <div className="p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
                  {loginError}
                </div>
              )}

              <button
                type="submit"
                disabled={isLoggingIn || !loginUsername || !loginPassword}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition"
              >
                {isLoggingIn ? "Logging in..." : "Login"}
              </button>
            </form>

            <div className="mt-6 p-3 sm:p-4 bg-blue-50 border border-blue-200 rounded text-xs sm:text-sm text-gray-700">
              <p className="font-medium mb-2">Demo Accounts:</p>
              <ul className="space-y-1 text-xs">
                <li className="break-words">👤 <strong>admin</strong> / <code className="bg-white px-1 rounded">admin123</code></li>
                <li className="break-words">👤 <strong>john_sales</strong> / <code className="bg-white px-1 rounded">john123</code></li>
                <li className="break-words">👤 <strong>sarah_analytics</strong> / <code className="bg-white px-1 rounded">sarah456</code></li>
                <li className="break-words">👤 <strong>mike_reporting</strong> / <code className="bg-white px-1 rounded">mike789</code></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-4 sm:px-6 sm:py-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-3">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold">Data Connector Platform</h1>
            <p className="text-gray-600 text-xs sm:text-sm">Logged in as <strong>{currentUser?.username}</strong> {currentUser?.is_staff && '(Admin)'}</p>
          </div>
          <button
            onClick={handleLogout}
            className="w-full sm:w-auto bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition text-sm"
          >
            Logout
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 lg:gap-6">
          {/* Left Sidebar - Increased to 2/4 width on desktop */}
          <div className="lg:col-span-2 space-y-4 lg:max-h-screen lg:overflow-y-auto pr-2">
          <ConnectionForm onSubmit={handleCreateConnection} isLoading={isLoading} />

          <div className="p-4 border rounded-lg bg-white shadow-sm">
            <h2 className="text-base sm:text-lg font-bold mb-3">Connections</h2>
            <select
              className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              onChange={(e) => {
                const conn = connections.find((c) => c.id === parseInt(e.target.value));
                setSelectedConnection(conn || null);
              }}
            >
              <option>Select a connection</option>
              {connections.map((conn) => (
                <option key={conn.id} value={conn.id}>
                  {conn.name}
                </option>
              ))}
            </select>
          </div>

          <FileViewer files={files} onFileSelect={setSelectedFile} onRefresh={loadInitialData} />
        </div>

        <div className="lg:col-span-2 space-y-4 lg:max-h-screen lg:overflow-y-auto pl-2">
          <div className="p-4 border rounded-lg bg-white shadow-sm">
            <h2 className="text-base sm:text-lg font-bold mb-3">Extract Data</h2>
            <input
              type="text"
              placeholder="Table Name"
              value={tableName}
              onChange={(e) => setTableName(e.target.value)}
              className="w-full p-2 border rounded mb-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-3">
              <div>
                <label className="block text-xs sm:text-sm font-medium mb-1">Batch Size</label>
                <input
                  type="number"
                  value={batchSize}
                  onChange={(e) => setBatchSize(parseInt(e.target.value) || 1000)}
                  min="1"
                  className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Rows per batch"
                />
              </div>
              <div>
                <label className="block text-xs sm:text-sm font-medium mb-1">Format</label>
                <select
                  value={format}
                  onChange={(e) => setFormat(e.target.value as 'json' | 'csv')}
                  className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="json">JSON</option>
                  <option value="csv">CSV</option>
                </select>
              </div>
            </div>
            <button
              onClick={handleExtractData}
              className="w-full px-4 py-2 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600 disabled:bg-gray-400 transition text-sm"
              disabled={isLoading || !selectedConnection || !tableName}
            >
              {isLoading ? "Extracting..." : "Extract Data"}
            </button>
          </div>

          {error && <div className="p-3 text-red-600 bg-red-50 border border-red-200 rounded text-sm">{error}</div>}

          <DataGrid columns={columns} data={data} setData={setData} onSave={handleSaveData} />
        </div>
        </div>
      </div>
    </main>
  );
}
