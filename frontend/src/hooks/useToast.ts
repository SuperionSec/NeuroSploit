import { useCallback } from "react"

type ToastStatus = "info" | "warning" | "success" | "error"

interface ToastOptions {
  title: string
  description?: string
  status?: ToastStatus
  duration?: number
  isClosable?: boolean
}

export function useToast() {
  return useCallback((options: ToastOptions) => {
    const { title, description, status = "info", duration = 5000 } = options
    const bg =
      status === "error" ? "#E53E3E" :
      status === "warning" ? "#DD6B20" :
      status === "success" ? "#38A169" :
      "#3182CE"
    const el = document.createElement("div")
    el.style.cssText = `position:fixed;top:20px;right:20px;background:${bg};color:white;padding:12px 20px;border-radius:8px;z-index:9999;max-width:400px;font-family:sans-serif;box-shadow:0 4px 12px rgba(0,0,0,0.3);animation:fadeIn 0.3s`
    el.innerHTML = `<strong>${title}</strong>${description ? `<br><small>${description}</small>` : ""}`
    document.body.appendChild(el)
    setTimeout(() => {
      el.style.opacity = "0"
      el.style.transition = "opacity 0.3s"
      setTimeout(() => el.remove(), 300)
    }, duration)
  }, [])
}