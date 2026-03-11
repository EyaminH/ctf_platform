from django.contrib import admin
from .models import Category, Challenge, Submission

@admin.action(description='Mark selected challenges as approved')
def approve_challenges(modeladmin, request, queryset):
    queryset.update(is_approved=True)

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'points', 'status', 'is_approved', 'created_at')
    list_filter = ('status', 'is_approved', 'category')
    search_fields = ('title', 'author__username')
    actions = [approve_challenges]

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'is_correct', 'submitted_at')
    list_filter = ('is_correct',)
    search_fields = ('user__username', 'challenge__title')

admin.site.register(Category)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Submission, SubmissionAdmin)
