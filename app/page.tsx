"use client";

import { useState, useEffect, useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { DataGrid } from "./components/DataGrid";
import { ConnectionForm } from "./components/ConnectionForm";
import { FileViewer } from "./components/FileViewer";
import { getConnections, createConnection, extractData, getFiles, submitData } from "./lib/api";
import { DatabaseConnection, StoredFile } from "./types";

export default function Home() {
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

  useEffect(() => {
    async function loadInitialData() {
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
    }
    loadInitialData();
  }, []);

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

  const columns = useMemo<ColumnDef<any>[]>(() => {
    if (data.length === 0) return [];
    return Object.keys(data[0]).map((key) => ({
      accessorKey: key,
      header: key,
    }));
  }, [data]);

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Data Connector Platform</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-1 space-y-4">
          <ConnectionForm onSubmit={handleCreateConnection} isLoading={isLoading} />

          <div className="p-4 border rounded-lg">
            <h2 className="text-lg font-bold mb-2">Connections</h2>
            <select
              className="w-full p-2 border rounded"
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

          <FileViewer files={files} onFileSelect={setSelectedFile} />
        </div>

        <div className="md:col-span-2 space-y-4">
          <div className="p-4 border rounded-lg">
            <h2 className="text-lg font-bold mb-2">Extract Data</h2>
            <input
              type="text"
              placeholder="Table Name"
              value={tableName}
              onChange={(e) => setTableName(e.target.value)}
              className="w-full p-2 border rounded mb-2"
            />
            <div className="grid grid-cols-2 gap-2 mb-2">
              <div>
                <label className="block text-sm font-medium mb-1">Batch Size</label>
                <input
                  type="number"
                  value={batchSize}
                  onChange={(e) => setBatchSize(parseInt(e.target.value) || 1000)}
                  min="1"
                  className="w-full p-2 border rounded"
                  placeholder="Rows per batch"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Format</label>
                <select
                  value={format}
                  onChange={(e) => setFormat(e.target.value as 'json' | 'csv')}
                  className="w-full p-2 border rounded"
                >
                  <option value="json">JSON</option>
                  <option value="csv">CSV</option>
                </select>
              </div>
            </div>
            <button
              onClick={handleExtractData}
              className="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
              disabled={isLoading || !selectedConnection || !tableName}
            >
              {isLoading ? "Extracting..." : "Extract Data"}
            </button>
          </div>

          {error && <p className="text-red-500">{error}</p>}

          <DataGrid columns={columns} data={data} setData={setData} onSave={handleSaveData} />
        </div>
      </div>
    </main>
  );
}
