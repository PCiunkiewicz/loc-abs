import { useEffect, useState } from "react";
import { GenericAPI } from "../services/api";

export default function ImporterPage() {
  const [configs, setConfigs] = useState<string[]>([]);
  const [configPath, setConfigPath] = useState<string>("");
  const [existOk, setExistOk] = useState<boolean>(true);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const api = new GenericAPI("importer/configs");
    api.get()
      .then((res) => setConfigs(res.data))
      .catch((err) => {
        setConfigs([]);
        setError(err.message);
      });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const api = new GenericAPI("importer/import");
    try {
      const res = await api.post({ config_path: configPath, exist_ok: existOk });
      setResponse(res.data);
      setError(null);
    } catch (err: any) {
      setResponse(null);
      setError(err.message);
    }
  };

  return (
    <div className="space-y-4 p-4">
      <h2 className="text-xl font-bold">Import Config</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex gap-4">
          <select
            className="flex-1"
            value={configPath}
            onChange={(e) => setConfigPath(e.target.value)}
            
          >
            <option value="">Select Config File</option>
            {configs.map((path) => (
              <option key={path} value={path}>
                {path.split("/").pop()}
              </option>
            ))}
          </select>

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={existOk}
              onChange={(e) => setExistOk(e.target.checked)}
            />
            Ignore Existing
          </label>
        </div>

        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          POST
        </button>
      </form>

      {response && (
        <div className="bg-green-100 p-3 rounded">
          <h3 className="font-semibold">Response</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}

      {error && <p className="text-red-500">Error: {error}</p>}
    </div>
  );
}
