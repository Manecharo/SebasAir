import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import useTranslation from './i18n/useTranslation';
import MapComponent from './components/MapComponent';
import Competitors from './components/Competitors';
import Reports from './components/Reports';
import ScheduleComparison from './components/ScheduleComparison';
import Report from './components/Report';
import FlightDataComponent from './components/FlightDataComponent';
import FlightTracker from './components/FlightTracker';
import MergedFlightView from './components/MergedFlightView';
import Login from './components/Login';
import Register from './components/Register';
import MyFleet from './components/MyFleet';
import ProtectedRoute from './components/ProtectedRoute';
import LanguageSwitcher from './components/LanguageSwitcher';
import { AuthProvider, useAuth } from './context/AuthContext';
import './App.css';
import logoImage from './assets/logo.png';
import AdminUserManagement from './components/Register';

// Create a NavLink component that highlights active links
const NavLink: React.FC<{ to: string; children: React.ReactNode; onClick?: () => void }> = ({ to, children, onClick }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link to={to} className={isActive ? 'active' : ''} onClick={onClick}>
      {children}
    </Link>
  );
};

const NavBar: React.FC = () => {
  const { t } = useTranslation();
  const { isAuthenticated, logout, user } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  
  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
    // Prevent scrolling when menu is open
    if (!menuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  };
  
  const closeMenu = () => {
    setMenuOpen(false);
    document.body.style.overflow = '';
  };
  
  const toggleProfile = () => {
    setProfileOpen(!profileOpen);
  };
  
  const closeProfile = () => {
    setProfileOpen(false);
  };
  
  return (
    <>
      <nav className="navbar">
        <div className="logo-container">
          <img src={logoImage} alt="Colcharter Flight Tracker Logo" className="logo-image" />
        </div>
        
        <button className="mobile-menu-button" onClick={toggleMenu} aria-label="Toggle menu">
          {menuOpen ? '✕' : '☰'}
        </button>
        
        <ul className={`nav-links ${menuOpen ? 'open' : ''}`}>
          {isAuthenticated && (
            <>
              <li><NavLink to="/schedule" onClick={closeMenu}>{t('navigation.schedule')}</NavLink></li>
              <li><NavLink to="/competitors" onClick={closeMenu}>{t('navigation.competitors')}</NavLink></li>
              <li><NavLink to="/reports" onClick={closeMenu}>{t('navigation.reports')}</NavLink></li>
              <li><NavLink to="/merged-flight-view" onClick={closeMenu}>{t('navigation.mergedFlightView')}</NavLink></li>
              <li><NavLink to="/my-fleet" onClick={closeMenu}>{t('navigation.myFleet')}</NavLink></li>
            </>
          )}
        </ul>
        
        <div className="auth-controls">
          {isAuthenticated ? (
            <div className="user-profile">
              <button className="profile-button" onClick={toggleProfile}>
                <span className="user-initial">{user?.name?.charAt(0) || 'U'}</span>
                <span className="user-name">{user?.name || t('auth.user')}</span>
                <span className="dropdown-arrow">▼</span>
              </button>
              
              {profileOpen && (
                <div className="profile-dropdown">
                  <div className="profile-header">
                    <span className="profile-name">{user?.name}</span>
                    <span className="profile-email">{user?.email}</span>
                    <span className="profile-role">{user?.role === 'admin' ? t('auth.admin') : t('auth.user')}</span>
                  </div>
                  <ul className="profile-menu">
                    {user?.role === 'admin' && (
                      <li>
                        <NavLink to="/admin/users" onClick={closeProfile}>
                          {t('navigation.userManagement')}
                        </NavLink>
                      </li>
                    )}
                    <li>
                      <button className="btn-logout" onClick={logout}>
                        {t('auth.logout')}
                      </button>
                    </li>
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <Link to="/login" className="btn-login">{t('auth.login')}</Link>
          )}
        </div>
      </nav>
      
      {/* Background overlay for mobile menu */}
      {menuOpen && <div className="menu-overlay" onClick={closeMenu}></div>}
      
      {/* Background overlay for profile dropdown */}
      {profileOpen && <div className="profile-overlay" onClick={closeProfile}></div>}
    </>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="app-container">
          <NavBar />
          
          <div className="content">
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<MapComponent />} />
              <Route path="/login" element={<Login />} />
              
              {/* Protected routes */}
              <Route element={<ProtectedRoute />}>
                <Route path="/schedule" element={<ScheduleComparison />} />
                <Route path="/competitors" element={<Competitors />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/flight-data" element={<FlightDataComponent />} />
                <Route path="/flight-tracker" element={<FlightTracker />} />
                <Route path="/merged-flight-view" element={<MergedFlightView />} />
                <Route path="/my-fleet" element={<MyFleet />} />
                <Route path="/admin/users" element={<AdminUserManagement />} />
              </Route>
              
              {/* Redirect to login if route doesn't exist */}
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </div>
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;
