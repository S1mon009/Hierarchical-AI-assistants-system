# 🧠 FastAPI Backend — Documentation

Welcome to the documentation for the **FastAPI backend** project.  
This backend provides a modular, modern architecture designed for scalability, security, and maintainability.  
It integrates **PostgreSQL**, **ChromaDB**, **Redis**, and **LangChain**-based AI assistants.

---

## 🚀 Overview

The backend is built using **FastAPI**, a high-performance web framework for Python.  
It exposes RESTful endpoints for user registration, authentication, and AI-related tasks,  
following a clear separation between schemas, routes, and services.

### Key Technologies

- **FastAPI** — main web framework
- **Pydantic v2** — data validation and schema definition
- **PostgreSQL** — main relational database
- **Redis** — caching and session management
- **ChromaDB** — vector database for storing embeddings
- **LangChain + Hugging Face** — AI agent orchestration
- **Celery** — task queue for background processing
- **Docker** — containerized development environment

---

## 🧩 Project Structure

```bash
src/
├── app.py                 # FastAPI application entry point
├── config/                # Environment configuration and settings
├── routes/                # API route definitions (auth, assistant, etc.)
├── schemas/               # Pydantic models for request/response validation
```
