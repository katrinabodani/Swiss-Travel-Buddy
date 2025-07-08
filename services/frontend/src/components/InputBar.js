export default function InputBar({ question, setQuestion, onSubmit, loading }) {
    return (
      <div className="mt-6">
        <textarea
          rows={3}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about Hunza Valley..."
          className="w-full p-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={onSubmit}
          disabled={loading}
          className="mt-2 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-xl disabled:opacity-50 transition"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-1">
              Thinking
              <span className="animate-bounce">.</span>
              <span className="animate-bounce delay-100">.</span>
              <span className="animate-bounce delay-200">.</span>
            </span>
          ) : (
            "Ask"
          )}
        </button>
      </div>
    );
  }
  