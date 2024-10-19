from langchain_core.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_messages
from langchain.agents.output_parsers import ReActSingleInputOutputParser

Llama_react='''
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

def exec_agent_init(action,tools,llm):
    llm.temperature = 0.3
    llm = llm.bind(stop=["\nObservation"])

    prompt = PromptTemplate.from_template(Llama_react)

    prompt = prompt.partial(
            tools=render_text_description(tools),
            tool_names=", ".join([t.name for t in tools]),
            action=action,
        )

    exec_agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_messages(x["intermediate_steps"]),
            }
            | prompt
            | llm
            | ReActSingleInputOutputParser()
    )

    agent_executor = AgentExecutor(agent=exec_agent, tools=tools, verbose=True,
                                        return_intermediate_steps=True)
    return agent_executor