

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe

from . import dao
from .models import Category, Course, Lesson, Tag, User, Comment
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseAppAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG KHÓA HỌC TRỰC TUYẾN'

    def get_urls(self):
        return [
                   path('course-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            'course_stats': dao.count_courses_by_cate(),
            'course_count': dao.count_courses(),

        })


my_admin_site = CourseAppAdminSite(name='myAdmin')


class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course'  # tên khoá ngoại (tuỳ chọn)


class TagInLineAdmin(admin.StackedInline):
    model = Course.tags.through


class CourseForm(forms.ModelForm):
    discription = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_filter = ['name']
    search_fields = ['name']


class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ['img']
    form = CourseForm
    inlines = [TagInLineAdmin]

    def img(self, course):
        if course:
            # return mark_safe(
            #     '<img src="/static/{url}" width="120" />'.format(url=course.image.name)
            # )
            # return mark_safe(f'<img width="200" src="/static/{course.image.name}"/>')
             return mark_safe(f'<img width="200" src="https://res.cloudinary.com/dmjcqxek3/image/upload/v1712582879/b6aqiiyypy3pk5dk4prv.png"/>')

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }

# Register your models here.
my_admin_site.register(Category, CategoryAdmin)
my_admin_site.register(Course, CourseAdmin)
my_admin_site.register(Lesson)
my_admin_site.register(User)
my_admin_site.register(Tag)
my_admin_site.register(Comment)