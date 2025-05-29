import GenericORMUI from "../Components/GenericORMUI";
import Navbar from "../Components/Navbar";


const terrainDefaults = {
  name: "",
  material: null,
  walkable: true,
  interactive: false,
  restricted: false,
  color: "#00f900",
  value: "#00f900",
  access_level: 0,
};

const TerrainForm = (
  form: Record<string, any>,
  onChange: (key: string, value: any) => void
) => {
  return (
    <div className="space-y-2">
      <input
        type="text"
        placeholder="Name (slug: lowercase, no spaces)"
        value={form.name}
        onChange={(e) =>
          onChange("name", e.target.value.toLowerCase().replace(/[^a-z0-9_-]/g, ""))
        }
      />

      <div className="flex gap-4">
        <label>
          <input
            type="checkbox"
            checked={form.walkable}
            onChange={(e) => onChange("walkable", e.target.checked)}
          />
          Walkable
        </label>
        <label>
          <input
            type="checkbox"
            checked={form.interactive}
            onChange={(e) => onChange("interactive", e.target.checked)}
          />
          Interactive
        </label>
        <label>
          <input
            type="checkbox"
            checked={form.restricted}
            onChange={(e) => onChange("restricted", e.target.checked)}
          />
          Restricted
        </label>
      </div>

      <div className="flex items-center gap-2">
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

        <label>
          Access Level:
          <input
            type="number"
            min={0}
            max={10}
            value={form.access_level}
            onChange={(e) => onChange("access_level", parseInt(e.target.value))}
          />
        </label>
      </div>
    </div>
  );
};

export default function TerrainsPage() {
  return (
    <div>
      <Navbar/>
    <GenericORMUI
      model="terrains"
      defaults={terrainDefaults}
      renderForm={TerrainForm}
      />
      </div>
  );
}