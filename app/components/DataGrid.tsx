'use client';

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  ColumnDef,
} from '@tanstack/react-table';
import { useState, useEffect } from 'react';

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

  const handleSave = async () => {
    if (onSave) {
      setIsSaving(true);
      try {
        await onSave(data);
      } catch (error) {
        console.error("Failed to save data:", error);
        // Optionally show an error message to the user
      } finally {
        setIsSaving(false);
      }
    }
  };

  return (
    <div className="p-2">
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
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 border">
          <thead className="bg-gray-50">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    className="px-2 sm:px-4 py-2 sm:py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} className="hover:bg-gray-50">
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
    </div>
  );
}
