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
  const railRef = useRef< any >(null);
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
        navigator.vibrate(8);
      } catch {
        // Ignore haptic failures
      }
    }
  }, []);

  const handlePointerY = useCallback(
    (clientY: number) => {
      if (!railRef.current) return;
      const rect = railRef.current.getBoundingClientRect();
      if (rect.height <= 0) return;
      const relativeY = clientY - rect.top;
      const clampedY = Math.max(0, Math.min(relativeY, rect.height - 1));
      const letterHeight = rect.height / letters.length;
      const index = Math.floor(clampedY / letterHeight);
      const letter = letters[Math.min(Math.max(0, index), letters.length - 1)];

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
    if (e.cancelable) e.preventDefault();
    setIsDragging(true);
    if (e.touches.length > 0) {
      handlePointerY(e.touches[0].clientY);
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (e.cancelable) e.preventDefault();
    if (e.touches.length > 0) {
      handlePointerY(e.touches[0].clientY);
    }
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
    setBalloonLetter(null);
    lastSelectedLetterRef.current = null;
  };

  // Mouse drag handlers
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
  const availableList = availableLetters || [];

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
      className={`relative select-none touch-none flex flex-col items-center justify-between py-1.5 px-1 w-6 rounded-full bg-surface-light/90 dark:bg-surface-dark/90 backdrop-blur-md border border-subtle-light dark:border-subtle-dark shadow-card z-30 cursor-pointer ${className}`}
    >
      {/* Magnified Floating Bubble Indicator while dragging */}
      {isDragging && balloonLetter && (
        <div
          style={{ top: `${balloonY}px` }}
          className="absolute right-8 -translate-y-1/2 flex items-center pointer-events-none transition-transform duration-75"
        >
          <div className="relative flex items-center justify-center w-11 h-11 rounded-2xl bg-brand-600 text-white font-black text-lg tabular-nums shadow-lg border border-white/25">
            {balloonLetter}
            <div className="absolute -right-1.5 top-1/2 -translate-y-1/2 w-0 h-0 border-y-4 border-y-transparent border-l-[6px] border-l-brand-600" />
          </div>
        </div>
      )}

      {/* Vertical Alphabet Track */}
      {letters.map((char) => {
        const isSelected = char === currentDisplayLetter;
        const hasEntries = availableList.length === 0 || availableList.includes(char);

        return (
          <button
            key={char}
            type="button"
            data-letter={char}
            aria-current={isSelected ? 'true' : undefined}
            onClick={(e) => {
              e.stopPropagation();
              onSelectLetter(char);
              triggerHapticFeedback();
            }}
            className={`w-4 h-3.5 flex items-center justify-center text-[9px] tabular-nums leading-none rounded-full transition-all duration-150 ${
              isSelected
                ? 'bg-brand-600 text-white font-black scale-115 shadow-xs'
                : hasEntries
                  ? 'font-bold text-slate-700 dark:text-slate-200 hover:text-brand-600 dark:hover:text-brand-400'
                  : 'font-normal text-slate-300 dark:text-slate-700 opacity-50'
            }`}
          >
            {char}
          </button>
        );
      })}
    </div>
  );
};
