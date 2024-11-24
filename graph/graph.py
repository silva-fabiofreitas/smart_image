from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

from graph.nodes.classifier import classifier_table
from graph.nodes.evaluator import evaluator_descriptions
from graph.nodes.structurer import table_parse
from graph.state import GraphState

load_dotenv()

TABLE_CLASSIFIER = 'table classifier'
EVALUATOR = 'evaluator'
PARSE = 'parse table'


def route_question(state: GraphState):
    print('---ROUTE QUESTION---')
    structure = state['structure']

    if structure:
        print('---ROUTE TO PARSE TABLE---')
        return PARSE
    else:
        print('---ROUTE QUESTION TO RAG')
        return TABLE_CLASSIFIER


workflow = StateGraph(GraphState)
workflow.add_node(TABLE_CLASSIFIER, classifier_table)
workflow.add_node(EVALUATOR, evaluator_descriptions)
workflow.add_node(PARSE, table_parse)

workflow.add_edge(TABLE_CLASSIFIER, EVALUATOR)
workflow.add_edge(EVALUATOR, END)
workflow.add_edge(PARSE, END)

workflow.set_conditional_entry_point(
    route_question,
    {
        PARSE: PARSE,
        TABLE_CLASSIFIER: TABLE_CLASSIFIER
    }
)

app = workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path='graph.png')