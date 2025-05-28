from agents import Agent,Runner

writer = Agent(
    name = 'writer Agent',
    instructions="You are a writer agent. Generate poems, stories,essays, email etc."

)

response - Runner.run_sync(
    writer,
    input="Write a 2 paragraph essay on Generative AI",
    run_config=config
)