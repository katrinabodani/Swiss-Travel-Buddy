export default function ChatBubble({ question, answer }) {
    return (
      <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-xl shadow">
        <p className="font-semibold text-blue-600 dark:text-blue-300">Q: {question}</p>
        <p className="mt-2 whitespace-pre-line">{answer}</p>
      </div>
    );
  }
  