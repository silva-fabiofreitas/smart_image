from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field, BaseModel
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)


class GradeTable(BaseModel):
    file: str = Field(description="File name")
    label: str = Field(description="Category or label assigned to the table")
    description: str = Field(description="Table description")
    new_classified: bool = Field(description="Updated with a new classification, 'yes' or 'no'")


structured_llm_evaluator = llm.with_structured_output(GradeTable)

system = (
    "You are an evaluator responsible for verifying if an image aligns with its historical descriptions and classifications. "
    "Ignore the table's name and focus solely on its structural and content characteristics. Follow these steps:\n\n"
    "1. **Analysis**: Carefully compare the current image against the historical descriptions and classifications provided.\n"
    " * Focus on the following elements:"
    "   - 1. **Headers:** Identify and list all column headers. Describe their layout, structure, and any distinctive formatting features (e.g., bold text, color, font style).\n"
    "   - 2. **Column Count and Purpose:** Specify the total number of columns. For each column, describe its structural role or general categorization (e.g., primary data column, summary column, etc.).\n"
    "   - 3. **Data Types:** Analyze the type of content expected in each column based on its design, such as text, numerical values, dates, or categories.\n"
    "   - 4. **Visual Design:** Describe the table's overall visual characteristics, including alignment (e.g., left, center, or right), presence and style of borders, row or column highlights, color schemes, shading, gridlines, or other decorative elements.\n"
    "   - 5. **Unique Features:** Note any distinctive elements such as merged cells, hierarchical headers, or icons.\n\n"
    "If this table’s structure or design significantly deviates from previously analyzed tables, label it as a “new description.”\n\n"
    "2. **Decision**:\n"
    "   - If the image matches the historical data, retain the existing description, category, and label.\n"
    "   - If the image does not match, reclassify it. Provide a new, detailed description, assign a new category, "
    "and create a unique label that accurately captures all the table's characteristics.\n"
    "3. **Output**:\n"
    "   - Indicate whether the description or label has been updated with a new classification with 'yes' or 'no'.\n"
    "   - If new classification ('yes'), include the updated description, category, and label.\n\n"
    "Ensure your classifications and labels are consistent and precise."
    "file: {file}."
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
        ('system', "previous descriptions:{agent_scratchpad}")
    ]
)

evaluate_classifier = prompt | structured_llm_evaluator
