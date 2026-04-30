# hanzi.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Hanzi:
    char: str
    initial: str
    final: str
    pinyin: str  # Add this line!
    tone: int
    splits: List[str] = field(default_factory=list)

