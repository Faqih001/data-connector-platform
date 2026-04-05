"use client";

import { useState, useEffect, useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { DataGrid } from "./components/DataGrid";
import { ConnectionForm } from "./components/ConnectionForm";
import { FileViewer } from "./components/FileViewer";
import { getConnections, createConnection, extractData } from "./lib/api";
import { DatabaseConnection } from "./types";

export default function Home() {
  const [connections, setConnections] = useState<DatabaseConnection[]>([]);
  const [selectedConnection, setSelectedConnection] = useState<
    DatabaseConnection | null
  >(null);
  const [tableName, setTableName] = useState("");
  const [data, setData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadConnections() {
      try {
        setIsLoading(true);
        const fetchedConnections = await getConnections();
        setConnections(fetchedConnections);
      } catch (err) {
        setError("Failed to load connections.");
      } finally {
        setIsLoading(false);
      }
    }
    loadConnections();
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
      const extractedData = await extractData(selectedConnection.id, tableName);
      setData(extractedData);
    } catch (err) {
      setError("Failed to extract data.");
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

          <div className="p-4 border rounded-lg">
            <h2 className="text-lg font-bold mb-2">Extract Data</h2>
            <input
              type="text"
              placeholder="Table/Collection Name"
              value={tableName}
              onChange={(e) => setTableName(e.target.value)}
              className="w-full p-2 border rounded mb-2"
            />
            <button
              onClick={handleExtractData}
              className="w-full p-2 bg-green-500 text-white rounded hover:bg-green-600"
              disabled={isLoading || !selectedConnection}
            >
              {isLoading ? "Extracting..." : "Extract Data"}
            </button>
          </div>

          <FileViewer />
        </div>

        <div className="md:col-span-2">
          {error && (
            <div className="text-red-500 bg-red-100 p-2 rounded mb-4">{error}</div>
          )}
          {data.length > 0 ? (
            <DataGrid data={data} columns={columns} setData={setData} />
          ) : (
            <div className="p-4 border rounded-lg text-center">
              <p>No data extracted yet.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
