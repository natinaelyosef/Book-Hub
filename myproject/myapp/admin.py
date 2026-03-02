from django.contrib import admin
from .models import (
    Features,
    AdminAccount,
    AccountRestriction,
    UserProfile,
    IssueReport,
    SupportConversation,
    SupportMessage,
    ModerationActivityLog,
)
# Register your models here.

admin.site.register(Features)
admin.site.register(AdminAccount)
admin.site.register(AccountRestriction)
admin.site.register(UserProfile)
admin.site.register(IssueReport)
admin.site.register(SupportConversation)
admin.site.register(SupportMessage)
admin.site.register(ModerationActivityLog)
