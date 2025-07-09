import { useEffect, useRef } from "react";

export default function AnalogClock({ size = 40 }) {
  const secondHand = useRef(null);
  const minuteHand = useRef(null);
  const hourHand = useRef(null);

  useEffect(() => {
    const updateClock = () => {
      const now = new Date();

      // Use Intl.DateTimeFormat to get Switzerland time parts
      const parts = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Europe/Zurich",
        hour12: false,
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
      }).formatToParts(now);

      const hourPart = parseInt(parts.find(p => p.type === 'hour').value, 10);
      const minutePart = parseInt(parts.find(p => p.type === 'minute').value, 10);
      const secondPart = parseInt(parts.find(p => p.type === 'second').value, 10);

      // Convert 24h to 12h
      const hour12 = (hourPart % 12) + minutePart / 60;

      const secondDeg = (secondPart / 60) * 360;
      const minuteDeg = (minutePart / 60) * 360;
      const hourDeg = (hour12 / 12) * 360;

      if (secondHand.current) secondHand.current.style.transform = `rotate(${secondDeg}deg)`;
      if (minuteHand.current) minuteHand.current.style.transform = `rotate(${minuteDeg}deg)`;
      if (hourHand.current) hourHand.current.style.transform = `rotate(${hourDeg}deg)`;
    };

    // Initialize and update every second
    updateClock();
    const timer = setInterval(updateClock, 1000);
    return () => clearInterval(timer);
  }, []);

  const half = size / 2;
  const handCommon = `absolute top-0 left-1/2 origin-bottom bg-black dark:bg-white`;

  return (
    <div
      style={{
        width: size,
        height: size,
        border: "2px solid",
        borderColor: "gray",
        borderRadius: "50%",
        position: "relative",
      }}
    >
      {/* Hour hand */}
      <div
        ref={hourHand}
        className={handCommon}
        style={{
          width: 2,
          height: half * 0.5,
          marginLeft: -1,
          marginTop: half * 0.5,
        }}
      />
      {/* Minute hand */}
      <div
        ref={minuteHand}
        className={handCommon}
        style={{
          width: 2,
          height: half * 0.75,
          marginLeft: -1,
          marginTop: half * 0.25,
        }}
      />
      {/* Second hand */}
      <div
        ref={secondHand}
        className={handCommon}
        style={{
          width: 1,
          backgroundColor: "red",
          height: half * 0.85,
          marginLeft: -0.5,
          marginTop: half * 0.15,
        }}
      />
    </div>
  );
}
