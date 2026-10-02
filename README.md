# AI Customer Support Agent with Generative AI & Agentic Workflow

An AI-powered customer support system that understands customer queries, retrieves relevant information from a knowledge base, generates context-aware responses, performs agentic actions, and escalates uncertain or sensitive cases to human support.

## Project Overview

The AI Customer Support Agent is designed to demonstrate how Generative AI, Retrieval-Augmented Generation (RAG), and agentic workflows can be combined to automate customer support.

The system uses a customer-support knowledge base containing product information, shipping policies, return policies, refund policies, payment policies, warranty information, and escalation rules.

For each customer query, the system:

1. Understands the customer query.
2. Identifies the query intent.
3. Retrieves relevant information from the knowledge base.
4. Calculates a confidence score.
5. Generates a grounded response when the information is sufficient.
6. Performs agentic actions such as checking order status.
7. Creates a support ticket when escalation is required.
8. Displays the conversation and support details through a Streamlit interface.

## Key Features

* Generative AI customer support
* Retrieval-Augmented Generation (RAG)
* Vector-based knowledge retrieval using ChromaDB
* Query intent detection
* Confidence-based response handling
* Mock order-status checking
* Automated support-ticket creation
* Human escalation for uncertain cases
* Sensitive-information protection
* Conversation history
* Streamlit chat interface
* Local persistent knowledge base

## System Workflow

```text
Customer Query
      ↓
Query Understanding
      ↓
Intent Detection
      ↓
Knowledge Retrieval
      ↓
Confidence Evaluation
      ↓
 ┌───────────────┬────────────────┐
 │               │                │
Reliable      Agentic Action   Low Confidence /
Query         Required         Sensitive Query
 │               │                │
 ↓               ↓                ↓
Generate       Order Status     Human
Response       / Ticket         Escalation
 │               │                │
 └───────────────┴────────────────┘
                 ↓
          Streamlit Chat UI
```

## Technologies Used

* Python 3.12
* Streamlit
* Groq API
* Groq Python SDK
* ChromaDB
* Python-dotenv
* Git
* GitHub

## Project Structure

```text
AI-Customer-Support-Agent
│
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── knowledge_base.py
│   ├── retriever.py
│   ├── support.py
│   └── tools.py
│
├── data/
│   └── knowledge_base.txt
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Module Description

### `app.py`

Provides the Streamlit chat interface and displays:

* Customer messages
* AI responses
* Intent
* Confidence score
* Escalation status
* Agent actions

### `agent.py`

Acts as the main orchestration layer.

It coordinates:

* Knowledge retrieval
* Intent detection
* Confidence evaluation
* LLM response generation
* Order-status tools
* Support-ticket creation
* Human escalation

### `knowledge_base.py`

Loads the customer-support knowledge base, divides it into sections, and stores the sections in ChromaDB.

### `retriever.py`

Searches the ChromaDB knowledge base for information relevant to the customer's query.

### `support.py`

Handles support logic including:

* Intent detection
* Sensitive-query detection
* Confidence calculation
* Escalation decisions

### `tools.py`

Contains mock agentic tools for:

* Checking order status
* Creating support tickets

## Knowledge Base

The sample NovaTech Store knowledge base contains:

* Company support hours
* Product information
* Shipping policy
* Return policy
* Refund policy
* Payment policy
* Warranty policy
* Account support
* Escalation policy
* Support safety guidelines

## Agentic Actions

The system includes mock tools that allow the AI agent to perform actions instead of only generating text.

### Order Status

Example:

```text
Customer:
Where is my order ORD1001?

Agent:
Your order ORD1001 is currently Shipped.
Product: NovaBook Pro 14.
Estimated delivery: 2 days.
```

### Human Support Ticket

When the system cannot safely answer a query, it creates a mock support ticket and escalates the issue.

Example:

```text
Customer:
What is NovaTech's cryptocurrency investment plan?

Agent:
I don't have enough reliable information to safely answer this request.
Your issue has been escalated to a human support agent.
```

## Safety and Escalation

The system is designed not to invent unsupported information.

Queries are escalated when:

* The retrieved information is insufficient.
* The confidence score is below the required threshold.
* Sensitive account or payment information is involved.
* The customer disputes a transaction or refund decision.
* The issue requires human intervention.

The system does not request:

* Passwords
* OTPs
* Complete payment card details

## Installation

Clone the repository:

```bash
git clone https://github.com/Ezhilarasipalani1428/AI-Customer-Support-Agent.git
```

Move into the project directory:

```bash
cd AI-Customer-Support-Agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root.

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Do not commit the `.env` file to GitHub.

## Build the Knowledge Base

Run:

```bash
python -m src.knowledge_base
```

The system will create the local ChromaDB knowledge store.

## Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in the browser.

## Testing

The system was tested with different types of customer queries.

### Test 1 — Knowledge-Based Query

```text
Query:
What is the return policy?

Result:
The AI generated a response using the retrieved return-policy information.

Intent:
return_refund

Escalated:
False
```

### Test 2 — Order Status

```text
Query:
Where is my order ORD1001?

Result:
Order status was retrieved using the mock order-status tool.

Intent:
order_status

Escalated:
False
```

### Test 3 — Unknown Query

```text
Query:
What is NovaTech's cryptocurrency investment plan?

Result:
The system detected insufficient reliable information and created a support ticket.

Intent:
general

Escalated:
True
```

### Test 4 — Sensitive Query

```text
Query:
I need help with my credit card number and payment.

Result:
The request was escalated to human support and the system instructed the customer not to share complete payment details.

Escalated:
True
```

## Project Outcomes

The project demonstrates:

* Generative AI-based customer support
* Retrieval-Augmented Generation
* Vector database usage
* Intent detection
* Confidence-based decision making
* Agentic tool execution
* Mock API interaction
* Human escalation
* Conversation-state management
* Safe handling of sensitive requests
* Streamlit-based AI application development

## Limitations

* The order-status system uses mock data.
* The support-ticket system is simulated.
* The knowledge base is manually created.
* The system does not connect to a real customer database.
* It does not use real-time company information.
* Confidence calculation is a simple lexical approach.
* External source verification is not currently implemented.

## Future Enhancements

* Integration with real customer/order databases
* Real-time order tracking APIs
* Real support-ticket platforms
* Advanced intent classification
* Improved confidence scoring
* Multi-agent customer support workflows
* Conversation memory with persistent storage
* Verified web-based knowledge retrieval
* PDF and document knowledge ingestion
* Analytics dashboard
* Deployment using cloud infrastructure

## Author

**Ezhilarasi P**

B.E. Computer Science and Engineering
Panimalar Engineering College
II Year

### Organization

InternsForge Skill India Pvt. Ltd.

### Project

AI Customer Support Agent with Generative AI & Agentic Workflow
