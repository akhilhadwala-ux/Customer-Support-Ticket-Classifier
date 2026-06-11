#  AI-Powered Customer Support Ticket Classifier

##  Project Overview

This project is an AI-powered Customer Support Ticket Classification system built using:

* Streamlit
* LangChain
* Groq LLM (Qwen 3 32B)
* Pydantic Validation
* Langfuse Observability

The application automatically analyzes customer support tickets and performs multiple tasks simultaneously:

 Ticket Categorization

 Priority Assignment

 Support Queue Routing

 Automated Response Draft Generation

 End-to-End LLM Tracing using Langfuse

The goal is to reduce manual ticket triaging effort and improve customer support efficiency through Generative AI.

---

#  Features

### 1. Automatic Ticket Categorization

Classifies incoming customer requests into:

* Billing
* Technical Support
* Account Management
* Product Issue
* Delivery
* Refund
* General Inquiry

---

### 2. Priority Detection

Assigns ticket urgency levels:

* Low
* Medium
* High
* Critical

This helps support teams prioritize customer requests effectively.

---

### 3. Intelligent Ticket Routing

Automatically routes tickets to the appropriate team:

| Category          | Routing Queue     |
| ----------------- | ----------------- |
| Billing           | Billing Support   |
| Technical Issues  | Technical Support |
| Account Problems  | Accounts Team     |
| Product Issues    | Product Team      |
| Delivery Problems | Logistics Team    |
| General Requests  | Customer Support  |

---

### 4. AI Response Draft Generation

Generates concise and professional customer responses.

Examples:

### Complaint

> "We're sorry for the inconvenience caused. Our team is reviewing your issue and will assist you shortly."

### Inquiry

> "Thank you for contacting us. We will be happy to assist you with your request."

### Positive Feedback

> "Thank you for your feedback. We appreciate your support and are glad you had a positive experience."

---

### 5. Langfuse Observability

Every LLM interaction is automatically tracked using Langfuse.

Monitor:

* Prompt execution
* Model responses
* Token usage
* Latency
* Workflow tracing

---

#  System Architecture

```text
Customer Ticket
       │
       ▼
   LangChain
       │
       ▼
RunnableParallel
 ├── Category Chain
 ├── Priority Chain
 ├── Routing Chain
 └── Response Draft Chain
       │
       ▼
   Groq LLM
(Qwen 3 32B Model)
       │
       ▼
 Structured Output
(Pydantic Validation)
       │
       ▼
 Langfuse Tracing
       │
       ▼
 JSON Response
```

---

#  Tech Stack

## Frontend

* Streamlit

## LLM

* Groq
* Qwen/Qwen3-32B

## Framework

* LangChain

## Validation

* Pydantic

## Monitoring

* Langfuse

## Environment Management

* Python Dotenv

---

# 📂 Project Structure

```text
project/
│
├── app.py
├── .env
├── requirements.txt
├── Tracing Langfuse.csv
└── README.md
```

---

#  Workflow

### Step 1

User enters a support ticket.

Example:

```text
My order was delivered damaged and I need a replacement.
```

### Step 2

The application performs parallel analysis:

* Category Classification
* Priority Detection
* Queue Routing
* Response Generation

### Step 3

Structured outputs are validated using Pydantic.

### Step 4

Results are displayed as JSON.

Example:

```json
{
  "ticket_id": "TCK-A12BC3",
  "channel": "email",
  "category": "Product Issue",
  "priority": "High",
  "routing_queue": "Product Team",
  "response_draft": "We're sorry for the inconvenience. Our team is reviewing your request and will assist you shortly."
}
```

---

#  Sample Use Cases

## Billing Issues

* Incorrect charges
* Payment failures
* Subscription problems

## Technical Support

* Login issues
* Website errors
* Application crashes

## Delivery Problems

* Missing packages
* Delayed shipments
* Damaged deliveries

## Product Issues

* Defective products
* Warranty requests
* Product malfunctions

---

#  Environment Variables

Create a `.env` file:

```env
groq_api_key=YOUR_GROQ_API_KEY
LANGFUSE_PUBLIC_KEY=YOUR_PUBLIC_KEY
LANGFUSE_SECRET_KEY=YOUR_SECRET_KEY
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

#  Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/customer-support-ticket-classifier.git
cd customer-support-ticket-classifier
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

#  Key Learnings

* Building structured-output LLM workflows
* Prompt engineering for classification tasks
* Pydantic-based output validation
* LangChain RunnableParallel execution
* LLM observability using Langfuse
* Multi-task inference using a single LLM

---

#  Future Enhancements

* Sentiment Analysis
* SLA Prediction
* Multi-language Ticket Support
* Agentic Escalation Workflows
* Ticket Summarization
* Vector Database Integration
* RAG-Based Customer Support

---

#  Author

**Hadwala Akhil**

Data Science | Machine Learning | Generative AI | LangChain

---

#  Key Takeaway

> This project demonstrates how Generative AI can automate customer support workflows by intelligently classifying, prioritizing, routing, and responding to support tickets while maintaining complete observability through Langfuse.
