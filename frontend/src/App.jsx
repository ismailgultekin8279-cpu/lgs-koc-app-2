import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ExamEntryPage from './pages/ExamEntryPage';
import OnboardingPage from './pages/OnboardingPage';
import LoginPage from './pages/LoginPage';
import { StudentProvider, useStudent } from './context/StudentContext';

function PrivateRoute({ children }) {
  const { student, loading } = useStudent();
  if (loading) return <div>Yükleniyor...</div>;
  if (!student) return <Navigate to="/login" />;
  return children;
}

function App() {
  return (
    <StudentProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/plan" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/exams" element={<PrivateRoute><ExamEntryPage /></PrivateRoute>} />
          <Route path="/analytics" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/settings" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        </Routes>
      </BrowserRouter>
    </StudentProvider>
  );
}

export default App;
