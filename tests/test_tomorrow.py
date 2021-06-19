from unittest import TestCase
from stocker.predict import tomorrow


class TestStocker(TestCase):
    def test_tomorrow_no_features(self):
        result = tomorrow('AAPL', features=[], steps=1,
                          training=0.7, period=14, years=0.2,
                          error_method='mse', plot=False)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)
        self.assertIsInstance(result[2], str)

    def test_tomorrow_all_features(self):
        result = tomorrow('AAPL', features=['Interest', 'Wiki_views', 'RSI', '%K', '%R'], steps=1,
                          training=0.7, period=14, years=0.2,
                          error_method='mse', plot=False)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)
        self.assertIsInstance(result[2], str)

    def test_tomorrow_multistep(self):
        result = tomorrow('AAPL', features=[], steps=5,
                          training=0.7, period=14, years=0.2,
                          error_method='mape', plot=False)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)
        self.assertIsInstance(result[2], str)
