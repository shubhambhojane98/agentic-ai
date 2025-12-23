document.addEventListener('DOMContentLoaded', function () {
    const addBtn = document.getElementById('add-btn');
    const todoInput = document.getElementById('todo-input');
    const todoList = document.getElementById('todo-list');

    function createTodoItem(text) {
        const li = document.createElement('li');
        li.textContent = text;
        li.addEventListener('click', function () {
            li.classList.toggle('completed');
        });
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.className = 'delete-btn';
        deleteBtn.onclick = function (e) {
            e.stopPropagation();
            li.remove();
        };
        li.appendChild(deleteBtn);
        return li;
    }

    addBtn.addEventListener('click', function () {
        const text = todoInput.value.trim();
        if (text) {
            const todoItem = createTodoItem(text);
            todoList.appendChild(todoItem);
            todoInput.value = '';
        }
    });

    todoInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            addBtn.click();
        }
    });
});
