import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import UploadSection from './components/UploadSection'
import QuerySection from './components/QuerySection'
import ResultsSection from './components/ResultsSection'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [query, setQuery] = useState('')
  const [retrievedContext, setRetrievedContext] = useState(null)
  const [answer, setAnswer] = useState(null)
  const queryClient = useQueryClient()

  // Retrieve context
  const retrieveMutation = useMutation({
    mutationFn: async (question) => {
      const response = await axios.post(`${API_URL}/api/v1/retrieval/query`, {
        question,
        top_k: 5
      })
      return response.data
    },
    onSuccess: (data) => {
      setRetrievedContext(data)
    }
  })

  // Generate answer
  const generateMutation = useMutation({
    mutationFn: async ({ context, question }) => {
      const response = await axios.post(`${API_URL}/api/v1/generation/generate`, {
        context,
        question,
        max_tokens: 2048,
        temperature: 0.7
      })
      return response.data
    },
    onSuccess: (data) => {
      setAnswer(data)
    }
  })

  // Combined RAG query
  const handleQuery = async () => {
    if (!query.trim()) return

    // Step 1: Retrieve context
    const retrievalResult = await retrieveMutation.mutateAsync(query)
    
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
      const response = await axios.get(`${API_URL}/api/v1/ingestion/stats`)
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
        />

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

