import { useEffect, useState } from "react";
import GenericORMUI from "../Components/GenericORMUI";
import { GenericAPI } from "../services/api";
import Navbar from "../Components/Navbar";

const runDefaults = {
  name: "",
  scenario: null,
  agents: null,
  runs: 1,
};

const apiScenario = new GenericAPI("scenarios");
const apiAgentConfig = new GenericAPI("agent_configs");

function RunsFormComponent({
  form,
  onChange,
}: {
  form: Record<string, any>;
  onChange: (key: string, value: any) => void;
}) {
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [agents, setAgents] = useState<any[]>([]);

  useEffect(() => {
    apiScenario.get().then((res) => setScenarios(res.data)).catch(() => setScenarios([]));
    apiAgentConfig.get().then((res) => setAgents(res.data)).catch(() => setAgents([]));
  }, []);

  return (
    <div>
      <input
        type="text"
        placeholder="Run Name"
        value={form.name}
        onChange={(e) => onChange("name", e.target.value)}
      />

      <select
        value={form.scenario ?? ""}
        onChange={(e) => onChange("scenario", e.target.value ? parseInt(e.target.value) : null)}
      >
        <option value="">Select Scenario</option>
        {scenarios.map((s) => (
          <option key={s.id} value={s.id}>
            {s.id} - {s.name}
          </option>
        ))}
      </select>

      <select
        value={form.agents ?? ""}
        onChange={(e) => onChange("agents", e.target.value ? parseInt(e.target.value) : null)}
      >
        <option value="">Select Agent Config</option>
        {agents.map((a) => (
          <option key={a.id} value={a.id}>
            {a.id} - {a.name}
          </option>
        ))}
      </select>

      <input
        type="number"
        min={1}
        max={10000}
        value={form.runs}
        onChange={(e) => onChange("runs", parseInt(e.target.value))}
      />
    </div>
  );
}

export default function RunsPage() {
  return (
    <div>
    <Navbar/>
    <GenericORMUI
      model="runs"
      defaults={runDefaults}
      renderForm={(form, onChange) => (
        <RunsFormComponent form={form} onChange={onChange} />
      )}
      />
      </div>
  );
}
