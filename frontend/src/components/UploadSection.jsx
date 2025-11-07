import React, { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function UploadSection() {
  const [file, setFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState(null)

  const uploadMutation = useMutation({
    mutationFn: async (file) => {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await axios.post(
        `${API_URL}/api/v1/ingestion/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )
      return response.data
    },
    onSuccess: (data) => {
      setUploadStatus({
        type: 'success',
        message: `Successfully indexed ${data.chunks} chunks from ${data.filename}`
      })
      setFile(null)
    },
    onError: (error) => {
      setUploadStatus({
        type: 'error',
        message: error.response?.data?.detail || 'Upload failed'
      })
    }
  })

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      const ext = selectedFile.name.split('.').pop().toLowerCase()
      if (!['pdf', 'md', 'markdown'].includes(ext)) {
        setUploadStatus({
          type: 'error',
          message: 'Only PDF and Markdown files are supported'
        })
        return
      }
      setFile(selectedFile)
      setUploadStatus(null)
    }
  }

  const handleUpload = () => {
    if (!file) return
    uploadMutation.mutate(file)
  }

  return (
    <div className="mb-8 p-6 bg-gray-900 rounded-lg border border-gray-800">
      <h2 className="text-xl font-semibold mb-4">Upload Document</h2>
      
      <div className="flex gap-4 items-end">
        <div className="flex-1">
          <label className="block text-sm text-gray-400 mb-2">
            PDF or Markdown file
          </label>
          <input
            type="file"
            accept=".pdf,.md,.markdown"
            onChange={handleFileChange}
            className="w-full px-4 py-2 rounded"
          />
        </div>
        
        <button
          onClick={handleUpload}
          disabled={!file || uploadMutation.isPending}
          className="px-6 py-2 font-semibold disabled:opacity-50"
        >
          {uploadMutation.isPending ? 'Uploading...' : 'Upload'}
        </button>
      </div>

      {uploadStatus && (
        <div className={`mt-4 p-3 rounded ${
          uploadStatus.type === 'success' 
            ? 'bg-green-900 text-green-200' 
            : 'bg-red-900 text-red-200'
        }`}>
          {uploadStatus.message}
        </div>
      )}
    </div>
  )
}

export default UploadSection

