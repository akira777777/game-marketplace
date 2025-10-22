import React from 'react';
import { clsx } from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  className,
  id,
  ...props
}) => {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={clsx(
          'block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm',
          'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100',
          'placeholder-gray-400 dark:placeholder-gray-500',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
          'disabled:bg-gray-50 dark:disabled:bg-gray-700 disabled:cursor-not-allowed',
          error && 'border-red-300 focus:ring-red-500',
          className
        )}
        {...props}
      />
      {(error || helperText) && (
        <p className={clsx(
          'mt-1 text-sm',
          error ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'
        )}>
          {error || helperText}
        </p>
      )}
    </div>
  );
};