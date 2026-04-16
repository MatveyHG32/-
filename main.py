from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

tasks = {
    'todo': ['Изучить Python', 'Сделать ДЗ'],
    'doing': ['Написать код'],
    'done': ['Установить Flask']
}

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; background: #f0f2f5; padding: 20px; }
        .board { display: flex; gap: 20px; }
        .column { 
            background: white; 
            padding: 15px; 
            border-radius: 8px; 
            width: 300px; 
            min-height: 400px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .column h2 { margin-top: 0; text-align: center; }
        .task { 
            background: #e3f2fd; 
            padding: 12px; 
            margin: 10px 0; 
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .task-buttons { display: flex; gap: 5px; }
        .btn { 
            padding: 5px 10px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer;
            font-size: 12px;
        }
        .btn-move { background: #2196F3; color: white; }
        .btn-delete { background: #f44336; color: white; }
        .btn:hover { opacity: 0.8; }
        form { display: flex; margin: 10px 0; }
        input { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button[type="submit"] { 
            padding: 8px 15px; 
            background: #4CAF50; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            margin-left: 5px; 
            cursor: pointer; 
        }
        .todo { border-top: 3px solid #2196F3; }
        .doing { border-top: 3px solid #FF9800; }
        .done { border-top: 3px solid #4CAF50; }
    </style>
</head>
<body>
    <h1 style="text-align: center;">📋 Канбан доска</h1>
    <div class="board">
        {% for col in ['todo', 'doing', 'done'] %}
        <div class="column {{ col }}">
            <h2>{{ {'todo': '📝 To Do', 'doing': '⚡ Doing', 'done': '✅ Done'}[col] }}</h2>
            <form method="POST" action="/add">
                <input type="text" name="task" placeholder="Новая задача..." required>
                <input type="hidden" name="column" value="{{ col }}">
                <button type="submit">+</button>
            </form>
            {% for task in tasks[col] %}
            <div class="task">
                <span>{{ task }}</span>
                <div class="task-buttons">
                    {% if col == 'todo' %}
                    <form method="POST" action="/move" style="display:inline;">
                        <input type="hidden" name="task" value="{{ task }}">
                        <input type="hidden" name="from" value="{{ col }}">
                        <input type="hidden" name="to" value="doing">
                        <button type="submit" class="btn btn-move">→</button>
                    </form>
                    {% elif col == 'doing' %}
                    <form method="POST" action="/move" style="display:inline;">
                        <input type="hidden" name="task" value="{{ task }}">
                        <input type="hidden" name="from" value="{{ col }}">
                        <input type="hidden" name="to" value="todo">
                        <button type="submit" class="btn btn-move">←</button>
                    </form>
                    <form method="POST" action="/move" style="display:inline;">
                        <input type="hidden" name="task" value="{{ task }}">
                        <input type="hidden" name="from" value="{{ col }}">
                        <input type="hidden" name="to" value="done">
                        <button type="submit" class="btn btn-move">→</button>
                    </form>
                    {% elif col == 'done' %}
                    <form method="POST" action="/move" style="display:inline;">
                        <input type="hidden" name="task" value="{{ task }}">
                        <input type="hidden" name="from" value="{{ col }}">
                        <input type="hidden" name="to" value="doing">
                        <button type="submit" class="btn btn-move">←</button>
                    </form>
                    {% endif %}
                    <form method="POST" action="/delete" style="display:inline;">
                        <input type="hidden" name="task" value="{{ task }}">
                        <input type="hidden" name="column" value="{{ col }}">
                        <button type="submit" class="btn btn-delete">✕</button>
                    </form>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML, tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    column = request.form['column']
    tasks[column].append(task)
    return redirect(url_for('index'))


@app.route('/move', methods=['POST'])
def move_task():
    task = request.form['task']
    from_col = request.form['from']
    to_col = request.form['to']

    if task in tasks[from_col]:
        tasks[from_col].remove(task)
        tasks[to_col].append(task)

    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_task():
    task = request.form['task']
    column = request.form['column']

    if task in tasks[column]:
        tasks[column].remove(task)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)