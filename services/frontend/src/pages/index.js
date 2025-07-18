import { useEffect, useState, useRef } from "react";
import AnalogClock from "../components/AnalogClock";
import { Upload } from "lucide-react";
import DarkModeToggle from "../components/DarkModeToggle";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const fileInputRef = useRef(null);

  // Swiss digital clock state
  const [swissDigital, setSwissDigital] = useState("");

  // Load theme preference
  useEffect(() => {
    const saved = localStorage.getItem("darkMode");
    if (saved !== null) {
      setDarkMode(saved === "true");
    } else {
      setDarkMode(window.matchMedia("(prefers-color-scheme: dark)").matches);
    }
  }, []);

  // Apply theme
  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
    localStorage.setItem("darkMode", darkMode);
  }, [darkMode]);

  // Update Swiss digital clock every second
  useEffect(() => {
    const update = () => {
      const now = new Date();
      const timeFmt = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Europe/Zurich",
        hour: "numeric",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      });
      const dateFmt = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Europe/Zurich",
        month: "long",
        day: "numeric",
        year: "numeric",
      });
      setSwissDigital(`${timeFmt.format(now)} • ${dateFmt.format(now)} CEST`);
    };
    update();
    const timer = setInterval(update, 1000);
    return () => clearInterval(timer);
  }, []);

  const ask = async () => {
    if (!question.trim()) return;
    const current = question;
    setQuestion("");
    setLoading(true);

    try {
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: current, top_k: 3 }),
      });
      const data = await res.json();
      setHistory((prev) => [
        ...prev,
        { role: "user", content: current },
        { role: "bot", content: data.answer || "No answer found." },
      ]);
    } catch {
      setHistory((prev) => [
        ...prev,
        { role: "user", content: current },
        { role: "bot", content: "❌ Error connecting to backend." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    // 1) Show the uploaded image in the chat
    const blobUrl = URL.createObjectURL(file);
    setHistory((prev) => [
      ...prev,
      { role: "user", type: "image", content: blobUrl },
    ]);

    const form = new FormData();
    form.append("file", file);

    try {
      // 2) Send to /ask/image
      const res = await fetch("/ask/image", { method: "POST", body: form });
      const data = await res.json();

      // 3) Bot reply from the `answer` field
      setHistory((prev) => [
        ...prev,
        { role: "bot", content: data.answer || "Sorry, I couldn't interpret that image." },
      ]);
    } catch (err) {
      console.error(err);
      setHistory((prev) => [
        ...prev,
        { role: "bot", content: "❌ Error processing image." },
      ]);
    } finally {
      setLoading(false);
      e.target.value = null;
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-black dark:text-white transition-colors">
      {/* Header with clocks and toggle */}
      <header className="relative flex items-center bg-white dark:bg-gray-800 shadow-md sticky top-0 z-10 border-b border-gray-200 dark:border-gray-700 px-6 py-3">
        <div className="absolute left-6 flex items-center space-x-3">
          <AnalogClock size={36} />
          <span className="font-mono font-bold text-sm text-gray-700 dark:text-gray-300 bg-white/50 dark:bg-gray-800/50 rounded px-0">
            {swissDigital}
          </span>
        </div>

        <h1 className="mx-auto text-2xl sm:text-3xl font-extrabold tracking-tight text-red-700 dark:text-white font-[Inter]">
          SWISS TRAVEL BUDDY
        </h1>

        <div className="absolute right-6">
          <DarkModeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
        </div>
      </header>

      {/* Main chat area */}
      <main className="flex flex-col justify-between max-w-3xl mx-auto px-4 py-0 h-[calc(100vh-5rem)]">
        <div className="flex-1 overflow-auto space-y-4 pr-1 mt-4">
          {history.map((entry, idx) => (
            <div
              key={idx}
              className={`flex items-center gap-2 w-full ${
                entry.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {entry.role === "bot" && (
                <img src="/bot.gif" alt="Bot" className="w-8 h-8 rounded-full" />
              )}

              {/** ——— Updated bubble ——— **/}
              {entry.type === "image" ? (
                <div className="bg-red-600 self-end rounded-xl p-1 max-w-[50%]">
                  <img
                    src={entry.content}
                    alt="Uploaded"
                    className="w-full rounded-lg block"
                  />
                </div>
              ) : (
                <div
                  className={`p-3 px-4 rounded-xl text-sm break-words whitespace-pre-wrap max-w-[80%] ${
                    entry.role === "user"
                      ? "bg-red-600 text-white self-end"
                      : "bg-gray-200 dark:bg-gray-700 text-black dark:text-white self-start"
                  }`}
                >
                  {entry.content}
                </div>
              )}
              {/** ———————————————— **/}

              {entry.role === "user" && (
                <img src="/user-avatar.gif" alt="You" className="w-8 h-8 rounded-full" />
              )}
            </div>
          ))}

          {loading && (
            <div className="mr-auto text-red-500 dark:text-red-300 flex gap-1 px-4 py-2">
              <span className="animate-bounce">.</span>
              <span className="animate-bounce delay-100">.</span>
              <span className="animate-bounce delay-200">.</span>
            </div>
          )}
        </div>

        {/* Input + icon container */}
        <div className="mt-6 relative">
          <textarea
            rows={2}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                ask();
              }
            }}
            placeholder="Need travel help in Switzerland? Start typing..."
            className="w-full pr-10 p-4 border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-400 resize-none"
          />
          {/* Upload icon right inside textarea */}
          <Upload
            onClick={() => fileInputRef.current.click()}
            className="absolute bottom-9 right-4 w-6 h-5 text-red-700 dark:text-gray-300 cursor-pointer"
          />
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            onChange={handleImageUpload}
            className="hidden"
          />
        </div>

        <button
          onClick={ask}
          disabled={loading}
          className="mt-1 w-full bg-red-600 hover:bg-red-700 text-white font-semibold py-2 disabled:opacity-50 transition"
        >
          Ask
        </button>
      </main>
    </div>
  );
}
