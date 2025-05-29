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
