# 🧠 NarrativeIQ

## 1. Project Overview

**NarrativeIQ** is a web-based analytical platform designed to aggregate news articles from multiple sources and analyze narrative tone, sentiment patterns, and comparative framing across publishers.

Users can explore how different news outlets report on the same topic and gain insights into tone variations, narrative divergence, and polarization patterns.

Key features:

* Multi-source news aggregation
* Sentiment scoring using VADER
* Cross-source comparison
* Narrative deviation and polarization metrics
* Interactive visual analytics dashboard

> ⚠️ Note: NarrativeIQ highlights differences in reporting tone; it does **not** assess factual correctness.

### Problem Statement

Modern news consumption is fragmented. Readers often rely on a limited number of sources, making it difficult to:

* Compare reporting tone across outlets
* Identify sentiment differences
* Detect narrative framing divergence
* Understand polarization patterns

Manual comparison is time-consuming and subjective.

### Proposed Solution

NarrativeIQ addresses this problem by:

1. Aggregating news articles from multiple APIs (NewsAPI, GNews)
2. Applying automated sentiment analysis using VADER
3. Computing source-level and comparative metrics
4. Visualizing sentiment distributions and narrative deviations
5. Presenting structured analytical summaries via an interactive dashboard

The platform transforms unstructured news content into measurable analytical insights.

---

## 2. Getting Started

Follow these steps to set up and run **NarrativeIQ** on your local machine.

### Prerequisites

* Python 3.10+ installed
* pip (Python package manager)
* Git installed
* (Optional) virtual environment tool: `venv` or `virtualenv`

---

### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/AbdulHadi117/NarrativeIQ.git
cd NarrativeIQ
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv        # create virtual environment
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. **Install required packages**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root with your API keys and database URI:

```env
NEWS_API_KEY=your_newsapi_key
GNEWS_API_KEY=your_gnews_api_key
FLASK_APP=app
FLASK_ENV=development
```

> 🔑 Make sure your `.env` is in `.gitignore` to avoid committing API keys.

5. **Initialize the database**

```bash
flask shell
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     exit()
```

This will create the `news.db` SQLite database with the necessary tables.

---

### Running the Application

Start the Flask development server:

```bash
flask run
```

The app will be accessible at:

```
http://127.0.0.1:5000
```

* **Home Page:** Enter a topic to fetch articles.
* **Dashboard:** Visualizes sentiment metrics and bias analysis.
* **Articles Page:** Displays all collected articles.
* **About Page:** Project description and methodology.

## 3. System Architecture & Workflow

### High-Level Architecture

```
User Interface (Frontend)
            ↓
Flask Backend (Application Layer)
            ↓
News Aggregation Layer (NewsAPI, GNews)
            ↓
Analysis Engine (VADER Sentiment & Bias Metrics)
            ↓
Database Layer (SQLite)
            ↓
Visualization Rendering (Charts, Tables, Cards)
```

### Architecture Components

1. **Presentation Layer** – HTML/CSS/JS frontend, dashboard rendering
2. **Application Layer** – Flask routes, request orchestration
3. **Data Aggregation Layer** – Fetches and normalizes API data
4. **Analysis Layer** – Performs sentiment scoring and bias computation
5. **Persistence Layer** – Stores articles and metrics in SQLite

### Application Workflow

1. User enters a topic on the homepage.
2. Backend fetches articles from NewsAPI and GNews.
3. Articles are normalized and stored in the database.
4. VADER sentiment analysis is applied to each article.
5. Source-level metrics (average sentiment, article count) are computed.
6. Comparative metrics (bias index, polarization) are calculated.
7. Results are displayed in an interactive dashboard with charts and tables.

---

## 4. Core Modules

### 1. News Aggregation

**Purpose:** Retrieve and standardize news articles from multiple APIs.

Responsibilities:

* API authentication and query handling
* Data normalization
* Duplicate filtering
* Error handling

---

### 2. Sentiment Analysis

**Purpose:** Evaluate emotional tone of news articles.

Responsibilities:

* Combine title + description for analysis
* Compute sentiment score using VADER
* Assign categorical sentiment label (Positive / Neutral / Negative)

---

### 3. Narrative Comparison

**Purpose:** Compare reporting tone across sources.

Responsibilities:

* Aggregate source-level sentiment averages
* Compute deviation metrics (bias index)
* Compute polarization metrics (standard deviation)
* Prepare structured comparison datasets

---

### 4. Data Persistence

**Purpose:** Store articles and metrics in SQLite.

Responsibilities:

* Article storage with timestamps
* Topic tracking
* Metadata management
* Query optimization

---

### 5. Visualization

**Purpose:** Render analytical results into interactive dashboards.

Responsibilities:

* Chart.js charts for sentiment distribution
* Source comparison bar charts
* Summary cards for bias index, polarization, article count
* Searchable topic input and interactive dashboard

---

## 5. Technology Stack

### Backend

* Python
* Flask
* SQLAlchemy
* Requests

### Frontend

* HTML5 / CSS3
* JavaScript
* Chart.js

### Database

* SQLite

### External APIs

* NewsAPI
* GNews

### NLP Tools

* NLTK VADER Sentiment Analyzer

---

## 6. Database Design

### Articles Table

| Field           | Type         | Description                   |
| --------------- | ------------ | ----------------------------- |
| id              | Integer (PK) | Unique article ID             |
| title           | Text         | Article headline              |
| description     | Text         | Article summary               |
| source          | String       | News source name              |
| topic           | String       | User query topic              |
| sentiment_score | Float        | Computed sentiment value      |
| sentiment_label | String       | Positive / Neutral / Negative |
| published_at    | DateTime     | Original publish time         |
| created_at      | DateTime     | Record insertion time         |

---

## 7. Development Phases

### Phase 1: Project Setup

* Initialize Git repository
* Configure environment (.env)
* Setup Flask project structure
* Initialize database and SQLAlchemy
* Configure blueprints

### Phase 2: API Integration

* Integrate NewsAPI and GNews
* Normalize API responses
* Handle duplicates and errors

### Phase 3: Sentiment Engine

* Implement VADER sentiment scoring
* Assign sentiment labels
* Store enriched articles

### Phase 4: Comparative Metrics

* Compute source-level averages
* Compute bias index & polarization
* Prepare datasets for dashboard

### Phase 5: Dashboard Implementation

* Build frontend pages (home, dashboard, articles, about)
* Integrate charts and tables
* Interactive topic search and visualization

### Phase 6: Testing & Optimization

* Remove duplicate records
* Handle API limits and errors
* Improve database queries
* Refactor code for maintainability

---

## 8. Scope & Scalability

### Project Scope

* Multi-source news aggregation
* Sentiment scoring and labeling
* Source-level comparison and bias metrics
* Interactive dashboard with charts and tables
* Persistent storage for historical analysis

### Scalability Considerations

* API response caching
* Background task processing (Celery / RQ)
* Asynchronous API calls
* Database indexing and query optimization
* Modular service design for maintainability

---

## 9. Future Enhancements

* Transformer-based sentiment models (HuggingFace)
* Topic modeling and clustering
* Framing intensity detection
* Historical trend analysis over time
* Automated PDF report generation
* Deployment to cloud platforms (Heroku, AWS, GCP)