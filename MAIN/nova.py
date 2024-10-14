from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define the prompt template for the chatbot
template = """Question: {question}

Answer: Let's think step by step."""

# Create the prompt template
prompt = ChatPromptTemplate.from_template(template)

# Initialize the Ollama LLM with the specific model version
model = OllamaLLM(model="llama3.1")

# Create a chain that combines the prompt and model
chain = prompt | model

def handle_conversation():
    context = ""
    print("Welcome to the AI Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting the chatbot. Goodbye!")
            break

        # Invoke the model with the user's input and current context
        result = chain.invoke({"context": context, "question": user_input})
        
        # Display the model's response
        print("Bot:", result)
        
        # Update the context for conversation continuity
        context += f"\nYou: {user_input}\nBot: {result}"

# Run the conversation handler
if __name__ == "__main__":
    handle_conversation()
