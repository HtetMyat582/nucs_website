from django.contrib import admin
from .models import User, Student, Faculty

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_editable = ('role',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'program')
    list_filter = ('program', )
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    
    @admin.display(description='First Name')
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(description='Last Name')
    def last_name(self, obj):
        return obj.user.last_name

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'department', 'designation')
    list_filter = ('department', 'designation')
    search_fields = ('user__username', 'user__email')

    @admin.display(description='First Name')
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(description='Last Name')
    def last_name(self, obj):
        return obj.user.last_name