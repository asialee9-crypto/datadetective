import { useMemo, useState } from "react";

import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
} from "recharts";

function DataCharts({ data, columns, dataTypes }) {
  const numericColumns = useMemo(() => {
    return columns.filter((column) => {
      const type = dataTypes[column] || "";

      return (
        type.includes("int") ||
        type.includes("float")
      );
    });
  }, [columns, dataTypes]);

  const categoricalColumns = useMemo(() => {
    return columns.filter(
      (column) => !numericColumns.includes(column)
    );
  }, [columns, numericColumns]);

  const [xColumn, setXColumn] = useState("");
  const [yColumn, setYColumn] = useState("");
  const [categoryColumn, setCategoryColumn] = useState("");
  const [valueColumn, setValueColumn] = useState("");

  const selectedX = numericColumns.includes(xColumn)
    ? xColumn
    : numericColumns[0];

  const selectedY = numericColumns.includes(yColumn)
    ? yColumn
    : numericColumns[1] || numericColumns[0];

  const selectedCategory = categoricalColumns.includes(
    categoryColumn
  )
    ? categoryColumn
    : categoricalColumns[0];

  const selectedValue = numericColumns.includes(valueColumn)
    ? valueColumn
    : numericColumns[0];

  const scatterData = useMemo(() => {
    if (!selectedX || !selectedY) return [];

    return data
      .filter(
        (row) =>
          typeof row[selectedX] === "number" &&
          Number.isFinite(row[selectedX]) &&
          typeof row[selectedY] === "number" &&
          Number.isFinite(row[selectedY])
      )
      .map((row) => ({
        x: row[selectedX],
        y: row[selectedY],
      }));
  }, [data, selectedX, selectedY]);

  const barData = useMemo(() => {
    if (!selectedCategory || !selectedValue) return [];

    const groups = {};

    data.forEach((row) => {
      const category = row[selectedCategory];
      const value = row[selectedValue];

      if (
        category == null ||
        typeof value !== "number" ||
        !Number.isFinite(value)
      ) {
        return;
      }

      const key = String(category);

      if (!groups[key]) {
        groups[key] = {
          name: key,
          total: 0,
          count: 0,
        };
      }

      groups[key].total += value;
      groups[key].count += 1;
    });

    return Object.values(groups)
      .map((group) => ({
        name: group.name,
        average: group.total / group.count,
      }))
      .slice(0, 20);
  }, [data, selectedCategory, selectedValue]);

  const histogramData = useMemo(() => {
    if (!selectedValue) return [];

    const values = data
      .map((row) => row[selectedValue])
      .filter(
        (value) =>
          typeof value === "number" &&
          Number.isFinite(value)
      );

    if (values.length === 0) return [];

    const min = Math.min(...values);
    const max = Math.max(...values);

    if (min === max) {
      return [
        {
          range: String(min),
          count: values.length,
        },
      ];
    }

    const binCount = 10;
    const binWidth = (max - min) / binCount;

    const bins = Array.from(
      { length: binCount },
      (_, index) => ({
        range: `${(min + index * binWidth).toFixed(1)}–${(
          min + (index + 1) * binWidth
        ).toFixed(1)}`,
        count: 0,
      })
    );

    values.forEach((value) => {
      const index = Math.min(
        Math.floor((value - min) / binWidth),
        binCount - 1
      );

      bins[index].count += 1;
    });

    return bins;
  }, [data, selectedValue]);

  if (!data || data.length === 0) {
    return <p>No visualization data available.</p>;
  }

  if (numericColumns.length === 0) {
    return (
      <p>
        This dataset does not contain numerical columns
        suitable for these charts.
      </p>
    );
  }

  return (
    <div className="charts-container">

      <div className="chart-card">
        <h3>Relationship Explorer</h3>
        <p>Explore relationships between numerical variables.</p>

        <div className="chart-controls">
          <label>
            X Axis
            <select
              value={selectedX}
              onChange={(event) =>
                setXColumn(event.target.value)
              }
            >
              {numericColumns.map((column) => (
                <option key={column} value={column}>
                  {column}
                </option>
              ))}
            </select>
          </label>

          <label>
            Y Axis
            <select
              value={selectedY}
              onChange={(event) =>
                setYColumn(event.target.value)
              }
            >
              {numericColumns.map((column) => (
                <option key={column} value={column}>
                  {column}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={320}>
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
              <CartesianGrid stroke="#30334a" />

              <XAxis
                type="number"
                dataKey="x"
                name={selectedX}
                stroke="#a5a8bf"
                domain={["auto", "auto"]}
              />

              <YAxis
                type="number"
                dataKey="y"
                name={selectedY}
                stroke="#a5a8bf"
                domain={["auto", "auto"]}
              />

              <Tooltip cursor={{ strokeDasharray: "3 3" }} />

              <Scatter
                name="Data Points"
                data={scatterData}
                fill="#a78bfa"
              />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {categoricalColumns.length > 0 && (
        <div className="chart-card">
          <h3>Category Comparison</h3>
          <p>Compare average values across categories.</p>

          <div className="chart-controls">
            <label>
              Category
              <select
                value={selectedCategory}
                onChange={(event) =>
                  setCategoryColumn(event.target.value)
                }
              >
                {categoricalColumns.map((column) => (
                  <option key={column} value={column}>
                    {column}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Numerical Value
              <select
                value={selectedValue}
                onChange={(event) =>
                  setValueColumn(event.target.value)
                }
              >
                {numericColumns.map((column) => (
                  <option key={column} value={column}>
                    {column}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="chart-wrapper">
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={barData}>
                <CartesianGrid stroke="#30334a" />

                <XAxis dataKey="name" stroke="#a5a8bf" />

                <YAxis stroke="#a5a8bf" />

                <Tooltip />

                <Bar
                  dataKey="average"
                  fill="#8b5cf6"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      <div className="chart-card">
        <h3>Distribution Explorer</h3>
        <p>See how values are distributed across your dataset.</p>

        <div className="chart-controls">
          <label>
            Numerical Column
            <select
              value={selectedValue}
              onChange={(event) =>
                setValueColumn(event.target.value)
              }
            >
              {numericColumns.map((column) => (
                <option key={column} value={column}>
                  {column}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={histogramData}>
              <CartesianGrid stroke="#30334a" />

              <XAxis
                dataKey="range"
                stroke="#a5a8bf"
                angle={-30}
                textAnchor="end"
                height={80}
              />

              <YAxis
                stroke="#a5a8bf"
                allowDecimals={false}
              />

              <Tooltip />

              <Bar
                dataKey="count"
                fill="#c4b5fd"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}

export default DataCharts;