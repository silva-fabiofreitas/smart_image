from dotenv import load_dotenv

from langgraph.graph import StateGraph, END

from graph.nodes.classifier import classifier_table
from graph.nodes.evaluator import evaluator_descriptions
from graph.state import GraphState

load_dotenv()

TABLE_CLASSIFIER = 'table classifier'
EVALUATOR = 'evaluator'


workflow = StateGraph(GraphState)
workflow.add_node(TABLE_CLASSIFIER, classifier_table)
workflow.add_node(EVALUATOR, evaluator_descriptions)

workflow.add_edge(TABLE_CLASSIFIER, EVALUATOR)
workflow.add_edge(EVALUATOR, END)

workflow.set_entry_point(TABLE_CLASSIFIER)

app = workflow.compile()
app.get_graph().draw_mermaid_png(output_file_path='graph.png')