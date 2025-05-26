import React, { useEffect, useState } from "react";
import { GenericAPI } from "../services/api";

const api = new GenericAPI("simulations");

const SimulationsPage: React.FC = () => {
  const [data, setData] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.get()
      .then(res => {
        console.log("✅ Response:", res.data);
        setData(res.data);
      })
      .catch(err => {
        const errorMessage = err.response?.data || err.message;
        console.error("❌ API Error:", errorMessage);
        setError(JSON.stringify(errorMessage));
      });
  }, []);

  return (
    <div className="p-4">
      <h2>Simulations</h2>
      {error ? (
        <p style={{ color: "red" }}>Error: {error}</p>
      ) : (
        <ul>
          {data.map((sim, index) => (
            <li key={index}>{JSON.stringify(sim)}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SimulationsPage;
