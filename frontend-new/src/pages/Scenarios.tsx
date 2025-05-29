import { useEffect, useState } from "react";
import GenericORMUI from "../Components/GenericORMUI";
import { GenericAPI } from "../services/api";
import Navbar from "../Components/Navbar";


const scenarioDefaults = {
  name: "",
  sim: null,
  virus: null,
  prevention: null,
};

const apiSim = new GenericAPI("simulations");
const apiVirus = new GenericAPI("viruses");
const apiPrevention = new GenericAPI("preventions");

function ScenariosFormComponent({
  form,
  onChange,
}: {
  form: Record<string, any>;
  onChange: (key: string, value: any) => void;
}) {
  const [sims, setSims] = useState<any[]>([]);
  const [viruses, setViruses] = useState<any[]>([]);
  const [preventions, setPreventions] = useState<any[]>([]);

  useEffect(() => {
    apiSim.get().then((res) => setSims(res.data)).catch(() => setSims([]));
    apiVirus.get().then((res) => setViruses(res.data)).catch(() => setViruses([]));
    apiPrevention.get().then((res) => setPreventions(res.data)).catch(() => setPreventions([]));
  }, []);

  return (
    <div>
      <input
        type="text"
        placeholder="Scenario Name"
        value={form.name}
        onChange={(e) => onChange("name", e.target.value)}
      />

      <select
        value={form.sim ?? ""}
        onChange={(e) => onChange("sim", e.target.value ? parseInt(e.target.value) : null)}
      >
        <option value="">Select Simulation</option>
        {sims.map((s) => (
          <option key={s.id} value={s.id}>
            {s.id} - {s.name}
          </option>
        ))}
      </select>

      <select
        value={form.virus ?? ""}
        onChange={(e) => onChange("virus", e.target.value ? parseInt(e.target.value) : null)}
      >
        <option value="">Select Virus</option>
        {viruses.map((v) => (
          <option key={v.id} value={v.id}>
            {v.id} - {v.name}
          </option>
        ))}
      </select>

      <select
        value={form.prevention ?? ""}
        onChange={(e) =>
          onChange("prevention", e.target.value ? parseInt(e.target.value) : null)
        }
      >
        <option value="">Select Prevention</option>
        {preventions.map((p) => (
          <option key={p.id} value={p.id}>
            {p.id} - {p.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default function ScenariosPage() {
  return (
    <div>
    <Navbar/>
    <GenericORMUI
      model="scenarios"
      defaults={scenarioDefaults}
      renderForm={(form, onChange) => (
        <ScenariosFormComponent form={form} onChange={onChange} />
      )}
      />
      </div>
  );
}
