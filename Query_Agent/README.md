# LLM Math Agent with LangGraph

This project builds an AI agent using LangGraph that can handle both general and math queries.

## Features
- Custom math functions: plus, subtract, multiply, divide
- General queries answered by LLM (OpenAI / Ollama / Gemini)
- Dynamic routing using LangGraph

## How it Works
1. User asks a question
2. Router detects if it's math-related
3. If math: calls relevant tool
4. If not: sends to LLM

## Requirements
- Python
- LangGraph
- OpenAI API or local LLM (Ollama)