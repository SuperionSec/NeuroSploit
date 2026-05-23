import { useState, useEffect, useCallback } from "react"
import {
  Box, Heading, Text, Card, CardBody, CardHeader, SimpleGrid, VStack, HStack,
  Button, Table, Thead, Tbody, Tr, Th, Td, Badge, IconButton, Spinner,
  Alert, AlertIcon, Modal, ModalOverlay, ModalContent, ModalHeader,
  ModalBody, ModalFooter, ModalCloseButton, FormControl, FormLabel,
  Input, Textarea, Select, Tag, useToast, useColorMode, Divider,
} from "@chakra-ui/react"
import { AddIcon, DeleteIcon, EditIcon, RepeatIcon } from "@chakra-ui/icons"
import { neurosploitApi } from "../../services/neurosploitApi"
import type { PromptPublic } from "../../types/neurosploit"

export function PromptsPage() {
  const [prompts, setPrompts] = useState<PromptPublic[]>([])
  const [presets, setPresets] = useState<PromptPublic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [modalOpen, setModalOpen] = useState(false)
  const [editingPrompt, setEditingPrompt] = useState<PromptPublic | null>(null)
  const [formName, setFormName] = useState("")
  const [formContent, setFormContent] = useState("")
  const [formCategory, setFormCategory] = useState("pentest")
  const [parsingId, setParsingId] = useState<string | null>(null)
  const toast = useToast()

  const fetchAll = useCallback(async () => {
    try {
      setLoading(true)
      setError("")
      const [promptsRes, presetsRes] = await Promise.all([
        neurosploitApi.prompts.list(),
        neurosploitApi.prompts.presets(),
      ])
      setPrompts(promptsRes.data)
      setPresets(presetsRes.data)
    } catch {
      setError("Failed to load prompts")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchAll() }, [fetchAll])

  const openCreate = () => {
    setEditingPrompt(null)
    setFormName("")
    setFormContent("")
    setFormCategory("pentest")
    setModalOpen(true)
  }

  const openEdit = (p: PromptPublic) => {
    setEditingPrompt(p)
    setFormName(p.name || "")
    setFormContent(p.content)
    setFormCategory(p.category || "pentest")
    setModalOpen(true)
  }

  const handleSave = async () => {
    try {
      if (editingPrompt) {
        await neurosploitApi.prompts.update(editingPrompt.id, { name: formName, content: formContent, category: formCategory })
        toast({ title: "Prompt updated", status: "success", duration: 3000 })
      } else {
        await neurosploitApi.prompts.create({ name: formName, content: formContent, category: formCategory })
        toast({ title: "Prompt created", status: "success", duration: 3000 })
      }
      setModalOpen(false)
      fetchAll()
    } catch {
      toast({ title: "Failed to save prompt", status: "error", duration: 3000 })
    }
  }

  const handleDelete = async (id: string) => {
    try {
      await neurosploitApi.prompts.delete(id)
      toast({ title: "Prompt deleted", status: "success", duration: 3000 })
      fetchAll()
    } catch {
      toast({ title: "Failed to delete prompt", status: "error", duration: 3000 })
    }
  }

  const handleParse = async (id: string) => {
    setParsingId(id)
    try {
      const res = await neurosploitApi.prompts.parse(id)
      toast({ title: "Prompt parsed successfully", description: `Found ${res.data.vulnerabilities_to_test?.length || 0} vuln types`, status: "success", duration: 5000 })
    } catch {
      toast({ title: "Failed to parse prompt", status: "error", duration: 3000 })
    } finally {
      setParsingId(null)
    }
  }

  if (loading) {
    return (
      <Box textAlign="center" py={20}>
        <Spinner size="xl" />
        <Text mt={4} color="gray.500">Loading prompts...</Text>
      </Box>
    )
  }

  if (error) {
    return (
      <Box textAlign="center" py={20}>
        <Alert status="error"><AlertIcon />{error}</Alert>
        <Button mt={4} onClick={fetchAll}>Retry</Button>
      </Box>
    )
  }

  return (
    <Box py={6} px={4} maxW="1200px" mx="auto">
      <HStack justify="space-between" mb={6}>
        <Heading size="lg">Prompt Manager</Heading>
        <Button leftIcon={<AddIcon />} colorScheme="blue" onClick={openCreate}>
          Create Prompt
        </Button>
      </HStack>

      {presets.length > 0 && (
        <Box mb={8}>
          <Heading size="md" mb={4}>Preset Templates</Heading>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
            {presets.map(p => (
              <Card key={p.id} variant="outline">
                <CardHeader pb={2}>
                  <Heading size="sm">{p.name}</Heading>
                </CardHeader>
                <CardBody pt={0}>
                  <Text fontSize="sm" color="gray.500" noOfLines={3}>{p.description || p.content}</Text>
                  <HStack mt={2} justify="space-between">
                    <Badge colorScheme="purple">{p.category}</Badge>
                    <Button size="xs" variant="ghost" onClick={() => openEdit(p)}>Use</Button>
                  </HStack>
                </CardBody>
              </Card>
            ))}
          </SimpleGrid>
        </Box>
      )}

      <Divider mb={6} />

      <Box>
        <Heading size="md" mb={4}>Your Prompts</Heading>
        {prompts.length === 0 ? (
          <Text color="gray.500" textAlign="center" py={8}>No custom prompts yet. Create one to get started.</Text>
        ) : (
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Name</Th>
                <Th>Category</Th>
                <Th>Content</Th>
                <Th>Actions</Th>
              </Tr>
            </Thead>
            <Tbody>
              {prompts.map(p => (
                <Tr key={p.id}>
                  <Td fontWeight="medium">{p.name}</Td>
                  <Td><Badge>{p.category}</Badge></Td>
                  <Td>
                    <Text noOfLines={2} fontSize="sm" color="gray.500">{p.content}</Text>
                  </Td>
                  <Td>
                    <HStack spacing={1}>
                      <IconButton
                        aria-label="Parse"
                        icon={<RepeatIcon />}
                        size="sm"
                        variant="ghost"
                        onClick={() => handleParse(p.id)}
                        isLoading={parsingId === p.id}
                        title="Parse for vulnerabilities"
                      />
                      <IconButton
                        aria-label="Edit"
                        icon={<EditIcon />}
                        size="sm"
                        variant="ghost"
                        onClick={() => openEdit(p)}
                      />
                      <IconButton
                        aria-label="Delete"
                        icon={<DeleteIcon />}
                        size="sm"
                        variant="ghost"
                        colorScheme="red"
                        onClick={() => handleDelete(p.id)}
                      />
                    </HStack>
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        )}
      </Box>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} size="xl">
        <ModalOverlay />
        <ModalContent maxW="700px">
          <ModalHeader>{editingPrompt ? "Edit Prompt" : "Create Prompt"}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4}>
              <FormControl isRequired>
                <FormLabel>Name</FormLabel>
                <Input value={formName} onChange={e => setFormName(e.target.value)} placeholder="e.g. OWASP Top 10 Pentest" />
              </FormControl>
              <FormControl>
                <FormLabel>Category</FormLabel>
                <Select value={formCategory} onChange={e => setFormCategory(e.target.value)}>
                  <option value="pentest">Pentest</option>
                  <option value="bug_bounty">Bug Bounty</option>
                  <option value="api">API Security</option>
                  <option value="cloud">Cloud Security</option>
                  <option value="mobile">Mobile Security</option>
                  <option value="custom">Custom</option>
                </Select>
              </FormControl>
              <FormControl isRequired>
                <FormLabel>Content</FormLabel>
                <Textarea
                  value={formContent}
                  onChange={e => setFormContent(e.target.value)}
                  placeholder="Describe what vulnerabilities to test for, testing methodology, scope..."
                  rows={12}
                  minH="200px"
                />
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button colorScheme="blue" onClick={handleSave}>Save</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  )
}