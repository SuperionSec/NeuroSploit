import { useState, useEffect, useCallback, useRef } from "react"
import {
  Box, Heading, Text, Card, CardBody, CardHeader, SimpleGrid, VStack, HStack,
  Button, Progress, Badge, Divider, Spinner, Alert, Code, Tag, useToast} from "@chakra-ui/react"
import { useParams, useNavigate } from "react-router-dom"
import { AlertTriangle } from "lucide-react"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { AgentStatus, AgentFinding } from "../../types/neurosploit"

export function AgentStatusPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [agent, setAgent] = useState<AgentStatus | null>(null)
  const [findings, setFindings] = useState<AgentFinding[]>([])
  const [logs, setLogs] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [stopping, setStopping] = useState(false)
  const logRef = useRef<HTMLDivElement>(null)
  const toast = useToast()

  const fetchStatus = useCallback(async () => {
    if (!id) return
    try {
      const res = await neurosploitApi.agent.status(id)
      setAgent(res.data)
      setError("")
    } catch {
      setError("Failed to fetch agent status")
    }
  }, [id])

  const fetchFindings = useCallback(async () => {
    if (!id) return
    try {
      const res = await neurosploitApi.agent.findings(id)
      setFindings(res.data)
    } catch {}
  }, [id])

  const fetchLogs = useCallback(async () => {
    if (!id) return
    try {
      const res = await neurosploitApi.agent.logs(id)
      setLogs(res.data)
    } catch {}
  }, [id])

  useEffect(() => {
    if (!id) return
    setLoading(true)
    Promise.all([fetchStatus(), fetchFindings(), fetchLogs()]).finally(() => setLoading(false))
  }, [id])

  useEffect(() => {
    if (!agent || agent.status === "completed" || agent.status === "failed" || agent.status === "stopped") return
    const timer = setInterval(() => {
      fetchStatus()
      fetchFindings()
    }, 3000)
    return () => clearInterval(timer)
  }, [agent?.status, fetchStatus, fetchFindings])

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight
    }
  }, [logs])

  const handleStop = async () => {
    if (!id) return
    try {
      setStopping(true)
      await neurosploitApi.agent.stop(id)
      toast({ title: "Agent stopped", status: "info", duration: 3000 })
      fetchStatus()
    } catch {
      toast({ title: "Failed to stop agent", status: "error", duration: 3000 })
    } finally {
      setStopping(false)
    }
  }

  const handlePause = async () => {
    if (!id) return
    try {
      await neurosploitApi.agent.pause(id)
      toast({ title: "Agent paused", status: "info", duration: 3000 })
      fetchStatus()
    } catch {
      toast({ title: "Failed to pause agent", status: "error", duration: 3000 })
    }
  }

  const handleResume = async () => {
    if (!id) return
    try {
      await neurosploitApi.agent.resume(id)
      toast({ title: "Agent resumed", status: "success", duration: 3000 })
      fetchStatus()
    } catch {
      toast({ title: "Failed to resume agent", status: "error", duration: 3000 })
    }
  }

  const handleRefreshLogs = () => fetchLogs()

  const elapsed = agent?.start_time
    ? Math.floor((Date.now() - new Date(agent.start_time).getTime()) / 1000)
    : agent?.elapsed_seconds || 0

  const formatElapsed = (s: number) => {
    const h = Math.floor(s / 3600)
    const m = Math.floor((s % 3600) / 60)
    const sec = s % 60
    if (h > 0) return `${h}h ${m}m ${sec}s`
    if (m > 0) return `${m}m ${sec}s`
    return `${sec}s`
  }

  const statusColor = (status: string) => {
    switch (status) {
      case "running": return "green"
      case "completed": return "blue"
      case "failed": case "stopped": return "red"
      case "paused": return "yellow"
      default: return "gray"
    }
  }

  if (loading) {
    return (
      <Box textAlign="center" py={20}>
        <Spinner size="xl" />
        <Text mt={4} color="gray.500">Loading agent status...</Text>
      </Box>
    )
  }

  if (error || !agent) {
    return (
      <Box textAlign="center" py={20}>
        <Alert status="error"><AlertTriangle size={16} />{error || "Agent not found"}</Alert>
        <Button mt={4} onClick={() => navigate("/neurosploit/scans")}>Back to Scans</Button>
      </Box>
    )
  }

  return (
    <Box py={6} px={4} maxW="1400px" mx="auto">
      <HStack justify="space-between" mb={6}>
        <Heading size="lg">Agent Monitor</Heading>
        <HStack>
          <Button variant="outline" onClick={() => navigate("/neurosploit/scans")}>Back to Scans</Button>
          {agent.status === "running" && (
            <>
              <Button colorScheme="yellow" onClick={handlePause}>Pause</Button>
              <Button colorScheme="red" onClick={handleStop} isLoading={stopping}>Stop</Button>
            </>
          )}
          {agent.status === "paused" && (
            <Button colorScheme="green" onClick={handleResume}>Resume</Button>
          )}
        </HStack>
      </HStack>

      <Card mb={6}>
        <CardBody>
          <Progress
            value={agent.progress}
            colorScheme={agent.status === "completed" ? "green" : agent.status === "failed" ? "red" : "blue"}
            hasStripe={agent.status === "running"}
            isAnimated={agent.status === "running"}
            size="lg"
            borderRadius="md"
            mb={4}
          />
          <HStack spacing={4} wrap="wrap">
            <Box textAlign="center" flex="1">
              <Text>Status</Text>
              <Text fontWeight="bold"><Badge colorScheme={statusColor(agent.status)} fontSize="lg" px={3} py={1}>{agent.status}</Badge></Text>
            </Box>
            <Box textAlign="center" flex="1">
              <Text>Progress</Text>
              <Text fontWeight="bold">{agent.progress}%</Text>
            </Box>
            <Box textAlign="center" flex="1">
              <Text>Phase</Text>
              <Text fontWeight="bold"><Tag size="lg">{agent.current_phase || "N/A"}</Tag></Text>
            </Box>
            <Box textAlign="center" flex="1">
              <Text>Elapsed</Text>
              <Text fontWeight="bold">{formatElapsed(elapsed)}</Text>
            </Box>
            <Box textAlign="center" flex="1">
              <Text>Findings</Text>
              <Text fontWeight="bold">{agent.findings_count}</Text>
            </Box>
          </HStack>
        </CardBody>
      </Card>

      <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={6}>
        <Card>
          <CardHeader><Heading size="md">Findings ({findings.length})</Heading></CardHeader>
          <CardBody maxH="500px" overflowY="auto">
            {findings.length === 0 ? (
              <Text color="gray.500" textAlign="center" py={8}>No findings yet</Text>
            ) : (
              <VStack spacing={3} align="stretch">
                {findings.map((f, i) => (
                  <Card key={f.id || i} variant="outline">
                    <CardBody py={3}>
                      <HStack justify="space-between" mb={1}>
                        <Text fontWeight="bold">{f.title}</Text>
                        <Badge colorScheme={
                          f.severity === "critical" ? "red" :
                          f.severity === "high" ? "orange" :
                          f.severity === "medium" ? "yellow" : "green"
                        }>{f.severity}</Badge>
                      </HStack>
                      <HStack spacing={4} fontSize="sm" color="gray.500">
                        <Text>{f.vulnerability_type}</Text>
                        <Text>Confidence: {f.confidence_score}%</Text>
                        <Badge variant="outline" colorScheme={f.validation_status === "ai_confirmed" ? "green" : "yellow"}>
                          {f.validation_status}
                        </Badge>
                      </HStack>
                      {f.endpoint && <Text fontSize="xs" color="gray.400" mt={1}>{f.endpoint}</Text>}
                    </CardBody>
                  </Card>
                ))}
              </VStack>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <HStack justify="space-between">
              <Heading size="md">Logs</Heading>
              <Button size="sm" variant="ghost" onClick={handleRefreshLogs}>Refresh</Button>
            </HStack>
          </CardHeader>
          <CardBody>
            <Box
              ref={logRef}
              bg="gray.900"
              _light={{ bg: "gray.100" }}
              borderRadius="md"
              p={4}
              maxH="500px"
              overflowY="auto"
              fontFamily="monospace"
              fontSize="sm"
            >
              {logs.length === 0 ? (
                <Text color="gray.500">No log entries</Text>
              ) : (
                logs.map((line, i) => (
                  <Text
                    key={i}
                    color={line.includes("ERROR") || line.includes("FAIL") ? "red.300" :
                           line.includes("WARN") ? "yellow.300" :
                           line.includes("FOUND") || line.includes("SUCCESS") ? "green.300" :
                           "gray.300"}
                    _light={{
                      color: line.includes("ERROR") || line.includes("FAIL") ? "red.700" :
                             line.includes("WARN") ? "yellow.700" :
                             line.includes("FOUND") || line.includes("SUCCESS") ? "green.700" :
                             "gray.700"
                    }}
                  >
                    {line}
                  </Text>
                ))
              )}
            </Box>
          </CardBody>
        </Card>
      </SimpleGrid>
    </Box>
  )
}