import unittest
import pandas as pd
import numpy as np
from trading_strategy import calculate_bollinger_bands, generate_signals, calculate_returns

class TestTradingStrategy(unittest.TestCase):

    def setUp(self):
        self.df = pd.read_csv("/Users/tsrk04/Desktop/-_-/SSN/projects/Invsto/HINDALCO_1D.xlsx - HINDALCO.csv")
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        self.df.set_index('datetime', inplace=True)
        self.df.sort_index(inplace=True)

    def test_input_data_validation(self):
        self.assertIsInstance(self.df.index, pd.DatetimeIndex, "Index must be of type DatetimeIndex")

        for col in ['open', 'high', 'low', 'close']:
            self.assertTrue(pd.api.types.is_float_dtype(self.df[col]), f"{col} must be of type float")

        self.assertTrue(pd.api.types.is_integer_dtype(self.df['volume']), "volume must be of type int")

        self.assertTrue(pd.api.types.is_string_dtype(self.df['instrument']), "instrument must be of type string")

    def test_calculate_bollinger_bands(self):
        df_with_bands = calculate_bollinger_bands(self.df.copy(), window=20)
        print(df_with_bands[['close', 'Middle_Band', 'Upper_Band', 'Lower_Band']].head(25)) 
        
        self.assertIn('Middle_Band', df_with_bands.columns)
        self.assertIn('Upper_Band', df_with_bands.columns)
        self.assertIn('Lower_Band', df_with_bands.columns)
        
        self.assertIsNotNone(df_with_bands['Middle_Band'].iloc[20])
        self.assertIsNotNone(df_with_bands['Upper_Band'].iloc[20])
        self.assertIsNotNone(df_with_bands['Lower_Band'].iloc[20])

    def test_generate_signals(self):
        df_with_bands = calculate_bollinger_bands(self.df.copy(), window=20)
        df_with_signals = generate_signals(df_with_bands)
        
        print(df_with_signals[['close', 'Lower_Band', 'Upper_Band', 'Signal']].head(25))  # Debugging print

        self.assertIn('Signal', df_with_signals.columns)
        self.assertIn('Position', df_with_signals.columns)

        self.assertTrue((df_with_signals['Signal'] == 1).any())  # Check if there's at least one buy signal
        self.assertTrue((df_with_signals['Signal'] == -1).any())  # Check if there's at least one sell signal

    def test_calculate_returns(self):
        df_with_bands = calculate_bollinger_bands(self.df.copy(), window=20)
        df_with_signals = generate_signals(df_with_bands)
        df_with_returns = calculate_returns(df_with_signals)

        self.assertIn('Market_Returns', df_with_returns.columns)
        self.assertIn('Strategy_Returns', df_with_returns.columns)
        self.assertIn('Cumulative_Market_Returns', df_with_returns.columns)
        self.assertIn('Cumulative_Strategy_Returns', df_with_returns.columns)

        print("Final Cumulative Market Returns:", df_with_returns['Cumulative_Market_Returns'].iloc[-1])
        print("Final Cumulative Strategy Returns:", df_with_returns['Cumulative_Strategy_Returns'].iloc[-1])

        self.assertGreater(df_with_returns['Cumulative_Market_Returns'].iloc[-1], 0)
        self.assertGreater(df_with_returns['Cumulative_Strategy_Returns'].iloc[-1], 0)

if __name__ == '__main__':
    unittest.main()