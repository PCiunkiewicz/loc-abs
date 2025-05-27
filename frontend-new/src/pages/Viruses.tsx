import GenericORMUI from "../Components/GenericORMUI";

const virusDefaults = {
  name: "",
  infectivity: 0.5,
  decay_rate: 0.1,
  color: "#ff0000",
  value: "#ff0000", 
};

const VirusForm = (
  form: Record<string, any>,
  onChange: (key: string, value: any) => void
) => {
  return (
    <div className="space-y-2">
      {/* Slug-safe name */}
      <input
        type="text"
        placeholder="Name (slug format)"
        value={form.name}
        onChange={(e) =>
          onChange("name", e.target.value.toLowerCase().replace(/[^a-z0-9_-]/g, ""))
        }
      />

      <label>
        Infectivity:
        <input
          type="number"
          step="0.01"
          min={0}
          max={1}
          value={form.infectivity}
          onChange={(e) => onChange("infectivity", parseFloat(e.target.value))}
        />
      </label>

      <label>
        Decay Rate:
        <input
          type="number"
          step="0.01"
          min={0}
          max={1}
          value={form.decay_rate}
          onChange={(e) => onChange("decay_rate", parseFloat(e.target.value))}
        />
      </label>

      <label>
        Color:
        <input
          type="color"
          value={form.color}
          onChange={(e) => {
            const color = e.target.value;
            onChange("color", color);
            onChange("value", color); 
          }}
        />
      </label>
    </div>
  );
};

export default function VirusesPage() {
  return (
    <GenericORMUI
      model="viruses"
      defaults={virusDefaults}
      renderForm={VirusForm}
    />
  );
}
