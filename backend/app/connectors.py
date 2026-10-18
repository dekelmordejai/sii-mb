"""Connector boundary: new trusted adapters implement load(), never user code."""
from typing import Protocol
from app.calculation import parse_csv


class Connector(Protocol):
    def load(self, content: str) -> tuple[list[dict], dict]: ...


class CSVConnector:
    def load(self, content: str):
        return parse_csv(content)


CONNECTORS: dict[str, Connector] = {"csv": CSVConnector()}
