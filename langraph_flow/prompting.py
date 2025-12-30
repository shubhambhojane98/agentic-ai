from dotenv import load_dotenv
from  langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


load_dotenv()


llm = ChatOpenAI(model="gpt-3.5-turbo")

## Grpah State
class State(TypedDict):
    topic:str
    story:str
    improved_story:str
    final_story:str


## Nodes

def generate_story(state:State):
    msg=llm.invoke(f"Write a one sentence story premise about {state["topic"]}")
    return {"story":msg.content}

def check_conflict(state:State):
    if "?" in state["story"] or "!" in state["story"]:
        return "Fail"
    return "Pass"

def improved_story(state:State):
    msg=llm.invoke(f"Enhance this story premise with vivid details: {state['story']}")
    # print("improved story", msg)
    return {"improved_story":msg.content}

def polish_story(state:State):
    msg=llm.invoke(f"Add an unexpected twist to this story premise: {state['improved_story']}")
    # print("final_story", msg)
    return {"final_story":msg.content}


#Build the graph
graph=StateGraph(State)
graph.add_node("generate",generate_story)
graph.add_node("improve", improved_story)
graph.add_node("polish", polish_story)


## Define the edges
graph.add_edge(START,"generate")
graph.add_conditional_edges("generate",check_conflict,{"Pass":"improve","Fail":"generate"})
graph.add_edge("improve","polish")
graph.add_edge("polish",END)


# Compile the graph
compiled_graph = graph.compile()

## invoke the graph
updated_state =  compiled_graph.invoke(State({"topic" : "Harry Potter"}))
print(updated_state)