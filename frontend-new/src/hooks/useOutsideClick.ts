import { useEffect, type RefObject } from "react";

export function useOutsideClick<T extends HTMLElement | null>(
  ref: RefObject<T>,
  onClickOutside: () => void
) {
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const el = ref?.current;
      if (el && !el.contains(event.target as Node)) {
        onClickOutside();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [ref, onClickOutside]);
}
