import DarkModeToggle from "./DarkModeToggle";

export default function Header({ darkMode, toggleDarkMode }) {
  return (
    <div className="flex items-center justify-between mb-4">
      <h1 className="text-3xl font-bold text-blue-700 dark:text-blue-300">
        SWISS TRAVEL BUDDY
      </h1>
      <DarkModeToggle darkMode={darkMode} setDarkMode={toggleDarkMode} />
    </div>
  );
}
