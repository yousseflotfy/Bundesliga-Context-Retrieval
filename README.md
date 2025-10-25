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

