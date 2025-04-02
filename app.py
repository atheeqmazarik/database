import os
import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SuperSecureP@ssw0rd'
app.config['MYSQL_DB'] = 'ticketing_system'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("homepage.html")  # Display homepage with the new dashboard links

@app.route("/dashboard")
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT t.id, t.title, t.status, u1.name AS created_by, 
               IFNULL(u2.name, 'Unassigned') AS assigned_to
        FROM tickets t
        JOIN users u1 ON t.created_by = u1.id
        LEFT JOIN users u2 ON t.assigned_to = u2.id
        ORDER BY t.created_at DESC
    """)
    tickets = cur.fetchall()
    cur.close()

    # Temporary user for testing until login system is added
    dummy_user = {"name": "Admin", "role": "admin"}

    return render_template("dashboard.html", tickets=tickets, user=dummy_user)

@app.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        # Dummy user ID for now (e.g., Alice with id=1)
        created_by = 1

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO tickets (title, description, created_by) VALUES (%s, %s, %s)",
            (title, description, created_by)
        )
        mysql.connection.commit()
        cur.close()

        return redirect("/dashboard")

    return render_template("create_ticket.html")


@app.route("/edit/<int:ticket_id>", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    cur = mysql.connection.cursor()

    if request.method == "POST":
        status = request.form["status"]
        assigned_to = request.form.get("assigned_to") or None

        cur.execute("UPDATE tickets SET status=%s, assigned_to=%s WHERE id=%s",
                    (status, assigned_to, ticket_id))
        mysql.connection.commit()
        cur.close()
        return redirect("/dashboard")

    cur.execute("SELECT id, name FROM users WHERE role = 'technician'")
    technicians = cur.fetchall()

    cur.execute("SELECT * FROM tickets WHERE id = %s", (ticket_id,))
    ticket = cur.fetchone()
    cur.close()

    return render_template("edit_ticket.html", ticket=ticket, technicians=technicians)

@app.route("/delete/<int:ticket_id>", methods=["POST"])
def delete_ticket(ticket_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tickets WHERE id = %s", (ticket_id,))
    mysql.connection.commit()
    cur.close()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
