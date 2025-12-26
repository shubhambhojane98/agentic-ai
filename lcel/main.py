from dotenv import load_dotenv
from  langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

# Take user input
user_query = input("Ask something: ")

# create a prompt template
system_template = "Write  5 line about given {topic}"
prompt_template = ChatPromptTemplate([
    ('system',system_template),
    ('user','Tell me about it.')
])

# messages = prompt_template.invoke({"topic": user_query})
# response = model.invoke(messages)
# final_output = response.content

# print("\n--- Response ---\n")
# print(final_output)

parser = StrOutputParser()

# create chain
chain = prompt_template|model|parser

response = chain.invoke({"topic": user_query})

print("\n--- Response ---\n")
print(response)