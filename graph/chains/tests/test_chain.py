from dotenv import load_dotenv
from graph.chains.classifier import classifier
from graph.chains.evaluator_of_classifier import evaluate_classifier
from graph.utils import encode_base64
from pathlib import Path
from pprint import pprint
load_dotenv()



# def test_classification_chain_label():
#     path = 'data/imgs/tabela5 - Copia.bmp'
#
#     image = encode_base64(path)
#     res = classifier.invoke({'image': image, 'file': path})
#     assert res


def test_evaluate_classifier():
    paths = [
        Path('data/imgs/tabela1.bmp'), Path('data/imgs/tabela2 - Copia.bmp'), Path('data/imgs/tabela5 - Copia (2).bmp'),
        Path('data/imgs/tabela4 - Copia (2).bmp')
    ]

    classifications = []
    print('---CLASSIFIER---')
    for path in paths:
        print('----IMAGE:', path, '----')
        image = encode_base64(path)
        if classifications:
            res = classifier.invoke({'image': image, 'file': path.stem, 'agent_scratchpad': classifications})
            classifications.append(res)
            pprint(res)
            continue
        res = classifier.invoke({'image': image, 'file': path.stem})
        classifications.append(res)
        pprint(res)

    print('---GRADER---')

    paths = [
        Path('data/imgs/tabela3.bmp'), Path('data/imgs/tabela2 - Copia.bmp'), Path('data/imgs/tabela5 - Copia (2).bmp'),
        Path('data/imgs/tabela4 - Copia (2).bmp')
    ]
    for path in paths:
        print('----IMAGE:', path, '----')
        image = encode_base64(path)
        res = evaluate_classifier.invoke(
            {'image': image, 'file': path.stem, 'agent_scratchpad': classifications}
        )

        pprint(res)
