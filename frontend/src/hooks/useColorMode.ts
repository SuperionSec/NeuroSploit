import { useState, useCallback } from "react"

type ColorMode = "light" | "dark"

export function useColorMode() {
  const [colorMode, setColorMode] = useState<ColorMode>("light")

  const toggleColorMode = useCallback(() => {
    setColorMode((prev) => (prev === "light" ? "dark" : "light"))
  }, [])

  return { colorMode, toggleColorMode }
}