from django.db import models

# Create your models here.


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    lesson_teacher_id = models.BigIntegerField(blank=True, null=True)
    publish_time = models.DateTimeField(blank=True, null=True)
    recommend = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)
    num_valuable = models.IntegerField(blank=True, null=True)
    num_happy = models.IntegerField(blank=True, null=True)
    num_bad = models.IntegerField(blank=True, null=True)
    num_score = models.IntegerField(blank=True, null=True)
    lesson_name = models.CharField(max_length=32, blank=True, null=True)
    teacher_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class User(models.Model):
    # 创建主键 创建username varchar
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    kind = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'user'


class LessonTeacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    teacher_name = models.CharField(max_length=32, blank=True, null=True)
    lesson_name = models.CharField(max_length=32, blank=True, null=True)
    school = models.CharField(max_length=32, blank=True, null=True)
    introduction = models.CharField(max_length=4096, blank=True, null=True)
    num_best = models.IntegerField(blank=True, null=True)
    num_good = models.IntegerField(blank=True, null=True)
    num_bad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lesson_teacher'


class ChoiceComments(models.Model):
    id = models.IntegerField(primary_key=True)
    lesson_teacher_id = models.IntegerField(blank=True, null=True)
    attitude = models.IntegerField(blank=True, null=True)
    content = models.IntegerField(blank=True, null=True)
    method = models.IntegerField(blank=True, null=True)
    achievement = models.IntegerField(blank=True, null=True)
    effect = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'choice_comments'