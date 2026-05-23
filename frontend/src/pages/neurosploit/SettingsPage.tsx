import { useColorMode } from "../../hooks/useColorMode"
import { useToast } from "../../hooks/useToast"
import { useState, useEffect, useCallback } from "react"
import {
  Box, Heading, Text, Card, CardBody, CardHeader, SimpleGrid, VStack, HStack,
  FormControl, FormLabel, Input, Switch, Select, Button, Divider, Spinner,
  Alert, NumberInput, NumberInputField,
  Tab, Tabs, TabList, TabPanels, TabPanel, Badge, Code} from "@chakra-ui/react"
import { AlertTriangle } from "lucide-react"
import { neurosploitApi } from "../../services/neurosploitApi"

type Settings = Record<string, any>

export function SettingsPage() {
  const [settings, setSettings] = useState<Settings | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")
  const toast = useToast()
  const { colorMode } = useColorMode()

  const fetchSettings = useCallback(async () => {
    try {
      setLoading(true)
      setError("")
      const res = await neurosploitApi.settings.get()
      setSettings(res.data)
    } catch {
      setError("Failed to load settings")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchSettings() }, [fetchSettings])

  const handleSave = async () => {
    if (!settings) return
    try {
      setSaving(true)
      await neurosploitApi.settings.update(settings)
      toast({ title: "Settings saved", status: "success", duration: 3000 })
    } catch {
      toast({ title: "Failed to save settings", status: "error", duration: 3000 })
    } finally {
      setSaving(false)
    }
  }

  const updateField = (key: string, value: any) => {
    setSettings(prev => prev ? { ...prev, [key]: value } : null)
  }

  if (loading) {
    return (
      <Box textAlign="center" py={20}>
        <Spinner size="xl" />
        <Text mt={4} color="gray.500">Loading settings...</Text>
      </Box>
    )
  }

  if (error) {
    return (
      <Box textAlign="center" py={20}>
        <Alert status="error"><AlertTriangle size={16} />{error}</Alert>
        <Button mt={4} onClick={fetchSettings}>Retry</Button>
      </Box>
    )
  }

  if (!settings) return null

  return (
    <Box py={6} px={4} maxW="1200px" mx="auto">
      <HStack justify="space-between" mb={6}>
        <Heading size="lg">NeuroSploit Settings</Heading>
        <Button colorScheme="blue" onClick={handleSave} isLoading={saving} size="lg">
          Save Settings
        </Button>
      </HStack>

      <Tabs variant="enclosed" colorScheme="blue">
        <TabList>
          <Tab>LLM Providers</Tab>
          <Tab>Features</Tab>
          <Tab>Scan Limits</Tab>
          <Tab>Sandbox</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
              <Card>
                <CardHeader><Heading size="sm">Anthropic</Heading></CardHeader>
                <CardBody>
                  <FormControl>
                    <FormLabel>API Key</FormLabel>
                    <Input
                      type="password"
                      value={settings.ANTHROPIC_API_KEY || ""}
                      onChange={e => updateField("ANTHROPIC_API_KEY", e.target.value)}
                      placeholder="sk-ant-..."
                    />
                  </FormControl>
                </CardBody>
              </Card>
              <Card>
                <CardHeader><Heading size="sm">OpenAI</Heading></CardHeader>
                <CardBody>
                  <FormControl>
                    <FormLabel>API Key</FormLabel>
                    <Input
                      type="password"
                      value={settings.OPENAI_API_KEY || ""}
                      onChange={e => updateField("OPENAI_API_KEY", e.target.value)}
                      placeholder="sk-..."
                    />
                  </FormControl>
                </CardBody>
              </Card>
              <Card>
                <CardHeader><Heading size="sm">Google Gemini</Heading></CardHeader>
                <CardBody>
                  <FormControl>
                    <FormLabel>API Key</FormLabel>
                    <Input
                      type="password"
                      value={settings.GEMINI_API_KEY || ""}
                      onChange={e => updateField("GEMINI_API_KEY", e.target.value)}
                      placeholder="AIza..."
                    />
                  </FormControl>
                </CardBody>
              </Card>
              <Card>
                <CardHeader><Heading size="sm">OpenRouter</Heading></CardHeader>
                <CardBody>
                  <FormControl>
                    <FormLabel>API Key</FormLabel>
                    <Input
                      type="password"
                      value={settings.OPENROUTER_API_KEY || ""}
                      onChange={e => updateField("OPENROUTER_API_KEY", e.target.value)}
                      placeholder="sk-or-..."
                    />
                  </FormControl>
                </CardBody>
              </Card>
              <Card>
                <CardHeader><Heading size="sm">Together AI</Heading></CardHeader>
                <CardBody>
                  <FormControl>
                    <FormLabel>API Key</FormLabel>
                    <Input
                      type="password"
                      value={settings.TOGETHER_API_KEY || ""}
                      onChange={e => updateField("TOGETHER_API_KEY", e.target.value)}
                    />
                  </FormControl>
                </CardBody>
              </Card>
              <Card>
                <CardHeader><Heading size="sm">Fireworks AI</Heading></CardHeader>
                <CardBody>
                  <FormControl>
                    <FormLabel>API Key</FormLabel>
                    <Input
                      type="password"
                      value={settings.FIREWORKS_API_KEY || ""}
                      onChange={e => updateField("FIREWORKS_API_KEY", e.target.value)}
                    />
                  </FormControl>
                </CardBody>
              </Card>
            </SimpleGrid>
            <Card mt={6}>
              <CardHeader><Heading size="sm">Default LLM Model</Heading></CardHeader>
              <CardBody>
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                  <FormControl>
                    <FormLabel>Model</FormLabel>
                    <Select
                      value={settings.DEFAULT_LLM_MODEL || "claude-sonnet-4-20250514"}
                      onChange={e => updateField("DEFAULT_LLM_MODEL", e.target.value)}
                    >
                      <option value="claude-sonnet-4-20250514">Claude Sonnet 4</option>
                      <option value="claude-3-5-sonnet-20241022">Claude 3.5 Sonnet</option>
                      <option value="gpt-4o">GPT-4o</option>
                      <option value="gpt-4-turbo">GPT-4 Turbo</option>
                      <option value="gemini-2.0-pro">Gemini 2.0 Pro</option>
                    </Select>
                  </FormControl>
                  <FormControl>
                    <FormLabel>Max Output Tokens</FormLabel>
                    <NumberInput
                      value={settings.MAX_OUTPUT_TOKENS || 64000}
                      onChange={(_, v) => updateField("MAX_OUTPUT_TOKENS", v)}
                      min={1024} max={200000}
                    >
                      <NumberInputField />
                    </NumberInput>
                  </FormControl>
                </SimpleGrid>
              </CardBody>
            </Card>
          </TabPanel>

          <TabPanel>
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
              {[
                { key: "ENABLE_REASONING", label: "Reasoning Engine", desc: "Chain-of-thought vulnerability analysis" },
                { key: "ENABLE_CVE_HUNT", label: "CVE Hunting", desc: "Search NVD + GitHub for known exploits" },
                { key: "ENABLE_KNOWLEDGE_AUGMENTATION", label: "Knowledge Augmentation", desc: "Enrich findings with RAG" },
                { key: "ENABLE_BROWSER_VALIDATION", label: "Browser Validation", desc: "Playwright-based XSS/CSRF verification" },
                { key: "ENABLE_VULN_AGENTS", label: "Per-Vuln Agents", desc: "Dedicated AI agent per vulnerability type" },
                { key: "ENABLE_SMART_ROUTER", label: "Smart Router", desc: "Auto-select best LLM per task" },
                { key: "ENABLE_RAG", label: "RAG", desc: "Retrieval-augmented generation" },
                { key: "ENABLE_CLI_AGENT", label: "CLI Agent", desc: "Terminal-based autonomous pentesting" },
                { key: "ENABLE_MULTI_AGENT", label: "Multi-Agent", desc: "Parallel specialist agent orchestration" },
                { key: "ENABLE_RESEARCHER_AI", label: "Researcher AI", desc: "Hypothesis-driven 0-day discovery" },
              ].map(({ key, label, desc }) => (
                <Card key={key}>
                  <CardBody>
                    <HStack justify="space-between">
                      <Box>
                        <Text fontWeight="bold">{label}</Text>
                        <Text fontSize="sm" color="gray.500">{desc}</Text>
                      </Box>
                      <Switch
                        isChecked={!!settings[key]}
                        onChange={e => updateField(key, e.target.checked)}
                        colorScheme="blue"
                        size="lg"
                      />
                    </HStack>
                  </CardBody>
                </Card>
              ))}
            </SimpleGrid>
          </TabPanel>

          <TabPanel>
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
              <Card>
                <CardHeader><Heading size="sm">Concurrency</Heading></CardHeader>
                <CardBody>
                  <VStack spacing={4}>
                    <FormControl>
                      <FormLabel>Max Concurrent Scans</FormLabel>
                      <NumberInput
                        value={settings.MAX_CONCURRENT_SCANS || 5}
                        onChange={(_, v) => updateField("MAX_CONCURRENT_SCANS", v)}
                        min={1} max={20}
                      >
                        <NumberInputField />
                      </NumberInput>
                    </FormControl>
                    <FormControl>
                      <FormLabel>Max Requests Per Second</FormLabel>
                      <NumberInput
                        value={settings.MAX_REQUESTS_PER_SECOND || 10}
                        onChange={(_, v) => updateField("MAX_REQUESTS_PER_SECOND", v)}
                        min={1} max={100}
                      >
                        <NumberInputField />
                      </NumberInput>
                    </FormControl>
                    <FormControl>
                      <FormLabel>Token Budget</FormLabel>
                      <NumberInput
                        value={settings.TOKEN_BUDGET || ""}
                        onChange={(_, v) => updateField("TOKEN_BUDGET", v || null)}
                        min={0} max={1000000}
                      >
                        <NumberInputField placeholder="Unlimited" />
                      </NumberInput>
                    </FormControl>
                  </VStack>
                </CardBody>
              </Card>
              <Card>
                <CardHeader><Heading size="sm">CLI Agent</Heading></CardHeader>
                <CardBody>
                  <FormControl>
                    <FormLabel>Max Runtime (seconds)</FormLabel>
                    <NumberInput
                      value={settings.CLI_AGENT_MAX_RUNTIME || 1800}
                      onChange={(_, v) => updateField("CLI_AGENT_MAX_RUNTIME", v)}
                      min={60} max={7200}
                    >
                      <NumberInputField />
                    </NumberInput>
                  </FormControl>
                </CardBody>
              </Card>
              <Card>
                <CardHeader><Heading size="sm">NVD / GitHub</Heading></CardHeader>
                <CardBody>
                  <VStack spacing={4}>
                    <FormControl>
                      <FormLabel>NVD API Key</FormLabel>
                      <Input
                        value={settings.NVD_API_KEY || ""}
                        onChange={e => updateField("NVD_API_KEY", e.target.value)}
                      />
                    </FormControl>
                    <FormControl>
                      <FormLabel>GitHub Token</FormLabel>
                      <Input
                        value={settings.GITHUB_TOKEN || ""}
                        onChange={e => updateField("GITHUB_TOKEN", e.target.value)}
                      />
                    </FormControl>
                  </VStack>
                </CardBody>
              </Card>
            </SimpleGrid>
          </TabPanel>

          <TabPanel>
            <Card>
              <CardHeader><Heading size="sm">Kali Sandbox</Heading></CardHeader>
              <CardBody>
                <Alert status="info" mb={4}>
                  <AlertTriangle size={16} />
                  Sandbox functionality requires Docker. Install Docker to enable Kali-based tool execution.
                </Alert>
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                  <FormControl>
                    <FormLabel>Sandbox Image</FormLabel>
                    <Input value={settings.KALI_SANDBOX_IMAGE || "neurosploit-kali:latest"} isReadOnly />
                  </FormControl>
                  <FormControl>
                    <FormLabel>Status</FormLabel>
                    <Badge colorScheme="gray" fontSize="md" p={2}>Not Available</Badge>
                  </FormControl>
                </SimpleGrid>
              </CardBody>
            </Card>
            <Card mt={6}>
              <CardHeader><Heading size="sm">Local LLM</Heading></CardHeader>
              <CardBody>
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                  <FormControl>
                    <FormLabel>Ollama URL</FormLabel>
                    <Input
                      value={settings.OLLAMA_BASE_URL || "http://localhost:11434"}
                      onChange={e => updateField("OLLAMA_BASE_URL", e.target.value)}
                    />
                  </FormControl>
                  <FormControl>
                    <FormLabel>LM Studio URL</FormLabel>
                    <Input
                      value={settings.LMSTUDIO_BASE_URL || "http://localhost:1234"}
                      onChange={e => updateField("LMSTUDIO_BASE_URL", e.target.value)}
                    />
                  </FormControl>
                </SimpleGrid>
              </CardBody>
            </Card>
          </TabPanel>
        </TabPanels>
      </Tabs>

      <HStack justify="flex-end" mt={8}>
        <Button colorScheme="blue" onClick={handleSave} isLoading={saving} size="lg">
          Save Settings
        </Button>
      </HStack>
    </Box>
  )
}