# OpenAI Agents SDK — Build Report

## 1. What I Changed and Why

For this assignment, I selected the OpenAI Agents SDK starter kit, which uses a triage agent to route user requests to specialized agents.

I modified the instructions of the **Math Tutor** agent in `main.py`. Originally, the Math Tutor was instructed to use the calculation tool and explain the result in one or two sentences.

I changed the instructions to make the Math Tutor behave like a friendly teacher helping beginners. The modified instructions require the agent to explain the calculation step by step, including the formula, substituted values, and final answer in simple language.

**Reason for the change:** I wanted to test whether changing an agent's instructions could improve the clarity and educational usefulness of its response without affecting the accuracy of the calculation.

**Hypothesis:** The modified Math Tutor would provide a more detailed explanation while producing the same correct numerical answer.

**Test question:** What is 18% of 2450?

I used the same question in both runs to make the comparison consistent. I did not change the calculation tool, the model configuration, or the agent handoff structure.

## 2. How the Framework Works

The OpenAI Agents SDK is a framework for building applications using AI agents, tools, and handoffs. In this starter kit, the system uses three agents to handle different types of user requests.

### Agents and Their Responsibilities

**Triage Agent:** This is the entry point of the application. It examines the user's request and decides whether to send it to the Math Tutor, the Writing Coach, or answer directly.

**Math Tutor Agent:** This agent handles arithmetic and quantitative questions. It uses the `calculate` tool to evaluate mathematical expressions. I modified this agent's instructions for my experiment.

**Writing Coach Agent:** This agent handles writing improvement requests. It uses the `word_count` tool to count words before and after editing.

### Tools

The starter kit defines two Python functions using the `@function_tool` decorator:

- `calculate(expression)`: Evaluates basic arithmetic expressions using Python's `ast` module and a restricted set of mathematical operators.
- `word_count(text)`: Counts words in a given text using Python's `split()` method.

These tools allow the specialist agents to perform specific operations rather than relying only on the language model's generated text.

### Handoffs and Execution

The Triage agent is configured with handoffs to the Math Tutor and Writing Coach. When it selects a specialist, the handoff callback displays a short reason for the decision.

The application uses `Runner.run_sync()` to execute the agent workflow. The Runner manages agent execution, tool calls, and handoffs until a final response is produced.

For my test question, the workflow was:

**User Question → Triage Agent → Math Tutor Agent → Calculate Tool → Final Explanation**

### Model Configuration

The starter kit uses the OpenAI Agents SDK with Groq as the model provider. The configured model is `openai/gpt-oss-120b`, accessed through an OpenAI-compatible API.

The API key is stored separately in a local `.env` file and is not included in the submitted code or experiment outputs.

## 3. Evidence and Results

I tested the original and modified versions of the OpenAI Agents SDK starter kit using the same question: **"What is 18% of 2450?"**

### Run 1 — Original Version

The original Math Tutor was instructed to use the calculation tool and explain the result in one or two sentences.

**Handoff reason:**
> The request asks for a percentage calculation, which is a quantitative problem.

**Math Tutor response:**
> 18% of 2450 is **441**. This is obtained by multiplying 2450 by 0.18.

The Triage agent correctly selected the Math Tutor, and the Math Tutor returned the correct numerical answer with a short explanation.

### Run 2 — Modified Version

I changed the Math Tutor's instructions to request a beginner-friendly, step-by-step explanation.

**Handoff reason:**
> The user asks for a percentage calculation, which is a quantitative math problem.

The modified Math Tutor explained the calculation in three steps:

1. Convert 18% into the decimal 0.18.
2. Multiply 0.18 by 2450.
3. Report the calculated result of 441.

The final answer was again **441**.

### Comparison

| Feature | Run 1 | Run 2 |
|---|---|---|
| Framework | OpenAI Agents SDK | OpenAI Agents SDK |
| Specialist selected | Math Tutor | Math Tutor |
| Numerical answer | 441 | 441 |
| Explanation | Short | Three numbered steps |
| Formula included | No | Yes |
| Instructions | Original | Modified |
| Execution result | Successful | Successful |

### Observations

Both runs produced the correct numerical answer. The main difference was the explanation style.

In Run 1, the Math Tutor provided a brief explanation. In Run 2, it showed the percentage conversion, multiplication expression, and final result in separate steps.

This supports my hypothesis that modifying agent instructions can influence response structure and clarity without changing the mathematical answer in this test.

The experiment used one test question, so the results demonstrate behavior for this example rather than proving that the modified instructions will always produce better explanations.

The complete outputs are saved in `run1_original.txt` and `run2_changed.txt`.

## 4. Comparison with CrewAI

For this assignment, I selected the OpenAI Agents SDK. Another framework available in the starter kits is CrewAI.

Both frameworks support multi-agent applications, but they organize agent collaboration differently.

| Feature | OpenAI Agents SDK | CrewAI |
|---|---|---|
| Main approach | Agents, tools, handoffs, and a Runner | Agents, tasks, and crews |
| Agent coordination | Agents can transfer control through handoffs | A crew coordinates agents assigned to tasks |
| Tools | Python functions can be registered using `@function_tool` | Tools can be assigned to agents |
| Execution | `Runner.run_sync()` executes the agent workflow | A crew executes its configured process |
| Typical use case | Routing requests to specialized agents | Coordinating agents to complete a multi-step task |

### Why OpenAI Agents SDK Was Suitable

The OpenAI Agents SDK was suitable for my experiment because the starter kit already included a Triage agent, a Math Tutor, and a Writing Coach.

Its handoff mechanism allowed the Triage agent to route the percentage question to the Math Tutor. I could then modify only the Math Tutor's instructions while keeping the rest of the workflow unchanged.

CrewAI would also be useful for applications requiring multiple agents to collaborate on a larger task, such as researching a topic, writing a report, and reviewing the result.

### What I Learned

The main lesson from this experiment was that agent instructions influence how an agent presents its response.

I also learned how the OpenAI Agents SDK connects agents with tools, uses handoffs to transfer control, and executes workflows through the Runner.

The comparison with CrewAI is based on the frameworks' design and starter-kit structure. I did not independently run a CrewAI experiment for this assignment.

## 5. Verification, Limitations, and AI Assistance

### Verification

I completed two successful executions of the OpenAI Agents SDK starter kit using the same mathematical question.

- **Run 1:** Executed the original Math Tutor instructions and received the correct answer, 441, with a short explanation.
- **Run 2:** Executed the modified Math Tutor instructions and received the same correct answer, 441, with a step-by-step explanation.
- **Code modification:** Changed only the Math Tutor's instructions in `main.py`.
- **Evidence:** Saved both execution outputs as `run1_original.txt` and `run2_changed.txt`.

The setup check also completed successfully using the `openai/gpt-oss-120b` model through Groq.

### Limitations

This experiment tested only one mathematical question. Therefore, the results cannot establish whether the modified instructions will consistently improve explanations across different types of problems.

The numerical answer was correct in both runs, but the experiment did not measure explanation quality using a formal evaluation metric.

The framework uses a language model, so responses may vary between executions even when the input and instructions remain unchanged.

### AI Assistance Disclosure

I used ChatGPT for step-by-step guidance during environment setup, understanding the starter-kit architecture, planning the experiment, interpreting the outputs, and drafting the report.

I executed the original and modified programs, supplied the test question, observed the results, and saved the execution evidence. The reported outputs are from the actual program runs, not simulated results.

### Conclusion

This experiment demonstrated how changing the instructions of a specialized agent can affect the format and detail of its response.

The OpenAI Agents SDK successfully routed the mathematical question from the Triage agent to the Math Tutor. The modified Math Tutor provided a more detailed explanation while preserving the correct numerical result.

The experiment helped me understand agent instructions, tool integration, handoffs, and execution using the OpenAI Agents SDK.