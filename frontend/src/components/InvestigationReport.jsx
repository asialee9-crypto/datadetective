import React from "react";

function InvestigationReport({ investigation }) {
  if (!investigation) {
    return null;
  }

  const { hypothesis, statistical_results, report } =
    investigation;

  return (
    <div className="investigation-report">

      <div className="report-header">
        <h2>🔎 Investigation Report</h2>
        <p>AI-powered statistical investigation</p>
      </div>

      <div className="report-card">
        <h3>Research Hypothesis</h3>
        <p>{hypothesis}</p>
      </div>

      <div className="report-card">
        <h3>Statistical Evidence</h3>

        <pre>
          {JSON.stringify(
            statistical_results,
            null,
            2
          )}
        </pre>
      </div>

      <div className="report-card">
        <h3>Executive Summary</h3>
        <p>{report.summary}</p>
      </div>

      <div className="report-card">
        <h3>Statistical Interpretation</h3>
        <p>{report.statistical_interpretation}</p>
      </div>

      <div className="report-card">
        <h3>Conclusion</h3>
        <p>{report.conclusion}</p>
      </div>

      <div className="report-card">
        <h3>Limitations</h3>

        <ul>
          {(report.limitations || []).map(
            (limitation, index) => (
              <li key={index}>
                {limitation}
              </li>
            )
          )}
        </ul>
      </div>

      <div className="report-card">
        <h3>Recommended Next Investigation</h3>
        <p>{report.next_investigation}</p>
      </div>

    </div>
  );
}

export default InvestigationReport;