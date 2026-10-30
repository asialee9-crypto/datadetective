# DataDetective

DataDetective turns a CSV file into an interactive data investigation. It profiles the dataset, visualizes important patterns, uses NVIDIA Nemotron through Nebius Token Factory to suggest testable hypotheses, runs statistical tests, and generates a plain-language investigation report.

## Features

- CSV upload and automatic data profiling
- Interactive charts and dataset preview
- AI-generated hypotheses
- Pearson correlation, chi-square, and Welch's t-test investigations
- AI-written evidence report grounded in the calculated statistics

## Tech stack

- React, Vite, Recharts
- FastAPI, pandas, SciPy, scikit-learn
- NVIDIA Nemotron via Nebius Token Factory

## Run locally

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

Fill in the three `NEBIUS_*` values in `backend/.env`. Never commit that file.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://127.0.0.1:8000` for local development.

## Deploy on Render

This repository includes `render.yaml` for a backend web service and a frontend static site.

1. Push the repository to GitHub.
2. In Render, choose **New > Blueprint** and connect the repository.
3. Supply `NEBIUS_API_KEY`, `NEBIUS_BASE_URL`, and `NEBIUS_MODEL` when prompted.
4. After the services are created, copy the backend URL into the frontend's `VITE_API_URL` environment variable (no trailing slash).
5. Copy the frontend URL into the backend's `CORS_ORIGINS` environment variable (no trailing slash).
6. Redeploy both services, then upload a sample CSV and complete one AI investigation.

Free hosting can sleep after inactivity, so the first request may be slow. Uploaded CSV data is processed in memory and is not intended to persist between requests or deployments.

## Security

API keys belong only in the backend environment. The repository ignores `.env`, virtual environments, dependency folders, generated builds, caches, and logs. If a key was ever committed or shared publicly, revoke and replace it immediately.

## License

[MIT](LICENSE)
