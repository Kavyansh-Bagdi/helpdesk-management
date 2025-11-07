import { login } from '../api.jsx';
import { navigate } from '../router.jsx';

export function Login() {
  const render = () => {
    return `
      <div class="container">
        <h2>Login</h2>
        <form id="login-form">
          <input type="email" id="email" placeholder="Email" required>
          <input type="password" id="password" placeholder="Password" required>
          <button type="submit">Login</button>
        </form>
        <div class="sub-form-container">
            <p>Don't have an account? <a href="/register">Register</a></p>
        </div>
      </div>
    `;
  };

  const addEventListeners = () => {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      try {
        const data = await login(email, password);
        localStorage.setItem('token', data.token);
        navigate('/tickets');
      } catch (error) {
        alert('Login failed: ' + error.message);
      }
    });
  };

  // Return an object with render and a method to add listeners
  return {
      render,
      addEventListeners
  };
}
