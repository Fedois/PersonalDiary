# Diaries App - README

## Distinctiveness and Complexity

This application stands out in its distinctiveness and complexity through its unique features. The distinctiveness is evident in the ability for users to create personalized diaries and add tasks (todos) to each one. This goes beyond a simple task list and introduces a hierarchical organization for better task management. The complexity is highlighted in the handling of relationships between models, the option to mark tasks as important or completed, and the implementation of a mobile-responsive design for enhanced user experience.

The decision to create this app with diary functionality adds a layer of complexity, providing users with a versatile tool for organizing tasks based on specific contexts or themes. The inclusion of features like marking tasks as important or completed enhances the user experience and demonstrates the project's commitment to functionality beyond basic requirements.

## File Contents

- **`diaries/`**
  - **`models.py`** - Defines the data models for User, Diary, and Todo, establishing relationships between them.
  - **`views.py`** - Manages the views for creating, displaying, and managing diaries and tasks.
  - **`urls.py`** - Configures the URL patterns for different views.
  - **`admin.py`** - Configures the Django admin interface for managing models (User, Diary, Todo).
  - **`apps.py`** - Defines configuration for the 'diaries' app, including the name.
  - **`tests.py`** - Contains test cases for the models (User, Diary, Todo).
  - **`templates/`** - Holds HTML templates for rendering the application's pages (layout, index, show, login, register, ).
  - **`static/`** - Contains logo and static files such as CSS/JavaScript for styling, media-query and client-side functionality.

## Running the Application

To run the TodoList application, follow these steps:

1. Clone the repository: `git clone https://github.com/me50/Fedois.git`
2. Change branch: `git checkout web50/projects/2020/x/capstone`
3. Apply database migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`


## Additional Information

- When the user create a diary or todo, the application utilizes Django's `messages` module to provide user feedback.
- The user interface has been designed with a focus on intuitive navigation.
- Testing has been performed on various devices to ensure a responsive user experience.