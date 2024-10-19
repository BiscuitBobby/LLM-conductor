from agents import planner
from models import llm
from parcer.extract import split_plan, extract_plan_details, get_current_task
from conductor.client.worker.worker_task import worker_task
import json
import os
from tools import arsenal

def read_steps_dict(filename="steps_dict.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {}

def write_steps_dict(steps_dict, filename="steps_dict.json"):
    with open(filename, "w") as file:
        json.dump(steps_dict, file, indent=4)

def create_function(func_name, current_plan, step_name, dep):
    @worker_task(task_definition_name=func_name)
    def dynamic_function(prompt=''):
        # Read the steps_dict from the JSON file
        steps_dict = read_steps_dict()

        query = ''
        for i in dep:
            query += f'{i} = {steps_dict.get(i, {}).get("output", "No output yet")}\n'
        query+= current_plan
        print("---")
        print(query)
        print("---")
        # Update the current step's output
        steps_dict[step_name] = steps_dict.get(step_name, {})  # Ensure step exists
        steps_dict[step_name]["output"] = f"output from task: {prompt}"

        write_steps_dict(steps_dict)

    globals()[func_name] = dynamic_function
    return func_name


def create_threads(plan):
    groups = []
    grouped_plan = split_plan(plan)
    for group in grouped_plan:
        task_list = []
        plans_string = "\n".join(grouped_plan[group])
        print(plans_string + "\n")

        state = extract_plan_details(plans_string)
        steps_dict = {}

        step = get_current_task(state)
        for i in range(len(state["steps"])):
            _, step_name, tool_name, tool_input = state["steps"][i]
            steps_dict[step_name] = {
                "tool_name": tool_name,
                "tool_input": tool_input,
                "step_name": '',
                "output": ''
            }

        for i in state["steps"]:
            current_plan = ''
            current_task = ''
            step_count = 0

            for j in state["steps"]:
                _, step_name, tool_name, tool_input = j
                steps_dict[step_name]['step_name'] = step_name
                tool_name = steps_dict[step_name]["tool_name"]
                tool_input = steps_dict[step_name]["tool_input"]
                tool_output = steps_dict[step_name]["output"]

                step_count += 1

                # Check if this is the current task
                if j == i:
                    # print(f"Current task: {tool_name}[{tool_input}] {step_name} = {tool_output}")
                    current_plan += f"Current task {step_name}: {tool_name}[{tool_input}]"
                    current_task = step_name  # steps_dict[step_name]["action"]
                    steps_dict[step_name]["output"] = f'Lemon{step_count}'
                    break
                # TODO: code clean up
                else:
                    # print(f"{tool_name}[{tool_input}] {step_name} = {tool_output}")
                    # current_plan += f"{step_name} = {tool_output}\n"
                    pass

            dependencies = []
            # create the dynamic worker function
            for task in steps_dict:
                if task in current_plan and task != current_task:
                    # print(task)
                    dependencies.append(task)
                    pass
                elif task == current_task:
                    step = steps_dict[task]['step_name']
                    func_name = f"{steps_dict[task]['tool_name']}_{step[1::]}"

                    # print(current_plan + "\n")
                    # print(func_name)
                    fn = create_function(func_name, current_plan, current_task, dependencies)
                    task_list.append(fn)

        # create function list
        x = eval(f"[{','.join(task_list)}]")
        groups.append(x)
    print(groups)
    return groups

planner = planner.agent_init(llm.gemini_pro,arsenal)
input_data = {"input": "find electronics shopping enthusiasts and find the total amount of money that they've spent"}

# plan = planner.invoke(input_data).content
plan = '''
Plan: Find users who are interested in electronics. #E1 = FindUser[Interested in electronics]
Plan: Retrieve total amount spent by users from #E1. #E2 = Retrieve[total amount spent by #E1]
Plan: Message John 'hi'. #E3 = Message[{john: hi}]
'''

create_threads(plan)