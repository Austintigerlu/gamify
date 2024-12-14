from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.core.exceptions import ValidationError

class User(AbstractUser):
    # AbstractUser already includes username, first_name, last_name, email, password
    pass

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    users = models.ManyToManyField(User, through='UserCourse')

    def calculate_completion(self, user):
        user_course = self.usercourse_set.filter(user=user).first()
        if user_course:
            completed_modules = self.modules.filter(completion=100).count()
            total_modules = self.modules.count()
            completion = (completed_modules / total_modules * 100) if total_modules > 0 else 0
            user_course.completion = completion
            user_course.save()
        return user_course.completion if user_course else 0

    def __str__(self):
        return self.name

class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField(null=True, blank=True)
    completion = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of course completion"
    )

    class Meta:
        unique_together = ('user', 'course')

class Module(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    completion = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of module completion"
    )

    def calculate_completion(self, user):
        total_content = self.contents.count()
        if total_content == 0:
            return 0
        
        completed_slides = self.contents.filter(slides__completion=True, type_of_content='SLIDE').count()
        completed_videos = self.contents.filter(videos__completion=True, type_of_content='VIDEO').count()
        completed_quizzes = self.contents.filter(quizzes__completion=True, type_of_content='QUIZ').count()
        
        total_completed = completed_slides + completed_videos + completed_quizzes
        completion = (total_completed / total_content) * 100
        
        self.completion = completion
        self.save()
        
        # Update course completion
        self.course.calculate_completion(user)
        return completion

    def __str__(self):
        return self.name

class Content(models.Model):
    CONTENT_TYPES = [
        ('SLIDE', 'Slide'),
        ('VIDEO', 'Video'),
        ('QUIZ', 'Quiz'),
    ]
    
    type_of_content = models.CharField(max_length=10, choices=CONTENT_TYPES)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='contents')
    abstract = models.TextField()

    def __str__(self):
        return f"{self.type_of_content} - {self.module.name}"

class Slide(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='slides')
    completion = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='videos')
    completion = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')

    def clean(self):
        if not self.slide and not self.video:
            raise ValidationError('Comment must be associated with either a slide or video')
        if self.slide and self.video:
            raise ValidationError('Comment cannot be associated with both slide and video')

    def __str__(self):
        return f"Comment by {self.user.username}"

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='quizzes')
    completion = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    question = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer

class Leaderboard(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    score = models.FloatField()
    username = models.CharField(max_length=150)  # Storing username for quick access

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"{self.username} - Rank {self.rank}"