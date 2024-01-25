"""Data transformations."""

from datetime import datetime

from aineko import AbstractNode


class Transform(AbstractNode):
    """Base class for message transformations."""

    def _pre_loop_hook(self, params: dict | None = None) -> None:
        """Initalize."""
        self.input_dataset = list(self.consumers.keys())[0]
        out = list(self.producers.keys())
        out.remove("logging")
        self.output_dataset = out[0]

    def _execute(self, params: dict | None = None) -> None:
        """Fetches messages from input dataset and transforms it."""
        message = self.consumers[self.input_dataset].next()
        transformed_message = self.transform(message)
        self.producers[self.output_dataset].produce(transformed_message)

    @staticmethod
    def convert_to_unix_timestamp(time_str: str, time_format: str) -> float:
        """
        Convert a time string in the format time_format to a UNIX timestamp.
        """
        # Convert the time string to a datetime object in UTC
        date_object = datetime.strptime(time_str, time_format)

        # Calculate the UNIX timestamp (number of seconds since the epoch)
        unix_timestamp = (date_object - datetime(1970, 1, 1)).total_seconds()

        return unix_timestamp

class CoinbaseL1Transform(Transform):
    """Transforms Coinbase L1 messages."""
    venue = "coinbase"
    asset_map = {
        "BTC-USD": "BTCUSD",
    }

    def transform(self, message: dict) -> dict:
        """Transforms Coinbase L1 messages.
        
        Example input message:
            {
                "type": "ticker",
                "sequence": 71278752848,
                "product_id": "BTC-USD",
                "price": "46963.47",
                "open_24h": "46144.91",
                "volume_24h": "44129.64251546",
                "low_24h": "45129.54",
                "high_24h": "49102.29",
                "volume_30d": "458294.87775013",
                "best_bid": "46958.88",
                "best_bid_size": "0.01464408",
                "best_ask": "46963.47",
                "best_ask_size": "0.00496500",
                "side": "buy",
                "time": "2024-01-11T20:27:07.723005Z",
                "trade_id": 594336544,
                "last_size": "0.00039092"
            }
        
        Example output message:
            {
                "timestamp": "1705004827.723005",
                "exchange": "coinbase",
                "symbol": "BTC-USD",
                "best_bid": "46958.88",
                "best_bid_size": "0.01464408",
                "best_ask": "46963.47",
                "best_ask_size": "0.00496500",
            }

        """
        update = {
            "timestamp": self.convert_to_unix_timestamp(
                    time_str=message["timestamp"],
                    time_format="%Y-%m-%d %H:%M:%S.%f"
                    ),
            "exchange": self.venue,
            "symbol": self.asset_map[message["message"]["product_id"]],
            "best_bid": float(message["message"]["best_bid"]),
            "best_bid_size": float(message["message"]["best_bid_size"]),
            "best_ask": float(message["message"]["best_ask"]),
            "best_ask_size": float(message["message"]["best_ask_size"]),
        }
        return update

class BinanceUSL1Transform(Transform):
    """Transforms Binance L1 messages."""
    venue = "binanceus"
    asset_map = {
        "BTCUSDT": "BTCUSD",
    }

    def transform(self, message: dict) -> dict:
        """Transforms BinanceUS L1 messages.
        
        Example input message:
            {
                "u": 2235521784,
                "s": "BTCUSDT",
                "b": "46901.96000000",
                "B": "0.01439000",
                "a": "46931.02000000",
                "A": "0.00087000"
            }
        
        Example output message:
            {
                "timestamp": "1705004827.723005",
                "exchange": "binance",
                "symbol": "BTCUSD",
                "best_bid": "46958.88",
                "best_bid_size": "0.01464408",
                "best_ask": "46963.47",
                "best_ask_size": "0.00496500",
            }

        """
        update = {
            "timestamp": self.convert_to_unix_timestamp(
                time_str=message["timestamp"],
                time_format="%Y-%m-%d %H:%M:%S.%f"
                ),
            "exchange": self.venue,
            "symbol": self.asset_map[message["message"]["s"]],
            "best_bid": float(message["message"]["b"]),
            "best_bid_size": float(message["message"]["B"]),
            "best_ask": float(message["message"]["a"]),
            "best_ask_size": float(message["message"]["A"]),
        }
        return update