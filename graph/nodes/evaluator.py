from pathlib import Path
from typing import Any, Dict

from ..chains.evaluator_of_classifier import evaluate_classifier
from ..state import GraphState
from ..utils import encode_base64


def evaluator_descriptions(state: GraphState) -> Dict[str, list[Any] | list[Path]]:
    """
       Classify table images

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): descriptions tables
        """

    print("---AVALIANDO DESCRIÇÃO---")

    image_path = state['image_path']
    descriptions = state['descriptions']

    path = Path(image_path)
    images = list(path.glob('*.*'))

    classifications = []
    for path in images:
        print("---IMAGE---", path.name)
        image = encode_base64(path)
        grade_table = evaluate_classifier.invoke(
            {'image': image, 'file': path.stem, 'agent_scratchpad': descriptions}
        )
        classifications.append(grade_table)

    return {'descriptions': classifications}
