import React, { useState, useMemo } from "react";
import type { JSX } from "react";
import { GenericAPI } from "../services/api";

type ORMProps = {
  model: string;
  defaults: Record<string, any>;
  renderForm: (
    form: Record<string, any>,
    onChange: (key: string, value: any) => void
  ) => JSX.Element;
};

const GenericORMUI: React.FC<ORMProps> = ({ model, defaults, renderForm }) => {
  const api = new GenericAPI(model);
  const [tab, setTab] = useState<"create" | "retrieve" | "update" | "delete">("create");
  const [form, setForm] = useState(() => ({ ...defaults }));
  const [objectList, setObjectList] = useState<any[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [response, setResponse] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  


  const fetchObjects = () => {
    api.get()
      .then(res => setObjectList(res.data))
      .catch(err => setError(JSON.stringify(err.response?.data || err.message)));
  };

  const handleChange = (key: string, value: any) => {
    setForm(prev => ({ ...prev, [key]: value }));
  };

  const handleCreate = () => {
    api.post(form)
      .then(res => {
        setResponse(res.data);
        fetchObjects();
      })
      .catch(err => setError(JSON.stringify(err.response?.data || err.message)));
  };

  const handleRetrieve = () => {
    if (!selectedId) return;
    api.get(selectedId)
      .then(res => setResponse(res.data))
      .catch(err => {
        setResponse(null);
        setError(JSON.stringify(err.response?.data || err.message));
      });
  };

  const handleUpdate = () => {
    if (!selectedId) return;
    api.patch(selectedId, form)
      .then(res => {
        setResponse(res.data);
        fetchObjects();
      })
      .catch(err => setError(JSON.stringify(err.response?.data || err.message)));
  };

  const handleDelete = () => {
    if (!selectedId) return;
    api.delete(selectedId)
      .then(res => {
        setResponse(res.data);
        fetchObjects();
      })
      .catch(err => setError(JSON.stringify(err.response?.data || err.message)));
  };

  const RenderFormWrapper = useMemo(() => renderForm(form, handleChange), [form]);

  return (
    <div className="p-4 space-y-6">
      <h2 className="text-2xl font-semibold">{model.toUpperCase()}</h2>

      <div className="flex gap-4 mb-4">
        {["create", "retrieve", "update", "delete"].map((t) => (
          <button
            key={t}
            className={`px-4 py-1 border rounded ${
              tab === t ? "bg-black text-white" : "bg-white text-black"
            }`}
            onClick={() => {
              setTab(t as any);
              setResponse(null);
              setError(null);
              if (t === "create") {
                setForm({ ...defaults });
                setSelectedId(null);
              }
              if (t === "update" || t === "delete" || t === "retrieve") {
                fetchObjects();
              }
            }}
          >
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {tab === "create" && (
        <form onSubmit={(e) => { e.preventDefault(); handleCreate(); }}>
          {RenderFormWrapper}
          <button type="submit">Create</button>
        </form>
      )}

      {tab === "retrieve" && (
        <>
          <select
            name="retrieveId"
            id="retrieveId"
            onChange={(e) => setSelectedId(parseInt(e.target.value))}
          >
            <option value="">Select {model}</option>
            {objectList.map((obj) => (
              <option key={obj.id} value={obj.id}>
                {obj.id} - {obj.name}
              </option>
            ))}
          </select>
          <button onClick={handleRetrieve} disabled={!selectedId}>
            Retrieve
          </button>
        </>
      )}

      {tab === "update" && (
        <>
          <select
            name="updateId"
            id="updateId"
            onChange={(e) => {
              const id = parseInt(e.target.value);
              setSelectedId(id);
              api.get(id).then((res) => setForm(res.data));
            }}
          >
            <option value="">Select {model}</option>
            {objectList.map((obj) => (
              <option key={obj.id} value={obj.id}>
                {obj.id} - {obj.name}
              </option>
            ))}
          </select>
          {selectedId && (
            <form onSubmit={(e) => { e.preventDefault(); handleUpdate(); }}>
              {RenderFormWrapper}
              <button type="submit">Update</button>
            </form>
          )}
        </>
      )}

      {tab === "delete" && (
        <>
          <select
            name="deleteId"
            id="deleteId"
            onChange={(e) => setSelectedId(parseInt(e.target.value))}
          >
            <option value="">Select {model}</option>
            {objectList.map((obj) => (
              <option key={obj.id} value={obj.id}>
                {obj.id} - {obj.name}
              </option>
            ))}
          </select>
          <button onClick={handleDelete} disabled={!selectedId}>
            Delete
          </button>
        </>
      )}

      {response && (
        <div className="border p-2 bg-green-50 mt-4">
          <strong>Response:</strong>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
      {error && (
        <div className="border p-2 bg-red-50 mt-4">
          <strong>Error:</strong>
          <pre>{error}</pre>
        </div>
      )}
    </div>
  );
};

export default GenericORMUI;
