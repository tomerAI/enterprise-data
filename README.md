# Enterprise Data Manager

A sophisticated data management system combining graph-based structured data processing with embeddings-based unstructured data analysis for enterprise-scale operations.

## 🎯 Vision
Providing a unified solution for handling both structured and unstructured data through:
- Graph-based modeling for structured data relationships
- Vector embeddings for unstructured data understanding
- RESTful API for seamless data operations

## 🏗️ Architecture

### Core Components
- FastAPI Backend: RESTful API with async processing and multi-format data ingestion
- Vector Store: PostgreSQL with pgvector extension for embedding storage and similarity search
- Graph Database: Neo4j with APOC for relationship modeling and graph traversal
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
   - Graph element creation and relationship mapping

3. **Storage Layer**
   - Vector embeddings in pgvector
   - Graph relationships in Neo4j
   - Metadata in PostgreSQL

4. **Retrieval Layer**
   - Semantic similarity search
   - Graph-enhanced retrieval
   - Hybrid ranking system

## 📋 Current Status

### Implemented Features
- FastAPI endpoints for data operations and retrieval
- PostgreSQL + pgvector integration for embedding storage
- Neo4j graph database integration
- OpenAI embeddings generation
- Document deduplication system
- Basic graph schema and relationships
- Multi-format file processing pipeline
- DBT data transformation integration

### In Development
- Advanced entity extraction
- Relationship inference engine
- Knowledge graph enrichment
- Result reranking system
- Batch processing capabilities
- Caching implementation

## 🗺️ Roadmap

### Phase 1: Core Enhancement
- Document chunking and preprocessing
- Advanced entity recognition
- Relationship type expansion
- Query optimization

### Phase 2: Advanced Features
- Automated knowledge graph construction
- Context-aware retrieval
- Dynamic relationship weighting
- Multi-model embedding support

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
- **Databases**: PostgreSQL, pgvector, Neo4j
- **Processing**: DBT, LangChain, OpenAI
- **Infrastructure**: Docker, Docker Compose