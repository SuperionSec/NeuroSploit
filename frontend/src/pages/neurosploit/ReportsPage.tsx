import { useState, useEffect, useCallback, useMemo } from "react"
import {
  Box, Heading, Text, Card, CardBody, Flex, Button, Badge, Select,
  HStack, VStack, Spinner, Divider, Alert, AlertIcon, useColorMode,
  useToast, IconButton, Modal, ModalOverlay, ModalContent, ModalHeader,
  ModalBody, ModalFooter, FormControl, FormLabel, Input
} from "@chakra-ui/react"
import {
  DownloadIcon, DeleteIcon, ViewIcon, RepeatIcon, AddIcon, ExternalLinkIcon
} from "@chakra-ui/icons"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { ReportPublic } from "../../types/neurosploit"

function relativeTime(ts: string): string {
  const diff = Math.floor((Date.now() - new Date(ts).getTime()) / 1000)
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

const FORMAT_STYLE: Record<string, { color: string; label: string }> = {
  html: { color: "blue", label: "HTML" },
  json: { color: "green", label: "JSON" },
  pdf: { color: "red", label: "PDF" },
}

export default function NeuroSploitReportsPage() {
  const { colorMode } = useColorMode()
  const toast = useToast()

  const [reports, setReports] = useState<ReportPublic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [formatFilter, setFormatFilter] = useState("all")
  const [showGenerateModal, setShowGenerateModal] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null)
  const [generating, setGenerating] = useState(false)
  const [generateScanId, setGenerateScanId] = useState("")
  const [generateFormat, setGenerateFormat] = useState("html")
  const [generateTitle, setGenerateTitle] = useState("")

  const fetchReports = useCallback(async () => {
    try {
      const data = await neurosploitApi.reports.list()
      setReports(data.reports || [])
      setError(null)
    } catch {
      setError("Failed to load reports")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    setLoading(true)
    fetchReports()
    const interval = setInterval(fetchReports, 30000)
    return () => clearInterval(interval)
  }, [fetchReports])

  const filteredReports = useMemo(() => {
    let result = [...reports]
    if (formatFilter !== "all") {
      result = result.filter((r) => r.format === formatFilter)
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase()
      result = result.filter(
        (r) =>
          (r.title || "").toLowerCase().includes(q) ||
          r.format.toLowerCase().includes(q)
      )
    }
    result.sort((a, b) => new Date(b.generated_at).getTime() - new Date(a.generated_at).getTime())
    return result
  }, [reports, formatFilter, searchQuery])

  const handleGenerate = useCallback(async () => {
    if (!generateScanId.trim()) {
      toast({ title: "Scan ID is required", status: "error", duration: 3000, position: "top-right" })
      return
    }
    setGenerating(true)
    try {
      await neurosploitApi.reports.generate({
        scan_id: generateScanId.trim(),
        format: generateFormat,
        title: generateTitle || undefined,
      })
      toast({ title: "Report generated", status: "success", duration: 3000, position: "top-right" })
      setShowGenerateModal(false)
      setGenerateScanId("")
      setGenerateFormat("html")
      setGenerateTitle("")
      fetchReports()
    } catch {
      toast({ title: "Failed to generate report", status: "error", duration: 3000, position: "top-right" })
    } finally {
      setGenerating(false)
    }
  }, [generateScanId, generateFormat, generateTitle, toast, fetchReports])

  const handleDelete = useCallback(async () => {
    if (!deleteTarget) return
    try {
      await neurosploitApi.reports.delete(deleteTarget)
      toast({ title: "Report deleted", status: "success", duration: 3000, position: "top-right" })
      setDeleteTarget(null)
      fetchReports()
    } catch {
      toast({ title: "Failed to delete report", status: "error", duration: 3000, position: "top-right" })
      setDeleteTarget(null)
    }
  }, [deleteTarget, toast, fetchReports])

  const handleDownload = useCallback((reportId: string, format: string) => {
    window.open(neurosploitApi.reports.downloadUrl(reportId, format), "_blank")
    toast({ title: `Downloading ${format.toUpperCase()}`, status: "info", duration: 2000, position: "top-right" })
  }, [toast])

  const handleView = useCallback((reportId: string) => {
    window.open(neurosploitApi.reports.viewUrl(reportId), "_blank")
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
          <Heading size="lg">Reports</Heading>
          <Text color={colorMode === "dark" ? "gray.400" : "gray.600"} mt={1}>
            View and download security assessment reports
          </Text>
        </Box>
        <HStack>
          <IconButton
            aria-label="Refresh"
            icon={<RepeatIcon />}
            variant="outline"
            onClick={fetchReports}
          />
          <Button colorScheme="blue" leftIcon={<AddIcon />} onClick={() => setShowGenerateModal(true)}>
            Generate Report
          </Button>
        </HStack>
      </Flex>

      {reports.length > 0 && (
        <Card variant="outline" mb={6}>
          <CardBody>
            <Flex gap={3} flexWrap="wrap">
              <Box minW="200px">
                <Select value={formatFilter} onChange={(e) => setFormatFilter(e.target.value)} size="sm">
                  <option value="all">All Formats</option>
                  <option value="html">HTML</option>
                  <option value="json">JSON</option>
                  <option value="pdf">PDF</option>
                </Select>
              </Box>
              <Box flex={1} minW="200px">
                <Input
                  placeholder="Search reports..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  size="sm"
                />
              </Box>
              <Text fontSize="sm" color="gray.500" alignSelf="center">
                {filteredReports.length} report{filteredReports.length !== 1 ? "s" : ""}
              </Text>
            </Flex>
          </CardBody>
        </Card>
      )}

      {reports.length === 0 ? (
        <Card variant="outline">
          <CardBody>
            <VStack spacing={4} py={8} textAlign="center">
              <ExternalLinkIcon boxSize={8} color="gray.400" />
              <Text color="gray.500">No reports yet</Text>
              <Button colorScheme="blue" leftIcon={<AddIcon />} onClick={() => setShowGenerateModal(true)}>
                Generate First Report
              </Button>
            </VStack>
          </CardBody>
        </Card>
      ) : (
        <VStack spacing={3} align="stretch">
          {filteredReports.map((report) => {
            const fs = FORMAT_STYLE[report.format] || { color: "gray", label: report.format.toUpperCase() }
            return (
              <Card key={report.id} variant="outline">
                <CardBody p={4}>
                  <Flex justify="space-between" align="center" gap={4} flexWrap="wrap">
                    <Box flex={1} minW={0}>
                      <Flex align="center" gap={2} mb={1} flexWrap="wrap">
                        <Text fontWeight="medium" noOfLines={1}>
                          {report.title || "Security Report"}
                        </Text>
                        <Badge colorScheme={fs.color} fontSize="xs">{fs.label}</Badge>
                        {report.auto_generated && (
                          <Badge colorScheme="yellow" variant="subtle" fontSize="xs">Auto</Badge>
                        )}
                      </Flex>
                      <Text fontSize="xs" color="gray.500">
                        {relativeTime(report.generated_at)} • Scan: {report.scan_id?.slice(0, 8)}...
                      </Text>
                    </Box>

                    <HStack spacing={1}>
                      <IconButton
                        aria-label="View"
                        icon={<ViewIcon />}
                        size="sm"
                        variant="ghost"
                        onClick={() => handleView(report.id)}
                      />
                      <IconButton
                        aria-label="Download HTML"
                        icon={<DownloadIcon />}
                        size="sm"
                        variant="ghost"
                        colorScheme="blue"
                        onClick={() => handleDownload(report.id, "html")}
                      />
                      <IconButton
                        aria-label="Download JSON"
                        icon={<DownloadIcon />}
                        size="sm"
                        variant="ghost"
                        colorScheme="green"
                        onClick={() => handleDownload(report.id, "json")}
                      />
                      <IconButton
                        aria-label="Delete"
                        icon={<DeleteIcon />}
                        size="sm"
                        variant="ghost"
                        colorScheme="red"
                        onClick={() => setDeleteTarget(report.id)}
                      />
                    </HStack>
                  </Flex>
                </CardBody>
              </Card>
            )
          })}
        </VStack>
      )}

      <Modal isOpen={showGenerateModal} onClose={() => setShowGenerateModal(false)} size="md">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Generate Report</ModalHeader>
          <ModalBody>
            <VStack spacing={4} align="stretch">
              <FormControl isRequired>
                <FormLabel>Scan ID</FormLabel>
                <Input
                  placeholder="Enter scan ID"
                  value={generateScanId}
                  onChange={(e) => setGenerateScanId(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Report Title</FormLabel>
                <Input
                  placeholder="Optional title"
                  value={generateTitle}
                  onChange={(e) => setGenerateTitle(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Format</FormLabel>
                <Select value={generateFormat} onChange={(e) => setGenerateFormat(e.target.value)}>
                  <option value="html">HTML</option>
                  <option value="json">JSON</option>
                  <option value="pdf">PDF</option>
                </Select>
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={() => setShowGenerateModal(false)}>Cancel</Button>
            <Button colorScheme="blue" onClick={handleGenerate} isLoading={generating}>
              Generate
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      <Modal isOpen={!!deleteTarget} onClose={() => setDeleteTarget(null)}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Delete Report</ModalHeader>
          <ModalBody>
            <Text>Are you sure you want to delete this report? This cannot be undone.</Text>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={() => setDeleteTarget(null)}>Cancel</Button>
            <Button colorScheme="red" onClick={handleDelete}>Delete</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  )
}