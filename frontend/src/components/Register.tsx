import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import useTranslation from '../i18n/useTranslation';
import { useAuth } from '../context/AuthContext';
import '../App.css';

const AdminUserManagement: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();
  const [users, setUsers] = useState<any[]>([]);
  const [newUser, setNewUser] = useState({
    name: '',
    email: '',
    password: '',
    role: 'user'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingUsers, setLoadingUsers] = useState(true);

  // Check if current user is admin, if not redirect to home
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    
    if (user?.role !== 'admin') {
      navigate('/');
      return;
    }
    
    // Fetch existing users
    fetchUsers();
  }, [isAuthenticated, user, navigate]);

  const fetchUsers = async () => {
    setLoadingUsers(true);
    try {
      // In a real application, this would be an API call
      // For now, we'll simulate it with a timeout
      setTimeout(() => {
        // Mock data for demonstration
        setUsers([
          { id: 1, name: 'Admin User', email: 'admin@example.com', role: 'admin' },
          { id: 2, name: 'Test User', email: 'user@example.com', role: 'user' }
        ]);
        setLoadingUsers(false);
      }, 1000);
    } catch (err) {
      setError('Failed to fetch users');
      setLoadingUsers(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setNewUser(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      // In a real application, this would be an API call to create a user
      // For now, we'll simulate it with a timeout
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Add the new user to our list (in a real app, this would come from the API response)
      const newId = users.length + 1;
      const createdUser = { ...newUser, id: newId };
      setUsers(prev => [...prev, createdUser]);
      
      // Reset the form
      setNewUser({
        name: '',
        email: '',
        password: '',
        role: 'user'
      });
      
      setSuccess(`User ${newUser.email} created successfully`);
    } catch (err) {
      setError('Failed to create user');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId: number) => {
    try {
      // In a real application, this would be an API call
      // For now, we'll simulate it with a timeout
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Remove the user from our list
      setUsers(prev => prev.filter(user => user.id !== userId));
      setSuccess('User deleted successfully');
    } catch (err) {
      setError('Failed to delete user');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>{t('navigation.userManagement')}</h2>
        
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="name">{t('auth.name')}</label>
            <input
              type="text"
              id="name"
              name="name"
              value={newUser.name}
              onChange={handleInputChange}
              required
              placeholder={t('auth.name')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">{t('auth.email')}</label>
            <input
              type="email"
              id="email"
              name="email"
              value={newUser.email}
              onChange={handleInputChange}
              required
              placeholder={t('auth.email')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">{t('auth.password')}</label>
            <input
              type="password"
              id="password"
              name="password"
              value={newUser.password}
              onChange={handleInputChange}
              required
              placeholder={t('auth.password')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="role">{t('auth.role')}</label>
            <select
              id="role"
              name="role"
              value={newUser.role}
              onChange={handleInputChange}
              required
            >
              <option value="user">{t('auth.user')}</option>
              <option value="admin">{t('auth.admin')}</option>
            </select>
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="btn-register" 
              disabled={loading}
            >
              {loading ? t('common.loading') : t('auth.register')}
            </button>
          </div>
        </form>
        
        <div className="users-list">
          <h3>{t('navigation.userManagement')}</h3>
          
          {loadingUsers ? (
            <p>{t('common.loading')}</p>
          ) : users.length === 0 ? (
            <p>{t('common.noData')}</p>
          ) : (
            <table className="users-table">
              <thead>
                <tr>
                  <th>{t('auth.name')}</th>
                  <th>{t('auth.email')}</th>
                  <th>{t('auth.role')}</th>
                  <th>{t('common.actions')}</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id}>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.role}</td>
                    <td>
                      <button 
                        className="btn-delete" 
                        onClick={() => handleDeleteUser(user.id)}
                        disabled={user.id === 1} // Prevent deleting the main admin
                      >
                        {t('common.delete')}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminUserManagement; 