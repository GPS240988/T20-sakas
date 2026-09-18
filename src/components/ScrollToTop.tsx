import React, { useState, useEffect, useCallback } from 'react';
import { ArrowUp } from 'lucide-react';

export interface ScrollToTopProps {
  /** Se fornecido, monitora e rola este elemento específico. Se omitido, monitora a janela (window). */
  containerRef?: React.RefObject<HTMLElement | null>;
  /** Distância em pixels para exibir o botão (padrão: 260px) */
  threshold?: number;
  /** Se o botão deve ficar posicionado relativamente ao container pai (ex: modais, gavetas) */
  isInsideContainer?: boolean;
  /** Título descritivo acessível */
  title?: string;
  /** Classe extra */
  className?: string;
}

export const ScrollToTop: React.FC<ScrollToTopProps> = ({
  containerRef,
  threshold = 260,
  isInsideContainer = false,
  title = "Voltar ao início",
  className = ""
}) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const checkScroll = () => {
      let currentScroll = 0;
      if (containerRef && containerRef.current) {
        currentScroll = containerRef.current.scrollTop;
      } else {
        currentScroll = window.scrollY || document.documentElement.scrollTop;
      }

      setIsVisible(currentScroll > threshold);
    };

    const target = containerRef ? containerRef.current : window;
    if (!target) return;

    target.addEventListener('scroll', checkScroll, { passive: true });
    checkScroll();

    return () => {
      target.removeEventListener('scroll', checkScroll);
    };
  }, [containerRef, threshold]);

  const handleScrollToTop = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
    if (containerRef && containerRef.current) {
      containerRef.current.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    } else {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  }, [containerRef]);

  if (!isVisible) return null;

  return (
    <button
      type="button"
      className={`scroll-to-top-fab ${isInsideContainer ? 'fab-inside-container' : 'fab-window'} ${className}`}
      onClick={handleScrollToTop}
      title={title}
      aria-label={title}
    >
      <ArrowUp size={20} className="fab-icon" />
    </button>
  );
};
