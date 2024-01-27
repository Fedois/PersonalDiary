from django.test import TestCase
from .models import User, Diary, Todo

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.diary = Diary.objects.create(name="Test Diary", user=self.user)
        self.todo = Todo.objects.create(
            diary=self.diary,
            title="Test Todo",
            description="This is a test todo",
            is_important=True,
            done=False,
            date="2024-01-20",
        )
    
    def test_user_model(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_diary_model(self):
        self.assertEqual(str(self.diary), "Test Diary")

    def text_diary_title_max_lenght(self):
        max_lenght = Diary._meta.get_field('title').max_length
        self.assertLessEqual(len(self.diary.title), max_lenght)

    def test_todo_model(self):
        self.assertEqual(str(self.todo), "todo: Test Todo, diary: Test Diary")

    def test_todo_title_max_lenght(self): 
        max_lenght = Todo._meta.get_field('title').max_length
        self.assertLessEqual(len(self.todo.title), max_lenght)

    def test_todo_default_values(self):
        self.assertFalse(self.todo.done)
        self.assertTrue(self.todo.is_important)

    def test_diary_user_relationship(self):
        self.assertEqual(self.diary.user, self.user)
        self.assertEqual(self.user.diaries.first(), self.diary)

    def test_todo_diary_relationship(self):
        self.assertEqual(self.todo.diary, self.diary)
        self.assertEqual(self.diary.todos.first(), self.todo)

