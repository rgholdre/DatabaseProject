import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { StudentProvider, useStudent } from './context/StudentContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Signup from './pages/Signup';
import ClassSearch from './pages/ClassSearch';
import MyEnrollments from './pages/MyEnrollments';
import StudentInfo from './pages/StudentInfo';
import Profile from './pages/Profile';
import Enrollments from './pages/Enrollments'
import './App.css';

// Protected Route component
function ProtectedRoute({ children }) {
  const { student } = useStudent();
  if (!student) {
    return <Navigate to="/" replace />;
  }
  return children;
}

function AppContent() {
  const { student } = useStudent();

  return (
    <div className="App">
      {student && <Navbar />}
      <Routes>
        <Route path="/" element={student ? <Navigate to="/classes" replace /> : <Login />} />
        <Route path="/signup" element={student ? <Navigate to="/classes" replace /> : <Signup />} />
        <Route path="/classes" element={
          <ProtectedRoute><ClassSearch /></ProtectedRoute>
        } />
        <Route path="/my-enrollments" element={
          <ProtectedRoute><MyEnrollments /></ProtectedRoute>
        } />
        <Route path="/profile" element={
          <ProtectedRoute><Profile /></ProtectedRoute>
        } />
        <Route path="/student" element={
          <ProtectedRoute><StudentInfo /></ProtectedRoute>
        } />
         <Route path="/enrollments" element={
          <ProtectedRoute><Enrollments /></ProtectedRoute>
        } />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <Router>
      <StudentProvider>
        <AppContent />
      </StudentProvider>
    </Router>
  );
}

export default App;

