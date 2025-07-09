export default function DarkModeToggle({ darkMode, setDarkMode }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-red-700 dark:text-white font-semibold">LIGHT</span>
      
      <label className="relative inline-block w-12 h-6">
        <input
          type="checkbox"
          className="sr-only peer"
          checked={darkMode}
          onChange={() => setDarkMode(!darkMode)}
        />
        
        <div className="w-full h-full bg-gray-300 dark:bg-gray-600 rounded-full peer-checked:bg-gray-600 transition-colors duration-300"></div>

        <div className="absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow-md transition-transform duration-300 transform peer-checked:translate-x-6" />
      </label>

      <span className="text-sm text-red-700 dark:text-white font-semibold">DARK</span>
    </div>
  );
}
