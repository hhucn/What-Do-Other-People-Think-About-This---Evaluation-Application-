from typing import List

from evaluation.domain.Comment import Comment


class PointOfViewQuestion:
    def __init__(self, question_id: int, user_comment: str, article_keywords: List[str], article_title: str, comment_selections: tuple[List[Comment], List[Comment]],
                 news_agency: str, recommendation_method: str):
        self.question_id = question_id
        self.comment_selections = comment_selections
        self.article_keywords = article_keywords
        self.user_comment = user_comment
        self.article_title = article_title
        self.news_agency = news_agency
        self.recommendation_method = recommendation_method

    def get_id(self) -> int:
        return self.question_id

    def get_comment_selections(self) -> tuple[List[Comment], List[Comment]]:
        return self.comment_selections

    def get_article_title(self) -> str:
        return self.article_title

    def get_article_keywords(self) -> str:
        return self.article_keywords

    def get_user_comment(self) -> str:
        return self.user_comment

    def get_news_agency(self) -> str:
        return self.news_agency

    def get_model_method(self) -> str:
        return self.recommendation_method
