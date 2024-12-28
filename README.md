# Enterprise Data Manager

A sophisticated data management system leveraging embeddings-based data analysis for enterprise-scale operations, enabling intelligent search and retrieval through vector representations.

## 🎯 Vision
Providing a unified solution for handling structured and unstructured data through:
- Vector embeddings for data understanding and representation
- Semantic similarity search capabilities
- RESTful API for seamless data operations

## 🏗️ Architecture

### Core Components
- FastAPI Backend: RESTful API with async processing and multi-format data ingestion
- Vector Store: PostgreSQL with pgvector extension for embedding storage and similarity search
- Embedding Generation: OpenAI API integration for high-quality embeddings
- Data Processing: DBT for transformation pipelines and data modeling
- Infrastructure: Containerized deployment with Docker and Docker Compose

### Data Flow
1. **Data Ingestion Layer**
   - Multi-format file upload support (CSV, JSON, etc.)
   - Temporary file management
   - Format-specific validation

2. **Processing Layer**
   - Document processing and metadata extraction
   - Embedding generation and deduplication
   - Vector representation creation

3. **Storage Layer**
   - Vector embeddings in pgvector
   - Metadata in PostgreSQL
   - Document references and relationships

4. **Retrieval Layer**
   - Semantic similarity search
   - Context-aware retrieval
   - Hybrid ranking system

## 📋 Current Status

### Implemented Features
- FastAPI endpoints for data operations and retrieval
- PostgreSQL + pgvector integration for embedding storage
- OpenAI embeddings generation
- Document deduplication system
- Multi-format file processing pipeline
- DBT data transformation integration

### In Development
- Advanced entity extraction
- Semantic search optimization
- Result reranking system
- Batch processing capabilities
- Caching implementation

## 🗺️ Roadmap

### Phase 1: Core Enhancement
- Document chunking and preprocessing
- Advanced metadata extraction
- Query optimization
- Vector indexing improvements

### Phase 2: Advanced Features
- Multi-model embedding support
- Context-aware retrieval
- Dynamic similarity scoring
- Advanced document clustering

### Phase 3: Scale & Performance
- Distributed processing
- Real-time updates
- Advanced caching strategies
- Performance monitoring

## 🚀 Quick Start

### Requirements
- Docker and Docker Compose
- OpenAI API key
- Python 3.9+

### Setup
1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Run: `docker-compose up -d`

## 🛠️ Tech Stack
- **Backend**: FastAPI, Python 3.9+
- **Databases**: PostgreSQL, pgvector
- **Processing**: DBT, LangChain, OpenAI
- **Infrastructure**: Docker, Docker Compose