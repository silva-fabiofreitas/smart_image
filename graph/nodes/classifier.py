from pathlib import Path
from typing import Any, Dict

from ..chains.classifier import classifier
from ..state import GraphState
from ..utils import encode_base64


def classifier_table(state: GraphState) -> Dict[str, list[Any] | list[Path]]:
    """
       Classify table images

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): image path and descriptions tables
        """

    print("---CLASSIFICAÇÃO INICIADA---")

    image_path = state['image_path']

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError('Arquivo não encontrado')
    images = list(path.glob('*.*'))

    classifications = []
    for path in images:
        print('----IMAGE:', path.name, '----')
        image = encode_base64(path)
        if classifications:
            res = classifier.invoke({'image': image, 'file': path.stem, 'agent_scratchpad': classifications})
            classifications.append(res)
            continue
        res = classifier.invoke({'image': image, 'file': path.stem})
        classifications.append(res)

    return {'image_path': image_path, 'descriptions': classifications}
