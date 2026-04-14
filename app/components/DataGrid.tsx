'use client';

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  ColumnDef,
} from '@tanstack/react-table';
import { useState, useEffect } from 'react';
import { Modal } from './Modal';

interface EditableCellProps {
  getValue: () => any;
  row: any;
  column: any;
  table: any;
}

const EditableCell = ({
  getValue,
  row: { index },
  column: { id },
  table,
}: EditableCellProps) => {
  const initialValue = getValue();
  const [value, setValue] = useState(initialValue);

  const onBlur = () => {
    table.options.meta?.updateData(index, id, value);
  };

  useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);

  return (
    <input
      value={value as string}
      onChange={(e) => setValue(e.target.value)}
      onBlur={onBlur}
      className="w-full bg-transparent border-0 focus:outline-none text-xs sm:text-sm"
    />
  );
};

interface DataGridProps<TData> {
  data: TData[];
  columns: ColumnDef<TData>[];
  onSave?: (data: TData[]) => Promise<void>;
}

export function DataGrid<TData>({ data: initialData, columns, onSave }: DataGridProps<TData>) {
  const [data, setData] = useState(initialData);
  const [isSaving, setIsSaving] = useState(false);
  const [selectedRows, setSelectedRows] = useState<Set<number>>(new Set());
  const [newColumnName, setNewColumnName] = useState('');
  const [modal, setModal] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    type: 'info' | 'error' | 'success' | 'warning';
    onConfirm?: () => void;
  }>({ isOpen: false, title: '', message: '', type: 'info' });

  useEffect(() => {
    setData(initialData);
  }, [initialData]);

  const defaultColumn: Partial<ColumnDef<TData>> = {
    cell: EditableCell,
  };

  const table = useReactTable({
    data,
    columns,
    defaultColumn,
    getCoreRowModel: getCoreRowModel(),
    meta: {
      updateData: (rowIndex: number, columnId: string, value: any) => {
        setData((old) =>
          old.map((row, index) => {
            if (index === rowIndex) {
              return {
                ...old[rowIndex],
                [columnId]: value,
              };
            }
            return row;
          })
        );
      },
    },
  });

  const handleAddRow = () => {
    const newRow: any = {};
    if (data.length > 0) {
      Object.keys(data[0] as any).forEach(key => {
        newRow[key] = '';
      });
    }
    setData([...data, newRow]);
  };

  const handleDeleteSelectedRows = () => {
    const newData = data.filter((_, index) => !selectedRows.has(index));
    setData(newData);
    setSelectedRows(new Set());
  };

  const handleAddColumn = () => {
    if (!newColumnName.trim()) {
      setModal({
        isOpen: true,
        title: 'Missing Column Name',
        message: 'Please enter a column name before adding.',
        type: 'warning',
      });
      return;
    }
    const updatedData = data.map(row => ({
      ...row,
      [newColumnName]: '',
    })) as TData[];
    setData(updatedData);
    setNewColumnName('');
    setModal({
      isOpen: true,
      title: 'Column Added',
      message: `Column "${newColumnName}" has been added successfully.`,
      type: 'success',
    });
  };

  const handleDeleteColumn = (columnName: string) => {
    const updatedData = data.map(row => {
      const { [columnName]: _, ...rest } = row as any;
      return rest;
    }) as TData[];
    setData(updatedData);
  };

  const handleRowSelect = (rowIndex: number) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(rowIndex)) {
      newSelected.delete(rowIndex);
    } else {
      newSelected.add(rowIndex);
    }
    setSelectedRows(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedRows.size === data.length) {
      setSelectedRows(new Set());
    } else {
      setSelectedRows(new Set(data.map((_, idx) => idx)));
    }
  };

  const handleSave = async () => {
    if (onSave) {
      setIsSaving(true);
      try {
        await onSave(data);
        setModal({
          isOpen: true,
          title: '✅ Success',
          message: 'All changes have been saved successfully!',
          type: 'success',
        });
      } catch (error) {
        console.error("Failed to save data:", error);
        setModal({
          isOpen: true,
          title: '❌ Save Failed',
          message: `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`,
          type: 'error',
        });
      } finally {
        setIsSaving(false);
      }
    }
  };

  return (
    <div className="p-2">
      {/* CRUD Action Buttons */}
      <div className="mb-4 space-y-3">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={handleAddRow}
            className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
          >
            ➕ Add Row
          </button>
          <button
            onClick={handleDeleteSelectedRows}
            disabled={selectedRows.size === 0}
            className="px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 disabled:bg-gray-400"
          >
            🗑️ Delete Selected ({selectedRows.size})
          </button>
          <button
            onClick={handleAddColumn}
            className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
          >
            ➕ Add Column
          </button>
        </div>

        {/* Add Column Input */}
        <div className="flex gap-2 items-end">
          <div className="flex-1">
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Column Name
            </label>
            <input
              type="text"
              value={newColumnName}
              onChange={(e) => setNewColumnName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddColumn()}
              placeholder="Enter new column name..."
              className="w-full px-2 py-1 border border-gray-300 rounded text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Save Button */}
      {onSave && (
        <div className="flex justify-end mb-4">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            {isSaving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      )}

      {/* Data Table */}
      <div className="overflow-x-auto border border-gray-300 rounded">
        <table className="w-full divide-y divide-gray-200">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-2 py-2 w-12">
                <input
                  type="checkbox"
                  checked={selectedRows.size === data.length && data.length > 0}
                  onChange={handleSelectAll}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
                />
              </th>
              {columns.map((col: any) => (
                <th
                  key={col.accessorKey}
                  className="px-2 sm:px-4 py-2 sm:py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider bg-gray-50 relative group"
                >
                  <div className="flex items-center justify-between">
                    <span>{col.header}</span>
                    <button
                      onClick={() => handleDeleteColumn(col.accessorKey)}
                      className="ml-2 opacity-0 group-hover:opacity-100 text-red-600 hover:text-red-800 text-xs"
                      title="Delete column"
                    >
                      ✕
                    </button>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {table.getRowModel().rows.map((row, rowIndex) => (
              <tr
                key={row.id}
                className={`hover:bg-gray-50 ${
                  selectedRows.has(rowIndex) ? 'bg-blue-50' : ''
                }`}
              >
                <td className="px-2 py-2 w-12">
                  <input
                    type="checkbox"
                    checked={selectedRows.has(rowIndex)}
                    onChange={() => handleRowSelect(rowIndex)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
                  />
                </td>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id} className="px-2 sm:px-4 py-2 sm:py-3 whitespace-nowrap">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {data.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No data available. Click <strong>Add Row</strong> to get started.
        </div>
      )}

      <Modal
        isOpen={modal.isOpen}
        title={modal.title}
        message={modal.message}
        type={modal.type}
        onClose={() => setModal({ ...modal, isOpen: false })}
      />
    </div>
  );
}
