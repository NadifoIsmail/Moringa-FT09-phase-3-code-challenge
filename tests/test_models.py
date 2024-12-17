import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

author1 = Author(2, "Jane Doe")
mag1 = Magazine(2, "Sports Week", "sports")
class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author._name, "John Doe")

    def test_article_creation(self):
        article = Article("Test Title", author1, mag1)
        self.assertEqual(article._title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "technology")
        self.assertEqual(magazine._name, "Tech Weekly")

if __name__ == "__main__":
    unittest.main()
