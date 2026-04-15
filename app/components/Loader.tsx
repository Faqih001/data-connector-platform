'use client';

export interface LoaderProps {
  fullScreen?: boolean;
  size?: 'sm' | 'md' | 'lg';
  message?: string;
}

export function Loader({ fullScreen = true, size = 'md', message }: LoaderProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
  };

  const containerClass = fullScreen
    ? 'fixed inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-50'
    : 'flex items-center justify-center py-8';

  return (
    <div className={containerClass}>
      <div className="flex flex-col items-center gap-4">
        {/* Modern animated spinner */}
        <div className={`${sizeClasses[size]} relative`}>
          {/* Outer rotating ring */}
          <div
            className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-500 border-r-blue-500"
            style={{
              animation: 'spin 1s linear infinite',
            }}
          />

          {/* Inner rotating ring - counter rotation */}
          <div
            className="absolute inset-2 rounded-full border-3 border-transparent border-b-purple-500 border-l-purple-500"
            style={{
              animation: 'spin 1.5s linear reverse infinite',
            }}
          />

          {/* Center dot */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" />
          </div>
        </div>

        {/* Loading message */}
        {message && (
          <div className="text-center">
            <p className="text-gray-700 font-medium">{message}</p>
            <div className="flex gap-1 mt-2 justify-center">
              <span
                className="w-1 h-1 bg-blue-500 rounded-full"
                style={{
                  animation: 'pulse 1.4s infinite',
                  animationDelay: '0s',
                }}
              />
              <span
                className="w-1 h-1 bg-blue-500 rounded-full"
                style={{
                  animation: 'pulse 1.4s infinite',
                  animationDelay: '0.2s',
                }}
              />
              <span
                className="w-1 h-1 bg-blue-500 rounded-full"
                style={{
                  animation: 'pulse 1.4s infinite',
                  animationDelay: '0.4s',
                }}
              />
            </div>
          </div>
        )}

        {/* CSS for animations */}
        <style>{`
          @keyframes spin {
            from {
              transform: rotate(0deg);
            }
            to {
              transform: rotate(360deg);
            }
          }

          @keyframes pulse {
            0%, 100% {
              opacity: 0.3;
            }
            50% {
              opacity: 1;
            }
          }
        `}</style>
      </div>
    </div>
  );
}

export default Loader;
