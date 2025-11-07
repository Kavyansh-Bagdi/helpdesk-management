import { getTicket, getComments, addComment, updateTicket } from '../api.jsx';
import { navigate } from '../router.jsx';

export function TicketDetail() {
  let ticket = null;
  let comments = [];
  const ticketId = window.location.pathname.split('/')[2];

  const render = () => {
    if (!ticket) {
      return `<div class="container"><p>Loading ticket...</p></div>`;
    }

    const commentsHtml = comments.map(comment => `
      <div class="comment-item">
        <p>${comment.text}</p>
        <span>By: User ${comment.author_id}</span>
      </div>
    `).join('');

    return `
      <div class="container">
        <a href="/tickets">&larr; Back to Tickets</a>
        <div class="ticket-detail">
          <h2>${ticket.title}</h2>
          <p>${ticket.description}</p>
          <p>Status: <span class="status status-${ticket.status}">${ticket.status}</span></p>
        </div>

        <div class="ticket-actions">
            <select id="status-select">
                <option value="open" ${ticket.status === 'open' ? 'selected' : ''}>Open</option>
                <option value="in_progress" ${ticket.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                <option value="closed" ${ticket.status === 'closed' ? 'selected' : ''}>Closed</option>
            </select>
            <button id="update-status-btn">Update Status</button>
        </div>

        <hr>

        <h3>Comments</h3>
        <div id="comments-list">
          ${commentsHtml || '<p>No comments yet.</p>'}
        </div>

        <div class="sub-form-container">
            <form id="add-comment-form">
              <textarea id="comment-text" placeholder="Add a comment..." required></textarea>
              <button type="submit">Add Comment</button>
            </form>
        </div>
      </div>
    `;
  };

  const addEventListeners = async () => {
    try {
      ticket = await getTicket(ticketId);
      comments = await getComments(ticketId);
      // This is a simplified re-render. In a real app, you'd use a state management solution.
      document.getElementById('app').innerHTML = render();
      attachDynamicListeners();
    } catch (error) {
        if (error.message.includes('401')) {
            navigate('/login');
        } else {
            alert('Failed to fetch ticket details: ' + error.message);
        }
    }
  };

  const attachDynamicListeners = () => {
    const commentForm = document.getElementById('add-comment-form');
    commentForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const text = document.getElementById('comment-text').value;
      try {
        const newComment = await addComment(ticketId, text);
        comments.push(newComment);
        document.getElementById('comment-text').value = '';
         // This is a simplified re-render.
        document.getElementById('app').innerHTML = render();
        attachDynamicListeners();
      } catch (error) {
        alert('Failed to add comment: ' + error.message);
      }
    });

    const updateBtn = document.getElementById('update-status-btn');
    updateBtn.addEventListener('click', async () => {
        const newStatus = document.getElementById('status-select').value;
        try {
            const updatedTicket = await updateTicket(ticketId, newStatus);
            ticket = updatedTicket;
            // This is a simplified re-render.
            document.getElementById('app').innerHTML = render();
            attachDynamicListeners();
        } catch (error) {
            alert('Failed to update status: ' + error.message);
        }
    });
  }

  return {
      render,
      addEventListeners
  };
}
