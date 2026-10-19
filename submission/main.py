"""OpenAI Agents SDK starter: a triage agent that hands off to specialists.

Run:  uv run python main.py

The SDK's big idea is small: an AGENT is instructions + tools + (optionally)
other agents it can HAND OFF to. A Runner loops until an agent gives a final answer.
Try:  "What is 18% of 2450?"   then   "Tighten this: we utilize synergies"
"""
import ast
import operator
import os

from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    handoff,
    set_tracing_disabled,
)
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

load_dotenv()

# --- 1. Point the SDK at Groq instead of OpenAI --------------------------
client = AsyncOpenAI(
    base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
    api_key=os.environ["GROQ_API_KEY"],
)
set_tracing_disabled(True)  # tracing uploads to OpenAI, which we are not using

# Wrap the model explicitly. Passing a bare string like "openai/gpt-oss-120b"
# would make the SDK treat "openai/" as ITS OWN provider prefix and strip it,
# sending Groq the wrong model name. The wrapper sends the name unchanged.
MODEL = OpenAIChatCompletionsModel(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    openai_client=client,
)

# --- 2. Tools: plain Python functions the model may call ------------------
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("only basic arithmetic is allowed")


@function_tool
def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as '0.18 * 2450'."""
    return str(_eval(ast.parse(expression, mode="eval").body))


@function_tool
def word_count(text: str) -> int:
    """Count the words in a piece of text."""
    return len(text.split())


# --- 3. Specialist agents -------------------------------------------------
math_tutor = Agent(
    name="Math Tutor",
    handoff_description="Handles arithmetic and quantitative questions.",
    instructions="You are a friendly math teacher helping beginners. "
    "ALWAYS use the calculate tool for arithmetic. "
    "Explain each calculation step by step, showing the formula, "
    "substituted values, and final answer. Use simple language.",
    tools=[calculate],
    model=MODEL,
)
writing_coach = Agent(
    name="Writing Coach",
    handoff_description="Handles editing and tightening of text.",
    instructions="You tighten writing. Use word_count before and after editing "
    "and report both numbers.",
    tools=[word_count],
    model=MODEL,
)

# --- 4. Triage agent: decides who should handle the request ---------------
# A hand-off is a tool the model calls. By default it takes NO arguments, and
# Groq rejects that empty schema ("'required' present but 'properties' is
# missing"). Giving the hand-off one small input fixes it, and it also lets
# you SEE why the triage agent chose each specialist.
class HandoffReason(BaseModel):
    reason: str = Field(description="One short sentence: why this specialist fits.")


def show_reason(ctx, data: HandoffReason):
    print(f"  (hand-off: {data.reason})")


triage = Agent(
    name="Triage",
    instructions="Route the user to the right specialist and give a short "
    "reason. If neither fits, answer briefly yourself.",
    handoffs=[
        handoff(math_tutor, on_handoff=show_reason, input_type=HandoffReason),
        handoff(writing_coach, on_handoff=show_reason, input_type=HandoffReason),
    ],
    model=MODEL,
)

if __name__ == "__main__":
    print("Agents SDK kit. Type 'quit' to exit.\n")
    history = []
    while True:
        user = input("You: ").strip()
        if user.lower() in {"quit", "exit", ""}:
            break
        history.append({"role": "user", "content": user})
        result = Runner.run_sync(triage, history)
        print(f"\n[{result.last_agent.name}] {result.final_output}\n")
        history = result.to_input_list()  # carry the conversation forward
