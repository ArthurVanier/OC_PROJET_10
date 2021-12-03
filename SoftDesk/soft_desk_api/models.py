from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    p_type = models.CharField(max_length=32)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Contributor(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_id = models.IntegerField()
    role = models.CharField(max_length=64)
    permission = models.CharField(max_length=32)


CHOICE_PRIORITY = [
    ('LOW', 'L'),
    ('MEDIUM', 'M'),
    ('HIGH', 'H')
]


CHOICE_TAG = [
    ('BUG', 'B'),
    ('IMPROVE', 'I'),
    ('TASK', 'T'),
]


CHOICE_STATUS = [
    ('TODO', 'T'),
    ('IN_PROGESS', 'P'),
    ('DONE', 'D'),
]


class Issue(models.Model):
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2048)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="author")
    attributed = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="attributed")
    created_time = models.DateTimeField()

    priority = models.CharField(max_length=16, choices=CHOICE_PRIORITY)
    tag = models.CharField(max_length=16, choices=CHOICE_TAG)
    status = models.CharField(max_length=16, choices=CHOICE_STATUS)


class Comment(models.Model):
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.CharField(max_length=2048)
    created_time = models.DateTimeField()
