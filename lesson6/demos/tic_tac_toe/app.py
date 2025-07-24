from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tic-tac-toe-secret'

def check_winner(board):
    # Rows, columns and diagonals
    lines = [board[0], board[1], board[2],
             [board[0][0], board[1][0], board[2][0]],
             [board[0][1], board[1][1], board[2][1]],
             [board[0][2], board[1][2], board[2][2]],
             [board[0][0], board[1][1], board[2][2]],
             [board[0][2], board[1][1], board[2][0]]]
    for line in lines:
        if line[0] and line[0] == line[1] == line[2]:
            return line[0]
    return None

def is_full(board):
    return all(cell for row in board for cell in row)

@app.route("/", methods=["GET", "POST"])
def index():
    if "board" not in session:
        session["board"] = [["", "", ""] for _ in range(3)]
        session["turn"] = "X"
        session["winner"] = None

    board = session["board"]
    turn = session["turn"]
    winner = session["winner"]

    if request.method == "POST" and not winner:
        row = int(request.form["row"])
        col = int(request.form["col"])
        if board[row][col] == "":
            board[row][col] = turn
            winner = check_winner(board)
            if winner:
                session["winner"] = winner
            elif is_full(board):
                session["winner"] = "Draw"
            else:
                session["turn"] = "O" if turn == "X" else "X"
        session["board"] = board

    return render_template("index.html", board=board, turn=session["turn"], winner=session["winner"])

@app.route("/reset")
def reset():
    session.pop("board", None)
    session.pop("turn", None)
    session.pop("winner", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)