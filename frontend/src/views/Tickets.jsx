import { getTickets, createTicket } from '../api.jsx';
import { navigate } from '../router.jsx';

export function Tickets() {
  let tickets = [];

  const render = () => {
    const ticketsHtml = tickets.map(ticket => `
      <div class="ticket-item" data-id="${ticket.id}">
        <h3>${ticket.title}</h3>
        <p>Status: <span class="status status-${ticket.status}">${ticket.status}</span></p>
      </div>
    `).join('');

    return `
      <div class="container">
        <h2>Tickets</h2>
        <div id="tickets-list">
          ${ticketsHtml || '<p>No tickets found.</p>'}
        </div>
        <hr>
        <div class="sub-form-container">
            <h3>Create New Ticket</h3>
            <form id="create-ticket-form">
              <input type="text" id="title" placeholder="Title" required>
              <textarea id="description" placeholder="Description" required></textarea>
              <button type="submit">Create Ticket</button>
            </form>
        </div>
      </div>
    `;
  };

  const addEventListeners = async () => {
    try {
        tickets = await getTickets();
        document.getElementById('tickets-list').innerHTML = tickets.map(ticket => `
            <div class="ticket-item" data-id="${ticket.id}">
                <h3>${ticket.title}</h3>
                <p>Status: <span class="status status-${ticket.status}">${ticket.status}</span></p>
            </div>
        `).join('');
    } catch (error) {
        if (error.message.includes('401')) {
            navigate('/login');
        } else {
            alert('Failed to fetch tickets: ' + error.message);
        }
        return;
    }

    document.querySelectorAll('.ticket-item').forEach(item => {
      item.addEventListener('click', () => {
        const ticketId = item.dataset.id;
        navigate(`/tickets/${ticketId}`);
      });
    });

    const form = document.getElementById('create-ticket-form');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('title').value;
      const description = document.getElementById('description').value;
      try {
        const newTicket = await createTicket(title, description);
        tickets.push(newTicket);
        // Re-render logic would be more complex in a real framework
        // For now, just navigate to the new ticket
        navigate(`/tickets/${newTicket.id}`);
      } catch (error) {
        alert('Failed to create ticket: ' + error.message);
      }
    });
  };

  return {
      render,
      addEventListeners
  };
}
