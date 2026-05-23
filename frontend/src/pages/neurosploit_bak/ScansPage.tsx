import { useState, useEffect, useCallback, useMemo } from "react"
import { Link, useNavigate } from "react-router-dom"
import {
  Box, Heading, Text, Card, CardBody, Flex, Grid, Button, Badge, Progress,
  Table, Thead, Tbody, Tr, Th, Td, Select, Input, Textarea, FormControl,
  FormLabel, HStack, VStack, Spinner, Divider, Alert, AlertIcon,
  useColorMode, useToast, IconButton, Modal, ModalOverlay, ModalContent,
  ModalHeader, ModalBody, ModalFooter
} from "@chakra-ui/react"
import {
  AddIcon, DeleteIcon, EditIcon, ViewIcon, RepeatIcon, InfoIcon, WarningIcon
} from "@chakra-ui/icons"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { ScanPublic } from "../../types/neurosploit"

function relativeTime(ts: string): string {
  const diff = Math.floor((Date.now() - new Date(ts).getTime()) / 1000)
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

const STATUS_COLORS: Record<string, string> = {
  pending: "gray",
  running: "green",
  paused: "yellow",
  completed: "blue",
  failed: "red",
  stopped: "orange",
}

export default function NeuroSploitScansPage() {
  const { colorMode } = useColorMode()
  const toast = useToast()
  const navigate = useNavigate()

  const [scans, setScans] = useState<ScanPublic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [statusFilter, setStatusFilter] = useState<string>("")
  const [page, setPage] = useState(1)

  const [showCreateModal, setShowCreateModal] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null)
  const [creating, setCreating] = useState(false)
  const [newScanName, setNewScanName] = useState("")
  const [newScanTargets, setNewScanTargets] = useState("")
  const [newScanType, setNewScanType] = useState("quick")
  const [newScanRecon, setNewScanRecon] = useState(true)

  const fetchScans = useCallback(async () => {
    try {
      const data = await neurosploitApi.scans.list(page, 50, statusFilter || undefined)
      setScans(data.scans || [])
      setError(null)
    } catch {
      setError("Failed to load scans")
    } finally {
      setLoading(false)
    }
  }, [page, statusFilter])

  useEffect(() => {
    setLoading(true)
    fetchScans()
    const interval = setInterval(fetchScans, 10000)
    return () => clearInterval(interval)
  }, [fetchScans])

  const handleCreate = useCallback(async () => {
    if (!newScanTargets.trim()) {
      toast({ title: "At least one target is required", status: "error", duration: 3000, position: "top-right" })
      return
    }

    setCreating(true)
    try {
      const targets = newScanTargets.split("\n").map((t) => t.trim()).filter(Boolean)
      const scan = await neurosploitApi.scans.create({
        name: newScanName || undefined,
        targets,
        scan_type: newScanType,
        recon_enabled: newScanRecon,
      })
      toast({ title: "Scan created", status: "success", duration: 3000, position: "top-right" })
      setShowCreateModal(false)
      setNewScanName("")
      setNewScanTargets("")
      setNewScanType("quick")
      setNewScanRecon(true)
      fetchScans()
      navigate(`/scan/${scan.id}`)
    } catch (err: unknown) {
      const errObj = err as { response?: { data?: { detail?: string } } }
      toast({ title: errObj?.response?.data?.detail || "Failed to create scan", status: "error", duration: 3000, position: "top-right" })
    } finally {
      setCreating(false)
    }
  }, [newScanName, newScanTargets, newScanType, newScanRecon, toast, fetchScans, navigate])

  const handleDelete = useCallback(async () => {
    if (!deleteTarget) return
    try {
      await neurosploitApi.scans.delete(deleteTarget)
      toast({ title: "Scan deleted", status: "success", duration: 3000, position: "top-right" })
      setDeleteTarget(null)
      fetchScans()
    } catch {
      toast({ title: "Failed to delete scan", status: "error", duration: 3000, position: "top-right" })
      setDeleteTarget(null)
    }
  }, [deleteTarget, toast, fetchScans])

  const handleAction = useCallback(async (scanId: string, action: "start" | "stop" | "pause" | "resume") => {
    try {
      await neurosploitApi.scans[action](scanId)
      toast({ title: `Scan ${action}ed`, status: "info", duration: 2000, position: "top-right" })
      fetchScans()
    } catch {
      toast({ title: `Failed to ${action} scan`, status: "error", duration: 2000, position: "top-right" })
    }
  }, [toast, fetchScans])

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
          <Heading size="lg">Scans</Heading>
          <Text color={colorMode === "dark" ? "gray.400" : "gray.600"} mt={1}>
            Manage all penetration testing scans
          </Text>
        </Box>
        <HStack>
          <Select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            placeholder="All statuses"
            size="sm"
            w="180px"
          >
            <option value="pending">Pending</option>
            <option value="running">Running</option>
            <option value="paused">Paused</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
            <option value="stopped">Stopped</option>
          </Select>
          <Button colorScheme="blue" leftIcon={<AddIcon />} onClick={() => setShowCreateModal(true)}>
            New Scan
          </Button>
        </HStack>
      </Flex>

      {scans.length === 0 ? (
        <Card variant="outline">
          <CardBody>
            <VStack spacing={4} py={8} textAlign="center">
              <InfoIcon boxSize={10} color="gray.400" />
              <Text color="gray.500">No scans found</Text>
              <Button colorScheme="blue" leftIcon={<AddIcon />} onClick={() => setShowCreateModal(true)}>
                Create First Scan
              </Button>
            </VStack>
          </CardBody>
        </Card>
      ) : (
        <VStack spacing={3} align="stretch">
          {scans.map((scan) => (
            <Card key={scan.id} variant="outline">
              <CardBody p={4}>
                <Flex justify="space-between" align="start" gap={4} flexWrap="wrap">
                  <Box flex={1} minW={0}>
                    <Flex align="center" gap={2} mb={1}>
                      <Heading size="sm" as={Link} to={`/scan/${scan.id}`} _hover={{ color: "blue.500" }}>
                        {scan.name || "Unnamed Scan"}
                      </Heading>
                      <Badge colorScheme={STATUS_COLORS[scan.status] || "gray"} fontSize="xs">
                        {scan.status}
                      </Badge>
                      <Badge colorScheme="purple" variant="outline" fontSize="xs">{scan.scan_type}</Badge>
                    </Flex>

                    {scan.status === "running" && (
                      <Box mt={2} mb={2}>
                        <Flex justify="space-between" mb={0.5}>
                          <Text fontSize="xs" color="gray.500">{scan.current_phase || "Scanning..."}</Text>
                          <Text fontSize="xs" fontWeight="bold">{scan.progress}%</Text>
                        </Flex>
                        <Progress value={scan.progress} colorScheme="green" size="xs" borderRadius="full" />
                      </Box>
                    )}

                    <Flex gap={3} fontSize="xs" color="gray.500" flexWrap="wrap" mt={1}>
                      <Text>{relativeTime(scan.created_at)}</Text>
                      {scan.total_endpoints > 0 && <Text>{scan.total_endpoints} endpoints</Text>}
                      {scan.total_vulnerabilities > 0 && (
                        <Flex gap={1} flexWrap="wrap">
                          {scan.critical_count > 0 && <Badge colorScheme="red" fontSize="xs">{scan.critical_count}C</Badge>}
                          {scan.high_count > 0 && <Badge colorScheme="orange" fontSize="xs">{scan.high_count}H</Badge>}
                          {scan.medium_count > 0 && <Badge colorScheme="yellow" fontSize="xs">{scan.medium_count}M</Badge>}
                          {scan.low_count > 0 && <Badge colorScheme="blue" fontSize="xs">{scan.low_count}L</Badge>}
                        </Flex>
                      )}
                    </Flex>
                  </Box>

                  <HStack spacing={1}>
                    <IconButton
                      aria-label="View"
                      icon={<ViewIcon />}
                      size="sm"
                      variant="ghost"
                      onClick={() => navigate(`/scan/${scan.id}`)}
                    />
                    {scan.status === "pending" && (
                      <IconButton aria-label="Start" icon={<RepeatIcon />} size="sm" variant="ghost" colorScheme="green" onClick={() => handleAction(scan.id, "start")} />
                    )}
                    {scan.status === "running" && (
                      <>
                        <IconButton aria-label="Pause" icon={<InfoIcon />} size="sm" variant="ghost" colorScheme="yellow" onClick={() => handleAction(scan.id, "pause")} />
                        <IconButton aria-label="Stop" icon={<WarningIcon />} size="sm" variant="ghost" colorScheme="red" onClick={() => handleAction(scan.id, "stop")} />
                      </>
                    )}
                    {scan.status === "paused" && (
                      <IconButton aria-label="Resume" icon={<RepeatIcon />} size="sm" variant="ghost" colorScheme="green" onClick={() => handleAction(scan.id, "resume")} />
                    )}
                    <IconButton
                      aria-label="Delete"
                      icon={<DeleteIcon />}
                      size="sm"
                      variant="ghost"
                      colorScheme="red"
                      onClick={() => setDeleteTarget(scan.id)}
                    />
                  </HStack>
                </Flex>
              </CardBody>
            </Card>
          ))}
        </VStack>
      )}

      <Modal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} size="lg">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create New Scan</ModalHeader>
          <ModalBody>
            <VStack spacing={4} align="stretch">
              <FormControl>
                <FormLabel>Scan Name</FormLabel>
                <Input
                  placeholder="Optional name for this scan"
                  value={newScanName}
                  onChange={(e) => setNewScanName(e.target.value)}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Targets</FormLabel>
                <Textarea
                  placeholder="https://example.com&#10;https://test.example.com"
                  value={newScanTargets}
                  onChange={(e) => setNewScanTargets(e.target.value)}
                  rows={3}
                />
                <Text fontSize="xs" color="gray.500" mt={1}>One URL per line</Text>
              </FormControl>

              <FormControl>
                <FormLabel>Scan Type</FormLabel>
                <Select value={newScanType} onChange={(e) => setNewScanType(e.target.value)}>
                  <option value="quick">Quick</option>
                  <option value="full">Full</option>
                  <option value="custom">Custom</option>
                </Select>
              </FormControl>

              <Flex align="center" gap={3}>
                <FormLabel mb={0}>Enable Reconnaissance</FormLabel>
                <Box
                  as="input"
                  type="checkbox"
                  checked={newScanRecon}
                  onChange={(e) => setNewScanRecon(e.target.checked)}
                />
              </Flex>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={() => setShowCreateModal(false)}>Cancel</Button>
            <Button colorScheme="blue" onClick={handleCreate} isLoading={creating}>
              Create Scan
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      <Modal isOpen={!!deleteTarget} onClose={() => setDeleteTarget(null)}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Delete Scan</ModalHeader>
          <ModalBody>
            <Text>Are you sure you want to delete this scan? This action cannot be undone.</Text>
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