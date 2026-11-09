# Divar Auto Data

**A Python-based Data Engineering project for collecting, processing, and analyzing vehicle listings from Divar.**

Divar Auto Data is an ongoing Data Engineering project designed to build a structured and reliable data pipeline for vehicle listings published on [Divar](https://divar.ir).

The project aims to collect passenger-car listings, extract their details, preserve raw data, standardize records, and prepare structured datasets for downstream analytics.

The long-term target is to cover passenger-car listings across Greater Tehran and build a foundation for vehicle market and price trend analysis.

> **Project status:** Work in Progress

---

## Project Objectives

- Collect vehicle listings through Divar's web API endpoints.
- Extract detailed information about each vehicle.
- Store raw records without modifying the original data.
- Organize records using a partitioned storage structure.
- Prevent duplicate records through token-based upsert logic.
- Standardize inconsistent values and prepare processed datasets.
- Build a foundation for incremental ingestion and historical price tracking.

---

## Architecture

```text
                 Divar
                   |
                   v
           Search & Pagination
                   |
                   v
            Detail Extraction
                   |
                   v
             Raw Data Layer
          Partitioned CSV Storage
             + Token Index
                   |
                   v
          Transformation Layer
          - Number normalization
          - Price standardization
          - Mileage standardization
          - Production year parsing
                   |
                   v
          Data Quality Validation
                   |
                   v
          Processed Data Layer
             listings.csv
                   |
                   v
          Analytics & Data History
             (Planned)
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Pandas | Data processing and transformation |
| Requests | API communication |
| CSV | Raw and processed data storage |
| Pytest | Automated testing |
| Git & GitHub | Version control |

---

## Implemented Features

### 1. Data Ingestion

- Search vehicle listings through Divar API endpoints.
- Retrieve detailed information for individual listings.
- Handle API pagination.
- Collect listings across three manufacturer-origin categories:
  - Domestic
  - Assembly
  - Foreign

### 2. Raw Data Storage

Raw records are stored in a partitioned CSV structure based on vehicle origin, brand, model, and variant.

Example:

```text
data/
└── raw/
    └── listings/
        ├── domestic/
        │   └── Peugeot/
        │       └── 206/
        │           └── Type 5/
        │               └── data.csv
        ├── assembly/
        └── foreign/
        └── token_index.csv
```

The storage layer includes:

- Token-based record identification.
- Upsert mechanism to prevent duplicate records.
- Token index for locating existing records.
- Record movement when vehicle classification or partition paths change.

### 3. Data Transformation

The transformation layer currently supports:

- Persian and Arabic numeral normalization.
- Price standardization.
- Mileage standardization.
- Jalali and Gregorian production-year parsing.
- Selecting the appropriate production year based on vehicle origin.
- Initial price-status classification for suspicious values.

Raw data is preserved separately from processed data.

### 4. Processed Data Storage

Standardized records are consolidated into:

```text
data/processed/listings.csv
```

The processed storage module writes the output through a temporary file before replacing the destination file.

### 5. Testing

The project includes automated tests for:

- API search and detail extraction.
- Data transformation.
- Path construction.
- Partitioned storage.
- Token-based upsert behavior.
- Processed data storage.
- Pipeline integration.

Run the tests with:

```bash
python -m pytest -v
```

---

## Project Structure

```text
divar-auto-data/
│
├── config/
│   └── settings.py
│
├── scripts/
│   └── data_quality_audit.py
│
├── src/
│   └── divar_auto_data/
│       ├── extraction/
│       ├── ingestion/
│       ├── storage/
│       ├── transformation/
│       └── main.py
│
├── tests/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── requirements.txt
└── README.md
```

Generated datasets are stored locally and are excluded from version control.

---

## Getting Started

### Prerequisites

- Python 3.11
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Mahyar-AlamBeigi/divar-auto-data.git

cd divar-auto-data
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run tests

```bash
python -m pytest -v
```

### 5. Run the pipeline

```bash
python -m src.divar_auto_data.main
```

The pipeline connects to the configured Divar API endpoints, collects listings, saves raw data, applies transformations, and generates the processed dataset.

---

## Current Limitations

This project is still under development. The following areas require further implementation or validation:

- Complete geographic coverage of Greater Tehran has not yet been verified.
- Manufacturer-origin classification requires further validation.
- Data quality checks are still in their initial stage.
- Current collection settings are configured for testing rather than full-scale collection.
- Incremental ingestion and listing lifecycle tracking are not implemented yet.
- Historical price tracking is not implemented yet.
- PostgreSQL integration and automated scheduling are planned.

The current API city configuration and collection limits should not be interpreted as proof of complete market coverage.

---

## Roadmap

### Phase 1 — Data Processing
- [x] Initial data standardization
- [x] Processed CSV storage
- [ ] Independent data quality validation layer

### Phase 2 — Data Collection
- [x] Search and detail extraction
- [x] Initial multi-origin collection
- [ ] Validate geographic coverage
- [ ] Validate manufacturer-origin categories
- [ ] Expand and validate collection coverage

### Phase 3 — Incremental Ingestion
- [ ] Track first-seen and last-seen timestamps
- [ ] Detect new and updated listings
- [ ] Handle inactive and removed listings

### Phase 4 — Data Storage & History
- [ ] PostgreSQL integration
- [ ] Historical price tracking
- [ ] Database schema and indexing

### Phase 5 — Automation & Reliability
- [ ] Scheduled pipeline execution
- [ ] Retry and error handling
- [ ] Structured logging
- [ ] Pipeline monitoring

### Phase 6 — Analytics
- [ ] Market price analysis
- [ ] Price trend analysis
- [ ] Power BI dashboard

---

## Author

**Mahyar Alambeygi**

Computer Engineering Student | Aspiring Data Engineer

- GitHub: [@Mahyar-AlamBeigi](https://github.com/Mahyar-AlamBeigi)
- Project: [Divar Auto Data](https://github.com/Mahyar-AlamBeigi/divar-auto-data)

---

*Built as a practical Data Engineering project, with a focus on reliable data collection, processing, and storage.*