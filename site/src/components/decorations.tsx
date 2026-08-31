export function Illumination({
  size = 60,
  letter = "B",
  color = "#8B1A1A",
}: {
  size?: number;
  letter?: string;
  color?: string;
}) {
  return (
    <svg width={size} height={size} viewBox="0 0 60 60" aria-hidden>
      <rect x="2" y="2" width="56" height="56" rx="3" fill={color} stroke="#C4A265" strokeWidth="2" />
      <rect x="6" y="6" width="48" height="48" rx="2" fill="none" stroke="#C4A265" strokeWidth="0.8" />
      <rect x="9" y="9" width="42" height="42" rx="1" fill="none" stroke="#C4A265" strokeWidth="0.4" />
      <line x1="2" y1="2" x2="9" y2="9" stroke="#C4A265" strokeWidth="0.4" />
      <line x1="58" y1="2" x2="51" y2="9" stroke="#C4A265" strokeWidth="0.4" />
      <line x1="2" y1="58" x2="9" y2="51" stroke="#C4A265" strokeWidth="0.4" />
      <line x1="58" y1="58" x2="51" y2="51" stroke="#C4A265" strokeWidth="0.4" />
      <circle cx="30" cy="30" r="16" fill="none" stroke="#C4A265" strokeWidth="0.5" opacity="0.5" />
      <text
        x="30"
        y="38"
        textAnchor="middle"
        fontFamily="var(--font-cinzel-decorative), serif"
        fontSize="28"
        fontWeight="700"
        fill="#C4A265"
      >
        {letter}
      </text>
    </svg>
  );
}

export function CrossDivider() {
  return (
    <svg
      width="100%"
      height="24"
      viewBox="0 0 600 24"
      preserveAspectRatio="xMidYMid meet"
      className="cross-divider"
      aria-hidden
    >
      <line x1="0" y1="12" x2="260" y2="12" stroke="#8B6914" strokeWidth="0.5" />
      <line x1="340" y1="12" x2="600" y2="12" stroke="#8B6914" strokeWidth="0.5" />
      <line x1="290" y1="4" x2="290" y2="20" stroke="#8B6914" strokeWidth="1" />
      <line x1="282" y1="12" x2="298" y2="12" stroke="#8B6914" strokeWidth="1" />
      <line x1="310" y1="4" x2="310" y2="20" stroke="#8B6914" strokeWidth="1" />
      <line x1="302" y1="12" x2="318" y2="12" stroke="#8B6914" strokeWidth="1" />
      <circle cx="300" cy="12" r="2" fill="#8B6914" />
    </svg>
  );
}

export function FleuronDivider() {
  return (
    <div className="fleuron" aria-hidden>
      &#10050; &#10050; &#10050;
    </div>
  );
}
