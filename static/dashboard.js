function showFullMessage(html) {
    document.getElementById('dashboard-container').style.display = 'none';
    var msgView = document.getElementById('full-message-view');
    msgView.innerHTML = html;
    msgView.style.display = 'block';
    window.scrollTo(0,0);
}
function backToDashboard() {
    document.getElementById('full-message-view').style.display = 'none';
    document.getElementById('dashboard-container').style.display = 'block';
    window.scrollTo(0,0);
}

function escapeAttr(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function renderEmailList(listId, emails, type) {
    const list = document.getElementById(listId);
    list.innerHTML = '';
    if (!emails.length) {
        list.innerHTML = `<li style="padding:18px 20px; color:#aaa;">No emails found.</li>`;
        return;
    }
    emails.forEach(email => {
        let dataAttrs = '';
        if (type === 'sent') {
            dataAttrs =
                'data-to="' + escapeAttr(email.to || '') + '" ' +
                'data-subject="' + escapeAttr(email.subject || '') + '" ' +
                'data-date="' + escapeAttr(email.date || '') + '" ' +
                'data-snippet="' + escapeAttr(email.snippet || '') + '" ' +
                'data-body="' + escapeAttr(email.body || '') + '" ' +
                'data-type="sent"';
        } else {
            dataAttrs =
                'data-from="' + escapeAttr(email.from || '') + '" ' +
                'data-subject="' + escapeAttr(email.subject || '') + '" ' +
                'data-date="' + escapeAttr(email.date || '') + '" ' +
                'data-snippet="' + escapeAttr(email.snippet || '') + '" ' +
                'data-body="' + escapeAttr(email.body || '') + '" ' +
                'data-type="received"';
        }
        list.innerHTML += `
            <li class="email-item" tabindex="0" ${dataAttrs}>
                <div class="email-summary">
                    <span class="${type === 'sent' ? 'email-to' : 'email-from'}" title="${type === 'sent' ? 'To' : 'From'}">${type === 'sent' ? email.to : email.from}</span>
                    <span class="email-subject">${email.subject}</span>
                    <span class="email-date">${email.date}</span>
                    <span class="email-status" style="margin-left:auto; min-width:70px; text-align:right; color:${email.status === 'Unread' ? 'red' : '#888'};">
                        ${email.status}
                    </span>
                </div>
            </li>
        `;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    renderEmailList('sent-list', sentEmails, 'sent');
    renderEmailList('received-list', receivedEmails, 'received');
    document.getElementById('sent-list').addEventListener('click', handleEmailClick);
    document.getElementById('received-list').addEventListener('click', handleEmailClick);
    document.getElementById('close-modal').onclick = closeModal;

    window.onclick = function(event) {
        const modal = document.getElementById('message-modal');
        if (event.target === modal) closeModal();
    };
});

function handleEmailClick(e) {
    let item = e.target.closest('.email-item');
    if (item) {
        let type = item.dataset.type;
        let body = item.dataset.body || '<i>No body found.</i>';
        // If not HTML, convert newlines to <br>
        if (!body.trim().startsWith('<')) {
            body = body.replace(/\n/g, '<br>');
        }
        let html = `
            <h2 style="color:#D89B94;">${type === 'sent' ? 'Sent Email' : 'Received Email'}</h2>
            ${type === 'sent'
                ? `<b>To:</b> ${item.dataset.to}<br>`
                : `<b>From:</b> ${item.dataset.from}<br>`
            }
            <b>Subject:</b> ${item.dataset.subject}<br>
            <b>Date:</b> ${item.dataset.date}<br>
            <b>Status:</b> ${item.querySelector('.email-status')?.textContent || ''}<br>
            ${item.dataset.snippet ? `<b>Snippet:</b> <div style="margin-top:8px; color:#444;">${item.dataset.snippet}</div>` : ''}
            <hr>
            <div class="email-body-content" style="margin-top:12px; color:#222; word-break:break-word;">
                ${body}
            </div>
        `;
        showModal(html);
    }
}

function showModal(html) {
    document.getElementById('modal-body').innerHTML = html;
    document.getElementById('message-modal').style.display = 'block';
    document.body.classList.add('modal-open');
}
function closeModal() {
    document.getElementById('message-modal').style.display = 'none';
    document.body.classList.remove('modal-open');
}

function closeComposeModal() {
    document.getElementById('compose-modal').style.display = 'none';
    document.body.classList.remove('modal-open');
}