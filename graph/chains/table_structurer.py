from typing import List, Optional

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()


# Define your desired data structure.
class Table(BaseModel):
    arquivo: str = Field(description="File name")
    titulo: Optional[str] = Field(description="Titulo da tabela")
    cenario: List[str] = Field(description="Nome dos cenários")
    cobertura: List[Optional[int]] = Field(description="Quantidade representando a Cobertura")
    percentual_cobertura: List[Optional[float]] = Field(description="Percentual de Cobertura %")


# Instância o modelo
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

structured_llm = llm.with_structured_output(Table)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Describe the image provided \n file:{file}"),
        (
            "user",
            [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image}"},
                }
            ],
        ),
    ]
)

chain_structured = prompt | structured_llm
