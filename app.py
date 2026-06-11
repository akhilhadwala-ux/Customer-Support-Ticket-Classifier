import os
import uuid
from google import genai
import numpy as np
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langfuse.langchain import CallbackHandler

# load variables from .env file
load_dotenv(dotenv_path=".env")
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

# API KEY
api_key = os.getenv("groq_api_key")

if not api_key:
    st.error("API key not found. Check your .env file")
    st.stop()

st.title("Customer Support Ticket Classifier")

################ Start ####################

llm = ChatGroq(
    model="qwen/qwen3-32b",  
    groq_api_key=api_key,
    reasoning_format="hidden" # the model is instructed to perform reasoning internally but return only the final answer
)
## ------------------- Pydantic Validation ------------- ##

class CategoryOutput(BaseModel):
    category: str = Field(
        description="Billing, Technical Support, Account Management, Product Issue, Delivery, Refund, General Inquiry"
    )

class PriorityOutput(BaseModel):
    priority: str = Field(
        description="Low, Medium, High, Critical"
    )

class RoutingOutput(BaseModel):
    routing_queue: str = Field(
        description="Support queue responsible for handling ticket"
    )

class ResponseDraftOutput(BaseModel):
    response_draft: str = Field(
        description="Professional customer support response"
    )


category_parser = PydanticOutputParser(
    pydantic_object=CategoryOutput
)

priority_parser = PydanticOutputParser(
    pydantic_object=PriorityOutput
)

routing_parser = PydanticOutputParser(
    pydantic_object=RoutingOutput
)

draft_parser = PydanticOutputParser(
    pydantic_object=ResponseDraftOutput
)

############ category_chain ############ 

category_prompt = ChatPromptTemplate.from_template(
"""
Classify the ticket into ONE category.

Categories:
- Billing
- Technical Support
- Account Management
- Product Issue
- Delivery
- Refund
- General Inquiry

Ticket:
{ticket_text}

{format_instructions}
""",
partial_variables={
    "format_instructions":category_parser.get_format_instructions()
}
)

category_chain = (
    category_prompt
    | llm
    | category_parser
    | RunnableLambda(lambda x: x.category)
)

############ Priority_chain ############ 
priority_prompt = ChatPromptTemplate.from_template(
"""
Determine ticket priority.

Labels:
- Low
- Medium
- High
- Critical

Ticket:
{ticket_text}

{format_instructions}
""",
partial_variables={
    "format_instructions":
    priority_parser.get_format_instructions()
}
)

priority_chain = (
    priority_prompt
    | llm
    | priority_parser
    | RunnableLambda(lambda x: x.priority)
)

############ Priority_chain ############ 
routing_prompt = ChatPromptTemplate.from_template(
"""
Choose the correct routing queue.

Queues:
- Billing Support
- Technical Support
- Accounts Team
- Product Team
- Logistics Team
- Customer Support

Ticket:
{ticket_text}

{format_instructions}
""",
partial_variables={
    "format_instructions":
    routing_parser.get_format_instructions()
}
)

routing_chain = (
    routing_prompt
    | llm
    | routing_parser
    | RunnableLambda(lambda x: x.routing_queue)
)
############ Priority_chain ############ 
draft_prompt = ChatPromptTemplate.from_template(
"""
Generate a customer support response draft.

Rules:
1. Keep the response concise (maximum 1-2 lines).
2. If the customer expresses frustration, inconvenience, dissatisfaction, a complaint, or a problem:
   - Start with a brief apology/regret statement.
   - Acknowledge the issue and mention that it will be addressed.
3. If the customer message is neutral (question, inquiry, information request):
   - Thank the customer for contacting us.
   - Provide a brief helpful response.
   - End with a polite note such as "Thank you for reaching out."
4. If the customer message is positive (appreciation, praise, satisfaction):
   - Thank the customer for their feedback/support.
   - Respond positively and professionally.
5. Do not use bullet points.
6. Do not exceed 2 sentences.

Ticket:
{ticket_text}

{format_instructions}
""",
partial_variables={
    "format_instructions": draft_parser.get_format_instructions()
}
)

draft_chain = (
    draft_prompt
    | llm
    | draft_parser
    | RunnableLambda(lambda x: x.response_draft)
)

############ analysis_parallel ############ 

analysis_parallel = RunnableParallel(
    {
        "category": category_chain,
        "priority": priority_chain,
        "routing_queue": routing_chain,
        "response_draft": draft_chain
    }
)

ticket_id = f"TCK-{uuid.uuid4().hex[:6].upper()}"

result = analysis_parallel.invoke(
    {
        "ticket_text": ticket_id
    }
)

ticket_text = st.text_area("Enter Ticket")

channel = st.selectbox(
    "Channel",
    ["email", "chat", "phone", "web"]
)

import uuid

if st.button("Classify Ticket"):

    if not ticket_text.strip():
        st.warning("Please enter a ticket.")
    else:
        try:
            with st.spinner("Analyzing ticket..."):

                # Generate Ticket ID
                ticket_id = f"TCK-{uuid.uuid4().hex[:6].upper()}"

                # Invoke RunnableParallel
                result = analysis_parallel.invoke(
                {"ticket_text": ticket_text},
                config={
                    "callbacks": [langfuse_handler]
                })

                # Build Final Output
                final_output = {
                    "ticket_id": ticket_id,
                    "channel": channel,
                    "category": result["category"],
                    "priority": result["priority"],
                    "routing_queue": result["routing_queue"],
                    "response_draft": result["response_draft"]
                }

            st.success("Ticket Classified Successfully")

            # JSON Output
            st.subheader("JSON Output")
            st.json(final_output)

        except Exception as e:
            st.error(f"Error: {e}")