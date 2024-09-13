from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class XmlNode:
    tag: str
    attributes: Dict[str, str]
    text: str


@dataclass
class XmlNodeDB:
    node: XmlNode
    children: List[XmlNodeDB]

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def get_link(self) -> Optional[str]:
        return self.node.attributes.get("href")
