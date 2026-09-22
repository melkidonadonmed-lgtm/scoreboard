import React, { useRef, useState, useCallback, useEffect } from 'react';

export interface AlphabetJumpRailProps {
  letters?: string[];
  activeLetter?: string;
  availableLetters?: string[];
  onSelectLetter: (letter: string) => void;
  className?: string;
}

export const DEFAULT_ALPHABET = [
  '#',
  'A',
  'B',
  'C',
  'D',
  'E',
  'F',
  'G',
  'H',
  'I',
  'J',
  'K',
  'L',
  'M',
  'N',
  'O',
  'P',
  'Q',
  'R',
  'S',
  'T',
  'U',
  'V',
  'W',
  'X',
  'Y',
  'Z',
];

export const AlphabetJumpRail: React.FC<AlphabetJumpRailProps> = ({
  letters = DEFAULT_ALPHABET,
  activeLetter,
  availableLetters,
  onSelectLetter,
  className = '',
}) => {
  const railRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [balloonLetter, setBalloonLetter] = useState<string | null>(null);
  const [balloonY, setBalloonY] = useState<number>(0);
  const lastSelectedLetterRef = useRef<string | null>(null);
  const availableSet = useRef<Set<string>>(new Set(availableLetters || []));

  useEffect(() => {
    availableSet.current = new Set(availableLetters || []);
  }, [availableLetters]);

  const triggerHapticFeedback = useCallback(() => {
    if (typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function') {
      try {
        navigator.vibrate(10);
      } catch {
        // Ignore haptic failures
      }
    }
  }, []);

  const handlePointerY = useCallback(
    (clientY: number) => {
      if (!railRef.current) return;
      const rect = railRef.current.getBoundingClientRect();
      const relativeY = clientY - rect.top;
      const clampedY = Math.max(0, Math.min(relativeY, rect.height - 1));
      const letterHeight = rect.height / letters.length;
      const index = Math.floor(clampedY / letterHeight);
      const letter = letters[Math.min(index, letters.length - 1)];

      setBalloonY(clampedY);
      setBalloonLetter(letter);

      if (letter && letter !== lastSelectedLetterRef.current) {
        lastSelectedLetterRef.current = letter;
        triggerHapticFeedback();
        onSelectLetter(letter);
      }
    },
    [letters, onSelectLetter, triggerHapticFeedback]
  );

  // Touch handlers
  const handleTouchStart = (e: React.TouchEvent) => {
    e.preventDefault();
    setIsDragging(true);
    if (e.touches.length > 0) {
      handlePointerY(e.touches[0].clientY);
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    e.preventDefault();
    if (e.touches.length > 0) {
      handlePointerY(e.touches[0].clientY);
    }
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
    setBalloonLetter(null);
    lastSelectedLetterRef.current = null;
  };

  // Mouse drag handlers (for desktop browser testing)
  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsDragging(true);
    handlePointerY(e.clientY);
  };

  useEffect(() => {
    if (!isDragging) return;

    const onMouseMove = (e: MouseEvent) => {
      handlePointerY(e.clientY);
    };

    const onMouseUp = () => {
      setIsDragging(false);
      setBalloonLetter(null);
      lastSelectedLetterRef.current = null;
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };
  }, [isDragging, handlePointerY]);

  const currentDisplayLetter = balloonLetter || activeLetter;

  return (
    <div
      ref={railRef}
      role="navigation"
      aria-label="Índice alfabético A-Z"
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      onTouchCancel={handleTouchEnd}
      onMouseDown={handleMouseDown}
      className={`relative select-none touch-none flex flex-col items-center justify-between py-1 px-1 w-6 z-30 cursor-pointer ${className}`}
    >
      {/* Magnified iOS Bubble / Balloon Indicator */}
      {isDragging && balloonLetter && (
        <div
          style={{ top: `${balloonY}px` }}
          className="absolute right-8 -translate-y-1/2 flex items-center pointer-events-none transition-all duration-75 animate-in fade-in zoom-in-75"
        >
          <div className="relative flex items-center justify-center w-12 h-12 rounded-full bg-brand-600 text-white font-extrabold text-2xl shadow-card border-2 border-white/20">
            {balloonLetter}
            {/* Arrow pointer toward rail */}
            <div className="absolute -right-1.5 top-1/2 -translate-y-1/2 w-0 h-0 border-y-4 border-y-transparent border-l-[6px] border-l-brand-600" />
          </div>
        </div>
      )}

      {/* Vertical Alphabet Characters */}
      {letters.map((char) => {
        const isSelected = char === currentDisplayLetter;
        const hasEntries = availableSet.current.size === 0 || availableSet.current.has(char);

        return (
          <button
            key={char}
            type="button"
            data-letter={char}
            onClick={(e) => {
              e.stopPropagation();
              onSelectLetter(char);
              triggerHapticFeedback();
            }}
            className={`w-full flex items-center justify-center text-[10px] leading-none transition-colors rounded-sm my-[0.5px] ${
              isSelected
                ? 'font-black text-brand-600 dark:text-brand-400 scale-125'
                : hasEntries
                  ? 'font-bold text-slate-700 dark:text-slate-200'
                  : 'font-normal text-slate-400/60 dark:text-slate-600'
            }`}
          >
            {char}
          </button>
        );
      })}
    </div>
  );
};
