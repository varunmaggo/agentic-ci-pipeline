
from langgraph.graph import StateGraph
from langgraph.checkpoint import MemorySaver

def read_model(state):
    state['model'] = open("model.json").read()
    return state

def read_code(state):
    state['code'] = open("services/api/Dockerfile").read()
    return state

def plan_fix(state):
    state['plan'] = "Add EXPOSE 5000 if missing"
    return state

def write_fix(state):
    state['patched'] = state['code'] + "\nEXPOSE 5000"
    return state

def validate(state):
    state['valid'] = "EXPOSE" in state['patched']
    return state

def is_valid(state):
    return "done" if state['valid'] else "read_model"

builder = StateGraph()
builder.set_state_type(dict)

builder.add_node("read_model", read_model)
builder.add_node("read_code", read_code)
builder.add_node("plan_fix", plan_fix)
builder.add_node("write_fix", write_fix)
builder.add_node("validate", validate)

builder.set_entry_point("read_model")
builder.add_edge("read_model", "read_code")
builder.add_edge("read_code", "plan_fix")
builder.add_edge("plan_fix", "write_fix")
builder.add_edge("write_fix", "validate")
builder.add_conditional_edges("validate", is_valid)

app = builder.compile()
app.invoke({})
