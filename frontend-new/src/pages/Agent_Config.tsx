import GenericORMUI from "../Components/GenericORMUI";
import Navbar from "../Components/Navbar";

const agentDefaults = {
  name: "",
  default: {
    info: {
      mask_type: "",
      vax_type: "",
      vax_doses: 0,
      schedule: {},
      work_zone: null,
      start_zone: null,
    },
    state: {
      x: 0,
      y: 0,
      status: "UNKNOWN",
    },
  },
  random_agents: 0,
  random_infected: 0,
  custom: [],
};

const AgentConfigForm = (
  form: Record<string, any>,
  onChange: (key: string, value: any) => void
) => {
  return (
    <div className="space-y-4">
      <div className="flex space-x-4">
        <input
          type="text"
          className="border p-2 rounded w-1/2"
          placeholder="Name"
          value={form.name}
          onChange={(e) => onChange("name", e.target.value)}
        />

        <input
          type="number"
          className="border p-2 rounded w-1/4"
          placeholder="Random Agents"
          value={form.random_agents}
          onChange={(e) => onChange("random_agents", parseInt(e.target.value))}
          min={0}
          max={1000}
        />

        <input
          type="number"
          className="border p-2 rounded w-1/4"
          placeholder="Random Infected"
          value={form.random_infected}
          onChange={(e) => onChange("random_infected", parseInt(e.target.value))}
          min={0}
          max={1000}
        />
      </div>

      <div className="flex space-x-4">
        <div className="w-1/2">
          <label className="block text-sm font-medium">Default Agent Configuration (JSON)</label>
          <textarea
            rows={10}
            className="w-full border p-2 rounded"
            value={JSON.stringify(form.default, null, 2)}
            onChange={(e) => {
              try {
                onChange("default", JSON.parse(e.target.value));
              } catch (_) {
              }
            }}
          />
        </div>

        <div className="w-1/2">
          <label className="block text-sm font-medium">Custom Agents (JSON)</label>
          <textarea
            rows={10}
            className="w-full border p-2 rounded"
            value={JSON.stringify(form.custom, null, 2)}
            onChange={(e) => {
              try {
                onChange("custom", JSON.parse(e.target.value));
              } catch (_) {
              }
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default function AgentConfigsPage() {
  return (
    <div>
    <Navbar/>
    <GenericORMUI
      model="agent_configs"
      defaults={agentDefaults}
      renderForm={AgentConfigForm}
      />
      </div>
  );
}
