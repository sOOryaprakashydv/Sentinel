import { useEffect, useRef, useState } from "react";
import { sentinelApi } from "@/services/api";
import type { InvestigationDetail } from "@/types";

const TERMINAL_STATES = new Set(["complete", "failed"]);

export function useInvestigationPoll(investigationId: number | undefined) {
  const [investigation, setInvestigation] = useState<InvestigationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    if (!investigationId) return;
    let cancelled = false;

    const fetchOnce = async () => {
      try {
        const data = await sentinelApi.getInvestigation(investigationId);
        if (cancelled) return;
        setInvestigation(data);
        setLoading(false);
        if (TERMINAL_STATES.has(data.status) && intervalRef.current) {
          window.clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      } catch {
        if (!cancelled) {
          setError("Could not load this investigation.");
          setLoading(false);
        }
      }
    };

    fetchOnce();
    intervalRef.current = window.setInterval(fetchOnce, 2500);

    return () => {
      cancelled = true;
      if (intervalRef.current) window.clearInterval(intervalRef.current);
    };
  }, [investigationId]);

  return { investigation, loading, error, isComplete: investigation ? TERMINAL_STATES.has(investigation.status) : false };
}
