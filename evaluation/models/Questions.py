from django.db import models


class Question(models.Model):
    user_comment = models.CharField(max_length=6000)
    article_keywords = models.CharField(max_length=1000)
    article_title = models.CharField(max_length=10000)
    news_agency = models.CharField(max_length=1000)

    def __str__(self):
        return self.user_comment
