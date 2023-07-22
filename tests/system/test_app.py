from unittest import TestCase
from unittest.mock import patch
from blog import Blog
import app
from post import Post


class AppTest(TestCase):

    def setUp(self):
        blog = Blog("Test", "Test Author")
        app.blogs = {"Test": blog}


    def test_menu_calls_create_blog(self):
        with patch("builtins.input") as mocked_input:
            with patch("app.ask_create_blog") as mocked_ask_create_blog:
                mocked_input.side_effect = ("c", "Test Create Blog", "Test Author", "q")

                app.menu()
                mocked_ask_create_blog.assert_called()


# Just Test - Whether the menu() call the Function print()
    def test_menu_prints_prompt(self):
        with patch("builtins.input", return_value="q") as mocked_input:
            app.menu()
            mocked_input.assert_called_with(app.MENU_PROMPT)


    def test_menu_calls_print_blogs(self):
# patch - Allows us To Extract the Value from Function DIRECTLY
# patch("app.print_blogs") - Receive a MODULE, That This Function is IN - "app" is a module, "print_blogs" is a Function
        with patch("app.print_blogs") as mocked_print_blogs:

# 2-nd "with" need in order to without this, will be an Error, because there waiting a TYPE something from User, in the input() function
# The input() is called, but nothing happens, but we assign the Result, what the User Type, IN a Vairable "q"
            with patch("builtins.input", return_value="q"):
                app.menu()
                mocked_print_blogs.assert_called()


    def test_print_blogs(self):
# patch("builtins.print") - Receive a MODULE, That This Function is IN - "builtins" is a module, "print" is a Built-in-Function
# "mocked_print" - Just a Name!
        with patch("builtins.print") as mocked_print:
# Call Function "print_blogs()" which iterate though items(blogs)
            app.print_blogs()
# Just Assert, whether the print() called with the CORRECT value - "Test by Test Author (0 posts)"
            mocked_print.assert_called_with('- Test by Test Author (0 posts)')


    def test_ask_create_blog(self):
        with patch("builtins.input", return_value="Test") as mocked_input:
# Call ask_create_blog() function
            app.ask_create_blog()
            mocked_input.side_effect = ("Test", "Test Author")

# Make sure that a blog was created
# Asserting, when we GET a key "Test", from app.blogs, that IS NOT going to be NONE
            self.assertIsNotNone(app.blogs.get("Test"))


    def test_ask_read_blog(self):

        with patch("builtins.input", return_value="Test"):
            with patch("app.print_posts") as mocked_print_posts:
                app.ask_read_blog()

                mocked_print_posts.assert_called_with(app.blogs["Test"])


    def test_print_posts(self):
        blog = app.blogs["Test"]
        blog.create_post("Test Post", "Test Content")

        with patch("app.print_post") as mocked_print_post:
            app.print_posts(blog)

            mocked_print_post.assert_called_with(blog.posts[0])


    def test_print_post(self):
        post = Post("Post title", "Post content")
        expected_print = '''
--- Post title ---

Post content

'''
        with patch("builtins.print") as mocked_print:
            app.print_post(post)
            mocked_print.assert_called_with(expected_print)


    def test_ask_create_post(self):
        blog = app.blogs['Test']
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Title', 'Test Content')

            app.ask_create_post()

            self.assertEqual(blog.posts[0].title, 'Test Title')
            self.assertEqual(blog.posts[0].content, 'Test Content')


