from typing import TypedDict, List, Any


class GraphState(TypedDict):
    structure: bool
    image_path: str
    descriptions: List[Any]
