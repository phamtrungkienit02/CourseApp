from django.db.models import Count
from courses.models import Course, Category


def load_courses(params={}):
    q = Course.objects.filter(active=True)

    kw = params.get('kw')
    if kw:
        q = q.fillter(subject__icontains=kw)

    cate_id = params.get('cate_id')
    if cate_id:
        q = q.fillter(category_id=cate_id)

    return q


def count_courses_by_cate():
    return Category.objects.annotate(counter=Count('course__id')).values('id', 'name', 'counter')\
                .order_by('-counter')


def count_courses():
    return Course.objects.filter(active=True).count()