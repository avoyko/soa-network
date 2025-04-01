import unittest
from unittest.mock import MagicMock, patch
from app.service import PostsService
from app.models import Post, Tag
from app.exceptions import NotFoundError, PermissionDeniedError, ValidationError
from datetime import datetime

class TestPostsService(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.service = PostsService(self.db)
        
    def test_create_post_success(self):
        # Arrange
        mock_post = Post(
            id="123", 
            title="Test Post", 
            description="Test Description",
            creator_id="user1", 
            is_private=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        
        with patch.object(self.service, '_get_or_create_tags', return_value=[Tag(name="test")]):
            # Act
            self.db.add.side_effect = lambda post: setattr(post, 'id', mock_post.id)
            post = self.service.create_post(
                title="Test Post",
                description="Test Description",
                creator_id="user1",
                is_private=False,
                tags=["test"]
            )
            
            # Assert
            self.assertEqual(post.id, "123")
            self.assertEqual(post.title, "Test Post")
            self.assertEqual(post.description, "Test Description")
            self.assertEqual(post.creator_id, "user1")
            self.assertEqual(post.is_private, False)
            self.db.add.assert_called_once()
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once()
    
    def test_create_post_validation_error(self):
        # Act & Assert
        with self.assertRaises(ValidationError):
            self.service.create_post(
                title="",
                description="Test Description",
                creator_id="user1",
                is_private=False,
                tags=["test"]
            )
    
    def test_get_post_success(self):
        # Arrange
        mock_post = Post(
            id="123", 
            title="Test Post", 
            description="Test Description",
            creator_id="user1", 
            is_private=False
        )
        mock_query = MagicMock()
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_post
        
        # Act
        post = self.service.get_post(post_id="123", requester_id="user1")
        
        # Assert
        self.assertEqual(post.id, "123")
        self.assertEqual(post.title, "Test Post")
    
    def test_get_post_not_found(self):
        # Arrange
        mock_query = MagicMock()
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        # Act & Assert
        with self.assertRaises(NotFoundError):
            self.service.get_post(post_id="123", requester_id="user1")
    
    def test_get_private_post_denied(self):
        # Arrange
        mock_post = Post(
            id="123", 
            title="Test Post", 
            description="Test Description",
            creator_id="user1", 
            is_private=True
        )
        mock_query = MagicMock()
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_post
        
        # Act & Assert
        with self.assertRaises(PermissionDeniedError):
            self.service.get_post(post_id="123", requester_id="user2")
    
    def test_update_post_success(self):
        # Arrange
        mock_post = Post(
            id="123", 
            title="Test Post", 
            description="Test Description",
            creator_id="user1", 
            is_private=False
        )
        mock_query = MagicMock()
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_post
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        
        # Act
        post = self.service.update_post(
            post_id="123",
            updater_id="user1",
            title="Updated Title"
        )
        
        # Assert
        self.assertEqual(post.title, "Updated Title")
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
    
    def test_update_post_not_owner(self):
        # Arrange
        mock_post = Post(
            id="123", 
            title="Test Post", 
            description="Test Description",
            creator_id="user1", 
            is_private=False
        )
        mock_query = MagicMock()
        self.db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_post
        
        # Act & Assert
        with self.assertRaises(PermissionDeniedError):
            self.service.update_post(
                post_id="123",
                updater_id="user2",
                title="Updated Title"
            )

if __name__ == '__main__':
    unittest.main()
