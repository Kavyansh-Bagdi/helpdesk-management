const routes = {};

export function addRoute(path, component) {
  routes[path] = component;
}

function navigate(path) {
  window.history.pushState({}, path, window.location.origin + path);
  render(path);
}

function handleLinkClick(event) {
  if (event.target.tagName === 'A' && event.target.href.startsWith(window.location.origin)) {
    event.preventDefault();
    const path = new URL(event.target.href).pathname;
    navigate(path);
  }
}

let rootElement = null;

export function startRouter(root) {
  rootElement = root;
  window.onpopstate = () => {
    render(window.location.pathname);
  };
  document.body.addEventListener('click', handleLinkClick);
  render(window.location.pathname);
}

async function render(path) {
  if (!rootElement) {
    return;
  }

  let componentGenerator = routes[path];

  if (!componentGenerator) {
      const matchingRoute = Object.keys(routes).find(route => {
          const routeParts = route.split('/');
          const pathParts = path.split('/');
          if (routeParts.length !== pathParts.length) {
              return false;
          }
          return routeParts.every((part, i) => {
              return part.startsWith(':') || part === pathParts[i];
          });
      });
      if (matchingRoute) {
          componentGenerator = routes[matchingRoute];
      }
  }

  componentGenerator = componentGenerator || routes['/404'];

  if (componentGenerator) {
    const component = componentGenerator();
    rootElement.innerHTML = await component.render();
    if (component.addEventListeners) {
      component.addEventListeners();
    }
  }
}

export { navigate };
