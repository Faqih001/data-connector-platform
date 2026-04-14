'use client';

import { useState, useEffect } from 'react';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface ToastMessage {
  id: string;
  message: string;
  type: ToastType;
  duration?: number;
}

interface ToastProps {
  toast: ToastMessage;
  onClose: (id: string) => void;
}

const Toast = ({ toast, onClose }: ToastProps) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose(toast.id);
    }, toast.duration || 4000);

    return () => clearTimeout(timer);
  }, [toast.id, toast.duration, onClose]);

  const typeStyles = {
    success: 'bg-gradient-to-r from-green-400 to-green-600 text-white border-green-700',
    error: 'bg-gradient-to-r from-red-400 to-red-600 text-white border-red-700',
    info: 'bg-gradient-to-r from-blue-400 to-blue-600 text-white border-blue-700',
    warning: 'bg-gradient-to-r from-yellow-400 to-yellow-600 text-white border-yellow-700',
  };

  const icons = {
    success: '✅',
    error: '❌',
    info: 'ℹ️',
    warning: '⚠️',
  };

  return (
    <div
      className={`
        ${typeStyles[toast.type]}
        flex items-center gap-3 px-4 py-3 rounded-lg shadow-xl
        border-l-4 backdrop-blur-sm
        animate-slideIn transform transition-all duration-300
        max-w-sm
      `}
    >
      <span className="text-xl flex-shrink-0">{icons[toast.type]}</span>
      <p className="flex-1 font-medium text-sm">{toast.message}</p>
      <button
        onClick={() => onClose(toast.id)}
        className="flex-shrink-0 text-white hover:opacity-75 transition-opacity ml-2"
      >
        ✕
      </button>
    </div>
  );
};

export default Toast;
