# admin/app.py

from fastapi import FastAPI
from sqladmin import Admin
from config.settings import engine
from admin.views import (
    UserAdmin, ConversationLogAdmin,
    ContentCategoryAdmin, EducationalContentAdmin,
    QuizQuestionAdmin, HelpDirectoryAdmin, PrivacyContentAdmin
)

def create_admin_app() -> FastAPI:
    app = FastAPI(title="Teman Aman Admin Panel")

    admin = Admin(app, engine)

    # Register semua view model
    admin.add_view(UserAdmin)
    admin.add_view(ConversationLogAdmin)
    admin.add_view(ContentCategoryAdmin)
    admin.add_view(EducationalContentAdmin)
    admin.add_view(QuizQuestionAdmin)
    admin.add_view(HelpDirectoryAdmin)
    admin.add_view(PrivacyContentAdmin)

    return app
