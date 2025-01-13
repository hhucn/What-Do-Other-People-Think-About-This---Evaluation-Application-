import unittest

from evaluation.models.utils.clean_text import remove_html_tags


class TestUtilsCleanText(unittest.TestCase):
    def test_remove_html_tags(self):
        text = "This is <br> a test text </br>"
        expected_text = "This is a test text "

        cleaned_text = remove_html_tags(text)
        self.assertEqual(cleaned_text, expected_text)

    def test_remove_html_tags_no_html_tags_in_text(self):
        text = "This is a test text"
        expected_text = "This is a test text"

        cleaned_text = remove_html_tags(text)
        self.assertEqual(cleaned_text, expected_text)


if __name__ == '__main__':
    unittest.main()
