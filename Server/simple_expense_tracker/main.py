from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP(name="ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
        
init_db()

@mcp.tool()
def add_expenses(date, amount, category, subcategory='', note=""):
    """
    Add a new expense to the database.

    Args:
        date (str): The date of the expense.
        amount (float): The amount of the expense.
        category (str): The category of the expense.
        subcategory (str, optional): The subcategory of the expense. Defaults to ''.
        note (str, optional): A note about the expense. Defaults to ''.

    Returns:
        dict: A dictionary with the status and the id of the added expense.
    """
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.execute("""
                INSERT INTO expenses (date, amount, category, subcategory, note)
                VALUES (?, ?, ?, ?, ?)
            """, (date, amount, category, subcategory, note))
        
        return {'status': 'ok', 'id': curr.lastrowid}
    
@mcp.tool()
def list_expenses(start_date, end_date):
    """
    List all expenses in the database in ascending order of id.

    Returns:
        list: A list of dictionaries, each containing the columns of the expenses table.
    """
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.execute("""
                            SELECT * FROM expenses
                            WHERE date BETWEEN ? AND ?
                            ORDER BY id ASC
                            """,
                            (start_date, end_date))
         
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, row)) for row in curr.fetchall()]

@mcp.tool()
def summarize(start_date, end_date, category=None):
    with sqlite3.connect(DB_PATH) as conn:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]
        
        if category:
            query += " AND category = ?"
            params.append(category)
            
        query += " GROUP BY category ORDER BY category ASC"
        
        curr = conn.execute(query, params)
        
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, row)) for row in curr.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()
