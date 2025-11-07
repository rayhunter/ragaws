import React from 'react'

function QuerySection({ query, setQuery, onQuery, isLoading }) {
  const handleSubmit = (e) => {
    e.preventDefault()
    onQuery()
  }

  return (
    <div className="mb-8 p-6 bg-gray-900 rounded-lg border border-gray-800">
      <h2 className="text-xl font-semibold mb-4">Query</h2>
      
      <form onSubmit={handleSubmit} className="flex gap-4">
        <div className="flex-1">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your documents..."
            rows={3}
            className="w-full px-4 py-3 rounded resize-none"
          />
        </div>
        
        <button
          type="submit"
          disabled={!query.trim() || isLoading}
          className="px-8 py-3 font-semibold disabled:opacity-50 self-end"
        >
          {isLoading ? 'Processing...' : 'Ask ▶'}
        </button>
      </form>
    </div>
  )
}

export default QuerySection

