# Bundesliga-Context-Retrieval

## Overview

This project implements an intelligent information retrieval pipeline designed for a hypothetical chatbot that answers user questions about **football clubs and coaches in Germany’s 1. Bundesliga**.
The system integrates **Wikidata** and **Wikipedia** to retrieve, process, and structure up-to-date information about Bundesliga clubs and their current coaches. The retrieved data is formatted into a **contextualized prompt** suitable for large language models (LLMs), enabling accurate and conversational responses to user queries such as *“Who is coaching Munich?”* or *“Who trains the team from Dortmund?”*.

---

## Project Objective

The goal of this project is to automate the process of collecting and structuring football-related information into a consistent prompt format that an LLM can understand and respond to. It demonstrates a modular design combining **entity recognition**, **semantic retrieval**, and **prompt engineering** to bridge knowledge graphs and conversational AI.

---

## System Functionality

The system follows a clear and logical flow:

1. **City and Club Mapping**
   The system queries **Wikidata** to identify all German cities hosting clubs that play in the **Bundesliga 1**, creating a structured mapping between cities, club names, and their corresponding Wikidata identifiers.

2. **City Extraction from User Queries**
   When a user submits a question (e.g., “Who trains the team from Leipzig?”), the system extracts the **city name** and retrieves the corresponding **club** from the predefined mapping.

3. **Coach Identification**
   Using the club name, the system queries **Wikidata** to determine the club’s **current coach**.

4. **Coach Information Retrieval**
   The coach’s **Wikipedia introduction** is fetched through the **Wikipedia API** to provide additional contextual information for the LLM.

5. **Prompt Formatting for LLM**
   The final step combines the extracted entities (city, club, coach, and biography) into a structured **system prompt** using a YAML-based prompt template. This ensures consistency, clarity, and effective context retrieval for the LLM to generate precise answers.

---

## Core Components

* **Wikidata Querying** – Retrieves structured data on Bundesliga clubs and their relationships.
* **Wikipedia Integration** – Provides descriptive background text for coaches.
* **Entity Extraction** – Identifies city entities from free-text user questions.
* **Prompt Engineering** – Converts factual data into a coherent and context-rich prompt for language model consumption.
* **LangChain Integration** – Uses `ChatPromptTemplate` for prompt instantiation and variable substitution.

---

## Key Features

* Robust information retrieval from open knowledge sources (Wikidata & Wikipedia)
* Modular design for easy adaptation to other sports or leagues
* Automatic handling of invalid or unrecognized city inputs
* YAML-based prompt management for transparency and maintainability
* Seamless integration with conversational LLM frameworks

---

## Example Use Case

A user asks:

> “Who is coaching in Munich?”

The system will:

1. Extract **Munich** as the city.
2. Retrieve **FC Bayern Munich** as the associated club.
3. Query **Wikidata** to identify the club’s current coach.
4. Fetch the coach’s Wikipedia introduction.
5. Format and deliver a structured prompt to the LLM for generating the response.

---

## Installation and Execution

1. **Clone the repository**

2. **Create and activate a virtual environment**

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Run the script**

   ```bash
   python bundesliga_chatbot_retriever.py
   ```

---

## Extra Information

**1. Advantages and disadvantages of using additional information**
Using additional information ensures the chatbot gives accurate, up-to-date, and context-aware answers instead of relying on the LLM’s general knowledge. It builds trust and relevance for domain-specific questions. However, it adds complexity — requiring retrieval pipelines, external queries, and handling possible data inconsistencies.


**2. Advantages and disadvantages of querying on every user question**
Querying every time guarantees the chatbot always uses the latest data, which is important in dynamic domains like football. But it also increases latency and dependency on external APIs, making the system slower and more prone to network errors. In this example to reduce latency the city/club qeuery runs once at the beginning.

**3. If coach information were only available via PDF**
The system would need a preprocessing step to extract and structure text from the PDFs, for example using OCR or NLP-based parsing. Instead of live queries, the chatbot would rely on this local, preprocessed dataset. This adds one-time setup effort but improves speed and control over data consistency.


**4. Potential for agents in this process**
Yes, agents could be very useful here. For example, one agent could handle data retrieval from Wikidata, another could summarize Wikipedia content, and a third could format the final prompt. This modular setup improves scalability, maintainability, and error isolation.


**5. Benefit of having a domain-specific data model**
A structured data model helps represent the relationships between cities, clubs, and coaches clearly. It allows the system to reason over this knowledge rather than just retrieve text. That leads to cleaner queries, easier updates, and more reliable answers from the chatbot.
