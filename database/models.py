# database/models.py

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Enum, ForeignKey, BigInteger,
    DateTime, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.settings import Base
import enum

# ENUM Definitions
class MessageType(enum.Enum):
    panic_button = "panic_button"
    crisis_detection = "crisis_detection"

class QuestionType(enum.Enum):
    multiple_choice = "multiple_choice"
    true_false = "true_false"

class DifficultyLevel(enum.Enum):
    very_easy = "very_easy"
    easy = "easy"
    medium = "medium"
    hard = "hard"
    very_hard = "very_hard"

# ===========================
# Table: Users
# ===========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_interaction = Column(DateTime, server_default=func.now())
    last_activity = Column(DateTime, server_default=func.now(), onupdate=func.now())
    total_interactions = Column(Integer, default=0)
    preferred_language = Column(String(5), default="id")
    created_at = Column(DateTime, server_default=func.now())

    conversation_logs = relationship("ConversationLog", back_populates="user", cascade="all, delete-orphan")


# ===========================
# Table: Conversation Logs
# ===========================
class ConversationLog(Base):
    __tablename__ = "conversation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    is_resolved = Column(Boolean, default=False)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text)

    user = relationship("User", back_populates="conversation_logs")



# ===========================
# Table: Content Categories
# ===========================
class ContentCategory(Base):
    __tablename__ = "content_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    color = Column(String(7), default="#007bff")
    icon = Column(String(50))
    is_active = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    educational_contents = relationship("EducationalContent", back_populates="category")


# ===========================
# Table: Educational Content
# ===========================
class EducationalContent(Base):
    __tablename__ = "educational_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("content_categories.id", ondelete="CASCADE"), nullable=False)
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    media_url = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship("ContentCategory", back_populates="educational_contents")


# ===========================
# Table: Quiz Questions
# ===========================
class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    options = Column(JSON)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text)
    difficulty_level = Column(Enum(DifficultyLevel), default=DifficultyLevel.medium)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


# ===========================
# Table: Help Directory
# ===========================
class HelpDirectory(Base):
    __tablename__ = "help_directory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    phone = Column(String(50))
    whatsapp = Column(String(50))
    website = Column(String(255))
    description = Column(Text)
    is_emergency = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


# ===========================
# Table: Privacy Content
# ===========================
class PrivacyContent(Base):
    __tablename__ = "privacy_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
