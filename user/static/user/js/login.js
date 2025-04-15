// Login.js
import React, { useState } from 'react';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // CSRF token handling for Django
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    try {
      const response = await fetch('/api/login/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      });
      
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || 'Login failed. Please try again.');
      } else {
        // Redirect or handle successful login
        window.location.href = '/dashboard';
      }
    } catch (error) {
      setError('Network error. Please try again later.');
      console.error('Login error:', error);
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <input type="hidden" name="csrfmiddlewaretoken" value={document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''} />
        
        <div className="login-logo">BenchMark</div>
        <div className="login-title">Sign in to your account</div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-group">
          <input
            type="text"
            className="login-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <input
            type="password"
            className="login-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        
        <button type="submit" className="login-button">Log in</button>
        
        <div className="create-account">
          <a href="/register">Create Account</a>
        </div>
      </form>
    </div>
  );
}

export default Login;