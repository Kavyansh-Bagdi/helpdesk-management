import { register } from '../api.jsx';
import { navigate } from '../router.jsx';

export function Register() {
  const render = () => {
    return `
      <div class="container">
        <h2>Register</h2>
        <form id="register-form">
          <input type="text" id="username" placeholder="Username" required>
          <input type="email" id="email" placeholder="Email" required>
          <input type="password" id="password" placeholder="Password" required>
          <button type="submit">Register</button>
        </form>
        <div class="sub-form-container">
            <p>Already have an account? <a href="/login">Login</a></p>
        </div>
      </div>
    `;
  };

  const addEventListeners = () => {
    const form = document.getElementById('register-form');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      try {
        await register(username, email, password);
        navigate('/login');
      } catch (error) {
        alert('Registration failed: ' + error.message);
      }
    });
  };

  return {
      render,
      addEventListeners
  };
}
