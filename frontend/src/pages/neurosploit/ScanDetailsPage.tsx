import { useState, useEffect, useCallback, useMemo } from "react"
import { useParams, useNavigate } from "react-router-dom"
import {
  Box, Heading, Text, Card, CardBody, Flex, Grid, Button, Badge, Progress,
  Table, Thead, Tbody, Tr, Th, Td, HStack, VStack, Spinner, Divider,
  Alert, useColorMode, useToast, IconButton, Code, Tabs,
  TabList, Tab, TabPanels, TabPanel
} from "@chakra-ui/react"
import {
  RefreshCw, Info, AlertTriangle, CheckCircle2, Eye
} from "lucide-react"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { ScanPublic, EndpointPublic, VulnerabilityPublic, ScanAgentTask } from "../../types/neurosploit"

const SEVERITY_COLORS: Record<string, string> = {
  critical: "red", high: "orange", medium: "yellow", low: "blue", info: "gray"}

export function ScanDetailsPage() {
  const { scanId } = useParams<{ scanId: string }>()
  const navigate = useNavigate()
  const { colorMode } = useColorMode()
  const toast = useToast()

  const [scan, setScan] = useState<ScanPublic | null>(null)
  const [endpoints, setEndpoints] = useState<EndpointPublic[]>([])
  const [vulnerabilities, setVulnerabilities] = useState<VulnerabilityPublic[]>([])
  const [tasks, setTasks] = useState<ScanAgentTask[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [vulnSeverityFilter, setVulnSeverityFilter] = useState("")
  const [currentTab, setCurrentTab] = useState(0)

  const fetchScan = useCallback(async () => {
    if (!scanId) return
    try {
      const data = await neurosploitApi.scans.get(scanId)
      setScan(data)
      setError(null)
    } catch {
      setError("Failed to load scan")
    }
  }, [scanId])

  const fetchEndpoints = useCallback(async () => {
    if (!scanId) return
    try {
      const data = await neurosploitApi.scans.getEndpoints(scanId, 1, 100)
      setEndpoints(data.endpoints || [])
    } catch {
      // ignore
    }
  }, [scanId])

  const fetchVulnerabilities = useCallback(async () => {
    if (!scanId) return
    try {
      const data = await neurosploitApi.scans.getVulnerabilities(scanId, vulnSeverityFilter || undefined, 1, 100)
      setVulnerabilities(data.vulnerabilities || data || [])
    } catch {
      // ignore
    }
  }, [scanId, vulnSeverityFilter])

  useEffect(() => {
    setLoading(true)
    Promise.all([fetchScan(), fetchEndpoints(), fetchVulnerabilities()]).finally(() => setLoading(false))
    const interval = setInterval(() => {
      fetchScan()
      fetchEndpoints()
      fetchVulnerabilities()
    }, 5000)
    return () => clearInterval(interval)
  }, [fetchScan, fetchEndpoints, fetchVulnerabilities])

  const handleAction = useCallback(async (action: "start" | "stop" | "pause" | "resume") => {
    if (!scanId) return
    try {
      await neurosploitApi.scans[action](scanId)
      toast({ title: `Scan ${action}ed`, status: "info", duration: 2000, position: "top-right" })
      fetchScan()
    } catch {
      toast({ title: `Failed to ${action} scan`, status: "error", duration: 2000, position: "top-right" })
    }
  }, [scanId, toast, fetchScan])

  const confidenceBadge = useCallback((score: number | null | undefined) => {
    if (score == null) return null
    const colorScheme = score >= 90 ? "green" : score >= 60 ? "yellow" : "red"
    return <Badge colorScheme={colorScheme} fontSize="xs">{score}</Badge>
  }, [])

  if (loading) {
    return (
      <Flex justify="center" align="center" h="64">
        <Spinner size="xl" color="blue.500" thickness="4px" />
      </Flex>
    )
  }

  if (error || !scan) {
    return (
      <Flex justify="center" align="center" h="64">
        <Alert status="error" borderRadius="md">
          <AlertTriangle size={16} />
          {error || "Scan not found"}
        </Alert>
      </Flex>
    )
  }

  return (
    <Box p={6} maxW="1400px" mx="auto">
      <Flex justify="space-between" align="center" mb={4} flexWrap="wrap" gap={3}>
        <Box>
          <Heading size="lg">{scan.name || "Scan Details"}</Heading>
          <Flex gap={2} mt={1} flexWrap="wrap">
            <Badge colorScheme={scan.status === "running" ? "green" : scan.status === "completed" ? "blue" : scan.status === "failed" ? "red" : scan.status === "paused" ? "yellow" : "gray"}>
              {scan.status}
            </Badge>
            <Badge colorScheme="purple" variant="outline">{scan.scan_type}</Badge>
            {scan.current_phase && <Badge colorScheme="cyan">{scan.current_phase}</Badge>}
          </Flex>
        </Box>

        <HStack>
          {scan.status === "pending" && (
            <Button colorScheme="green" leftIcon={<RefreshCw />} size="sm" onClick={() => handleAction("start")}>Start</Button>
          )}
          {scan.status === "running" && (
            <>
              <Button colorScheme="yellow" leftIcon={<Info />} size="sm" onClick={() => handleAction("pause")}>Pause</Button>
              <Button colorScheme="red" leftIcon={<AlertTriangle />} size="sm" onClick={() => handleAction("stop")}>Stop</Button>
            </>
          )}
          {scan.status === "paused" && (
            <Button colorScheme="green" leftIcon={<RefreshCw />} size="sm" onClick={() => handleAction("resume")}>Resume</Button>
          )}
          <Button variant="outline" size="sm" onClick={() => { fetchScan(); fetchEndpoints(); fetchVulnerabilities() }}>
            <RefreshCw mr={1} />Refresh
          </Button>
        </HStack>
      </Flex>

      {scan.status === "running" && (
        <Box mb={6}>
          <Flex justify="space-between" mb={1}>
            <Text fontSize="sm">Progress</Text>
            <Text fontSize="sm" fontWeight="bold">{scan.progress}%</Text>
          </Flex>
          <Progress value={scan.progress} colorScheme="blue" borderRadius="full" size="sm" hasStripe isAnimated />
        </Box>
      )}

      <Grid templateColumns={{ base: "1fr", md: "repeat(6, 1fr)" }} gap={4} mb={6}>
        {[
          { label: "Endpoints", value: scan.total_endpoints, color: "blue" },
          { label: "Vulnerabilities", value: scan.total_vulnerabilities, color: "red" },
          { label: "Critical", value: scan.critical_count, color: "red" },
          { label: "High", value: scan.high_count, color: "orange" },
          { label: "Medium", value: scan.medium_count, color: "yellow" },
          { label: "Low", value: scan.low_count, color: "blue" },
        ].map((s) => (
          <Card key={s.label} variant="outline">
            <CardBody p={3} textAlign="center">
              <Box textAlign="center" flex="1">
                <Text fontWeight="bold" fontSize="xl" color={`${s.color}.500`}>{s.value}</Text>
                <Text fontSize="xs">{s.label}</Text>
              </Box>
            </CardBody>
          </Card>
        ))}
      </Grid>

      <Tabs variant="enclosed" colorScheme="blue" index={currentTab} onChange={setCurrentTab}>
        <TabList mb={4}>
          <Tab>Overview</Tab>
          <Tab>Findings ({vulnerabilities.length})</Tab>
          <Tab>Endpoints ({endpoints.length})</Tab>
          <Tab>Tasks ({tasks.length})</Tab>
        </TabList>

        <TabPanels>
          <TabPanel p={0}>
            <Card variant="outline">
              <CardBody>
                <VStack spacing={3} align="stretch">
                  <Flex justify="space-between">
                    <Text fontWeight="medium">Created</Text>
                    <Text color="gray.500">{new Date(scan.created_at).toLocaleString()}</Text>
                  </Flex>
                  {scan.started_at && (
                    <Flex justify="space-between">
                      <Text fontWeight="medium">Started</Text>
                      <Text color="gray.500">{new Date(scan.started_at).toLocaleString()}</Text>
                    </Flex>
                  )}
                  {scan.completed_at && (
                    <Flex justify="space-between">
                      <Text fontWeight="medium">Completed</Text>
                      <Text color="gray.500">{new Date(scan.completed_at).toLocaleString()}</Text>
                    </Flex>
                  )}
                  {scan.targets && scan.targets.length > 0 && (
                    <>
                      <Divider />
                      <Text fontWeight="medium">Targets</Text>
                      {scan.targets.map((t: { url: string }, i: number) => (
                        <Text key={i} fontSize="sm" color="gray.500">• {t.url}</Text>
                      ))}
                    </>
                  )}
                </VStack>
              </CardBody>
            </Card>
          </TabPanel>

          <TabPanel p={0}>
            <VStack spacing={2} align="stretch">
              <Flex gap={2} mb={2} flexWrap="wrap">
                <Text fontSize="sm" fontWeight="medium">Severity:</Text>
                {["", "critical", "high", "medium", "low", "info"].map((s) => (
                  <Badge
                    key={s || "all"}
                    as="button"
                    onClick={() => { setVulnSeverityFilter(s); setCurrentTab(1) }}
                    colorScheme={vulnSeverityFilter === s ? "blue" : SEVERITY_COLORS[s] || "gray"}
                    variant={vulnSeverityFilter === s ? "solid" : "outline"}
                    fontSize="xs"
                    cursor="pointer"
                  >
                    {s || "All"}
                  </Badge>
                ))}
              </Flex>

              {vulnerabilities.length === 0 ? (
                <Text color="gray.500" textAlign="center" py={6}>No findings yet</Text>
              ) : (
                vulnerabilities.map((vuln) => (
                  <Card key={vuln.id} variant="outline" size="sm">
                    <CardBody p={3}>
                      <Flex justify="space-between" align="start" gap={2} flexWrap="wrap">
                        <Box flex={1} minW={0}>
                          <Flex align="center" gap={2} mb={1}>
                            <Badge colorScheme={SEVERITY_COLORS[vuln.severity] || "gray"} fontSize="xs">
                              {vuln.severity}
                            </Badge>
                            <Text fontWeight="medium" fontSize="sm" noOfLines={1}>{vuln.title}</Text>
                            {confidenceBadge(vuln.confidence_score)}
                          </Flex>
                          <Text fontSize="xs" color="gray.500" noOfLines={1}>
                            {vuln.vulnerability_type} {vuln.affected_endpoint && `• ${vuln.affected_endpoint}`}
                          </Text>
                        </Box>
                      </Flex>
                    </CardBody>
                  </Card>
                ))
              )}
            </VStack>
          </TabPanel>

          <TabPanel p={0}>
            {endpoints.length === 0 ? (
              <Text color="gray.500" textAlign="center" py={6}>No endpoints discovered</Text>
            ) : (
              <Card variant="outline">
                <Box overflowX="auto">
                  <Table variant="simple" size="sm">
                    <Thead>
                      <Tr>
                        <Th>URL</Th>
                        <Th>Method</Th>
                        <Th>Status</Th>
                        <Th>Technologies</Th>
                      </Tr>
                    </Thead>
                    <Tbody>
                      {endpoints.map((ep) => (
                        <Tr key={ep.id}>
                          <Td fontSize="sm" maxW="400px" isTruncated>
                            <Code fontSize="xs">{ep.url}</Code>
                          </Td>
                          <Td><Badge colorScheme="blue" fontSize="xs">{ep.method}</Badge></Td>
                          <Td>
                            <Badge
                              colorScheme={ep.response_status && ep.response_status < 400 ? "green" : ep.response_status && ep.response_status < 500 ? "yellow" : "red"}
                              fontSize="xs"
                            >
                              {ep.response_status || "N/A"}
                            </Badge>
                          </Td>
                          <Td>
                            <HStack spacing={1} flexWrap="wrap">
                              {ep.technologies?.slice(0, 3).map((t, i) => (
                                <Badge key={i} variant="outline" fontSize="xs">{t}</Badge>
                              ))}
                            </HStack>
                          </Td>
                        </Tr>
                      ))}
                    </Tbody>
                  </Table>
                </Box>
              </Card>
            )}
          </TabPanel>

          <TabPanel p={0}>
            {tasks.length === 0 ? (
              <Text color="gray.500" textAlign="center" py={6}>No tasks recorded</Text>
            ) : (
              <VStack spacing={2} align="stretch">
                {tasks.map((task) => (
                  <Card key={task.id} variant="outline" size="sm">
                    <CardBody p={3}>
                      <Flex justify="space-between" align="center" gap={3}>
                        <Box flex={1} minW={0}>
                          <Flex align="center" gap={2} mb={1}>
                            <Badge
                              colorScheme={
                                task.status === "completed" ? "green"
                                : task.status === "running" ? "blue"
                                : task.status === "failed" ? "red"
                                : "gray"
                              }
                              fontSize="xs"
                            >
                              {task.status}
                            </Badge>
                            <Text fontWeight="medium" fontSize="sm">{task.task_name}</Text>
                          </Flex>
                          <Text fontSize="xs" color="gray.500">
                            {task.task_type} {task.tool_name && `• ${task.tool_name}`}
                          </Text>
                        </Box>
                        <Text fontSize="xs" color="gray.500" flexShrink={0}>
                          {task.items_found > 0 && `${task.items_found} found`}
                        </Text>
                      </Flex>
                    </CardBody>
                  </Card>
                ))}
              </VStack>
            )}
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  )
}