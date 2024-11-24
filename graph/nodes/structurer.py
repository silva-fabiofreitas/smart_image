from pathlib import Path
from typing import Any, Dict

from ..chains.table_structurer import chain_structured
from ..state import GraphState
from ..utils import encode_base64


def table_parse(state: GraphState) -> Dict[str, list[Any] | list[Path]]:
    """
       Classify table images

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): descriptions tables
        """

    print("---PARSE TABLE---")

    image_path = state['image_path']

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError('Arquivo não encontrado')

    descriptions = []

    print("---IMAGE---", path.name)
    image = encode_base64(path)
    parse_table = chain_structured.invoke(
        {'image': image, 'file': path.stem}
    )
    descriptions.append(parse_table)
    return {'descriptions': descriptions}