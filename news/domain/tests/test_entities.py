import unittest
from news.domain.entities import NewsModel, NewsConnectionModel


class TestNewsEntities(unittest.TestCase):
    def setUp(self):
        self.news_data = {
            "id": "test_id",
            "title": "Test Title",
            "author": "Test Author",
            "description": "Test Description",
            "content": "Test Content",
            "image": "test.jpg",
            "published_on": 1234567890,
            "link": "https://test.com"
        }
        
        self.connection_data = {
            "count": 1,
            "first": "first_id",
            "last": "last_id",
            "data": [self.news_data]
        }

    def test_news_model_creation(self):
        # Test creating a NewsModel from dictionary
        news = NewsModel.from_dict(self.news_data)
        self.assertEqual(news.id, self.news_data["id"])
        self.assertEqual(news.title, self.news_data["title"])
        self.assertEqual(news.author, self.news_data["author"])
        self.assertEqual(news.description, self.news_data["description"])
        self.assertEqual(news.content, self.news_data["content"])
        self.assertEqual(news.image, self.news_data["image"])
        self.assertEqual(news.published_on, self.news_data["published_on"])
        self.assertEqual(news.link, self.news_data["link"])

    def test_news_connection_model_creation(self):
        # Test creating a NewsConnectionModel from dictionary
        connection = NewsConnectionModel.from_dict(self.connection_data)
        self.assertEqual(connection.count, self.connection_data["count"])
        self.assertEqual(connection.first, self.connection_data["first"])
        self.assertEqual(connection.last, self.connection_data["last"])
        self.assertEqual(len(connection.data), 1)
        
        # Test the nested NewsModel
        news = connection.data[0]
        self.assertIsInstance(news, NewsModel)
        self.assertEqual(news.id, self.news_data["id"])
        self.assertEqual(news.title, self.news_data["title"])
        self.assertEqual(news.author, self.news_data["author"])
        self.assertEqual(news.description, self.news_data["description"])
        self.assertEqual(news.content, self.news_data["content"])
        self.assertEqual(news.image, self.news_data["image"])
        self.assertEqual(news.published_on, self.news_data["published_on"])
        self.assertEqual(news.link, self.news_data["link"])