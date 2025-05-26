import React, { useEffect, useState } from "react";
import { GenericAPI } from "../services/api";

const TestAPI: React.FC = () => {
  const [result, setResult] = useState<string>("Loading...");

  useEffect(() => {
    const api = new GenericAPI("simulations");

    api
      .get()
      .then((response) => {
        setResult(JSON.stringify(response.data, null, 2));
      })
      .catch((error) => {
        setResult(`Error: ${error.message}`);
      });
  }, []);

  return (
    <div>
      <h2>API Test</h2>
      <pre>{result}</pre>
    </div>
  );
};

export default TestAPI;
