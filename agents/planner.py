from langchain.tools.render import render_text_description
from langchain.prompts import PromptTemplate

planner_prompt = """
If the task requires multiple steps, break it down and create a step-by-step plan. For each step, specify:
- The external tool to use
- The tool input to gather evidence

Store each result in a variable (#E) that can be referenced by later steps (e.g., #E1, #E2, etc.).

YOU ONLY HAVE ACCESS TO THESE TOOLS:
{tools}

Example:
Task: Who worked on the project, and how much longer would it have taken if Rebecca worked at double their speed?
Plan: Identify who worked on the project. #E1 = FindUser[Worked on project]
Plan: Retrieve time spent by user(s) from #E1. #E2 = Retrieve[time spent by #E1]
Plan: Calculate how much longer Rebecca would take (2x the time of #E2). #E3 = Wolfram[2 * time]

Now, start planning! Avoid unnecessary steps, and follow each plan with a single #En ToolName[<ToolInput>].

Task: {input}
"""

def agent_init(llm,tools):
    llm.temperature = 0.3

    prompt = PromptTemplate.from_template(planner_prompt)
    prompt = prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    planner = prompt.pipe(llm)
    return planner

#planner = planning_agent_init(llm,tools)
