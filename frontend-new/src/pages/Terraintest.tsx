import React from "react";
import Navbar from "../Components/Navbar";
import { useState, useEffect } from "react";
import { GenericAPI } from "../services/api";

// default values for creating a new terrain (used to reset form or initialize it)
const terrainDefaults: Partial<Terrain> = {
  name: "",
  material: null,
  walkable: true,
  interactive: false,
  restricted: false,
  color: "#00f900",
  value: "#00f900",
  access_level: 0,
};

// defines what a Terrain object looks like
// used for type checking and ensuring consistency
type Terrain = {
  id: number;
  name: string;
  material: string | null;
  walkable: boolean;
  interactive: boolean;
  restricted: boolean;
  color: string;
  value: string;
  access_level: number;
};

const ProductDashboard: React.FC = () => {
  const api = new GenericAPI("terrains"); // set up API instance for "terrains" endpoint
  const [form, setForm] = useState(() => ({ ...terrainDefaults })); // local state for form fields, initialized with default terrain values
  const [response, setResponse] = useState<any | null>(null); // response from API (used mostly for debugging or feedback)
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = React.useState(false); // tracks whether the modal (popup form) is open
  const [terrains, setTerrains] = useState<any[]>([]); // list of all terrain objects fetched from the API
  const [editingId, setEditingId] = useState<number | null>(null); // ID of the item currently being edited (null if creating new)
  const [searchQuery, setSearchQuery] = useState(""); // search query used to filter the list in the table

  const handleCreate = () => {
    const { id, ...formWithoutId } = form as Terrain; // make sure to not send the ID field when creating new
    // send POST request to create a new terrain
    api
      .post(formWithoutId)
      .then((res) => {
        // store API response and refresh list
        setResponse(res.data);
        fetchObjects();
      })
      .catch((err) =>
        setError(JSON.stringify(err.response?.data || err.message))
      );
  };

  // handles delete button click and confirms before sending request
  const handleDelete = (id: number) => {
    if (confirm("Are you sure you want to delete this terrain?")) {
      api
        .delete(id)
        .then(() => {
          fetchObjects();
        })
        .catch((err) =>
          setError(JSON.stringify(err.response?.data || err.message))
        );
    }
  };

  
  const fetchObjects = () => {
    // fetches all terrains from the API
    api
      .get()
      .then((res) => setTerrains(res.data)) 
      .catch((err) =>
        setError(JSON.stringify(err.response?.data || err.message))
      );
  };

  // useEffect runs once when component mounts to load terrain data
  useEffect(() => {
    fetchObjects();
  }, []);

  return (
    <div>
      <Navbar />
      <section className="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5 antialiased">
        <div className="mx-auto max-w-screen-2xl px-4 lg:px-12">
          <div className="bg-white dark:bg-gray-800 relative shadow-md sm:rounded-lg overflow-hidden">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-3 md:space-y-0 md:space-x-4 p-4">
              <div className="flex-1 flex items-center space-x-2">
                <h5>
                  <span className="text-gray-500">All Products:</span>{" "}
                  <span className="dark:text-white">123456</span>
                </h5>
                <h5 className="text-gray-500 dark:text-gray-400 ml-1">
                  1-100 (436)
                </h5>
                <button
                  type="button"
                  className="group"
                  data-tooltip-target="results-tooltip">
                  <svg
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-4 w-4 text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                    viewBox="0 0 20 20"
                    fill="currentColor">
                    <path
                      fillRule="evenodd"
                      clipRule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    />
                  </svg>
                  <span className="sr-only">More info</span>
                </button>
                <div
                  id="results-tooltip"
                  role="tooltip"
                  className="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700">
                  Showing 1–100 of 436 results
                  <div className="tooltip-arrow" data-popper-arrow="" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <div className="flex flex-col md:flex-row items-center justify-between gap-4 mx-4 py-4 border-t dark:border-gray-700">
        {/* 🔍 Search Input (80%) */}
        <div className="w-full md:w-4/5">
          <form className="w-full cursor-pointer">
            <label htmlFor="product-search" className="sr-only">
              Search
            </label>
            <div className="relative w-full">
              <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <svg
                  aria-hidden="true"
                  className="w-5 h-5 text-gray-500 dark:text-gray-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg">
                  <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 
                          4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                  />
                </svg>
              </div>
              <input
                type="text"
                id="product-search"
                placeholder="Search by name"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg
             focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 p-2
             dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white
             dark:focus:ring-primary-500 dark:focus:border-primary-500"
              />
            </div>
          </form>
        </div>

        {/* ➕ Add Terrain Button */}
        <button
          onClick={() => setIsModalOpen(true)}
          type="button"
          className="flex items-center justify-center text-black bg-primary-700 hover:bg-primary-800
             focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 py-2
             dark:bg-primary-600 dark:hover:bg-primary-700 focus:outline-none dark:focus:ring-primary-800 cursor-pointer">
          <svg
            className="h-4 w-4 mr-2"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true">
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
            />
          </svg>
          Add Terrain
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
          <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
              <th scope="col" className="p-4">
                Name
              </th>
              <th scope="col" className="p-4">
                Access Level
              </th>
              <th scope="col" className="p-4">
                Restricted
              </th>
              <th scope="col" className="p-4">
                Interactive
              </th>
              <th scope="col" className="p-4">
                Walkable
              </th>
              <th scope="col" className="p-4">
                Color
              </th>

              <th scope="col" className="p-4 text-center" colSpan={3}>
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {terrains
              .filter((terrain) =>
                terrain.name.toLowerCase().includes(searchQuery.toLowerCase())
              )
              .map((terrain) => (
                <tr
                  key={terrain.id}
                  className="border-b dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700">
                  <td className="px-4 py-3">
                    <span className="bg-primary-100 text-primary-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-primary-900 dark:text-primary-300">
                      {terrain.name}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="bg-primary-100 text-primary-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-primary-900 dark:text-primary-300">
                      {terrain.access_level}
                    </span>
                  </td>
                  <td>{terrain.walkable ? "Yes" : "No"}</td>
                  <td>{terrain.interactive ? "Yes" : "No"}</td>
                  <td>{terrain.restricted ? "Yes" : "No"}</td>
                  <td className="px-4 py-3 flex items-center gap-2">
                    <span
                      className="w-4 h-4 rounded"
                      style={{ backgroundColor: terrain.color }}></span>
                    <span>{terrain.color}</span>
                  </td>
                  {/* Actions */}
                  <td className="px-2 py-3 text-center">
                    <button
                      type="button"
                      onClick={() => {
                        setForm(terrain);
                        setEditingId(terrain.id);
                        setIsModalOpen(true);
                      }}
                      className="cursor-pointer text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-md text-xs px-4 py-1.5 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-800">
                      Edit
                    </button>
                  </td>
                  <td className=" px-2 py-3 text-center">
                    <button
                      type="button"
                      onClick={() => handleDelete(terrain.id)}
                      className="cursor-pointer text-white bg-red-600 hover:bg-red-700 focus:ring-4 focus:ring-red-300 font-medium rounded-md text-xs px-4 py-1.5 dark:bg-red-500 dark:hover:bg-red-600 dark:focus:ring-red-800">
                      Delete
                    </button>
                  </td>
                  <td className="px-2 py-3 text-center">
                    <button
                      type="button"
                      className=" cursor-pointer text-white bg-gray-600 hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 font-medium rounded-md text-xs px-4 py-1.5 dark:bg-gray-500 dark:hover:bg-gray-600 dark:focus:ring-gray-800">
                      Preview
                    </button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
      {isModalOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-white/10 backdrop-blur-md"
          onClick={() => setIsModalOpen(false)}>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (editingId !== null) {
                api
                  .patch(editingId, form)
                  .then((res) => {
                    setResponse(res.data);
                    fetchObjects();
                    setIsModalOpen(false);
                    setEditingId(null); // Reset
                  })
                  .catch((err) =>
                    setError(JSON.stringify(err.response?.data || err.message))
                  );
              } else {
                handleCreate();
                setIsModalOpen(false);
              }
            }}
            className="bg-gray-900 text-white rounded-lg shadow-lg p-6 w-full max-w-2xl space-y-6"
            onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold">
                {editingId ? "Edit Terrain" : "Create Terrain"}
              </h2>
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="text-gray-400 hover:text-white cursor-pointer">
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 
              8.586l4.293-4.293a1 1 0 111.414 
              1.414L11.414 10l4.293 4.293a1 1 0 
              01-1.414 1.414L10 11.414l-4.293 
              4.293a1 1 0 01-1.414-1.414L8.586 
              10 4.293 5.707a1 1 0 010-1.414z"
                  />
                </svg>
              </button>
            </div>

            {/* Form Fields */}
            <div className="space-y-4">
              {/* Name Input */}
              <div>
                <label className="block text-sm font-medium mb-1">Name</label>
                <input
                  value={form.name || ""}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="w-full bg-gray-800 border border-gray-700 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="Enter name"
                  required
                />
              </div>

              {/* Toggles + Color + Access Level */}
              <div className="flex flex-wrap items-center gap-6">
                {/* Toggles */}
                <div className="flex gap-4">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={form.walkable || false}
                      onChange={(e) =>
                        setForm({ ...form, walkable: e.target.checked })
                      }
                      className="accent-red-500"
                    />
                    Walkable
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={form.interactive || false}
                      onChange={(e) =>
                        setForm({ ...form, interactive: e.target.checked })
                      }
                      className="accent-red-500"
                    />
                    Interactive
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={form.restricted || false}
                      onChange={(e) =>
                        setForm({ ...form, restricted: e.target.checked })
                      }
                      className="accent-red-500"
                    />
                    Restricted
                  </label>
                </div>

                {/* Color Box */}
                <div className="flex flex-col items-center">
                  <span className="text-sm mb-1">Color</span>
                  <input
                    className="w-8 h-8 rounded-md cursor-pointer"
                    type="color"
                    value={form.color || ""}
                    onChange={(e) =>
                      setForm({ ...form, color: e.target.value })
                    }
                  />
                </div>

                {/* Access Level Stepper */}
                <div className="flex flex-col items-center">
                  <span className="text-sm mb-1">Access Level</span>
                  <div className="flex items-center bg-gray-800 rounded-md px-3 py-1">
                    <button
                      type="button"
                      onClick={() =>
                        setForm((prev) => ({
                          ...prev,
                          access_level: Math.max(
                            0,
                            (prev.access_level || 0) - 1
                          ),
                        }))
                      }
                      className="text-lg px-2 cursor-pointer">
                      –
                    </button>
                    <span className="px-4">{form.access_level || 0}</span>
                    <button
                      type="button"
                      onClick={() =>
                        setForm((prev) => ({
                          ...prev,
                          access_level: (prev.access_level || 0) + 1,
                        }))
                      }
                      className="text-lg px-2 cursor-pointer">
                      +
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-4">
              <button
                type="submit"
                className="bg-white text-gray-900 px-6 py-2 rounded-md border border-white hover:bg-gray-200 cursor-pointer">
                {editingId ? "Update" : "Create"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default ProductDashboard;
