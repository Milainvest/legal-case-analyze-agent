s# Tech Context

## Core Technologies

*   **Programming Languages:** Python 3.11+, TypeScript (Ref: 5.1, 5.2)
*   **Frameworks/Libraries:**
    *   Backend: FastAPI, LangChain, SQLAlchemy, Alembic (Ref: 5.1)
    *   Frontend: Next.js (AppRouter), React Hooks, shadcn/ui, Tailwind CSS (Ref: 5.2)
*   **Databases:** PostgreSQL (Main), Redis (Cache), Pinecone (Vector DB - Prod), FAISS (Vector DB - Dev) (Ref: 5.1)
*   **AI Services:** OpenAI API (Ref: 5.1)
*   **Cloud Services:** AWS/GCP (Target Platform), Vercel (Potential Frontend Hosting - inferred from Next.js usage) (Ref: 5.3)
*   **Messaging:** RabbitMQ (Ref: 5.1)

## Development Environment

*   **Setup Instructions:** [Details TBD - likely involves Poetry, Node.js/npm/pnpm, Docker Compose]
*   **Key Tools:**
    *   Backend: Poetry, Docker Compose, pre-commit, mypy, pyright, black, isort, flake8, pylint, pytest (Ref: 5.1)
    *   Frontend: npm/pnpm/yarn (inferred), Vite, ESLint, Prettier, Jest, React Testing Library (Ref: 5.2)
    *   Infra: Docker, Terraform, GitHub Actions (Ref: 5.3)
*   **Environment Variables:** Required for API keys (e.g., OpenAI), database connections, cloud services. Specifics TBD. (Inferred)

## Technical Constraints

*   LLM limitations (hallucinations, knowledge cutoffs). (Ref: 7.2)
*   Potential instability of web scraping targets. (Ref: 7.2)
*   API call limits (e.g., OpenAI). (Ref: 7.2)
*   Resource usage limits (Cloud/Infra). (Ref: 7.2)
*   Performance targets (Report generation < 30s new / < 5s cached, Page load < 2s, Chat response < 3s). (Ref: 4.1)
*   Legal constraints regarding copyright and scraping. (Ref: 7.1)
*   Privacy regulations (GDPR/CCPA). (Ref: 7.1)

## Key Dependencies

*   External Case Law Sources (for scraping)
*   OpenAI API
*   Cloud Platform Services (AWS/GCP)
*   Vector Database (Pinecone/FAISS)

*(This file details the 'what' and 'how' of the technology stack and development setup, based on docs/requirment_definition.md Section 5, 4, and 7.)*
