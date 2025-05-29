import { useState, useRef } from "react";
import { Link } from "react-router-dom";
import { useOutsideClick } from "../hooks/useOutsideClick";
import type { JSX } from "react";

const Navbar = (): JSX.Element => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isEnvironmentDropdownOpen, setIsEnvironmentDropdownOpen] = useState(false);
  const [isInfectionDataDropdownOpen, setIsInfectionDataDropdownOpen] = useState(false);
  const [isScenariosAgentsDropdownOpen, setIsScenariosAgentsDropdownOpen] = useState(false);

  const envRef = useRef<HTMLLIElement>(null);
  const infRef = useRef<HTMLLIElement>(null);
  const scnRef = useRef<HTMLLIElement>(null);
  const sysRef = useRef<HTMLLIElement>(null);

  useOutsideClick(envRef, () => setIsDropdownOpen(false));
  useOutsideClick(infRef, () => setIsEnvironmentDropdownOpen(false));
  useOutsideClick(scnRef, () => setIsInfectionDataDropdownOpen(false));
  useOutsideClick(sysRef, () => setIsScenariosAgentsDropdownOpen(false));

  return (
    <nav className="bg-white border-gray-200 dark:bg-gray-900 dark:border-gray-700 w-full">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <Link to="/" className="flex items-center space-x-3 rtl:space-x-reverse">
          <img
            src="https://flowbite.com/docs/images/logo.svg"
            className="h-8"
            alt="Flowbite Logo"
          />
          <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white cursor-pointer">
            LocAbs
          </span>
        </Link>

        <button
          onClick={() => setIsMenuOpen((prev) => !prev)}
          type="button"
          className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
        >
          <span className="sr-only">Open main menu</span>
          <svg className="w-5 h-5" fill="none" viewBox="0 0 17 14">
            <path stroke="currentColor" strokeWidth="2" d="M1 1h15M1 7h15M1 13h15" />
          </svg>
        </button>

        <div className={`${isMenuOpen ? "block" : "hidden"} w-full md:block md:w-auto`}>
          <ul className="flex flex-col font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">

            <li className="relative" ref={envRef}>
              <button
                onClick={() => setIsDropdownOpen((prev) => !prev)}
                className="flex items-center justify-between w-full py-2 px-3 text-gray-900 dark:text-white md:p-0 md:w-auto cursor-pointer
"
              >
                Environment
                <svg className="w-2.5 h-2.5 ms-2.5" fill="none" viewBox="0 0 10 6">
                  <path stroke="currentColor" strokeWidth="2" d="m1 1 4 4 4-4" />
                </svg>
              </button>
              {isDropdownOpen && (
                <div className="absolute z-10 mt-2 w-44 bg-white rounded-lg shadow-sm dark:bg-gray-700">
                  <ul className="py-2 text-sm text-gray-700 dark:text-gray-400">
                    <li>
                      <Link to="/Terrain" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                        Terrains
                      </Link>
                    </li>
                    <li>
                      <Link to="/Simulation" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                        Simulation
                      </Link>
                    </li>
                  </ul>
                </div>
              )}
            </li>

            <li className="relative" ref={infRef}>
              <button
                onClick={() => setIsEnvironmentDropdownOpen((prev) => !prev)}
                className="flex items-center justify-between w-full py-2 px-3 text-gray-900 dark:text-white md:p-0 md:w-auto cursor-pointer"
              >
                Infection Data
                <svg className="w-2.5 h-2.5 ms-2.5" fill="none" viewBox="0 0 10 6">
                  <path stroke="currentColor" strokeWidth="2" d="m1 1 4 4 4-4" />
                </svg>
              </button>
              {isEnvironmentDropdownOpen && (
                <div className="absolute z-10 mt-2 w-44 bg-white rounded-lg shadow-sm dark:bg-gray-700">
                  <ul className="py-2 text-sm text-gray-700 dark:text-gray-400">
                    <li>
                      <Link to="/Viruses" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                        Viruses
                      </Link>
                    </li>
                    <li>
                      <Link to="/Prevention" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                        Prevention
                      </Link>
                    </li>
                  </ul>
                </div>
              )}
            </li>

            <li className="relative" ref={scnRef}>
              <button
                onClick={() => setIsInfectionDataDropdownOpen((prev) => !prev)}
                className="flex items-center justify-between w-full py-2 px-3 text-gray-900 dark:text-white md:p-0 md:w-auto cursor-pointer"
              >
                Scenarios & Agent
                <svg className="w-2.5 h-2.5 ms-2.5" fill="none" viewBox="0 0 10 6">
                  <path stroke="currentColor" strokeWidth="2" d="m1 1 4 4 4-4" />
                </svg>
              </button>
              {isInfectionDataDropdownOpen && (
                <div className="absolute z-10 mt-2 w-44 bg-white rounded-lg shadow-sm dark:bg-gray-700">
                  <ul className="py-2 text-sm text-gray-700 dark:text-gray-400">
                    <li><Link to="/Scenarios" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Scenarios</Link></li>
                    <li><Link to="/AgentConfigs" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Agent Config</Link></li>
                    <li><Link to="/Runs" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Runs</Link></li>
                  </ul>
                </div>
              )}
            </li>

            <li className="relative" ref={sysRef}>
              <button
                onClick={() => setIsScenariosAgentsDropdownOpen((prev) => !prev)}
                className="flex items-center justify-between w-full py-2 px-3 text-gray-900 dark:text-white md:p-0 md:w-auto cursor-pointer"
              >
                System
                <svg className="w-2.5 h-2.5 ms-2.5" fill="none" viewBox="0 0 10 6">
                  <path stroke="currentColor" strokeWidth="2" d="m1 1 4 4 4-4" />
                </svg>
              </button>
              {isScenariosAgentsDropdownOpen && (
                <div className="absolute z-10 mt-2 w-44 bg-white rounded-lg shadow-sm dark:bg-gray-700">
                  <ul className="py-2 text-sm text-gray-700 dark:text-gray-400">
                    <li><Link to="/Importer" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Importer</Link></li>
                    <li><Link to="/Admin" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Admin</Link></li>
                  </ul>
                </div>
              )}
            </li>

          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
