import GenericORMUI from "../Components/GenericORMUI";
import Navbar from "../Components/Navbar";

const preventionDefaults = {
  name: "",
  mask: {
    N95: 0.85,
    NONE: 0,
    CLOTH: 0.3,
    SURGICAL: 0.5,
  },
  vax: {
    MRNA: [0, 0.31, 0.88],
    ASTRA: [0, 0.31, 0.67],
  },
};

const PreventionsForm = (
  form: Record<string, any>,
  onChange: (key: string, value: any) => void
) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Name"
        value={form.name}
        onChange={(e) => onChange("name", e.target.value)}
      />
      <label>
        Mask Info (JSON):
        <textarea
          rows={6}
          value={JSON.stringify(form.mask, null, 2)}
          onChange={(e) => {
            try {
              onChange("mask", JSON.parse(e.target.value));
            } catch {
            }
          }}
        />
      </label>

      <label>
        Vax Info (JSON):
        <textarea
          rows={6}
          value={JSON.stringify(form.vax, null, 2)}
          onChange={(e) => {
            try {
              onChange("vax", JSON.parse(e.target.value));
            } catch {
            }
          }}
        />
      </label>
    </div>
  );
};

export default function PreventionsPage() {
  return (
    <div>
    <Navbar/>
    <GenericORMUI
      model="preventions"
      defaults={preventionDefaults}
      renderForm={PreventionsForm}
      />
      </div>
  );
}
