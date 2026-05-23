import { useColorMode } from "../../hooks/useColorMode"
import { useToast } from "../../hooks/useToast"
import { useState, useEffect, useCallback, useMemo } from "react"
import {
  Box, Heading, Text, Card, CardBody, Flex, Grid, Button, Badge, Progress,
  Input, FormControl, FormLabel, HStack, VStack, Spinner, Divider,
  Alert, Code, Tabs, TabList, Tab,
  TabPanels, TabPanel, Select, SimpleGrid,
  Collapse, Tooltip
} from "@chakra-ui/react"
import {
  Plus, ChevronDown, ChevronUp, Info, Search
} from "lucide-react"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { VulnTypeCategoryPublic, VulnLabChallengePublic, VulnLabStats } from "../../types/neurosploit"

const SEVERITY_COLORS: Record<string, string> = {
  critical: "red", high: "orange", medium: "yellow", low: "blue", info: "gray"}

const CATEGORY_TABS = [
  "All",
  "Injection",
  "Authentication",
  "XSS",
  "SSRF",
  "File Inclusion",
  "Information Disclosure",
  "Configuration",
  "Business Logic",
  "Cryptography",
]

export function VulnLabPage() {
  const { colorMode } = useColorMode()
  const toast = useToast()

  const [categories, setCategories] = useState<Record<string, VulnTypeCategoryPublic>>({})
  const [challenges, setChallenges] = useState<VulnLabChallengePublic[]>([])
  const [stats, setStats] = useState<VulnLabStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeCategory, setActiveCategory] = useState("All")
  const [searchFilter, setSearchFilter] = useState("")
  const [expandedCat, setExpandedCat] = useState<string | null>(null)
  const [targetUrl, setTargetUrl] = useState("")
  const [isRunning, setIsRunning] = useState(false)
  const [runningType, setRunningType] = useState<string | null>(null)
  const [runningChallengeId, setRunningChallengeId] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    try {
      const [typesData, challengesData, statsData] = await Promise.all([
        neurosploitApi.vulnLab.getTypes(),
        neurosploitApi.vulnLab.listChallenges({ limit: 50 }),
        neurosploitApi.vulnLab.getStats(),
      ])
      setCategories(typesData.categories || {})
      setChallenges(challengesData.challenges || [])
      setStats(statsData)
      setError(null)
    } catch {
      setError("Failed to load vulnerability lab data")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    setLoading(true)
    fetchData()
  }, [fetchData])

  useEffect(() => {
    if (!runningChallengeId || !isRunning) return
    const poll = setInterval(async () => {
      try {
        const status = await neurosploitApi.vulnLab.getChallenge(runningChallengeId)
        if (["completed", "failed", "stopped", "error"].includes(status.status)) {
          setIsRunning(false)
          clearInterval(poll)
          fetchData()
          if (status.status === "completed") {
            toast({
              title: status.result === "detected" ? "Vulnerability detected!" : "Test completed",
              status: status.result === "detected" ? "success" : "info",
              duration: 4000,
              position: "top-right"})
          }
        }
      } catch {
        // ignore
      }
    }, 3000)
    return () => clearInterval(poll)
  }, [runningChallengeId, isRunning, toast, fetchData])

  const handleRun = useCallback(async (vulnType: string) => {
    if (!targetUrl.trim()) {
      toast({ title: "Target URL is required", status: "error", duration: 3000, position: "top-right" })
      return
    }
    setIsRunning(true)
    setRunningType(vulnType)
    try {
      const resp = await neurosploitApi.vulnLab.run({
        target_url: targetUrl.trim(),
        vuln_type: vulnType})
      setRunningChallengeId(resp.challenge_id)
      toast({ title: `Testing ${vulnType}...`, status: "info", duration: 3000, position: "top-right" })
    } catch (err: unknown) {
      const errObj = err as { response?: { data?: { detail?: string } } }
      toast({
        title: errObj?.response?.data?.detail || "Failed to start test",
        status: "error",
        duration: 3000,
        position: "top-right"})
      setIsRunning(false)
    }
  }, [targetUrl, toast])

  const filteredCategories = useMemo(() => {
    const entries = Object.entries(categories)
    if (activeCategory === "All") {
      return entries.map(([key, cat]) => ({
        key,
        ...cat,
        types: searchFilter
          ? cat.types.filter(
              (t) =>
                t.key.toLowerCase().includes(searchFilter.toLowerCase()) ||
                t.title.toLowerCase().includes(searchFilter.toLowerCase())
            )
          : cat.types})).filter((c) => c.types.length > 0)
    }
    const matchEntries = entries.filter(([key]) =>
      key.toLowerCase().includes(activeCategory.toLowerCase())
    )
    return matchEntries.map(([key, cat]) => ({
      key,
      ...cat,
      types: searchFilter
        ? cat.types.filter(
            (t) =>
              t.key.toLowerCase().includes(searchFilter.toLowerCase()) ||
              t.title.toLowerCase().includes(searchFilter.toLowerCase())
          )
        : cat.types})).filter((c) => c.types.length > 0)
  }, [categories, activeCategory, searchFilter])

  const totalTypes = useMemo(() => {
    let count = 0
    Object.values(categories).forEach((cat) => { count += cat.types?.length || 0 })
    return count
  }, [categories])

  if (loading) {
    return (
      <Flex justify="center" align="center" h="64">
        <Spinner size="xl" color="purple.500" thickness="4px" />
      </Flex>
    )
  }

  return (
    <Box p={6} maxW="1400px" mx="auto">
      {error && (
        <Alert status="error" mb={4} borderRadius="md">
          <AlertTriangle size={16} />
          {error}
        </Alert>
      )}

      <Flex justify="space-between" align="center" mb={4} flexWrap="wrap" gap={3}>
        <Box>
          <Heading size="lg">Vulnerability Lab</Heading>
          <Text color={colorMode === "dark" ? "gray.400" : "gray.600"} mt={1}>
            {totalTypes} vulnerability types across {Object.keys(categories).length} categories
          </Text>
        </Box>
      </Flex>

      {stats && stats.total > 0 && (
        <SimpleGrid columns={{ base: 2, md: 4 }} spacing={4} mb={6}>
          {[
            { label: "Total Tests", value: stats.total, color: "purple" },
            { label: "Running", value: stats.running, color: "blue" },
            { label: "Detection Rate", value: `${stats.detection_rate}%`, color: "green" },
            { label: "Detected", value: stats.result_counts?.detected || 0, color: "green" },
          ].map((s) => (
            <Card key={s.label} variant="outline">
              <CardBody p={4}>
                <Box textAlign="center" flex="1">
                  <Text fontWeight="bold" fontSize="xl" color={`${s.color}.500`}>
                    {s.value}
                  </Text>
                  <Text fontSize="xs">{s.label}</Text>
                </Box>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>
      )}

      <Card variant="outline" mb={6}>
        <CardBody>
          <FormControl mb={4}>
            <FormLabel>Target URL</FormLabel>
            <Input
              placeholder="https://lab.example.com/vuln-page"
              value={targetUrl}
              onChange={(e) => setTargetUrl(e.target.value)}
              isDisabled={isRunning}
              size="md"
            />
          </FormControl>

          {isRunning && (
            <Alert status="info" mb={4} borderRadius="md">
              <Spinner size="sm" mr={2} />
              Testing: {runningType}
            </Alert>
          )}
        </CardBody>
      </Card>

      <Box mb={4}>
        <Flex gap={2} flexWrap="wrap" mb={3}>
          {CATEGORY_TABS.map((cat) => (
            <Badge
              key={cat}
              as="button"
              onClick={() => { setActiveCategory(cat); setExpandedCat(null) }}
              colorScheme={activeCategory === cat ? "purple" : "gray"}
              variant={activeCategory === cat ? "solid" : "outline"}
              cursor="pointer"
              px={3}
              py={1.5}
              fontSize="sm"
            >
              {cat}
            </Badge>
          ))}
        </Flex>

        <Input
          placeholder="Search vulnerability types..."
          value={searchFilter}
          onChange={(e) => setSearchFilter(e.target.value)}
          size="sm"
          maxW="400px"
        />
      </Box>

      <VStack spacing={3} align="stretch">
        {filteredCategories.map((cat) => (
          <Card key={cat.key} variant="outline">
            <CardBody p={0}>
              <Flex
                p={3}
                justify="space-between"
                align="center"
                cursor="pointer"
                onClick={() => setExpandedCat(expandedCat === cat.key ? null : cat.key)}
                _hover={{ bg: colorMode === "dark" ? "whiteAlpha.50" : "blackAlpha.50" }}
              >
                <Flex align="center" gap={2}>
                  <Heading size="sm">{cat.label}</Heading>
                  <Badge colorScheme="purple" fontSize="xs">{cat.types.length} types</Badge>
                </Flex>
                <ChevronDown
                  transform={expandedCat === cat.key ? "rotate(180deg)" : undefined}
                  transition="transform 0.2s"
                />
              </Flex>

              <Collapse in={expandedCat === cat.key}>
                <Divider />
                <Box p={3}>
                  <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={2}>
                    {cat.types.map((vtype) => (
                      <Card key={vtype.key} variant="outline" size="sm">
                        <CardBody p={3}>
                          <Flex justify="space-between" align="start" gap={2}>
                            <Box flex={1} minW={0}>
                              <Flex align="center" gap={2} mb={1} flexWrap="wrap">
                                <Text fontWeight="medium" fontSize="sm" noOfLines={1}>{vtype.title}</Text>
                                <Box w={2} h={2} borderRadius="full" bg={`${SEVERITY_COLORS[vtype.severity] || "gray"}.500`} />
                              </Flex>
                              <Flex gap={1} fontSize="xs" color="gray.500" flexWrap="wrap">
                                {vtype.cwe_id && <Text>{vtype.cwe_id}</Text>}
                                {vtype.description && <Text noOfLines={2}>{vtype.description}</Text>}
                              </Flex>
                            </Box>
                            <Button
                              size="xs"
                              colorScheme="purple"
                              isDisabled={isRunning || !targetUrl.trim()}
                              isLoading={isRunning && runningType === vtype.key}
                              onClick={(e) => { e.stopPropagation(); handleRun(vtype.key) }}
                              flexShrink={0}
                            >
                              Run
                            </Button>
                          </Flex>
                        </CardBody>
                      </Card>
                    ))}
                  </SimpleGrid>
                </Box>
              </Collapse>
            </CardBody>
          </Card>
        ))}
      </VStack>

      {challenges.length > 0 && (
        <Box mt={8}>
          <Heading size="md" mb={4}>Recent Challenges ({challenges.length})</Heading>
          <VStack spacing={2} align="stretch">
            {challenges.slice(0, 10).map((ch) => (
              <Card key={ch.id} variant="outline" size="sm">
                <CardBody p={3}>
                  <Flex justify="space-between" align="center" gap={3} flexWrap="wrap">
                    <Box flex={1} minW={0}>
                      <Flex align="center" gap={2} mb={1} flexWrap="wrap">
                        <Text fontWeight="medium" fontSize="sm" noOfLines={1}>
                          {ch.challenge_name || ch.vuln_type}
                        </Text>
                        <Badge
                          colorScheme={
                            ch.status === "completed" ? "green"
                            : ch.status === "running" ? "blue"
                            : ch.status === "failed" ? "red"
                            : "gray"
                          }
                          fontSize="xs"
                        >
                          {ch.status}
                        </Badge>
                        {ch.result && (
                          <Badge
                            colorScheme={ch.result === "detected" ? "green" : ch.result === "not_detected" ? "red" : "yellow"}
                            fontSize="xs"
                          >
                            {ch.result.replace("_", " ")}
                          </Badge>
                        )}
                      </Flex>
                      <Flex gap={2} fontSize="xs" color="gray.500" flexWrap="wrap">
                        <Text noOfLines={1} maxW="300px">{ch.target_url}</Text>
                        {ch.findings_count > 0 && <Text>• {ch.findings_count} findings</Text>}
                      </Flex>
                    </Box>
                  </Flex>
                </CardBody>
              </Card>
            ))}
          </VStack>
        </Box>
      )}
    </Box>
  )
}