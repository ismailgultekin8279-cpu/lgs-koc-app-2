import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        this.setState({ error, errorInfo });
        console.error("Uncaught error:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: 20, backgroundColor: '#fee2e2', color: '#991b1b', height: '100vh' }}>
                    <h1>Bir Hata Oluştu :(</h1>
                    <p>Uygulama yüklenirken beklenmedik bir hata oluştu.</p>
                    <details style={{ whiteSpace: 'pre-wrap', marginTop: 20 }}>
                        <summary>Hata Detayları (Tıklayınız)</summary>
                        <h3>{this.state.error && this.state.error.toString()}</h3>
                        <p>{this.state.errorInfo && this.state.errorInfo.componentStack}</p>
                    </details>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
