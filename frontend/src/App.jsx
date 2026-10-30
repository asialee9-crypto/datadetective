
import InvestigationReport from "./components/InvestigationReport";
import { useState } from "react";
import {
  Search,
  Upload,
  Database,
  BrainCircuit,
  BarChart3,
  FlaskConical,
  CheckCircle,
  AlertCircle,
  LoaderCircle,
} from "lucide-react";

import DataCharts from "./components/DataCharts";
import "./App.css";

const API_URL = String(
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
)
  .trim()
  .replace(/^VITE_API_URL\s*=\s*/i, "")
  .replace(/^['"]|['"]$/g, "")
  .replace(/\/$/, "");

function App() {
  // Dataset state
  const [file, setFile] = useState(null);
  const [dataset, setDataset] = useState(null);

  // AI hypotheses
  const [hypotheses, setHypotheses] = useState([]);

  // Statistical investigation
  const [investigation, setInvestigation] = useState(null);
  const [investigationReport, setInvestigationReport] = useState(null);

  // Loading and error states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");

  // -----------------------------------------
  // HELPER: Handle API errors
  // -----------------------------------------

  async function checkResponse(response) {
    if (!response.ok) {
      let message = "Something went wrong.";

      try {
        const data = await response.json();
        message =
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail);
      } catch {
        message = `Request failed: ${response.status}`;
      }

      throw new Error(message);
    }

    return response.json();
  }

  // -----------------------------------------
  // FEATURE 1: Upload CSV
  // -----------------------------------------

  async function uploadDataset(selectedFile) {
    if (!selectedFile) return;

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Please upload a CSV file.");
      return;
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setError("The maximum file size is 5 MB.");
      return;
    }

    setLoading(true);
    setError("");
    setStatus("Analyzing your dataset...");

    setFile(null);
    setDataset(null);
    setHypotheses([]);
    setInvestigation(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await checkResponse(response);

      setFile(selectedFile);
      setDataset(data);
      setStatus("Dataset uploaded successfully!");
    } catch (err) {
      setError(err.message);
      setStatus("");
    } finally {
      setLoading(false);
    }
  }

  // -----------------------------------------
  // FEATURE 2: Generate AI hypotheses
  // -----------------------------------------

  async function generateHypotheses() {
    if (!file) return;

    setLoading(true);
    setError("");
    setStatus("NVIDIA Nemotron is generating hypotheses...");
    setHypotheses([]);
    setInvestigation(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_URL}/generate-hypotheses`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await checkResponse(response);

      setHypotheses(data.hypotheses || []);
      setStatus("AI hypothesis generation complete!");
    } catch (err) {
      setError(err.message);
      setStatus("");
    } finally {
      setLoading(false);
    }
  }

  // -----------------------------------------
  // FEATURE 3: Investigate a hypothesis
  // -----------------------------------------

  async function investigateHypothesis(hypothesis) {
    if (!file) return;

    setLoading(true);
    setError("");
    setInvestigation(null);

    setStatus("Running statistical investigation...");

    try {
      const formData = new FormData();

      formData.append("file", file);
      formData.append(
        "hypothesis",
        hypothesis.hypothesis
      );

      formData.append(
        "column1",
        hypothesis.columns[0]
      );

      formData.append(
        "column2",
        hypothesis.columns[1]
      );

      formData.append(
        "recommended_test",
        hypothesis.recommended_test
      );

      const response = await fetch(
        `${API_URL}/investigate`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await checkResponse(response);

      setInvestigation(data);
setInvestigationReport(null);

setStatus("Generating AI investigation report...");

const reportResponse = await fetch(
  `${API_URL}/investigation/report`,
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      hypothesis: data.hypothesis,
      statistical_results: data.statistical_results,
    }),
  }
);

const reportData = await checkResponse(reportResponse);

setInvestigationReport(reportData);

setStatus("Investigation complete!");
    } catch (err) {
      setError(err.message);
      setStatus("");
    } finally {
      setLoading(false);
    }
  }

  // -----------------------------------------
  // Calculate missing values
  // -----------------------------------------

  const missingValues = dataset
    ? Object.values(dataset.missing_values || {}).reduce(
        (total, count) => total + count,
        0
      )
    : 0;

  // -----------------------------------------
  // Dashboard UI
  // -----------------------------------------

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">
        <div className="logo">
          <Search size={26} />
          <span>DataDetective</span>
        </div>

        <div className="sidebar-section">
          <p className="sidebar-label">WORKSPACE</p>

          <div className="nav-item active">
            <BarChart3 size={18} />
            Dashboard
          </div>

        </div>

        <div className="sidebar-bottom">
          <p>Powered by</p>
          <strong>NVIDIA Nemotron</strong>
          <span>via Nebius Token Factory</span>
        </div>
      </aside>

      {/* MAIN CONTENT */}

      <main className="main">

        <header className="header">
          <div>
            <h1>DataDetective</h1>
            <p>
              Turn raw data into evidence-backed insights.
            </p>
          </div>

          <div className="ai-badge">
            <BrainCircuit size={17} />
            AI-Powered Analytics
          </div>
        </header>

        {/* UPLOAD SECTION */}

        <section className="card upload-section">
          <div className="section-heading">
            <Upload size={22} />

            <div>
              <h2>Upload Your Dataset</h2>
              <p>
                Start an investigation by uploading a CSV file.
              </p>
            </div>
          </div>

          <label
            className="upload-box"
            onDragOver={(event) => event.preventDefault()}
            onDrop={(event) => {
              event.preventDefault();

              if (!loading) {
                uploadDataset(event.dataTransfer.files[0]);
              }
            }}
          >
            <Upload size={36} />

            <h3>
              {file ? file.name : "Choose a CSV dataset"}
            </h3>

            <p>
              Drag and drop a file here or click to browse.
            </p>

            <span>CSV files only · Maximum 5 MB</span>

            <input
              type="file"
              accept=".csv"
              disabled={loading}
              onChange={(event) => {
                uploadDataset(event.target.files[0]);
                event.target.value = "";
              }}
            />
          </label>
        </section>

        {/* STATUS MESSAGES */}

        {loading && (
          <div className="status loading">
            <LoaderCircle
              size={18}
              className="spinner"
            />
            {status}
          </div>
        )}

        {error && (
          <div className="status error">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        {!loading && status && !error && (
          <div className="status success">
            <CheckCircle size={18} />
            {status}
          </div>
        )}

        {/* DATASET OVERVIEW */}

        {dataset && (
          <section className="dashboard-section">

            <div className="section-title">
              <Database size={22} />
              <h2>Dataset Overview</h2>
            </div>

            <div className="stats-grid">

              <div className="stat-card">
                <p>Total Rows</p>
                <h2>{dataset.rows.toLocaleString()}</h2>
              </div>

              <div className="stat-card">
                <p>Total Columns</p>
                <h2>{dataset.columns}</h2>
              </div>

              <div className="stat-card">
                <p>Missing Values</p>
                <h2>{missingValues}</h2>
              </div>

              <div className="stat-card">
                <p>Duplicate Rows</p>
                <h2>
                  {dataset.profile?.duplicate_rows ?? 0}
                </h2>
              </div>

            </div>

            {/* COLUMN INFORMATION */}

            <div className="card">
              <h3>Column Information</h3>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Column</th>
                      <th>Data Type</th>
                      <th>Missing Values</th>
                    </tr>
                  </thead>

                  <tbody>
                    {dataset.column_names.map((column) => (
                      <tr key={column}>
                        <td>{column}</td>

                        <td>
                          {dataset.data_types[column]}
                        </td>

                        <td>
                          {dataset.missing_values[column]}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* DATA PREVIEW */}

            <div className="card">
              <h3>Dataset Preview</h3>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      {dataset.column_names.map((column) => (
                        <th key={column}>{column}</th>
                      ))}
                    </tr>
                  </thead>

                  <tbody>
                    {(dataset.preview || []).map((row, index) => (
                      <tr key={index}>
                        {dataset.column_names.map((column) => (
                          <td key={column}>
                            {row[column] == null
                              ? "—"
                              : String(row[column])}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            {/* DATA VISUALIZATIONS */}

{dataset?.chart_data?.length > 0 && (
  <div className="visualization-section">

    <div className="section-title">
      <BarChart3 size={22} />
      <h2>Interactive Data Visualizations</h2>
    </div>

    <DataCharts
      data={dataset.chart_data}
      columns={dataset.column_names}
      dataTypes={dataset.data_types}
    />

  </div>
)}
                    

            {/* AI HYPOTHESIS GENERATION */}

            <div className="card ai-section">
              <div className="section-heading">
                <BrainCircuit size={25} />

                <div>
                  <h2>AI Hypothesis Generator</h2>

                  <p>
                    Let NVIDIA Nemotron discover
                    relationships worth investigating.
                  </p>
                </div>
              </div>

              <button
                className="primary-button"
                onClick={generateHypotheses}
                disabled={loading}
              >
                <BrainCircuit size={18} />
                Generate AI Hypotheses
              </button>
            </div>

          </section>
        )}

        {/* HYPOTHESIS CARDS */}

        {hypotheses.length > 0 && (
          <section className="dashboard-section">

            <div className="section-title">
              <FlaskConical size={22} />
              <h2>Suggested Investigations</h2>
            </div>

            <div className="hypothesis-grid">

              {hypotheses.map((hypothesis) => (
                <div
                  className="card hypothesis-card"
                  key={hypothesis.id}
                >
                  <span className="hypothesis-label">
                    HYPOTHESIS {hypothesis.id}
                  </span>

                  <h3>{hypothesis.hypothesis}</h3>

                  <p>{hypothesis.explanation}</p>

                  <div className="test-badge">
                    {hypothesis.recommended_test.replaceAll(
                      "_",
                      " "
                    )}
                  </div>

                  <button
                    className="primary-button"
                    disabled={loading}
                    onClick={() =>
                      investigateHypothesis(hypothesis)
                    }
                  >
                    <Search size={17} />
                    Investigate
                  </button>
                </div>
              ))}

            </div>

          </section>
        )}

        {/* INVESTIGATION RESULTS */}

        {investigation && (
          <section className="dashboard-section">

            <div className="section-title">
              <BarChart3 size={22} />
              <h2>Investigation Results</h2>
            </div>

            <div className="card">

              <span className="hypothesis-label">
                EVIDENCE REPORT
              </span>

              <h3>{investigation.hypothesis}</h3>

              <div className="results-grid">

                {Object.entries(
                  investigation.statistical_results || {}
                )
                  .filter(
                    ([key, value]) =>
                      typeof value === "number"
                  )
                  .map(([key, value]) => (
                    <div className="result-stat" key={key}>
                      <p>{key.replaceAll("_", " ")}</p>

                      <h3>
                        {Number.isInteger(value)
                          ? value
                          : value.toPrecision(4)}
                      </h3>
                    </div>
                  ))}

              </div>

              <div className="interpretation">
                <div className="section-heading">
                  <BrainCircuit size={22} />

                  <h3>Nemotron's Interpretation</h3>
                </div>

                <p>{investigation.ai_interpretation}</p>
              </div>

              <div className="evidence-note">
                Statistical calculations performed with SciPy.
                AI interpretation generated by NVIDIA Nemotron
                through Nebius Token Factory.
              </div>

            </div>

          </section>
        )}
        {/* AI INVESTIGATION REPORT */}

{investigationReport && (
  <section className="dashboard-section">
    <InvestigationReport
      investigation={investigationReport}
    />
  </section>
)}

      </main>
    </div>
  );
}

export default App;
