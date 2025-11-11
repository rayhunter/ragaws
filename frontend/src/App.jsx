import React, { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import UploadSection from './components/UploadSection'
import QuerySection from './components/QuerySection'
import ResultsSection from './components/ResultsSection'

function App() {
  const [query, setQuery] = useState('')
  const [retrievedContext, setRetrievedContext] = useState(null)
  const [answer, setAnswer] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)
  const queryClient = useQueryClient()

  const apiUrl = useMemo(() => {
    if (import.meta.env.VITE_API_URL) {
      return import.meta.env.VITE_API_URL
    }
    if (window.__RAG_API_URL__) {
      return window.__RAG_API_URL__
    }
    return window.location.origin
  }, [])

  const axiosInstance = useMemo(() => {
    const instance = axios.create({
      baseURL: apiUrl,
      timeout: 30_000,
    })
    return instance
  }, [apiUrl])

  // Retrieve context
  const retrieveMutation = useMutation({
    mutationFn: async (question) => {
      const response = await axiosInstance.post('/api/v1/retrieval/query', {
        question,
        top_k: 5
      })
      return response.data
    },
    onSuccess: (data) => {
      setRetrievedContext(data)
      setErrorMessage(null)
    },
    onError: (error) => {
      setErrorMessage(error.response?.data?.detail || 'Failed to retrieve context from the API.')
    }
  })

  // Generate answer
  const generateMutation = useMutation({
    mutationFn: async ({ context, question }) => {
      const response = await axiosInstance.post('/api/v1/generation/generate', {
        context,
        question,
        max_tokens: 2048,
        temperature: 0.7
      })
      return response.data
    },
    onSuccess: (data) => {
      setAnswer(data)
      setErrorMessage(null)
    },
    onError: (error) => {
      setErrorMessage(error.response?.data?.detail || 'Failed to generate an answer.')
    }
  })

  // Combined RAG query
  const handleQuery = async () => {
    if (!query.trim()) return

    // Step 1: Retrieve context
    const retrievalResult = await retrieveMutation.mutateAsync(query)
    if (!retrievalResult?.context) {
      return
    }

    // Step 2: Generate answer with retrieved context
    await generateMutation.mutateAsync({
      context: retrievalResult.context,
      question: query
    })
  }

  // Get index stats
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      const response = await axiosInstance.get('/api/v1/ingestion/stats')
      return response.data
    },
    refetchInterval: 30000 // Refresh every 30 seconds
  })

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="mb-8 border-b border-gray-800 pb-4">
          <h1 className="text-3xl font-bold mb-2">txtai RAG Dashboard</h1>
          <p className="text-gray-400">
            Production-grade RAG system with decoupled retrieval and generation
          </p>
          {stats && (
            <div className="mt-4 text-sm text-gray-500">
              Indexed Documents: {stats.total_documents || 0}
            </div>
          )}
        </header>

        {/* Upload Section */}
        <UploadSection />

        {/* Query Section */}
        <QuerySection
          query={query}
          setQuery={setQuery}
          onQuery={handleQuery}
          isLoading={retrieveMutation.isPending || generateMutation.isPending}
          apiUrl={apiUrl}
        />

        {errorMessage && (
          <div className="mb-6 p-4 bg-red-900 text-red-100 rounded-lg border border-red-700">
            <p className="text-sm font-semibold">Request error</p>
            <p className="text-sm mt-1">{errorMessage}</p>
            <p className="text-xs text-red-200 mt-3">Using API endpoint: {apiUrl}</p>
          </div>
        )}

        {/* Results Section */}
        <ResultsSection
          retrievedContext={retrievedContext}
          answer={answer}
          query={query}
        />
      </div>
    </div>
  )
}

export default App
