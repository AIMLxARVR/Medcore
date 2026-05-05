import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

/**
 * ErrorBoundary component to catch React component errors
 * Prevents entire app from crashing when a component fails
 */
class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReset = (): void => {
    this.setState({
      hasError: false,
      error: null,
    });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '200px',
          padding: '32px',
          textAlign: 'center',
          background: '#FEF2F2',
          borderRadius: '12px',
          margin: '16px',
          border: '1px solid #FECACA',
        }}>
          <AlertTriangle 
            size={32} 
            color="#DC2626" 
            style={{ marginBottom: '12px' }}
          />
          <h3 style={{
            fontSize: '16px',
            fontWeight: 700,
            color: '#0F172A',
            marginBottom: '8px',
          }}>
            Something went wrong
          </h3>
          <p style={{
            fontSize: '13px',
            color: '#64748B',
            marginBottom: '16px',
            maxWidth: '400px',
          }}>
            {this.state.error?.message || 'An unexpected error occurred. Please try again.'}
          </p>
<button 
            onClick={this.handleReset}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '5px 11px',
              fontSize: '12px',
              fontWeight: 700,
              background: '#0C4A6E',
              color: '#fff',
              border: '1px solid #0C4A6E',
              borderRadius: '8px',
              cursor: 'pointer',
              fontFamily: 'inherit',
            }}
          >
            <RefreshCw size={12} />
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

/**
 * Higher-order component to wrap a component with ErrorBoundary
 * 
 * @param Component - Component to wrap
 * @returns Wrapped component with error boundary
 */
export function withErrorBoundary<P extends object>(
  WrappedComponent: React.ComponentType<P>,
  errorBoundaryProps?: Omit<Props, 'children'>
): React.ComponentType<P> {
  return function WithErrorBoundary(props: P) {
    return (
      <ErrorBoundary {...errorBoundaryProps}>
        <WrappedComponent {...props} />
      </ErrorBoundary>
    );
  };
}
