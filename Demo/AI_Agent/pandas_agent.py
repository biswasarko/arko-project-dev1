from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFacePipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import pandas as pd

# Step 1: Load the Hugging Face model and tokenizer
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Step 2: Create a text2text-generation pipeline
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)

# Step 3: Wrap the pipeline with HuggingFacePipeline
llm = HuggingFacePipeline(pipeline=pipe)

# Step 4: Define a prompt template for converting natural language to pandas queries
prompt_template = PromptTemplate(
    input_variables=["columns", "user_query"],
    template="""
    You are an AI assistant that converts natural language into valid Pandas queries.
    The dataset has the following columns: {columns}.
    User Query: {user_query}

    Write the corresponding Pandas query:
    """
)

# Step 5: Create the LangChain chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Example dataset
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["New York", "Los Angeles", "Chicago"],
}
df = pd.DataFrame(data)

# Example input query
# user_query = "Get all rows where age is greater than 30."
user_query = """You are an agent which transforms natural text to pandas queries. 
We have a pandas df with structure: name, age, city. 
Write a query that will create a new df from old df , while filtering data where age is greater than 30. Please provide only df code."""

# Step 6: Execute the chain and get the response
response = chain.run(columns=", ".join(df.columns), user_query=user_query)

# Step 7: Evaluate the generated query
try:
    print("Generated Query:")
    print(response)
    result = eval(response)  # Caution: Always validate the generated code
    print("\nQuery Result:")
    print(result)
except Exception as e:
    print("Error executing query:", e)
