from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy data
tickets = [
    {'id': 1, 'title': 'Server Issue', 'status': 'Open', 'description': 'Server down.'},
    {'id': 2, 'title': 'Login Failure', 'status': 'Resolved', 'description': 'User unable to log in.'}
]

@app.route('/')
def home():
    # Calculate ticket statistics
    open_tickets = sum(1 for t in tickets if t['status'] == 'Open')
    resolved_tickets = sum(1 for t in tickets if t['status'] == 'Resolved')
    in_progress_tickets = sum(1 for t in tickets if t['status'] == 'In Progress')

    # Fetch the most recent tickets (for demonstration, use the first 5 tickets)
    recent_tickets = tickets[:5]

    return render_template('home.html',
                           title="Home",
                           open_tickets=open_tickets,
                           resolved_tickets=resolved_tickets,
                           in_progress_tickets=in_progress_tickets,
                           recent_tickets=recent_tickets)


@app.route('/tickets')
def ticket_list():
    return render_template('ticket_list.html', tickets=tickets, title="Tickets")

@app.route('/ticket/<int:ticket_id>')
def ticket_details(ticket_id):
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    if not ticket:
        return "Ticket not found", 404
    return render_template('ticket_details.html', ticket=ticket, title=f"Ticket {ticket_id}")

@app.route('/create-ticket', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        # Retrieve form data
        new_ticket = {
            'id': len(tickets) + 1,
            'title': request.form['title'],
            'status': request.form['status'],
            'description': request.form['description']
        }
        tickets.append(new_ticket)
        return redirect(url_for('ticket_list'))
    return render_template('form.html', form_title="Create New Ticket")

@app.route('/edit-ticket/<int:ticket_id>', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    if not ticket:
        return "Ticket not found", 404

    if request.method == 'POST':
        # Update ticket details based on form submission
        ticket['title'] = request.form['title']
        ticket['status'] = request.form['status']
        ticket['description'] = request.form['description']
        return redirect(url_for('ticket_list'))
    
    return render_template('edit_ticket.html', ticket=ticket, form_title="Edit Ticket")


if __name__ == '__main__':
    app.run(debug=True)
