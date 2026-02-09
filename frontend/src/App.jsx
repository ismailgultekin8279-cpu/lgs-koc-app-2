import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import StudentDashboard from './pages/StudentDashboard';
import CoachDashboard from './pages/CoachDashboard';
import OnboardingPage from './pages/OnboardingPage';
import ExamEntryPage from './pages/ExamEntryPage';
import ExamResultsPage from './pages/ExamResultsPage';
import SettingsPage from './pages/SettingsPage';
import CurriculumPage from './pages/CurriculumPage';
import CurriculumAdminPage from './pages/CurriculumAdminPage';
import Layout from './components/layout/Layout';

// Layout wrapper to adapt 'children' prop to 'Outlet' pattern
const LayoutWrapper = () => {
  return (
    <Layout>
      <Outlet />
    </Layout>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected/Layout Routes */}
        <Route element={<LayoutWrapper />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/student-dashboard" element={<StudentDashboard />} />
          <Route path="/plan" element={<StudentDashboard />} />
          <Route path="/coach-dashboard" element={<CoachDashboard />} />
          <Route path="/onboarding" element={<OnboardingPage />} />
          <Route path="/exams" element={<ExamEntryPage />} />
          <Route path="/analytics" element={<ExamResultsPage />} />
          <Route path="/curriculum" element={<CurriculumPage />} />
          <Route path="/admin/curriculum" element={<CurriculumAdminPage />} />
          <Route path="/settings" element={<SettingsPage />} />

          {/* Legacy/Duplicate Routes Handling */}
          <Route path="/exam-entry" element={<Navigate to="/exams" replace />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
