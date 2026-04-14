'use client';

import { useState, useCallback } from 'react';
import Toast, { ToastMessage, ToastType } from './Toast';

interface ToastContainerProps {
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
}

export interface ToastMethods {
  success: (message: string, duration?: number) => void;
  error: (message: string, duration?: number) => void;
  info: (message: string, duration?: number) => void;
  warning: (message: string, duration?: number) => void;
}

const ToastContainer = ({ position = 'bottom-right' }: ToastContainerProps) => {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const positionClass = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4',
  };

  const showToast = useCallback((message: string, type: ToastType, duration?: number) => {
    const id = Date.now().toString();
    const newToast: ToastMessage = { id, message, type, duration: duration || 4000 };
    setToasts((prev) => [...prev, newToast]);
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  return (
    <>
      <div
        className={`fixed ${positionClass[position]} z-50 flex flex-col gap-2 pointer-events-none`}
      >
        {toasts.map((toast) => (
          <div key={toast.id} className="pointer-events-auto">
            <Toast toast={toast} onClose={removeToast} />
          </div>
        ))}
      </div>

      {/* Global toast instance methods attached to window */}
      {typeof window !== 'undefined' && (
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.toastMethods = {
                success: (msg, duration) => window.showToast && window.showToast(msg, 'success', duration),
                error: (msg, duration) => window.showToast && window.showToast(msg, 'error', duration),
                info: (msg, duration) => window.showToast && window.showToast(msg, 'info', duration),
                warning: (msg, duration) => window.showToast && window.showToast(msg, 'warning', duration)
              };
            `,
          }}
        />
      )}

      {/* Expose showToast to window */}
      <script
        dangerouslySetInnerHTML={{
          __html: `window.showToast = ${showToast.toString()}`,
        }}
      />
    </>
  );
};

export { ToastContainer };
export { useToast };

function useToast() {
  const showToast = useCallback((message: string, type: ToastType, duration?: number) => {
    const id = Date.now().toString();
    const event = new CustomEvent('showToast', {
      detail: { id, message, type, duration: duration || 4000 },
    });
    window.dispatchEvent(event);
  }, []);

  return {
    success: (msg: string, duration?: number) => showToast(msg, 'success', duration),
    error: (msg: string, duration?: number) => showToast(msg, 'error', duration),
    info: (msg: string, duration?: number) => showToast(msg, 'info', duration),
    warning: (msg: string, duration?: number) => showToast(msg, 'warning', duration),
  };
}

export default ToastContainer;
