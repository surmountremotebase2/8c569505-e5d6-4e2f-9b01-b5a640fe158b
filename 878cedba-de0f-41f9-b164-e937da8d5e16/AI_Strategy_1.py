from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # In this strategy, only one asset, the SPX index, is being considered.
        self.tickers = ["SPX"]

    @property
    def interval(self):
        # Using 1hour interval for MACD calculation.
        return "1hour"

    @property
    def assets(self):
        # The strategy works on the SPX index
        return self.tickers

    @property
    def data(self):
        # No additional data required outside of OHLCV for MACD calculation.
        return []

    def run(self, data):
        # Use MACD technical indicator to generate buy/sell signals
        macd_data = MACD("SPX", data["ohlcv"], 12, 26) # Standard fast=12, slow=26
        macd_line = macd_data["MACD"]
        signal_line = macd_data["signal"]
        
        # Initialize allocation to 0 as the starting point.
        call_allocation = 0
        put_allocation = 0
        
        # Entry strategy: MACD line crosses above signal line for CALL, below for PUT.
        if len(macd_line) > 1:
            if macd_line[-1] > signal_line[-1] and macd_line[-2] < signal_line[-2]:
                # Indicates momentum is turning positive, buy CALL
                log("Buying SPX 0 DTE CALL")
                call_allocation = 1 # Simplified to indicate a position, in practice this would be specific option identifiers
            elif macd_line[-1] < signal_line[-1] and macd_line[-2] > signal_line[-2]:
                # Indicates momentum is turning negative, buy PUT
                log("Buying SPX 0 DTE PUT")
                put_allocation = 1 # Simplified to indicate a position, in practice this would be specific option identifiers

        # This demonstrates a simplified position logic for educational purposes.
        # Actual trading would require managing option specifications like strike price and not just allocation.
        return TargetAllocation({"SPX_CALL_0DTE": call_allocation, "SPX_PUT_0DTE": put_allocation})