'use client';

import React from 'react';
import { AgGridReact } from 'ag-grid-react';
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const DataGrid = ({ rowData, columnDefs }) => {
    const onGridReady = (params) => {
        params.api.sizeColumnsToFit();
    };

    const onCellValueChanged = (params) => {
        console.log("Cell value changed:", params);
        // Here you would handle the update, e.g., by sending it to the backend
    };

    return (
        <div className="ag-theme-alpine" style={{ height: 400, width: 600 }}>
            <AgGridReact
                rowData={rowData}
                columnDefs={columnDefs}
                onGridReady={onGridReady}
                onCellValueChanged={onCellValueChanged}>
            </AgGridReact>
        </div>
    );
};

export default DataGrid;
