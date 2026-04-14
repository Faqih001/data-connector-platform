'use client';

import React from 'react';

interface ModalProps {
  isOpen: boolean;
  title: string;
  message: string;
  onClose: () => void;
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
  type?: 'info' | 'error' | 'success' | 'warning';
}

export function Modal({
  isOpen,
  title,
  message,
  onClose,
  onConfirm,
  confirmText = 'OK',
  cancelText = 'Cancel',
  type = 'info',
}: ModalProps) {
  if (!isOpen) return null;

  const bgColor = {
    info: 'bg-blue-50',
    error: 'bg-red-50',
    success: 'bg-green-50',
    warning: 'bg-yellow-50',
  }[type];

  const borderColor = {
    info: 'border-blue-200',
    error: 'border-red-200',
    success: 'border-green-200',
    warning: 'border-yellow-200',
  }[type];

  const titleColor = {
    info: 'text-blue-900',
    error: 'text-red-900',
    success: 'text-green-900',
    warning: 'text-yellow-900',
  }[type];

  const buttonColor = {
    info: 'bg-blue-600 hover:bg-blue-700',
    error: 'bg-red-600 hover:bg-red-700',
    success: 'bg-green-600 hover:bg-green-700',
    warning: 'bg-yellow-600 hover:bg-yellow-700',
  }[type];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className={`${bgColor} border-2 ${borderColor} rounded-lg shadow-xl max-w-md w-full mx-4 p-6 bg-white`}>
        <h2 className={`${titleColor} text-lg font-bold mb-3`}>{title}</h2>
        <p className="text-gray-700 mb-6 text-sm leading-relaxed">{message}</p>
        
        <div className="flex gap-3 justify-end">
          {onConfirm && (
            <>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400 font-medium text-sm"
              >
                {cancelText}
              </button>
              <button
                onClick={onConfirm}
                className={`px-4 py-2 text-white rounded-md ${buttonColor} font-medium text-sm`}
              >
                {confirmText}
              </button>
            </>
          )}
          {!onConfirm && (
            <button
              onClick={onClose}
              className={`px-4 py-2 text-white rounded-md ${buttonColor} font-medium text-sm`}
            >
              {confirmText}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
