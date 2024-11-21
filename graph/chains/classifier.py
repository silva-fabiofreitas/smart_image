from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field, BaseModel
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)


class TableDescription(BaseModel):
    file: str = Field(description="File name")
    label: str = Field(description="Category or label assigned to the table")
    description: str = Field(description="Table description")


structured_llm_description = llm.with_structured_output(TableDescription)

system = prompt_text = """
Analyze the provided image of a table and describe its structure with attention to detail. Focus on the following elements:

1. **Headers**: List all the headers present and describe their roles or relevance.  
2. **Number of Columns**: Count the columns and specify their purpose.  
3. **Types of Information**: Describe the type of data in each column (e.g., text, numbers, dates, categories).  
4. **General Format**: Describe detail appearance of the table, including alignment, borders, colors, or any visual styles that stand out.

"Based on this detailed description, create a unique label for the table that accurately reflects all its characteristics. If the table's description differs from the previous descriptions, assign a new label.

file: {file}
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "user",
            [
                {"type": "image_url", "image_url": {"url": "data:image/bmp;base64,{image}"}}
            ]
        ),
        ('ai', "previous descriptions:{agent_scratchpad}")
    ]
).partial(agent_scratchpad='')

classifier = prompt | structured_llm_description

if __name__ == '__main__':
    import pprint
    from graph.utils import encode_base64
    from pathlib import Path
    paths = [
        Path('data/imgs/tabela1.bmp'), Path('data/imgs/tabela2.bmp'),
        Path('data/imgs/tabela5 - Copia.bmp')]

    classifications = []
    for path in paths:
        print('----IMAGE:', path, '----')
        image = encode_base64(path)
        if classifications:
            res = classifier.invoke({'image': image, 'file': path.stem, 'agent_scratchpad': ', '.join(classifications)})
            classifications.append(res.json())
            continue
        res = classifier.invoke({'image': image, 'file': path.stem})
        classifications.append(res.json())
    pprint.pprint(classifications)


