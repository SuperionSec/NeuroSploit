import { useEffect, useMemo, useState, useCallback, useRef } from "react"
import { Link } from "react-router-dom"
import {
  Box, Heading, Text, SimpleGrid, Card, CardBody, Flex, Grid, Badge, Progress, Table, Thead, Tbody, Tr, Th, Td, Spinner, HStack,
  VStack, Divider, Tag, Container, Alert, IconButton, Select,
  useColorMode, useToast
} from "@chakra-ui/react"
import {
  Plus, Trash2, Pencil, Eye, RefreshCw, Settings,
  Info, AlertTriangle, CheckCircle2, Clock, ExternalLink
} from "lucide-react"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { ActivityFeedItem, DashboardStats } from "../../types/neurosploit"

function relativeTime(ts: string): string {
  const diff = Math.floor((Date.now() - new Date(ts).getTime()) / 1000)
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

const SEVERITY_COLORS: Record<string, string> = {
  critical: "red", high: "orange", medium: "yellow", low: "blue", info: "gray"}

const ACTIVITY_ICONS: Record<string, string> = {
  scan: "blue",
  vulnerability: "red",
  agent_task: "purple",
  report: "green"}

export function HomePage() {
  const { colorMode } = useColorMode()
  const toast = useToast()

  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [activityFeed, setActivityFeed] = useState<ActivityFeedItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [refreshing, setRefreshing] = useState(false)
  const [activityFilter, setActivityFilter] = useState<string>("all")

  const prevFindingsRef = useRef(0)
  const consecutiveErrorsRef = useRef(0)

  const fetchData = useCallback(async () => {
    try {
      const [statsData, activityData] = await Promise.all([
        neurosploitApi.dashboard.stats(),
        neurosploitApi.dashboard.activityFeed(20),
      ])
      setStats(statsData)
      setActivityFeed(activityData.activities || [])

      const totalFindings = statsData.vulnerabilities.total
      if (prevFindingsRef.current > 0 && totalFindings > prevFindingsRef.current) {
        const diff = totalFindings - prevFindingsRef.current
        toast({
          title: `${diff} new finding${diff > 1 ? "s" : ""} discovered`,
          status: "warning",
          duration: 3000,
          position: "top-right"})
      }
      prevFindingsRef.current = totalFindings

      consecutiveErrorsRef.current = 0
      setError(null)
    } catch {
      consecutiveErrorsRef.current++
      if (consecutiveErrorsRef.current >= 3) {
        setError("Connection issues detected. Retrying...")
      }
    }
  }, [toast])

  useEffect(() => {
    setLoading(true)
    fetchData().finally(() => setLoading(false))
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [fetchData])

  const handleRefresh = useCallback(async () => {
    setRefreshing(true)
    await fetchData()
    setRefreshing(false)
    toast({ title: "Dashboard refreshed", status: "info", duration: 2000, position: "top-right" })
  }, [fetchData, toast])

  const statCards = useMemo(() => {
    if (!stats) return []
    return [
      { label: "Total Scans", value: stats.scans.total, color: "blue" },
      { label: "Running", value: stats.scans.running, color: "green" },
      { label: "Completed", value: stats.scans.completed, color: "purple" },
      { label: "Total Vulns", value: stats.vulnerabilities.total, color: "red" },
      { label: "Critical", value: stats.vulnerabilities.critical, color: "red" },
      { label: "High", value: stats.vulnerabilities.high, color: "orange" },
    ]
  }, [stats])

  const severityData = useMemo(() => {
    if (!stats) return []
    return [
      { label: "Critical", value: stats.vulnerabilities.critical, color: "red" },
      { label: "High", value: stats.vulnerabilities.high, color: "orange" },
      { label: "Medium", value: stats.vulnerabilities.medium, color: "yellow" },
      { label: "Low", value: stats.vulnerabilities.low, color: "blue" },
      { label: "Info", value: stats.vulnerabilities.info, color: "gray" },
    ]
  }, [stats])

  const totalSeverity = severityData.reduce((s, d) => s + d.value, 0)

  const filteredActivity = useMemo(() => {
    if (activityFilter === "all") return activityFeed
    return activityFeed.filter((a) => a.type === activityFilter)
  }, [activityFeed, activityFilter])

  if (loading) {
    return (
      <Flex justify="center" align="center" h="64">
        <Spinner size="xl" color="blue.500" thickness="4px" />
      </Flex>
    )
  }

  return (
    <Box p={6} maxW="1400px" mx="auto">
      {error && (
        <Alert status="warning" mb={4} borderRadius="md">
          <AlertTriangle size={16} />
          {error}
        </Alert>
      )}

      <Flex justify="space-between" align="center" mb={6} flexWrap="wrap" gap={3}>
        <Box>
          <Heading size="lg" display="flex" alignItems="center" gap={2}>
            <Box as="span" fontSize="2xl">⚡</Box>
            NeuroSploit Dashboard
          </Heading>
          <Text color={colorMode === "dark" ? "gray.400" : "gray.600"} mt={1}>
            AI-Powered Penetration Testing Platform
          </Text>
        </Box>
        <HStack>
          <IconButton
            aria-label="Refresh"
            icon={<RefreshCw />}
            onClick={handleRefresh}
            isLoading={refreshing}
            variant="outline"
          />
          <Link to="/scan/new">
            <Box as="span" display="inline-flex" alignItems="center" gap={2} px={4} py={2} bg="blue.500" color="white" borderRadius="md" fontWeight="semibold" _hover={{ bg: "blue.600" }}>
              <Plus />
              New Scan
            </Box>
          </Link>
        </HStack>
      </Flex>

      <SimpleGrid columns={{ base: 2, sm: 3, lg: 6 }} spacing={4} mb={6}>
        {statCards.map((stat) => (
          <Card key={stat.label} variant="outline">
            <CardBody p={4}>
              <Flex align="center" gap={3}>
                <Box textAlign="center" flex="1">
                  <Text fontWeight="bold" fontSize="xl" color={`${stat.color}.500`}>{stat.value}</Text>
                  <Text fontSize="xs" color={colorMode === "dark" ? "gray.400" : "gray.600"}>{stat.label}</Text>
                </Box>
              </Flex>
            </CardBody>
          </Card>
        ))}
      </SimpleGrid>

      <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} gap={6} mb={6}>
        <Card variant="outline">
          <CardBody>
            <Heading size="md" mb={4}>Vulnerability Severity Distribution</Heading>
            {totalSeverity === 0 ? (
              <Text color="gray.500" textAlign="center" py={8}>No vulnerabilities yet</Text>
            ) : (
              <VStack spacing={3} align="stretch">
                {severityData.map((sev) => (
                  <Box key={sev.label}>
                    <Flex justify="space-between" mb={1}>
                      <Flex align="center" gap={2}>
                        <Box w={3} h={3} borderRadius="full" bg={`${sev.color}.500`} />
                        <Text fontSize="sm">{sev.label}</Text>
                      </Flex>
                      <Text fontSize="sm" fontWeight="bold">{sev.value} ({totalSeverity > 0 ? Math.round((sev.value / totalSeverity) * 100) : 0}%)</Text>
                    </Flex>
                    <Progress value={totalSeverity > 0 ? (sev.value / totalSeverity) * 100 : 0} colorScheme={sev.color} borderRadius="full" size="sm" />
                  </Box>
                ))}
              </VStack>
            )}
          </CardBody>
        </Card>

        <Card variant="outline">
          <CardBody>
            <Heading size="md" mb={4}>Scan Status Overview</Heading>
            {stats && (
              <VStack spacing={3} align="stretch">
                {[
                  { label: "Running", value: stats.scans.running, color: "green" },
                  { label: "Completed", value: stats.scans.completed, color: "purple" },
                  { label: "Stopped", value: stats.scans.stopped, color: "yellow" },
                  { label: "Failed", value: stats.scans.failed, color: "red" },
                  { label: "Pending", value: stats.scans.pending, color: "gray" },
                ].map((s) => (
                  <Flex key={s.label} justify="space-between" align="center">
                    <Flex align="center" gap={2}>
                      <Box w={3} h={3} borderRadius="full" bg={`${s.color}.500`} />
                      <Text fontSize="sm">{s.label}</Text>
                    </Flex>
                    <Badge colorScheme={s.color} fontSize="sm">{s.value}</Badge>
                  </Flex>
                ))}
              </VStack>
            )}
          </CardBody>
        </Card>
      </Grid>

      <Card variant="outline">
        <CardBody>
          <Flex justify="space-between" align="center" mb={4} flexWrap="wrap" gap={2}>
            <Heading size="md">Activity Feed</Heading>
            <HStack spacing={1}>
              {(["all", "scan", "vulnerability", "agent_task", "report"] as const).map((f) => (
                <Badge
                  key={f}
                  as="button"
                  onClick={() => setActivityFilter(f)}
                  colorScheme={activityFilter === f ? "blue" : "gray"}
                  variant={activityFilter === f ? "solid" : "outline"}
                  cursor="pointer"
                  fontSize="xs"
                  px={2}
                  py={1}
                >
                  {f === "all" ? "All" : f === "agent_task" ? "Tasks" : f === "vulnerability" ? "Vulns" : f.charAt(0).toUpperCase() + f.slice(1) + "s"}
                </Badge>
              ))}
            </HStack>
          </Flex>

          {filteredActivity.length === 0 ? (
            <Text color="gray.500" textAlign="center" py={6}>No recent activity</Text>
          ) : (
            <VStack spacing={1} align="stretch" maxH="400px" overflowY="auto">
              {filteredActivity.map((activity, idx) => (
                <Box
                  key={`${activity.type}-${activity.timestamp}-${idx}`}
                  as={Link}
                  to={activity.link}
                  p={3}
                  borderRadius="md"
                  _hover={{ bg: colorMode === "dark" ? "whiteAlpha.100" : "blackAlpha.50" }}
                  transition="background 0.2s"
                  textDecoration="none"
                >
                  <Flex gap={3}>
                    <Badge
                      colorScheme={ACTIVITY_ICONS[activity.type] || "gray"}
                      variant="subtle"
                      fontSize="xs"
                      h="fit-content"
                      mt={1}
                    >
                      {activity.type.replace("_", " ")}
                    </Badge>
                    <Box flex={1} minW={0}>
                      <Flex align="center" gap={2} mb={0.5}>
                        <Text fontSize="xs" color="gray.500" textTransform="uppercase">
                          {activity.type.replace("_", " ")}
                        </Text>
                        <Text fontSize="xs" color="gray.600">{activity.action}</Text>
                      </Flex>
                      <Text fontWeight="medium" noOfLines={1}>{activity.title}</Text>
                      {activity.description && (
                        <Text fontSize="sm" color="gray.500" noOfLines={1}>{activity.description}</Text>
                      )}
                    </Box>
                    <Flex direction="column" align="flex-end" gap={1} flexShrink={0}>
                      {activity.severity && (
                        <Badge colorScheme={SEVERITY_COLORS[activity.severity]} fontSize="xs">{activity.severity}</Badge>
                      )}
                      {activity.status && !activity.severity && (
                        <Badge
                          fontSize="xs"
                          colorScheme={
                            activity.status === "completed" ? "green"
                            : activity.status === "running" ? "blue"
                            : activity.status === "failed" ? "red"
                            : activity.status === "stopped" ? "yellow"
                            : "gray"
                          }
                        >
                          {activity.status}
                        </Badge>
                      )}
                      <Text fontSize="xs" color="gray.500">{relativeTime(activity.timestamp)}</Text>
                    </Flex>
                  </Flex>
                </Box>
              ))}
            </VStack>
          )}
        </CardBody>
      </Card>
    </Box>
  )
}