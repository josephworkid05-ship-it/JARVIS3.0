# J.A.R.V.I.S. — Personal AI Assistant (Version 3.0 / Phase 3: Machine Learning Layer)

> *"Just A Rather Very Intelligent System"* — A modular, extensible, tool-empowered personal AI assistant inspired by Tony Stark's JARVIS from Iron Man.

Version 3.0 introduces a dedicated **Machine Learning Subsystem**, combining Generative AI / LLM reasoning with traditional, high-performance local Machine Learning (powered by `scikit-learn`, `pandas`, `NumPy`, and `joblib`).

---

## Key Features in Version 3.0 (Phase 3)

* **Dedicated Machine Learning Subsystem (`/ml`):**
  * **Unified MLManager Facade:** Seamless orchestration of `ModelRegistry`, `FeaturePipeline`, `TrainingPipeline`, `InferenceEngine`, and `EvaluationEngine`.
  * **9 Core ML Capabilities:**
    1. **Classification:** Logistic Regression, Random Forest, Gradient Boosting.
    2. **Regression:** Linear Regression, Ridge, Random Forest Regressor, Gradient Boosting Regressor.
    3. **Clustering:** Centroid-based K-Means, DBSCAN.
    4. **Anomaly Detection:** Unsupervised Isolation Forest, Local Outlier Factor.
    5. **Forecasting:** Autoregressive lag-feature time series forecasting with uncertainty intervals.
    6. **Recommendation:** Cosine-similarity collaborative and content ranking.
    7. **Text Classification:** TF-IDF feature extraction with Multinomial Naive Bayes / Logistic Regression.
    8. **Sentiment Analysis:** Text polarity classification.
    9. **Pattern Detection:** Pearson correlation heatmaps and IQR outlier boundary profiling.
  * **Leakage-Free Feature Pipeline:** Fits scalers, imputers, and one-hot encoders strictly on training splits.
  * **Model Versioning & Registry:** Organizes models under `ml/models_store/<model_name>/v1/`, `v2/`, `latest/` with immutable `metadata.json` audit logs.
  * **Data Privacy:** 100% local model training and inference. Zero third-party data leakage.
* **Hybrid AI Intent Router (`LLM + ML`):**
  * Categorizes tasks into `LLM`, `ML`, or `HYBRID`.
  * Guarantees strict numerical honesty: LLMs never fabricate ML predictions; numerical results come exclusively from verified model pipelines with explainability statements (predictive association, not causation).
* **Data Science Workspace & Automated Profiler:**
  * Automated 14-step inspection: row/column counts, data types, missing value percentages, duplicates, summary statistics, correlation analysis, outlier detection, candidate target identification, and task recommendations.
* **Interactive Stark ML Web Dashboard:**
  * Live model registry browser with version history and evaluation metrics.
  * Interactive dataset inspector and custom CSV file uploader.
  * 1-click autonomous model training console.
  * Live inference console with interactive feature inputs, confidence bars, and top feature importance graphs.
* **Learning Mode (MBA-Focused AI Tutoring):**
  * Interactive conceptual explanations of algorithms with intuition, hyperparameters, advantages, limitations, and MBA business use cases (Customer Churn, Sales Forecasting, Credit Risk, Marketing Segmentation, Fraud Detection, Customer Lifetime Value).
* **Future AI Extensibility Protocols:**
  * Clean interfaces for Computer Vision, Deep Learning (PyTorch/ONNX), Reinforcement Learning, Local LLMs (Ollama/llama.cpp), and Vector Databases (RAG).

## Project Architecture

```
F26069/
├── config/
│   ├── __init__.py
│   └── settings.py          # Centralized configuration & environment loader
├── core/
│   ├── __init__.py
│   ├── agent.py             # Autonomous agent loop, lifecycle & voice dispatch
│   ├── memory.py            # Sliding-window short-term conversation memory
│   ├── planner.py           # LLM reasoning engine (OpenAI, Gemini, Simulation)
│   ├── prompt.py            # System prompt, JARVIS personality, tool-use format
│   └── voice.py             # Asynchronous Windows SAPI speech synthesis engine
├── tools/
│   ├── __init__.py          # Default tool registry initializer
│   ├── base.py              # BaseTool interface & ToolResult types
│   ├── registry.py          # Dynamic tool discovery, validation & dispatch
│   ├── calculator.py        # Safe AST-based mathematical evaluator
│   ├── time_tool.py         # System time, date, and timezone tool
│   └── web_search.py        # DuckDuckGo web search & instant answers
├── web/
│   ├── app.py               # Flask REST API server & Web HUD backend
│   ├── templates/
│   │   └── index.html       # Holographic Stark Industries HUD layout
│   └── static/
│       ├── css/hud.css      # Sci-fi neon cyan glassmorphism & scanlines
│       └── js/hud.js        # Arc Reactor canvas, Web Speech & Audio synth
├── utils/
│   ├── __init__.py
│   ├── env_loader.py        # Zero-dependency .env parser & Windows SSL setup
│   └── logger.py            # Structured logging (console and logs/jarvis.log)
├── tests/
│   ├── test_jarvis.py       # Phase 1 unit test suite (30 tests passing)
│   └── test_voice_and_web.py # Phase 2 voice & web test suite (10 tests passing)
├── .env.example             # Configuration and API key template
├── .gitignore               # Excludes secrets, logs, and cache
├── main.py                  # Interactive terminal interface with Stark HUD
├── run.bat                  # 1-click Windows Terminal launcher
├── run_web.bat              # 1-click Windows Web HUD launcher
└── README.md                # Full documentation & roadmap
```


---

## Getting Started

### 1. Run Immediately (No Setup Required)

JARVIS runs immediately in **Offline Simulation Mode** without needing any API key:

```bash
# Using the Windows launcher:
run.bat

# Or using the Python launcher directly:
py main.py
```

### 2. Connect a Live LLM (Optional)

To enable live autonomous reasoning with an LLM provider:

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` and configure your preferred provider:

#### Option A: OpenAI (GPT-4o, GPT-4o-mini)
```env
OPENAI_API_KEY="sk-..."
OPENAI_MODEL="gpt-4o-mini"
```

#### Option B: Groq (Ultra-fast Llama 3)
```env
OPENAI_BASE_URL="https://api.groq.com/openai/v1"
OPENAI_MODEL="llama-3.1-70b-versatile"
OPENAI_API_KEY="gsk_..."
```

#### Option C: Local Ollama
```env
OPENAI_BASE_URL="http://localhost:11434/v1"
OPENAI_MODEL="llama3"
OPENAI_API_KEY="ollama"
```

#### Option D: Google Gemini
```env
GEMINI_API_KEY="AIza..."
GEMINI_MODEL="gemini-1.5-flash"
```

3. Rerun `py main.py` or `run.bat`. The system telemetry will confirm the active neural uplink.

---

## Interactive Terminal Commands

Inside the chat interface, you can type natural prompts or use slash commands:

| Command | Description |
| :--- | :--- |
| `/help` | Display command manual and usage tips |
| `/tools` | Inspect registered tools and parameter specifications |
| `/status` | View system diagnostics, active provider, and memory count |
| `/clear` | Clear active conversation memory |
| `/save [file]` | Save current conversation history to JSON (default: `data/conversation_history.json`) |
| `/load [file]` | Restore conversation history from JSON |
| `/exit` | Power down JARVIS and terminate session |

---

## Security & Safety

1. **No Hardcoded Secrets:** All credentials are loaded exclusively from `.env` or system environment variables.
2. **Safe Math Execution:** `calculator.py` parses expressions using Python's `ast` module. Arbitrary code execution, `eval()`, `exec()`, imports, and builtins are strictly rejected.
3. **Strict Decoupling:** Tools are executed through a validated `ToolRegistry` with schema checking and error isolation. Unhandled tool exceptions never crash the agent loop.

---

## Running Automated Tests

To run the full unit and integration test suite:

```bash
py tests/test_jarvis.py
```

All 30 automated tests validate safe math evaluation, chronometer queries, web search handling, LLM response parsing, memory trimming, persistence, tool registry schemas, slash commands, max reasoning steps enforcement, and the full end-to-end agent loop.

---

## Future Roadmap

The modular architecture of Version 0.1 is specifically structured for subsequent phases:

* **Phase 2: Voice Interface**
  * Speech-to-Text (Whisper / Vosk)
  * Text-to-Speech (Piper / Edge-TTS / ElevenLabs)
  * Wake word detection ("Jarvis")
* **Phase 3: Long-term Memory & Knowledge Base**
  * Vector database integration (ChromaDB / SQLite-VSS)
  * Semantic user profile and episodic memory retrieval
* **Phase 4: Web Browsing & Document Access**
  * Headless browser integration (Playwright)
  * File reading & document understanding (PDF, Markdown, Code)
* **Phase 5: Computer Control & Automation**
  * Desktop awareness (screen OCR and window management)
  * Controlled application launching and keyboard/mouse automation
* **Phase 6: Multi-Step Autonomous Planning**
  * Hierarchical planning engine with task decomposition and self-reflection
