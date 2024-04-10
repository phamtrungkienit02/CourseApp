from rest_framework import serializers

from .models import Category, Course, Tag, Lesson, User, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BaseSerializer(serializers.ModelSerializer):
    #image = serializers.SerializerMethodField(source="image")
    tags = TagSerializer(many=True)

    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url

        return req
    # def get_image(self, course):
    #     if course.image:
    #         request = self.context.get('request')

            # if request:
            #     return request.build_absolute_uri('/static/%s' % course.image.name)
            # return '/static/%s' % course.image.name


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_add', 'category']
        # fields = '__all__'


class LessonSerializer(BaseSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'created_add']


class LessonDetailSerializer(LessonSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_add', 'user']

class AuthenticatedLessonDetailsSerializer(LessonDetailSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        return lesson.like_set.filter(active=True).exists()

    class Meta:
        model = LessonDetailSerializer.Meta.model
        fields = LessonDetailSerializer.Meta.fields + ['liked']