# Databricks PS Smart Engagement Assistant

A full-stack prototype that analyzes Professional Services engagement data to surface actionable insights and automation opportunities.

## Features
- **Realistic Mock Data Generation**: Simulates Slack threads, Jira tickets, and meeting notes.
- **Advanced NLP Analysis**: Uses local Hugging Face models for topic extraction, sentiment analysis, and clustering.
- **Interactive Dashboard**: Built with Plotly Dash, featuring responsive design and accessibility support.
- **Automation Opportunity Detection**: Identifies repetitive patterns and suggests automations.

## Setup Instructions

### Prerequisites
- Python 3.10+

### Installation

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download NLP Models:**
    This step downloads the necessary Hugging Face models to your local machine.
    ```bash
    python download_models.py
    ```

4.  **Generate Mock Data:**
    Creates a realistic dataset in `data/engagement.db`.
    ```bash
    python generate_mock_data.py
    ```

5.  **Run the Dashboard:**
    ```bash
    python app.py
    ```

## Project Structure
- `src/data_gen`: Scripts for generating realistic mock data.
- `src/analysis`: NLP pipeline and analysis logic.
- `src/dashboard`: Dash application components and pages.
- `data`: Stores the SQLite database and raw data.
- `models`: Stores cached Hugging Face models.

## Databricks Deployment

To sync the notebooks in `databricks/` to your Databricks workspace:

1.  **Configure Databricks CLI**:
    ```bash
    databricks configure --token
    # Enter your host (e.g., https://adb-123456789.1.azuredatabricks.net) and token
    ```

2.  **Run Sync Script**:
    ```bash
    ./sync_to_databricks.sh
    ```
    This will upload the files to `/Workspace/Users/<your-email>/ps_engagement_assistant`.

## Accessibility
This dashboard is designed with accessibility in mind, featuring:
- High-contrast color palettes (IBM Carbon / Okabe-Ito).
- ARIA labels for interactive elements.
- Responsive layout for all device sizes.
