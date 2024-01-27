from django.urls import path

from . import views

urlpatterns = [
    # AUTH USER
    path("login", views.login_user, name="login"),
    path("register", views.register_user, name="register"),
    path('logout', views.logout_user, name="logout"),

    # PROJECT VIEWS
    path("", views.index, name="index"),
    path("diary/<int:id>", views.show, name="show"),
    path("create-diary", views.create_diary, name="create"),
    path("diary/<int:id>/create-todo", views.create_todo, name="create-todo"),
    path("diary/<int:id>/next-page", views.next_page, name="next"),
    path("diary/<int:id>/back-page", views.back_page, name="back"),

    # API
    path("todo-done/<int:id>", views.todo_done, name="todo_done"),
    path("edit-todo/<int:id>", views.edit_todo, name="edit"),
    path("delete-todo/<int:id>", views.delete_todo, name="delete")
]