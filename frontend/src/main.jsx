import './style.css';
import { addRoute, startRouter } from './router.jsx';
import { Home } from './views/Home.jsx';
import { Login } from './views/Login.jsx';
import { Register } from './views/Register.jsx';
import { Tickets } from './views/Tickets.jsx';
import { TicketDetail } from './views/TicketDetail.jsx';
import { NotFound } from './views/NotFound.jsx';
import { Header } from './components/Header.jsx';

const app = document.querySelector('#app');

function renderWithHeader(view) {
    return async () => {
        const header = Header();
        const viewContent = view();
        app.innerHTML = header.render() + await viewContent.render();
        header.addEventListeners();
        viewContent.addEventListeners();
    };
}

addRoute('/', renderWithHeader(Home));
addRoute('/login', renderWithHeader(Login));
addRoute('/register', renderWithHeader(Register));
addRoute('/tickets', renderWithHeader(Tickets));
addRoute('/tickets/:id', renderWithHeader(TicketDetail));
addRoute('/404', renderWithHeader(NotFound));


startRouter(app);
