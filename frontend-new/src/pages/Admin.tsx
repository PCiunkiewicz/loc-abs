import { useState } from "react";
import { GenericAPI } from "../services/api";

export default function AdminPage() {
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [confirming, setConfirming] = useState(false);

  const handleReset = () => {
    setResult(null);
    setError(null);
    new GenericAPI("admin/resetdb")
      .get()
      .then((res) => setResult(res.data))
      .catch((err) => setError(err.message));
  };

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-xl font-semibold">Admin Panel</h2>

      {!confirming && (
        <button
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          onClick={() => setConfirming(true)}
        >
          Reset DB
        </button>
      )}

      {confirming && (
        <div className="space-y-2">
          <p className="text-sm text-gray-700">
            This action cannot be undone. Are you sure you want to reset the database?
          </p>
          <div className="space-x-2">
            <button
              className="px-3 py-1 border rounded"
              onClick={() => setConfirming(false)}
            >
              Cancel
            </button>
            <button
              className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
              onClick={handleReset}
            >
              Confirm
            </button>
          </div>
        </div>
      )}

      {result && (
        <div className="p-2 bg-green-100 border border-green-400 rounded">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      {error && (
        <div className="p-2 bg-red-100 border border-red-400 rounded">
          <p>Error: {error}</p>
        </div>
      )}
    </div>
  );
}
