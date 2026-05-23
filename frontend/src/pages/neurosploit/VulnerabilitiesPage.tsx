import { useState, useEffect, useCallback, useMemo } from "react"
import {
  Box, Heading, Text, Card, CardBody, Flex, Grid, Button, Badge, Progress,
  Table, Thead, Tbody, Tr, Th, Td, Select, Input, HStack, VStack, Spinner,
  Divider, Alert, AlertIcon, useColorMode, useToast, Code, IconButton,
  Collapse
} from "@chakra-ui/react"
import {
  ChevronDown, ChevronUp, Eye, Search
} from "lucide-react"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { VulnerabilityPublic } from "../../types/neurosploit"

const SEVERITY_COLORS: Record<string, string> = {
  critical: "red", high: "orange", medium: "yellow", low: "blue", info: "gray",
}

const SEVERITY_ORDER: Record<string, number> = {
  critical: 0, high: 1, medium: 2, low: 3, info: 4,
}

export function VulnerabilitiesPage() {
  const { colorMode } = useColorMode()
  const toast = useToast()

  const [vulnerabilities, setVulnerabilities] = useState<VulnerabilityPublic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [severityFilter, setSeverityFilter] = useState("")
  const [typeFilter, setTypeFilter] = useState("")
  const [searchQuery, setSearchQuery] = useState("")
  const [expandedId, setExpandedId] = useState<string | null>(null)
  const [page, setPage] = useState(1)

  const fetchVulnerabilities = useCallback(async () => {
    try {
      const data = await neurosploitApi.vulnerabilities.list()
      const vulns = Array.isArray(data) ? data : data.vulnerabilities || data.types || []
      setVulnerabilities(vulns.map((v: Record<string, unknown>) => ({
        ...v,
        severity: v.severity || "info",
        vulnerability_type: v.vulnerability_type || "unknown",
        title: v.title || "Untitled",
        id: v.id || String(Math.random()),
        cvss_score: v.cvss_score ?? null,
      })) as VulnerabilityPublic[])
      setError(null)
    } catch {
      setError("Failed to load vulnerabilities")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    setLoading(true)
    fetchVulnerabilities()
    const interval = setInterval(fetchVulnerabilities, 15000)
    return () => clearInterval(interval)
  }, [fetchVulnerabilities])

  const uniqueTypes = useMemo(() => {
    const types = new Set(vulnerabilities.map((v) => v.vulnerability_type).filter(Boolean))
    return Array.from(types).sort()
  }, [vulnerabilities])

  const filteredVulns = useMemo(() => {
    let result = [...vulnerabilities]
    if (severityFilter) {
      result = result.filter((v) => v.severity === severityFilter)
    }
    if (typeFilter) {
      result = result.filter((v) => v.vulnerability_type === typeFilter)
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase()
      result = result.filter(
        (v) =>
          v.title.toLowerCase().includes(q) ||
          v.vulnerability_type.toLowerCase().includes(q) ||
          (v.affected_endpoint && v.affected_endpoint.toLowerCase().includes(q))
      )
    }
    result.sort((a, b) => (SEVERITY_ORDER[a.severity] ?? 99) - (SEVERITY_ORDER[b.severity] ?? 99))
    return result
  }, [vulnerabilities, severityFilter, typeFilter, searchQuery])

  const toggleExpand = useCallback((id: string) => {
    setExpandedId((prev) => (prev === id ? null : id))
  }, [])

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
        <Alert status="error" mb={4} borderRadius="md">
          <AlertIcon />
          {error}
        </Alert>
      )}

      <Flex justify="space-between" align="center" mb={6} flexWrap="wrap" gap={3}>
        <Box>
          <Heading size="lg">Vulnerabilities</Heading>
          <Text color={colorMode === "dark" ? "gray.400" : "gray.600"} mt={1}>
            Browse and filter all discovered vulnerabilities
          </Text>
        </Box>
      </Flex>

      <Card variant="outline" mb={6}>
        <CardBody>
          <Flex gap={3} flexWrap="wrap">
            <Box minW="200px">
              <Select
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
                placeholder="All severities"
                size="sm"
              >
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
                <option value="info">Info</option>
              </Select>
            </Box>

            <Box minW="200px">
              <Select
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value)}
                placeholder="All types"
                size="sm"
              >
                {uniqueTypes.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </Select>
            </Box>

            <Box flex={1} minW="200px">
              <Input
                placeholder="Search vulnerabilities..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                size="sm"
              />
            </Box>

            <Text fontSize="sm" color="gray.500" alignSelf="center">
              {filteredVulns.length} result{filteredVulns.length !== 1 ? "s" : ""}
            </Text>
          </Flex>
        </CardBody>
      </Card>

      {filteredVulns.length === 0 ? (
        <Card variant="outline">
          <CardBody>
            <VStack spacing={3} py={8} textAlign="center">
              <Search boxSize={8} color="gray.400" />
              <Text color="gray.500">No vulnerabilities match your filters</Text>
              {severityFilter || typeFilter || searchQuery ? (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => { setSeverityFilter(""); setTypeFilter(""); setSearchQuery("") }}
                >
                  Clear Filters
                </Button>
              ) : null}
            </VStack>
          </CardBody>
        </Card>
      ) : (
        <VStack spacing={2} align="stretch">
          {filteredVulns.map((vuln) => (
            <Card key={vuln.id} variant="outline" size="sm">
              <CardBody p={0}>
                <Flex
                  p={3}
                  justify="space-between"
                  align="start"
                  cursor="pointer"
                  onClick={() => toggleExpand(vuln.id)}
                  _hover={{ bg: colorMode === "dark" ? "whiteAlpha.50" : "blackAlpha.50" }}
                  gap={3}
                  flexWrap="wrap"
                >
                  <Box flex={1} minW={0}>
                    <Flex align="center" gap={2} mb={1} flexWrap="wrap">
                      <Badge colorScheme={SEVERITY_COLORS[vuln.severity] || "gray"} fontSize="xs">
                        {vuln.severity}
                      </Badge>
                      <Text fontWeight="medium" fontSize="sm" noOfLines={1}>{vuln.title}</Text>
                      {vuln.confidence_score != null && (
                        <Badge
                          colorScheme={vuln.confidence_score >= 90 ? "green" : vuln.confidence_score >= 60 ? "yellow" : "red"}
                          fontSize="xs"
                        >
                          {vuln.confidence_score}%
                        </Badge>
                      )}
                    </Flex>
                    <Flex gap={2} fontSize="xs" color="gray.500" flexWrap="wrap">
                      <Text>{vuln.vulnerability_type}</Text>
                      {vuln.cwe_id && <Text>• {vuln.cwe_id}</Text>}
                      {vuln.cvss_score && <Text>• CVSS {vuln.cvss_score}</Text>}
                      {vuln.affected_endpoint && (
                        <Text noOfLines={1} maxW="300px">• {vuln.affected_endpoint}</Text>
                      )}
                    </Flex>
                  </Box>
                  <IconButton
                    aria-label="Toggle details"
                    icon={expandedId === vuln.id ? <ChevronUp /> : <ChevronDown />}
                    size="xs"
                    variant="ghost"
                    onClick={(e) => { e.stopPropagation(); toggleExpand(vuln.id) }}
                  />
                </Flex>

                <Collapse in={expandedId === vuln.id}>
                  <Box p={4} borderTopWidth={1}>
                    <VStack spacing={3} align="stretch">
                      {vuln.description && (
                        <Box>
                          <Text fontWeight="medium" fontSize="sm" mb={1}>Description</Text>
                          <Text fontSize="sm" color="gray.500">{vuln.description}</Text>
                        </Box>
                      )}

                      {vuln.poc_evidence && (
                        <Box>
                          <Text fontWeight="medium" fontSize="sm" mb={1}>Proof of Concept</Text>
                          <Code p={2} borderRadius="md" fontSize="xs" whiteSpace="pre-wrap" display="block">
                            {vuln.poc_evidence}
                          </Code>
                        </Box>
                      )}

                      {vuln.poc_payload && (
                        <Box>
                          <Text fontWeight="medium" fontSize="sm" mb={1}>Payload</Text>
                          <Code p={2} borderRadius="md" fontSize="xs" whiteSpace="pre-wrap" display="block">
                            {vuln.poc_payload}
                          </Code>
                        </Box>
                      )}

                      {vuln.confidence_breakdown && Object.keys(vuln.confidence_breakdown).length > 0 && (
                        <Box>
                          <Text fontWeight="medium" fontSize="sm" mb={1}>Confidence Breakdown</Text>
                          {Object.entries(vuln.confidence_breakdown).map(([key, val]) => (
                            <Flex key={key} justify="space-between" mb={1}>
                              <Text fontSize="xs" color="gray.500">{key}</Text>
                              <Text fontSize="xs" fontWeight="bold">{val}</Text>
                            </Flex>
                          ))}
                        </Box>
                      )}

                      {vuln.remediation && (
                        <Box>
                          <Text fontWeight="medium" fontSize="sm" mb={1}>Remediation</Text>
                          <Text fontSize="sm" color="gray.500">{vuln.remediation}</Text>
                        </Box>
                      )}

                      {vuln.impact && (
                        <Box>
                          <Text fontWeight="medium" fontSize="sm" mb={1}>Impact</Text>
                          <Text fontSize="sm" color="gray.500">{vuln.impact}</Text>
                        </Box>
                      )}

                      {vuln.references && vuln.references.length > 0 && (
                        <Box>
                          <Text fontWeight="medium" fontSize="sm" mb={1}>References</Text>
                          <VStack spacing={0} align="start">
                            {vuln.references.map((ref: string, i: number) => (
                              <Text key={i} fontSize="xs" color="blue.500">{ref}</Text>
                            ))}
                          </VStack>
                        </Box>
                      )}
                    </VStack>
                  </Box>
                </Collapse>
              </CardBody>
            </Card>
          ))}
        </VStack>
      )}
    </Box>
  )
}