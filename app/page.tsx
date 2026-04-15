"use client";

import { useState, useEffect, useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { DataGrid } from "./components/DataGrid";
import { ConnectionForm } from "./components/ConnectionForm";
import { FileViewer } from "./components/FileViewer";
import { TableCreationForm } from "./components/TableCreationForm";
import { Loader } from "./components/Loader";
import { useToast } from "./components/ToastContext";
import { getConnections, createConnection, extractData, getFiles, submitData, getTables, getExtractedDataByTable, updateExtractedData } from "./lib/api";
import { DatabaseConnection, StoredFile } from "./types";

const API_URL = 'http://localhost:8001/api';

export default function Home() {
  // Toast context
  const toast = useToast();
  
  // All state declarations - MUST come first
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
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
  const [availableTables, setAvailableTables] = useState<string[]>([]);
  const [tableName, setTableName] = useState("");
  const [batchSize, setBatchSize] = useState<number>(1000);
  const [format, setFormat] = useState<'json' | 'csv'>('json');
  const [data, setData] = useState<any[]>([]);
  const [extractedDataInfo, setExtractedDataInfo] = useState<any>(null);
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
      } finally {
        setIsCheckingAuth(false);
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

  // Fetch tables when connection is selected
  useEffect(() => {
    if (selectedConnection && isLoggedIn) {
      const fetchTablesForConnection = async () => {
        try {
          const tables = await getTables(selectedConnection.id);
          setAvailableTables(tables);
          setTableName(""); // Reset table name when connection changes
        } catch (err) {
          console.error("Failed to fetch tables for connection:", selectedConnection.name, err);
          setAvailableTables([]);
        }
      };
      fetchTablesForConnection();
    } else {
      setAvailableTables([]);
      setTableName("");
    }
  }, [selectedConnection, isLoggedIn]);

  // Fetch data when table name changes
  useEffect(() => {
    if (selectedConnection && tableName) {
      const fetchDataForTable = async () => {
        try {
          setIsLoading(true);
          setError(null);
          const result = await getExtractedDataByTable(selectedConnection.id, tableName);
          setData(result.data || []);
          setExtractedDataInfo(result);
        } catch (err) {
          setError("Failed to fetch data for table.");
          setData([]);
          setExtractedDataInfo(null);
        } finally {
          setIsLoading(false);
        }
      };
      fetchDataForTable();
    } else {
      setData([]);
      setExtractedDataInfo(null);
    }
  }, [selectedConnection, tableName]);

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
      setError(null);
      const newConnection = await createConnection(connection);
      setConnections([...connections, newConnection]);
      toast.success(`Connection "${newConnection.name}" created successfully!`);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to create connection";
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveData = async (updatedData: any[]) => {
    if (!extractedDataInfo) {
      setError("No data loaded to save.");
      return;
    }
    try {
      setIsLoading(true);
      setError(null);
      await updateExtractedData(extractedDataInfo.id, updatedData);
      setData(updatedData); // Optimistically update UI
      // Optionally re-fetch to confirm
      const result = await getExtractedDataByTable(selectedConnection!.id, tableName);
      setData(result.data || []);
      setExtractedDataInfo(result);
    } catch (err) {
      setError("Failed to save data.");
    } finally {
      setIsLoading(false);
    }
  };

  // Conditional rendering - MUST come last
  // Show loader while checking authentication
  if (isCheckingAuth) {
    return <Loader fullScreen message="Loading..." />;
  }

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

        {/* Quick Action Buttons - Admin Only */}
        {currentUser?.is_staff && (
          <div className="mb-6 space-y-3">
            <div className="flex flex-col sm:flex-row gap-2">
              <a
                href="http://localhost:8001/api/connections/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 bg-gradient-to-r from-cyan-400 to-cyan-600 hover:from-cyan-500 hover:to-cyan-700 text-white font-medium py-2 px-4 rounded-lg transition text-center text-sm"
              >
                🔗 API Connections
              </a>
              <a
                href="http://localhost:8001/api/files/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 bg-gradient-to-r from-orange-400 to-orange-600 hover:from-orange-500 hover:to-orange-700 text-white font-medium py-2 px-4 rounded-lg transition text-center text-sm"
              >
                📊 API Files
              </a>
              <a
                href="http://localhost:8001/admin/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 bg-gradient-to-r from-purple-400 to-purple-600 hover:from-purple-500 hover:to-purple-700 text-white font-medium py-2 px-4 rounded-lg transition text-center text-sm"
              >
                📊 Admin Panel
              </a>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 lg:gap-6">
          {/* Left Sidebar - ConnectionForm + FileViewer */}
          <div className="lg:col-span-2 space-y-4 lg:max-h-screen lg:overflow-y-auto pr-2">
            <ConnectionForm onSubmit={handleCreateConnection} isLoading={isLoading} />
            <FileViewer files={files} onFileSelect={setSelectedFile} onRefresh={loadInitialData} />
          </div>

          {/* Right Sidebar - Connections + Extract Data + DataGrid */}
          <div className="lg:col-span-2 space-y-4 lg:max-h-screen lg:overflow-y-auto pl-2">
            {/* Connections Section */}
            <div className="p-4 border rounded-lg bg-white shadow-sm">
              <h2 className="text-base sm:text-lg font-bold mb-3">🔗 Connections</h2>
              <select
                className="w-full p-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={selectedConnection?.id || ""}
                onChange={(e) => {
                  const conn = connections.find((c) => c.id === parseInt(e.target.value));
                  setSelectedConnection(conn || null);
                }}
              >
                <option value="">Select a connection</option>
                {connections.map((conn) => (
                  <option key={conn.id} value={conn.id}>
                    {conn.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Table Creation Section - Show when no tables exist */}
            {selectedConnection && availableTables.length === 0 && (
              <TableCreationForm 
                connection={selectedConnection}
                onTableCreated={() => {
                  // Reload tables after creation
                  if (selectedConnection) {
                    const fetchTablesForConnection = async () => {
                      try {
                        const tables = await getTables(selectedConnection.id);
                        setAvailableTables(tables);
                      } catch (err) {
                        console.error("Failed to refresh tables:", err);
                      }
                    };
                    fetchTablesForConnection();
                  }
                }}
              />
            )}

            {/* Extract Data Section */}
            <div className="p-4 border rounded-lg bg-white shadow-sm">
              <h2 className="text-base sm:text-lg font-bold mb-3">📊 Extract Data</h2>
              <div className="mb-3">
                <label htmlFor="tableName" className="block text-sm font-medium text-gray-700">
                  Table Name
                </label>
                  <select
                    id="tableName"
                    value={tableName}
                    onChange={(e) => setTableName(e.target.value)}
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    disabled={!selectedConnection || availableTables.length === 0}
                  >
                  <option value="">{availableTables.length > 0 ? 'Select a table' : 'No tables found'}</option>
                  {availableTables.map((table) => (
                    <option key={table} value={table}>
                      {table}
                    </option>
                  ))}
                </select>
              </div>
              {error && <p className="text-red-500 mt-4">{error}</p>}
            </div>

            {/* Extracted Data Grid */}
            <div className="p-4 border rounded-lg bg-white shadow-sm relative">
              <h2 className="text-base sm:text-lg font-bold mb-4">📊 Extracted Data</h2>
              {isLoading ? (
                <Loader fullScreen={false} size="md" message="Loading data..." />
              ) : (
                <DataGrid
                  columns={columns}
                  data={data}
                  onSave={handleSaveData}
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
