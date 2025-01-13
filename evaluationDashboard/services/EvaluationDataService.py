from evaluation.models import PointOfViewSetAnswer, Question, CommentSelection, Comment, Participant
from evaluation.models.AnswerRepository import CommentAnswer


class EvaluationDataService:

    @staticmethod
    def get_question_data():
        questions_data = []

        for question in Question.objects.all():
            questions_data.append({
                "question_id": question.id,
                "user_comment": question.user_comment,
                "article_title": question.article_title,
                "keywords": question.article_keywords,
                "news_agency": question.news_agency
            })
        return questions_data

    @staticmethod
    def get_comment_selections():
        comment_selections = []

        selections = CommentSelection.objects.all()
        for selection in selections:
            comment_selections.append({
                "question_id": selection.question_id,
                "recommendation_method": selection.recommendation_method
            })

        return comment_selections

    @staticmethod
    def get_comments():
        comments = []

        for comment in Comment.objects.all():
            comments.append({
                "comment_selection": comment.comment_selection.id,
                "comment_id": comment.id,
                "text": comment.text
            })

        return comments

    @staticmethod
    def get_comment_answers():
        comment_answers = []
        answers = CommentAnswer.objects.all()

        for answer in answers:
            comment_answers.append({
                "answer_id": answer.id,
                "participant_id": answer.participant_id,
                "question_id": answer.question.id,
                "news_agency": answer.question.news_agency,
                "keywords": answer.question.article_keywords,
                "comment_selection_id": answer.comment_selection.id,
                "comment_text": answer.comment.text,
                "recommendation_method": answer.comment_selection.recommendation_method,
                "comment_id": answer.comment.id,
                "good_recommendation": answer.good_recommendation
            })

        return comment_answers

    @staticmethod
    def get_point_of_view_answer_data():
        evaluation_data = []
        answers = PointOfViewSetAnswer.objects.all()

        for answer in answers:
            question = Question.objects.get(id=answer.question_id)
            evaluation_data.append(
                {"question_id": answer.question.id,
                 "user_comment": question.user_comment,
                 "keywords": answer.question.article_keywords,
                 "news_agency": answer.question.news_agency,
                 "recommendation_method": answer.recommendation_method,
                 "selected_recommendation_method": answer.selected_method,
                 "participant_id": answer.participant_id}
            )

        return evaluation_data

    @staticmethod
    def get_participant_data():
        participants_data = []

        for participant in Participant.objects.all():
            participants_data.append({
                "participant_id": participant.id,
                "gender": participant.gender,
                "age": participant.age,
                "education": participant.education
            })

        return participants_data
