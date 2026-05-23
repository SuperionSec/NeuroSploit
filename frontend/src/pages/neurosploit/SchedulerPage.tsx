import { useState, useEffect, useCallback, useMemo } from "react"
import {
  Box, Heading, Text, Card, CardBody, Flex, Button, Badge,
  Input, FormControl, FormLabel, HStack, VStack, Spinner, Divider,
  Alert, useColorMode, useToast, Select, SimpleGrid, Stat,
  StatLabel, StatNumber, Modal, ModalOverlay, ModalContent, ModalHeader,
  ModalBody, ModalFooter, Switch
} from "@chakra-ui/react"
import {
  Plus, Trash2, RefreshCw, Clock
} from "lucide-react"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { ScheduleJob } from "../../types/neurosploit"

function relativeTime(ts: string | null): string {
  if (!ts) return "N/A"
  const diff = Math.floor((Date.now() - new Date(ts).getTime()) / 1000)
  if (diff < 0) {
    const abs = Math.abs(diff)
    if (abs < 60) return `in ${abs}s`
    if (abs < 3600) return `in ${Math.floor(abs / 60)}m`
    if (abs < 86400) return `in ${Math.floor(abs / 3600)}h`
    return `in ${Math.floor(abs / 86400)}d`
  }
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

const CRON_PRESETS = [
  { label: "Every Hour", value: "0 * * * *" },
  { label: "Every 6 Hours", value: "0 */6 * * *" },
  { label: "Daily at 2 AM", value: "0 2 * * *" },
  { label: "Daily at Midnight", value: "0 0 * * *" },
  { label: "Weekdays 9 AM", value: "0 9 * * 1-5" },
  { label: "Weekly Monday", value: "0 0 * * 1" },
  { label: "Monthly 1st", value: "0 0 1 * *" },
  { label: "Custom", value: "custom" },
]

const SCAN_TYPES = ["quick", "full", "custom"] as const

export function SchedulerPage() {
  const { colorMode } = useColorMode()
  const toast = useToast()

  const [jobs, setJobs] = useState<ScheduleJob[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null)
  const [creating, setCreating] = useState(false)

  const [jobId, setJobId] = useState("")
  const [target, setTarget] = useState("")
  const [scanType, setScanType] = useState("quick")
  const [cronPreset, setCronPreset] = useState("0 2 * * *")
  const [customCron, setCustomCron] = useState("")
  const [scheduleMode, setScheduleMode] = useState<"preset" | "interval">("preset")
  const [intervalMinutes, setIntervalMinutes] = useState("60")

  const fetchJobs = useCallback(async () => {
    try {
      const data = await neurosploitApi.scheduler.list()
      setJobs(data || [])
      setError(null)
    } catch {
      setError("Failed to load schedules")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    setLoading(true)
    fetchJobs()
    const interval = setInterval(fetchJobs, 15000)
    return () => clearInterval(interval)
  }, [fetchJobs])

  const activeJobCount = useMemo(() => jobs.filter((j) => j.status === "active").length, [jobs])
  const totalRunCount = useMemo(() => jobs.reduce((sum, j) => sum + (j.run_count || 0), 0), [jobs])

  const resetForm = useCallback(() => {
    setJobId("")
    setTarget("")
    setScanType("quick")
    setCronPreset("0 2 * * *")
    setCustomCron("")
    setScheduleMode("preset")
    setIntervalMinutes("60")
  }, [])

  const handleCreate = useCallback(async () => {
    if (!jobId.trim()) {
      toast({ title: "Job ID is required", status: "error", duration: 3000, position: "top-right" })
      return
    }
    if (!target.trim()) {
      toast({ title: "Target URL is required", status: "error", duration: 3000, position: "top-right" })
      return
    }

    setCreating(true)
    try {
      const cron = scheduleMode === "preset" ? (cronPreset === "custom" ? customCron : cronPreset) : undefined
      const interval = scheduleMode === "interval" ? parseInt(intervalMinutes) || 60 : undefined

      await neurosploitApi.scheduler.create({
        job_id: jobId.trim(),
        target: target.trim(),
        scan_type: scanType,
        cron_expression: cron,
        interval_minutes: interval,
      })
      toast({ title: `Schedule "${jobId}" created`, status: "success", duration: 3000, position: "top-right" })
      setShowCreateModal(false)
      resetForm()
      fetchJobs()
    } catch (err: unknown) {
      const errObj = err as { response?: { data?: { detail?: string } } }
      toast({
        title: errObj?.response?.data?.detail || "Failed to create schedule",
        status: "error",
        duration: 3000,
        position: "top-right",
      })
    } finally {
      setCreating(false)
    }
  }, [jobId, target, scanType, cronPreset, customCron, scheduleMode, intervalMinutes, toast, resetForm, fetchJobs])

  const handleDelete = useCallback(async () => {
    if (!deleteTarget) return
    try {
      await neurosploitApi.scheduler.delete(deleteTarget)
      toast({ title: `Schedule "${deleteTarget}" deleted`, status: "success", duration: 3000, position: "top-right" })
      setDeleteTarget(null)
      fetchJobs()
    } catch {
      toast({ title: "Failed to delete schedule", status: "error", duration: 3000, position: "top-right" })
      setDeleteTarget(null)
    }
  }, [deleteTarget, toast, fetchJobs])

  const handlePause = useCallback(async (id: string) => {
    try {
      await neurosploitApi.scheduler.pause(id)
      toast({ title: `Schedule paused`, status: "info", duration: 2000, position: "top-right" })
      fetchJobs()
    } catch {
      toast({ title: "Failed to pause schedule", status: "error", duration: 2000, position: "top-right" })
    }
  }, [toast, fetchJobs])

  const handleResume = useCallback(async (id: string) => {
    try {
      await neurosploitApi.scheduler.resume(id)
      toast({ title: `Schedule resumed`, status: "success", duration: 2000, position: "top-right" })
      fetchJobs()
    } catch {
      toast({ title: "Failed to resume schedule", status: "error", duration: 2000, position: "top-right" })
    }
  }, [toast, fetchJobs])

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
          < />
          {error}
        </Alert>
      )}

      <Flex justify="space-between" align="center" mb={6} flexWrap="wrap" gap={3}>
        <Box>
          <Heading size="lg">Scan Scheduler</Heading>
          <Text color={colorMode === "dark" ? "gray.400" : "gray.600"} mt={1}>
            Schedule automated recurring scans with cron or interval
          </Text>
        </Box>
        <Button colorScheme="blue" leftIcon={<Plus />} onClick={() => setShowCreateModal(true)}>
          New Schedule
        </Button>
      </Flex>

      {jobs.length > 0 && (
        <SimpleGrid columns={{ base: 1, sm: 3 }} spacing={4} mb={6}>
          <Card variant="outline">
            <CardBody p={4}>
              <Stat>
                <StatNumber fontSize="xl" color="blue.500">{jobs.length}</StatNumber>
                <StatLabel fontSize="xs">Total Schedules</StatLabel>
              </Stat>
            </CardBody>
          </Card>
          <Card variant="outline">
            <CardBody p={4}>
              <Stat>
                <StatNumber fontSize="xl" color="green.500">{activeJobCount}</StatNumber>
                <StatLabel fontSize="xs">Active</StatLabel>
              </Stat>
            </CardBody>
          </Card>
          <Card variant="outline">
            <CardBody p={4}>
              <Stat>
                <StatNumber fontSize="xl" color="purple.500">{totalRunCount}</StatNumber>
                <StatLabel fontSize="xs">Total Runs</StatLabel>
              </Stat>
            </CardBody>
          </Card>
        </SimpleGrid>
      )}

      {jobs.length === 0 ? (
        <Card variant="outline">
          <CardBody>
            <VStack spacing={4} py={8} textAlign="center">
              <Clock boxSize={10} color="gray.400" />
              <Text color="gray.500">No scheduled jobs yet</Text>
              <Button colorScheme="blue" leftIcon={<Plus />} onClick={() => setShowCreateModal(true)}>
                Create First Schedule
              </Button>
            </VStack>
          </CardBody>
        </Card>
      ) : (
        <VStack spacing={3} align="stretch">
          {jobs.map((job) => (
            <Card key={job.id} variant="outline">
              <CardBody p={4}>
                <Flex justify="space-between" align="start" gap={4} flexWrap="wrap">
                  <Box flex={1} minW={0}>
                    <Flex align="center" gap={2} mb={1} flexWrap="wrap">
                      <Heading size="sm">{job.id}</Heading>
                      <Badge colorScheme={job.status === "active" ? "green" : "yellow"} fontSize="xs">
                        {job.status}
                      </Badge>
                      <Badge colorScheme="purple" variant="outline" fontSize="xs">
                        {job.scan_type}
                      </Badge>
                    </Flex>

                    <Flex gap={3} fontSize="xs" color="gray.500" flexWrap="wrap" mt={1}>
                      <Text noOfLines={1} maxW="250px">{job.target}</Text>
                      <Text>• {job.schedule}</Text>
                      {job.run_count > 0 && <Text>• {job.run_count} runs</Text>}
                    </Flex>

                    {(job.next_run || job.last_run) && (
                      <Flex gap={3} fontSize="xs" color="gray.500" mt={1}>
                        {job.next_run && <Text>Next: {relativeTime(job.next_run)}</Text>}
                        {job.last_run && <Text>Last: {relativeTime(job.last_run)}</Text>}
                      </Flex>
                    )}
                  </Box>

                  <HStack spacing={1}>
                    {job.status === "active" ? (
                      <Button size="sm" variant="outline" colorScheme="yellow" onClick={() => handlePause(job.id)}>
                        Pause
                      </Button>
                    ) : (
                      <Button size="sm" variant="outline" colorScheme="green" onClick={() => handleResume(job.id)}>
                        Resume
                      </Button>
                    )}
                    <Button size="sm" variant="outline" colorScheme="red" onClick={() => setDeleteTarget(job.id)}>
                      <Trash2 />
                    </Button>
                  </HStack>
                </Flex>
              </CardBody>
            </Card>
          ))}
        </VStack>
      )}

      <Modal isOpen={showCreateModal} onClose={() => { setShowCreateModal(false); resetForm() }} size="lg">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create New Schedule</ModalHeader>
          <ModalBody>
            <VStack spacing={4} align="stretch">
              <FormControl isRequired>
                <FormLabel>Job ID</FormLabel>
                <Input
                  placeholder="daily-scan-prod"
                  value={jobId}
                  onChange={(e) => setJobId(e.target.value)}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Target URL</FormLabel>
                <Input
                  placeholder="https://example.com"
                  value={target}
                  onChange={(e) => setTarget(e.target.value)}
                />
              </FormControl>

              <FormControl>
                <FormLabel>Scan Type</FormLabel>
                <Select value={scanType} onChange={(e) => setScanType(e.target.value)}>
                  {SCAN_TYPES.map((t) => (
                    <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
                  ))}
                </Select>
              </FormControl>

              <FormControl>
                <FormLabel>Schedule Mode</FormLabel>
                <HStack>
                  <Button
                    size="sm"
                    variant={scheduleMode === "preset" ? "solid" : "outline"}
                    colorScheme="blue"
                    onClick={() => setScheduleMode("preset")}
                    flex={1}
                  >
                    Cron Presets
                  </Button>
                  <Button
                    size="sm"
                    variant={scheduleMode === "interval" ? "solid" : "outline"}
                    colorScheme="blue"
                    onClick={() => setScheduleMode("interval")}
                    flex={1}
                  >
                    Interval
                  </Button>
                </HStack>
              </FormControl>

              {scheduleMode === "preset" && (
                <>
                  <FormControl>
                    <FormLabel>Cron Preset</FormLabel>
                    <Select value={cronPreset} onChange={(e) => setCronPreset(e.target.value)}>
                      {CRON_PRESETS.map((p) => (
                        <option key={p.value} value={p.value}>{p.label}</option>
                      ))}
                    </Select>
                  </FormControl>
                  {cronPreset === "custom" && (
                    <FormControl>
                      <FormLabel>Custom Cron Expression</FormLabel>
                      <Input
                        placeholder="*/30 * * * *"
                        value={customCron}
                        onChange={(e) => setCustomCron(e.target.value)}
                      />
                    </FormControl>
                  )}
                </>
              )}

              {scheduleMode === "interval" && (
                <FormControl>
                  <FormLabel>Interval (minutes)</FormLabel>
                  <Input
                    type="number"
                    min="1"
                    value={intervalMinutes}
                    onChange={(e) => setIntervalMinutes(e.target.value)}
                  />
                </FormControl>
              )}
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={() => { setShowCreateModal(false); resetForm() }}>Cancel</Button>
            <Button colorScheme="blue" onClick={handleCreate} isLoading={creating}>
              Create Schedule
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>

      <Modal isOpen={!!deleteTarget} onClose={() => setDeleteTarget(null)}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Delete Schedule</ModalHeader>
          <ModalBody>
            <Text>Are you sure you want to delete schedule "{deleteTarget}"? This cannot be undone.</Text>
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