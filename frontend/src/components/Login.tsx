import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useTranslation from '../i18n/useTranslation';
import { useAuth } from '../context/AuthContext';
import '../App.css';

const Login: React.FC = () => {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // In a real application, this would call your backend API
      // For now, we'll simulate a successful login with mock data
      // const response = await axios.post('http://localhost:8000/auth/login', { 
      //   email, password 
      // });
      
      // Mock successful login
      const mockResponse = {
        data: {
          user: {
            id: 1,
            name: 'Test User',
            email: email,
            role: email.includes('admin') ? 'admin' : 'user'
          },
          token: 'mock-jwt-token'
        }
      };
      
      // Call the login function from AuthContext
      login(mockResponse.data.token, mockResponse.data.user);
      
      // Redirect to home page
      navigate('/');
    } catch (err) {
      console.error('Login error:', err);
      setError(t('errors.loginFailed'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>{t('auth.login')}</h2>
        <p className="auth-subtitle">{t('flightTracker.title')}</p>
        
        {error && <div className="auth-error">{error}</div>}
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">{t('auth.email')}</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder={`${t('auth.email')}...`}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">{t('auth.password')}</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder={`${t('auth.password')}...`}
            />
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="btn-login" 
              disabled={loading}
            >
              {loading ? t('common.loading') : t('auth.login')}
            </button>
          </div>
          
          <div className="auth-note">
            <p>{t('errors.unauthorized')}</p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login; 