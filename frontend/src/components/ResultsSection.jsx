import React from 'react'

function ResultsSection({ retrievedContext, answer, query }) {
  if (!retrievedContext && !answer) {
    return null
  }

  return (
    <div className="space-y-6">
      {/* Retrieved Chunks Panel */}
      {retrievedContext && (
        <div className="p-6 bg-gray-900 rounded-lg border border-gray-800">
          <h2 className="text-xl font-semibold mb-4">Retrieved Chunks</h2>
          
          <div className="space-y-4">
            {retrievedContext.chunks && retrievedContext.chunks.length > 0 ? (
              retrievedContext.chunks.map((chunk, idx) => (
                <div
                  key={idx}
                  className="p-4 bg-gray-800 rounded border border-gray-700"
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs text-gray-400">
                      Chunk {idx + 1}
                    </span>
                    <span className="text-xs text-gray-500">
                      Score: {chunk.score?.toFixed(3) || 'N/A'}
                    </span>
                  </div>
                  <p className="text-sm text-gray-300 whitespace-pre-wrap">
                    {chunk.text}
                  </p>
                  {chunk.metadata && (
                    <div className="mt-2 text-xs text-gray-500">
                      Source: {chunk.metadata.filename || 'Unknown'}
                    </div>
                  )}
                </div>
              ))
            ) : (
              <p className="text-gray-400">No chunks retrieved</p>
            )}
          </div>
        </div>
      )}

      {/* LLM Response */}
      {answer && (
        <div className="p-6 bg-gray-900 rounded-lg border border-gray-800">
          <h2 className="text-xl font-semibold mb-4">LLM Response</h2>
          
          <div className="mb-4 p-3 bg-gray-800 rounded">
            <div className="text-sm text-gray-400 mb-1">Question:</div>
            <div className="text-white">{query}</div>
          </div>
          
          <div className="mb-4">
            <div className="text-sm text-gray-400 mb-2">Answer:</div>
            <div className="p-4 bg-gray-800 rounded whitespace-pre-wrap">
              {answer.answer}
            </div>
          </div>
          
          <div className="text-xs text-gray-500">
            Model: {answer.model}
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultsSection

