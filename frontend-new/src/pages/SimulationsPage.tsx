// import React, { useEffect, useState } from "react";
// import { GenericAPI } from "../services/api";

// type Simulation = {
//   id: number;
//   name: string;
//   mapfile: string;
//   xy_scale: number;
//   t_step: number;
//   save_resolution: number;
//   max_iter: number;
//   save_verbose: boolean;
//   terrain: number[];
// };

// const api = new GenericAPI("simulations");
// const terrainApi = new GenericAPI("terrains");

// const emptySim: Omit<Simulation, "id"> = {
//   name: "",
//   mapfile: "bow_view_manor",
//   xy_scale: 2.77,
//   t_step: 5,
//   save_resolution: 12,
//   max_iter: 250,
//   save_verbose: false,
//   terrain: [],
// };

// const SimulationsPage: React.FC = () => {
//   const [sims, setSims] = useState<Simulation[]>([]);
//   const [terrains, setTerrains] = useState<{ id: number; name: string }[]>([]);
//   const [form, setForm] = useState<Omit<Simulation, "id">>(emptySim);
//   const [editingId, setEditingId] = useState<number | null>(null);
//   const [error, setError] = useState<string | null>(null);

//   const fetchData = () => {
//     api.get()
//       .then(res => setSims(res.data))
//       .catch(err => setError(err.response?.data || err.message));
//     terrainApi.get()
//       .then(res => setTerrains(res.data))
//       .catch(err => console.error(err));
//   };

//   useEffect(fetchData, []);

//   const handleChange = (
//     key: keyof typeof emptySim,
//     value: string | number | boolean | number[]
//   ) => {
//     setForm(prev => ({ ...prev, [key]: value } as any));
//   };

//   const handleSubmit = (e: React.FormEvent) => {
//     e.preventDefault();

//     console.log("🚀 Submitting:", form); // Log what we're sending

//     const action = editingId
//       ? api.patch(editingId, form)
//       : api.post(form);

//     action
//       .then(() => {
//         setForm(emptySim);
//         setEditingId(null);
//         fetchData();
//       })
//       .catch(err => {
//         const message = err.response?.data || err.message;
//         console.error("❌ POST Error:", message);
//         setError(JSON.stringify(message));
//       });
//   };

//   const startEdit = (sim: Simulation) => {
//     const { id, ...rest } = sim;
//     setForm(rest);
//     setEditingId(id);
//   };

//   const handleDelete = (id: number) => {
//     if (!window.confirm("Delete this simulation?")) return;
//     api.delete(id)
//       .then(() => fetchData())
//       .catch(err => setError(err.response?.data || err.message));
//   };

//   return (
//     <div className="p-4">
//       <h1>Simulations CRUD</h1>

//       <form onSubmit={handleSubmit} className="mb-4 space-y-2">
//         <div>
//           <label>Name:</label>
//           <input
//             type="text"
//             value={form.name}
//             onChange={e => handleChange("name", e.target.value)}
//             required
//           />
//         </div>

//         <div>
//           <label>Map File:</label>
//           <input
//             type="text"
//             value={form.mapfile}
//             onChange={e => handleChange("mapfile", e.target.value)}
//             required
//           />
//         </div>

//         <div>
//           <label>XY Scale:</label>
//           <input
//             type="number"
//             step="0.1"
//             value={form.xy_scale}
//             onChange={e => handleChange("xy_scale", parseFloat(e.target.value))}
//           />
//         </div>

//         <div>
//           <label>Time Step:</label>
//           <input
//             type="number"
//             min={1}
//             value={form.t_step}
//             onChange={e => handleChange("t_step", parseInt(e.target.value))}
//           />
//         </div>

//         <div>
//           <label>Save Resolution:</label>
//           <input
//             type="number"
//             min={1}
//             value={form.save_resolution}
//             onChange={e =>
//               handleChange("save_resolution", parseInt(e.target.value))
//             }
//           />
//         </div>

//         <div>
//           <label>Max Iterations:</label>
//           <input
//             type="number"
//             min={1}
//             value={form.max_iter}
//             onChange={e => handleChange("max_iter", parseInt(e.target.value))}
//           />
//         </div>

//         <div>
//           <label>
//             <input
//               type="checkbox"
//               checked={form.save_verbose}
//               onChange={e => handleChange("save_verbose", e.target.checked)}
//             />
//             Save Verbose
//           </label>
//         </div>

//         <div>
//           <label>Terrains (Ctrl+click to multiselect):</label>
//           <select
//             multiple
//             value={form.terrain.map(String)}
//             onChange={e =>
//               handleChange(
//                 "terrain",
//                 Array.from(e.target.selectedOptions, o => parseInt(o.value))
//               )
//             }
//           >
//             {terrains.map(t => (
//               <option key={t.id} value={t.id}>
//                 {t.name}
//               </option>
//             ))}
//           </select>
//         </div>

//         <button type="submit">
//           {editingId ? "Update" : "Create"} Simulation
//         </button>
//         {editingId != null && (
//           <button
//             type="button"
//             onClick={() => {
//               setForm(emptySim);
//               setEditingId(null);
//             }}
//           >
//             Cancel
//           </button>
//         )}
//       </form>

//       {error && <p className="text-red-500">Error: {error}</p>}

//       <ul className="space-y-2">
//         {sims.map(sim => (
//           <li key={sim.id} className="border p-2">
//             <pre>{JSON.stringify(sim, null, 2)}</pre>
//             <button onClick={() => startEdit(sim)}>Edit</button>
//             <button onClick={() => handleDelete(sim.id)}>Delete</button>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default SimulationsPage;


import GenericORMUI from "../Components/GenericORMUI";

const simDefaults = {
  name: "",
  mapfile: "bow_view_manor",
  xy_scale: 2.77,
  t_step: 5,
  save_resolution: 12,
  max_iter: 250,
  save_verbose: false,
  terrain: [],
};

const SimForm = (form: any, onChange: (key: string, value: any) => void) => (
  <div className="space-y-2">
    <input
      type="text"
      placeholder="Name"
      value={form.name}
      onChange={e => onChange("name", e.target.value)}
    />
    <input
      type="text"
      placeholder="Map File"
      value={form.mapfile}
      onChange={e => onChange("mapfile", e.target.value)}
    />
    <input
      type="number"
      placeholder="XY Scale"
      value={form.xy_scale}
      onChange={e => onChange("xy_scale", parseFloat(e.target.value))}
    />
    <input
      type="number"
      placeholder="Time Step"
      value={form.t_step}
      onChange={e => onChange("t_step", parseInt(e.target.value))}
    />
    <input
      type="number"
      placeholder="Save Resolution"
      value={form.save_resolution}
      onChange={e => onChange("save_resolution", parseInt(e.target.value))}
    />
    <input
      type="number"
      placeholder="Max Iter"
      value={form.max_iter}
      onChange={e => onChange("max_iter", parseInt(e.target.value))}
    />
    <label>
      <input
        type="checkbox"
        checked={form.save_verbose}
        onChange={e => onChange("save_verbose", e.target.checked)}
      />
      Save Verbose
    </label>
  </div>
);

export default function SimulationsPage() {
  return (
    <GenericORMUI model="simulations" defaults={simDefaults} renderForm={SimForm} />
  );
}
