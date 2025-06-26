# class 01

## Agentic AI Frameworks

- Langgraph
- Crew AI
- Auto en
- Google ADK
- OpenAI Agent SDK (we use this)

## Steps

- get/retrive API key from Gemini Google
- install openAI agents SDK
  ```
  pip install openai-agents # or `uv add openai-agents`, etc
  ```
- apply API key in .env
- install dotenv

```
pip install python-dotenv
```

### Who will force to run Agents?
- The answer is runner
- Runner works in 2 ways
  - Runner.run_sync (works syncronously line by line)
  - Runner.run (works concurrently parallely)
```python
from agents import Agent, Runner,
response = Runner.run_sync(
    writer,
    input = 'Write a 2 paragraph essay on Generative AI..',
    run_config = config
    )
```
- take 3 parameter
1. starting_agent=`agent`
2. input prompt
3. run_config

#### what is `config`?
- config has configuration about LLM models
```python
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
``` 
- 3 parameters
  - model 
  - model_provider

# Homework

- create a translator agent(urdu to english or viceversa)
