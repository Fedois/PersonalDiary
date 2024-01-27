document.addEventListener('DOMContentLoaded', () => {
    if(window.innerWidth <= 790 && document.querySelector('#book')){
        document.querySelector('#change-page-sx').name = 'date_mobile'
        document.querySelector('#change-page-dx').name = 'date_mobile'  
    }

    if(document.getElementById('container-index')){
        localStorage.clear()
        
        if(document.getElementById('btn-open')){
            document.getElementById('btn-open').addEventListener('click', ()=>{
                document.getElementById('open-diaries').style.display = 'block'
            })
        }
    
        document.getElementById('new-diary-btn').addEventListener('click', ()=>{
            document.getElementById('new-diary-index').style.display = 'block'
        })
    }

    document.getElementById('sub-diary').addEventListener('click', () => {
        localStorage.clear()
    })
    
    document.querySelectorAll('.diary-list').forEach(diary => {
        if(localStorage.getItem('diary')){
            diary.id == localStorage.getItem('diary') ? diary.classList.add('active') : null
        }
    });
})


// FUNCTIONS
function get_diary(){
    fetch('/diaries')
    .then(response => response.json())
    .then(data => {
        if(data.status == 200){
            console.log(data);
        }
    });
}

function set_active(id){
    localStorage.setItem('diary', id)
}

function form_diary(mode){
    const form = document.querySelector('#new-diary-form')
    mode === 'show' ?  form.style.height = '33px' : form.style.height = '0'
}

function form_todo(mode){
    const form = document.querySelector('#new-todo-form')
    mode === 'show' ? form.style.height = '378px' : form.style.height = '0'
}

function update_todo(mode, id){
    const todo = document.getElementById(`todo-${id}`)
    if(mode === 'done'){
        fetch(`/todo-done/${id}`, {
            method: 'PUT',
            headers: {'content-type':'application/json', 'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
        })
        .then(response => response.json())
        .then(data => {
            const btn_done = document.getElementById(`add-done-${id}`)
            if(data.done == true){
                todo.classList.add('is_done')
                btn_done.title = 'Undo done'
                btn_done.innerHTML = '<b>&#8634;</b>'
            }else{
                todo.classList.remove('is_done')
                btn_done.title = 'Done'
                btn_done.innerHTML = '&#10004;'
            }        
        })
    }else if(mode === 'text'){
        title = todo.querySelector('.todo-title').textContent
        description = todo.querySelector('.todo-description').textContent
        btns_todo = document.getElementById(`btns-todo-${id}`)
        btns_todo.style.display = 'none'

        todo.querySelector('.todo-title').innerHTML = `<input type="text" name="title" value="${title}" required>`
        todo.querySelector('.todo-description').innerHTML = `<textarea rows="5" name="description" required>${description}</textarea><br>
                                                            <button class="save-edit">Save</button>&nbsp<span class="undo-edit pointer underline">Undo</span>`
        
        todo.querySelector('.save-edit').addEventListener('click', function(){
            fetch(`/edit-todo/${id}`, {
                method: 'PUT',
                headers: {'content-type':'application/json', 'X-CSRFToken': getCookie('csrftoken')},
                mode: 'same-origin',
                body: JSON.stringify({
                    title: todo.querySelector('input').value,
                    description: todo.querySelector('textarea').value
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.message){
                    todo.querySelector('.todo-title').innerHTML = todo.querySelector('input').value
                    todo.querySelector('.todo-description').innerHTML = todo.querySelector('textarea').value
                    btns_todo.style.display = 'block'
                }
            })
        })

        todo.querySelector('.undo-edit').addEventListener('click', function(){
            todo.querySelector('.todo-title').innerHTML = title
            todo.querySelector('.todo-description').innerHTML = description
            btns_todo.style.display = 'block'
        })
    }
}

function delete_todo(id){
    const todo = document.getElementById(`todo-${id}`).parentNode
    if(confirm('are you sure you want to delete this todo?') == true){
        fetch(`/delete-todo/${id}`, {
            method: 'DELETE',
            headers: {'content-type':'application/json', 'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
        })
        .then(response => response.json())
        .then(() => {
            todo.style.display = 'none'
        })
    }
}

function menu(mode){
    if(mode == 'open'){
        document.querySelector('aside').style.width = '250px'
        document.querySelector('aside').style.borderLeft = '1px solid lightgray'
    }else if(mode == 'close'){
        document.querySelector('aside').style.width = '0'
        document.querySelector('aside').style.borderLeft = '0'
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}