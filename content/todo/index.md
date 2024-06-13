---
title: "To-Do List"
date: 2024-06-12
draft: false
---

{{< rawhtml >}}
<style>
    .todo-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }
    .todo-container h2 {
        text-align: center;
        color: #333;
    }
    #new-todo {
        width: calc(100% - 22px);
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    button {
        padding: 10px 20px;
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    button:hover {
        background-color: #218838;
    }
    #todo-list {
        list-style: none;
        padding: 0;
    }
    .todo-item {
        padding: 10px;
        border-bottom: 1px solid #ccc;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .todo-item input[type="checkbox"] {
        margin-right: 10px;
    }
    .todo-item button {
        background-color: #dc3545;
        padding: 5px 10px;
    }
    .todo-item button:hover {
        background-color: #c82333;
    }
    .calendar-container {
        max-width: 500px;
        margin: 20px auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }
    .calendar-container h2 {
        text-align: center;
        color: #333;
    }
    .calendar {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
    }
    .calendar .day {
        width: calc(100% / 7 - 4px);
        padding: 10px;
        border: 1px solid #ccc;
        box-sizing: border-box;
        text-align: center;
        margin-bottom: 4px;
        cursor: pointer;
    }
    .calendar .day.complete {
        background-color: #28a745;
        color: white;
    }
    .calendar .day:hover {
        background-color: #ddd;
    }
</style>

<div class="todo-container">
    <h2 id="todo-title">To-Do List</h2>
    <input type="text" id="new-todo" placeholder="Add a new task">
    <button onclick="addTodo()">Add</button>
    <ul id="todo-list"></ul>
</div>

<div class="calendar-container">
    <h2>Task Calendar</h2>
    <div id="calendar" class="calendar"></div>
</div>

<script>
    var selectedDate = new Date().toISOString().split('T')[0];

    function addTodo() {
        var todoInput = document.getElementById("new-todo");
        var todoText = todoInput.value.trim();
        if (todoText !== "") {
            var todoList = document.getElementById("todo-list");
            var listItem = document.createElement("li");
            listItem.className = "todo-item";
            listItem.innerHTML = '<input type="checkbox" onclick="markComplete(this)">' + todoText + ' <button onclick="removeTodo(this)">Delete</button>';
            todoList.appendChild(listItem);
            saveTodoForDate(selectedDate, todoText);
            todoInput.value = "";
        }
    }

    function removeTodo(button) {
        var listItem = button.parentElement;
        listItem.parentElement.removeChild(listItem);
        saveTodosWithCompletionState(selectedDate);
    }

    function markComplete(checkbox) {
        var listItem = checkbox.parentElement;
        if (checkbox.checked) {
            listItem.classList.add('complete');
        } else {
            listItem.classList.remove('complete');
        }
        updateTaskCompletion(selectedDate);
    }

    function saveTodoForDate(date, todoText) {
        var todos = JSON.parse(localStorage.getItem(date)) || [];
        todos.push({ text: todoText, checked: false });
        localStorage.setItem(date, JSON.stringify(todos));
        console.log("Saved tasks for", date, ":", localStorage.getItem(date));
    }

    function loadTodosForDate(date) {
        var todos = JSON.parse(localStorage.getItem(date)) || [];
        var todoList = document.getElementById("todo-list");
        todoList.innerHTML = ""; // Clear current list
        todos.forEach(function(todo) {
            var listItem = document.createElement("li");
            listItem.className = "todo-item";
            listItem.innerHTML = '<input type="checkbox" onclick="markComplete(this)"' + (todo.checked ? ' checked' : '') + '>' + todo.text + ' <button onclick="removeTodo(this)">Delete</button>';
            todoList.appendChild(listItem);
        });
        document.getElementById("todo-title").innerText = "To-Do List for " + date;
        console.log("Loaded tasks for", date, ":", localStorage.getItem(date));
    }

    function updateTaskCompletion(date) {
        var checkboxes = document.querySelectorAll(".todo-item input[type='checkbox']");
        var completed = Array.from(checkboxes).every(function(checkbox) {
            return checkbox.checked;
        });
        var dayElement = document.getElementById(date);
        if (completed) {
            dayElement.classList.add('complete');
        } else {
            dayElement.classList.remove('complete');
        }
        saveTodosWithCompletionState(date);
    }

    function saveTodosWithCompletionState(date) {
        var todoListItems = document.querySelectorAll(".todo-item");
        var todos = Array.from(todoListItems).map(function(item) {
            var checkbox = item.querySelector("input[type='checkbox']");
            return { text: item.textContent.replace(" Delete", ""), checked: checkbox.checked };
        });
        localStorage.setItem(date, JSON.stringify(todos));
        console.log("Updated tasks with completion state for", date, ":", localStorage.getItem(date));
    }

    function generateCalendar() {
        var calendar = document.getElementById("calendar");
        var currentDate = new Date();
        var monthStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
        var monthEnd = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);

        for (var day = monthStart.getDate(); day <= monthEnd.getDate(); day++) {
            var date = new Date(currentDate.getFullYear(), currentDate.getMonth(), day).toISOString().split('T')[0];
            var dayElement = document.createElement("div");
            dayElement.className = "day";
            dayElement.id = date;
            dayElement.innerText = day;

            dayElement.addEventListener("click", function() {
                selectedDate = this.id;
                loadTodosForDate(selectedDate);
            });

            var todos = JSON.parse(localStorage.getItem(date)) || [];
            if (todos.length > 0) {
                var completed = todos.every(function(todo) {
                    return todo.checked;
                });
                if (completed) {
                    dayElement.classList.add('complete');
                }
            }

            calendar.appendChild(dayElement);
        }
        console.log("Generated calendar for month");
    }

    document.addEventListener("DOMContentLoaded", function() {
        console.log("Page loaded");
        loadTodosForDate(selectedDate);
        generateCalendar();
        updateTaskCompletion(selectedDate);
    });
</script>
{{< /rawhtml >}}
