"""Shannon entropy helper — high entropy sections/files are a strong packing
/encryption signal used throughout Section 18 and the risk engine."""
import math
from collections import Counter


def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())
