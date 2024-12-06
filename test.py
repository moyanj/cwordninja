import unittest
import cwordninja as wordninja


class TestWordNinja(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(list(wordninja.split("derekanderson")), ["derek", "anderson"])

    def test_with_underscores_etc(self):
        self.assertEqual(list(wordninja.split("derek anderson")), ["derek", "anderson"])
        self.assertEqual(list(wordninja.split("derek-anderson")), ["derek", "anderson"])
        self.assertEqual(list(wordninja.split("derek_anderson")), ["derek", "anderson"])
        self.assertEqual(list(wordninja.split("derek/anderson")), ["derek", "anderson"])

    def test_caps(self):
        self.assertEqual(list(wordninja.split("DEREKANDERSON")), ["DEREK", "ANDERSON"])

    def test_digits(self):
        self.assertEqual(list(wordninja.split("win32intel")), ["win", "32", "intel"])

    def test_apostrophes(self):
        self.assertEqual(
            list(wordninja.split("that'sthesheriff'sbadge")),
            ["that's", "the", "sheriff's", "badge"],
        )

    def test_custom_model(self):
        lm = wordninja.LanguageModel("test_lang.txt.gz")
        self.assertEqual(list(lm.split("derek")), ["der", "ek"])

    def test_custom_model_raw(self):
        lm = wordninja.LanguageModel("test_lang.txt")
        print(lm._wordcost)
        self.assertEqual(list(lm.split("derek")), ["der", "ek"])

    def test_lsplit(self):
        self.assertEqual(wordninja.lsplit("derekanderson"), ["derek", "anderson"])


if __name__ == "__main__":
    unittest.main()
