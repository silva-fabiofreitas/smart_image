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
    reclassified: bool = Field(description="the table is reclassified")


structured_llm_evaluator = llm.with_structured_output(GradeTable)

system = (
    "You are an evaluator responsible for verifying if an image aligns with its historical descriptions and classifications. "
    "Ignore the table's name and focus solely on its structural and content characteristics. Follow these steps:\n\n"
    "1. **Analysis**: Carefully compare the current image against the historical descriptions and classifications provided.\n"
    " * Focus on the following elements:"
    "   - 1. **Headers**: List all the headers present and describe their roles or relevance."
    "   - 2. **Number of Columns**: Count the columns and specify their purpose."
    "   - 3.**Types of Information**: Describe the type of data in each column (e.g., text, numbers, dates, categories)."  
    "   - 4. **General Format**: Describe detail appearance of the table, including alignment, borders, colors, or any visual styles that stand out."
    "2. **Decision**:\n"
    "   - If the image matches the historical data, retain the existing description, category, and label.\n"
    "   - If the image does not match, reclassify it. Provide a new, detailed description, assign a new category, "
    "and create a unique label that accurately captures all the table's characteristics.\n"
    "3. **Output**:\n"
    "   - Indicate whether the image was reclassified with 'yes' or 'no'.\n"
    "   - If reclassified ('yes'), include the updated description, category, and label.\n\n"
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
