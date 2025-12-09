# Retail Insights Assistant - Senior Architecture Presentation Plan

## Target Audience
- Senior AI/ML Architects
- Engineering Managers
- Technical Directors at Blend360

## Presentation Strategy
Show **depth of thinking**, not just implementation. Every slide should answer "WHY" not just "WHAT".

---

## Slide Structure (12-14 slides)

### Slide 1: Title
- Retail Insights Assistant
- GenAI Multi-Agent System for Enterprise Analytics
- Candidate Name | AI Architect Role | December 2024

### Slide 2: Executive Summary (The Hook)
**What we built | Why it matters | Key differentiators**
- Problem: Executives need instant insights without SQL
- Solution: 4-agent GenAI system with enterprise guardrails
- Impact: Natural language → Business insights in <5 seconds
- Scale-ready: Architecture designed for 100GB+ (demo runs on 128K rows)

### Slide 3: Problem Deep Dive
**Understanding the Business Challenge**
- Retail data complexity: 100s of dimensions, millions of transactions
- Current pain: SQL knowledge gap, delayed decisions, siloed insights
- User personas: Executive (summaries), Analyst (ad-hoc queries), Ops (real-time)
- Success metrics: Query accuracy, response latency, user adoption

### Slide 4: Solution Architecture Overview
**High-level system diagram with ALL components**
- User Interface Layer (ADK Web)
- Security Layer (NeMo Guardrails)
- Agent Orchestration Layer (Google ADK + Gemini)
- Data Processing Layer (PandasAI + OpenAI)
- Query Execution Layer (DuckDB → BigQuery path)
- Data Layer (CSV → Data Warehouse evolution)

### Slide 5: Multi-Agent Design (Core Innovation)
**Why 4 agents? What each does. How they communicate.**
```
Orchestrator Agent (Gemini 2.5 Pro)
├── Guardrails Check → NeMo + OpenAI (off-topic, injection prevention)
└── QA Pipeline (SequentialAgent)
    ├── Query Resolution Agent → PandasAI + GPT-4o (NL → SQL)
    ├── Data Extraction Agent → DuckDB (SQL execution)
    └── Response Validation Agent → Gemini (formatting + insights)
```
**Design Decisions:**
- Why SequentialAgent over ParallelAgent? Data dependency
- Why separate SQL generation from execution? Audit trail, retry logic
- Why Gemini for orchestration, OpenAI for SQL? Cost/capability trade-off

### Slide 6: Technology Selection Rationale
**Not just WHAT we used, but WHY we chose it over alternatives**

| Component | Chosen | Alternatives Considered | Decision Rationale |
|-----------|--------|------------------------|---------------------|
| Agent Framework | Google ADK | LangChain, CrewAI, AutoGen | Native Vertex AI integration, production-ready |
| Orchestration LLM | Gemini 2.5 Pro | GPT-4, Claude | Best reasoning, lower cost at scale |
| SQL Generation | PandasAI + OpenAI | LangChain SQL, Vanna.ai | Higher accuracy on complex queries |
| Query Engine | DuckDB | SQLite, Pandas | 10x faster OLAP, columnar storage |
| Guardrails | NVIDIA NeMo | Custom regex, Guardrails AI | Colang DSL, policy-as-code |

### Slide 7: Security & Guardrails Architecture
**Enterprise-grade input validation**
- Layer 1: Pattern matching (SQL injection, prompt injection)
- Layer 2: Topic classification (on-topic vs off-topic)
- Layer 3: LLM-based intent validation (NeMo + OpenAI)
- Blocked query examples: "DROP TABLE", "Write me an email", "What's the weather"
- Audit logging: Every query logged with classification result

### Slide 8: Query-Response Pipeline (Detailed Flow)
**Step-by-step with timing estimates**
```
User: "What are the top 5 selling categories?"
│
├─[1] Orchestrator receives query (10ms)
├─[2] Guardrails validation (200ms) → PASS
├─[3] Query Resolution Agent
│   └─ PandasAI generates SQL (1.2s)
│   └─ SQL: SELECT category, SUM(amount)... ORDER BY... LIMIT 5
├─[4] Data Extraction Agent
│   └─ DuckDB executes (50ms)
│   └─ Returns: [{category: "Set", total: 45M}, ...]
├─[5] Response Validation Agent (800ms)
│   └─ Formats table, adds insights
│
└─[6] Response to user (Total: 2.3s)
    "Set category leads with ₹45M (32% of total)..."
```

### Slide 9: Data Engineering Approach
**Analysis of 7 raw CSV files → Selection rationale**

| File | Rows | Decision | Technical Reason |
|------|------|----------|------------------|
| Amazon Sale Report | 128K | ✓ Selected | Clean schema, complete transactions |
| International sale Report | 37K | ✗ Skipped | Mixed schemas, date range mismatch |
| Sale Report (Inventory) | 9K | ✗ Skipped | No date column, different SKU format |
| May-2022.csv | 1.3K | ✗ Skipped | Zero SKU overlap |
| Others | <100 | ✗ Skipped | Not tabular data |

**Schema Design:**
- Column mapping for clean SQL: `ship-city` → `city`
- Data types: amounts as DECIMAL, dates parsed, B2B as boolean
- Null handling: Amount null = cancelled order (valid, not error)

### Slide 10: Scaling to 100GB+ (Critical Slide)
**This is what they want to see - architect-level thinking**

#### A. Data Ingestion & ETL
```
Raw Data (GCS) → Dataflow/PySpark → BigQuery
- Batch: Daily incremental loads via Airflow
- Streaming: Pub/Sub for real-time order events
- Quality: Great Expectations for validation
```

#### B. Storage Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    DATA PLATFORM                         │
├─────────────────────────────────────────────────────────┤
│  Landing Zone (GCS)    → Raw CSVs, JSONs               │
│  Staging (BigQuery)    → Validated, typed              │
│  Analytics (BigQuery)  → Aggregated, partitioned       │
│  Serving (Redis)       → Query cache, session state    │
└─────────────────────────────────────────────────────────┘
```

#### C. Query Optimization
- BigQuery partitioning by order_date (monthly)
- Clustering by category, state for common queries
- Materialized views for top-N aggregations
- RAG for schema: Embed table descriptions in vector DB

#### D. LLM Optimization at Scale
- Prompt caching: Identical questions hit Redis first
- Model routing: Simple queries → Gemini Flash, Complex → Pro
- Token budget: Max 4K tokens per query
- Fallback: If LLM fails, show cached similar query

### Slide 11: Observability & Monitoring
**Production-ready operations**

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| Query latency (p95) | Prometheus + Grafana | >5s |
| LLM token usage | Custom metrics | >$100/day |
| SQL accuracy | Human feedback loop | <90% |
| Error rate | Cloud Logging | >5% |
| Guardrail blocks | Dashboard | Anomaly detection |

**Tracing:**
- OpenTelemetry for end-to-end request tracing
- Each agent step logged with duration
- Failed queries stored for analysis

### Slide 12: Cost Analysis
**Demo vs Production estimates**

| Component | Demo (128K rows) | Production (100GB) |
|-----------|------------------|---------------------|
| DuckDB | $0 (in-memory) | → BigQuery: ~$50/month |
| Gemini 2.5 Pro | ~$0.01/query | ~$0.01/query |
| OpenAI GPT-4o | ~$0.02/query | ~$0.02/query (cached: $0) |
| Redis Cache | - | ~$30/month |
| GCS Storage | - | ~$20/month |
| **Total/month** | **~$5** | **~$200-500** |

**Cost Optimization Strategies:**
1. Cache repeated queries (60% hit rate expected)
2. Use Gemini Flash for simple classifications
3. Batch similar queries during low-traffic hours
4. Set token limits and query quotas per user

### Slide 13: Limitations & Future Roadmap
**Honest assessment + Vision**

**Current Limitations:**
- 3 months of data only (no YoY analysis)
- Single data source (Amazon India only)
- Schema hardcoded (won't adapt to changes)
- Session memory only (no cross-session context)

**Roadmap (Priority Order):**
1. **Q1**: Redis caching + BigQuery migration
2. **Q2**: RAG for dynamic schema discovery
3. **Q3**: Multi-source integration (add Shopify, Magento)
4. **Q4**: Streaming analytics (real-time dashboards)

### Slide 14: Summary & Demo
**Key Takeaways**

✓ **Multi-Agent Architecture**: 4 specialized agents with clear responsibilities
✓ **Production Security**: NeMo Guardrails block off-topic and malicious queries
✓ **Scale-Ready Design**: Clear path from DuckDB → BigQuery
✓ **Cost-Conscious**: Caching, model routing, token limits
✓ **Observable**: Metrics, tracing, alerting built-in

**Live Demo:**
- "What are the top 5 selling categories?"
- "Show sales by state"
- "What's the cancellation rate?"
- (Blocked) "Write me an email" → Guardrail response

---

## Design Guidelines for V2

### Color Palette (Professional, not generic)
- Primary: #0F4C75 (Deep Blue - trust, enterprise)
- Secondary: #3282B8 (Bright Blue - technology)
- Accent: #BBE1FA (Light Blue - highlights)
- Text Dark: #1B262C (Near Black)
- Text Light: #FFFFFF
- Success: #00C49A (Teal)
- Warning: #F39C12 (Orange)
- Error: #E74C3C (Red)

### Typography
- Titles: Arial Bold 28-32pt
- Subtitles: Arial 18-20pt
- Body: Arial 12-14pt
- Code: Courier New 10-11pt

### Visual Principles
1. **Architecture diagrams** - Use proper boxes, arrows, layers
2. **Tables for comparisons** - Technology choices, trade-offs
3. **Numbered lists for processes** - Step-by-step flows
4. **Metrics with numbers** - Not "fast" but "50ms"
5. **Color-coded status** - Green = selected, Red = rejected

### What Makes This Senior-Level
1. **Trade-off analysis** - Every choice has a "why not X"
2. **Numbers everywhere** - Latency, cost, rows, percentages
3. **Failure modes** - What happens when things break
4. **Evolution path** - Demo → Production → Enterprise
5. **Honest limitations** - Shows maturity, not ignorance
