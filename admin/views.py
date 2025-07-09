# admin/views.py

from sqladmin import ModelView
from database.models import (
    User, ConversationLog,
    ContentCategory, EducationalContent,
    QuizQuestion, HelpDirectory, PrivacyContent
)

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.telegram_id, User.total_interactions, User.created_at]

class ConversationLogAdmin(ModelView, model=ConversationLog):
    column_list = [ConversationLog.id, ConversationLog.user_id, ConversationLog.message_type, ConversationLog.timestamp]

class ContentCategoryAdmin(ModelView, model=ContentCategory):
    column_list = [ContentCategory.id, ContentCategory.name, ContentCategory.is_active]

class EducationalContentAdmin(ModelView, model=EducationalContent):
    column_list = [EducationalContent.id, EducationalContent.title, EducationalContent.category_id, EducationalContent.is_active]

class QuizQuestionAdmin(ModelView, model=QuizQuestion):
    column_list = [QuizQuestion.id, QuizQuestion.question, QuizQuestion.difficulty_level, QuizQuestion.is_active]

class HelpDirectoryAdmin(ModelView, model=HelpDirectory):
    column_list = [HelpDirectory.id, HelpDirectory.name, HelpDirectory.category, HelpDirectory.is_active]

class PrivacyContentAdmin(ModelView, model=PrivacyContent):
    column_list = [PrivacyContent.id, PrivacyContent.title, PrivacyContent.is_active]
