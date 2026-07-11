from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)

from backend.agent.llm import llm

from backend.agent.tools import (
    inspect_dataframe_tool,
    generate_cleaning_code_tool,
    execute_generated_code_tool,
    validate_output_tool,
)

# --------------------------------------------------------
# TOOLS
# --------------------------------------------------------

tools = [
    inspect_dataframe_tool,
    generate_cleaning_code_tool,
    execute_generated_code_tool,
    validate_output_tool,
]

# --------------------------------------------------------
# PROMPT
# --------------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an autonomous data cleansing agent.

You have access to four tools.

You MUST follow this workflow exactly.

Step 1:
Call inspect_dataframe_tool using the CSV file path.

Step 2:
The tool returns a dataframe summary string.
Pass ONLY that summary as the 'schema_summary'
argument when calling generate_cleaning_code_tool.

Also pass the ORIGINAL user instruction as
'user_instruction'.

Step 3:
generate_cleaning_code_tool returns executable
Python code.

Pass ONLY that generated code as
'generated_code' when calling
execute_generated_code_tool.

Also pass:

- the ORIGINAL CSV path
- the ORIGINAL user instruction

execute_generated_code_tool automatically
repairs execution failures internally.
Never attempt to regenerate code yourself.

Step 4:
If execution succeeds,
call validate_output_tool using:

- original CSV path
- execution output path
- original user instruction

Finally return:

- success
- output CSV path
- validation warnings

Never invent values.

Always use tool outputs.

Never skip any step.
""",
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# --------------------------------------------------------
# AGENT
# --------------------------------------------------------

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# --------------------------------------------------------
# EXECUTOR
# --------------------------------------------------------

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
)

# --------------------------------------------------------
# EXPLANATION CHAIN
# --------------------------------------------------------

from langchain_core.output_parsers import StrOutputParser

explanation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a data engineering assistant.

Write ONE short paragraph explaining, in plain English,
what was done to the dataset.

Do not mention Docker, LangChain or implementation details.

Keep it under 120 words.
""",
        ),
        (
            "human",
            """
User Instruction:
{instruction}

Generated Python Code:
{generated_code}

Validation Warnings:
{validation_warnings}
""",
        ),
    ]
)

explanation_chain = (
    explanation_prompt
    | llm
    | StrOutputParser()
)