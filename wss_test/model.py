"""Data transformations."""

import time

from aineko import AbstractNode


class TopOfBook(AbstractNode):
    """Run a model."""

    def _pre_loop_hook(self, params: dict | None = None) -> None:
        """Initialize."""
        self.model_state = {}

    def _execute(self, params: dict | None = None) -> None:
        """Fetches messages from input dataset and transforms it."""
        message = self.consumers["l1_updates"].next()
        self.update_model(message)
        result = self.predict()
        self.producers["top_of_book"].produce(result)

    def update_model(self, message: dict) -> None:
        """Update model state."""
        self.model_state.update(
            {
                message["message"]["exchange"]: {
                    "best_bid": message["message"]["best_bid"],
                    "best_ask": message["message"]["best_ask"],
                    "best_bid_size": message["message"]["best_bid_size"],
                    "best_ask_size": message["message"]["best_ask_size"],
                    "timestamp": message["message"]["timestamp"],
                }
                }
        )

    def predict(self) -> dict:
        """Predict.
        
        For each exchange aggregate the best bid and best ask and return the best bid and best ask.
        """
        exchanges = self.model_state.keys()
        best_bid = 0
        best_ask = 1e16
        for exchange in exchanges:
            if self.model_state[exchange]["best_bid"] > best_bid:
                best_bid =self.model_state[exchange]["best_bid"]
            if self.model_state[exchange]["best_ask"] < best_ask:
                best_ask =self.model_state[exchange]["best_ask"]
        return {"best_bid": best_bid, "best_ask": best_ask, "timestamp": time.time()}