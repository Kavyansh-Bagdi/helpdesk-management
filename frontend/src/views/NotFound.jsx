export function NotFound() {
  const render = () => {
    return `
      <div class="container">
        <h2>404 - Not Found</h2>
        <div class="sub-form-container">
            <p>The page you are looking for does not exist.</p>
            <a href="/">Go Home</a>
        </div>
      </div>
    `;
  };

  const addEventListeners = () => {};

  return {
      render,
      addEventListeners
  };
}
