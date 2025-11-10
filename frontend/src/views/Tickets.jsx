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
              <input type="file" id="image" accept="image/*" multiple>
              <div id="image-preview-container" class="image-preview-container" style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
              </div>
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

    const imageInput = document.getElementById('image');
    const imagePreviewContainer = document.getElementById('image-preview-container');

    imageInput.addEventListener('change', () => {
      imagePreviewContainer.innerHTML = '';
      const files = imageInput.files;
      if (files) {
        for (const file of files) {
          const reader = new FileReader();
          reader.onload = (e) => {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '200px';
            img.style.marginTop = '10px';
            imagePreviewContainer.appendChild(img);
          };
          reader.readAsDataURL(file);
        }
      }
    });

    const form = document.getElementById('create-ticket-form');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('title').value;
      const description = document.getElementById('description').value;
      const imageInput = document.getElementById('image');
      const images = imageInput.files;
      try {
        const newTicket = await createTicket(title, description, images);
        tickets.push(newTicket);
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
