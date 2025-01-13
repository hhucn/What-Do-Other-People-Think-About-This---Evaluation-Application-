class Comment:

    def __init__(self, comment_id: int, text: str):
        self.comment_id = comment_id
        self.text = text

    def get_id(self) -> int:
        return self.comment_id

    def get_text(self) -> str:
        return self.text
