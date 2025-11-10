import { navigate } from '../router.jsx';

export function Header() {
  const render = () => {
    const token = localStorage.getItem('token');
    return `
      <header>
        <nav>
            <div class="nav-left">
                <a href="/" class="logo">
                    <svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="48px" height="48px" baseProfile="basic"><path fill="#6be3a2" d="M39.707,14.293l-10-10C29.52,4.105,29.266,4,29,4H13c-2.757,0-5,2.243-5,5v30c0,2.757,2.243,5,5,5h22	c2.757,0,5-2.243,5-5V15C40,14.735,39.895,14.48,39.707,14.293z"/><path fill="#324561" d="M40,16h-7c-2.757,0-5-2.243-5-5V4c0-0.552,0.447-1,1-1s1,0.448,1,1v7c0,1.654,1.346,3,3,3h7	c0.553,0,1,0.448,1,1S40.553,16,40,16z"/><path fill="#324561" d="M32,25H16c-0.553,0-1-0.448-1-1s0.447-1,1-1h16c0.553,0,1,0.448,1,1S32.553,25,32,25z"/><path fill="#324561" d="M32,30H16c-0.553,0-1-0.448-1-1s0.447-1,1-1h16c0.553,0,1,0.448,1,1S32.553,30,32,30z"/><path fill="#324561" d="M26,35H16c-0.553,0-1-0.448-1-1s0.447-1,1-1h10c0.553,0,1,0.448,1,1S26.553,35,26,35z"/></svg>
                </a>
                <a href="/">Home</a>
                ${token ? `<a href="/tickets">Tickets</a>` : ''}
            </div>
            <div class="nav-right">
              ${token ? `
                <a href="#" id="logout-link">Logout</a>
              ` : `
                <a href="/login">Login</a>
                <a href="/register">Register</a>
              `}
            </div>
        </nav>
      </header>
    `;
  };

  const addEventListeners = () => {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
      logoutLink.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        navigate('/login');
      });
    }
  };

  return {
      render,
      addEventListeners
  };
}
