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

system = (
    "Analyze the provided image of a table, focusing exclusively on its structure and design. "
    "Avoid considering its title or specific values. Provide a detailed description based on the following aspects:\n\n"
    "1. **Headers:** Identify and list all column headers. Describe their layout, structure, and any distinctive formatting features (e.g., bold text, color, font style).\n"
    "2. **Column Count and Purpose:** Specify the total number of columns. For each column, describe its structural role or general categorization (e.g., primary data column, summary column, etc.).\n"
    "3. **Data Types:** Analyze the type of content expected in each column based on its design, such as text, numerical values, dates, or categories.\n"
    "4. **Visual Design:** Describe the table's overall visual characteristics, including alignment (e.g., left, center, or right), presence and style of borders, row or column highlights, color schemes, shading, gridlines, or other decorative elements.\n"
    "5. **Unique Features:** Note any distinctive elements such as merged cells, hierarchical headers, or icons.\n\n"
    "If the structure or design of this table deviates significantly from previously analyzed tables, assign a new label and description.\n\n"
    "Input File: {file}"
)

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


