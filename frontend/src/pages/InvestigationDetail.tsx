import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { LuLoaderCircle, LuDownload } from "react-icons/lu";
import { useInvestigationPoll } from "@/hooks/useInvestigationPoll";
import { sentinelApi } from "@/services/api";
import type {
  AISummaryOut, IOCOut, MitreMappingOut, RiskScoreOut, StaticAnalysisOut, ThreatIntelResultOut,
} from "@/types";
import FileInfoCard from "@/components/cards/FileInfoCard";
import RiskCard from "@/components/cards/RiskCard";
import StaticAnalysisCard from "@/components/cards/StaticAnalysisCard";
import IOCCard from "@/components/cards/IOCCard";
import ThreatIntelCard from "@/components/cards/ThreatIntelCard";
import MitreCard from "@/components/cards/MitreCard";
import AISummaryCard from "@/components/cards/AISummaryCard";
import TimelineCard from "@/components/cards/TimelineCard";
import SeverityBadge from "@/components/ui/SeverityBadge";

export default function InvestigationDetail() {
  const { id } = useParams();
  const investigationId = id ? Number(id) : undefined;
  const { investigation, loading, isComplete } = useInvestigationPoll(investigationId);

  const [staticAnalysis, setStaticAnalysis] = useState<StaticAnalysisOut | null>(null);
  const [iocs, setIocs] = useState<IOCOut[]>([]);
  const [threatIntel, setThreatIntel] = useState<ThreatIntelResultOut[]>([]);
  const [risk, setRisk] = useState<RiskScoreOut | null>(null);
  const [mitre, setMitre] = useState<MitreMappingOut[]>([]);
  const [aiSummary, setAiSummary] = useState<AISummaryOut | null>(null);

  useEffect(() => {
    if (!investigationId || !investigation) return;
    sentinelApi.getStaticAnalysis(investigationId).then(setStaticAnalysis).catch(() => {});
    sentinelApi.getIocs(investigationId).then((r) => setIocs(r.items)).catch(() => {});
    sentinelApi.getThreatIntel(investigationId).then((r) => setThreatIntel(r.results)).catch(() => {});
    sentinelApi.getRisk(investigationId).then(setRisk).catch(() => {});
    sentinelApi.getMitre(investigationId).then((r) => setMitre(r.items)).catch(() => {});
    sentinelApi.getAISummary(investigationId).then(setAiSummary).catch(() => {});
  }, [investigationId, investigation, isComplete]);

  if (loading) {
    return <div className="flex items-center gap-2 text-ink-500"><LuLoaderCircle className="animate-spin" /> Loading investigation…</div>;
  }
  if (!investigation) {
    return <div className="text-critical-600">Investigation not found.</div>;
  }

  return (
    <div>
      <header className="mb-6 flex items-start justify-between">
        <div>
          <div className="text-xs text-ink-500 mb-1">Investigation #{investigation.id}</div>
          <h1 className="text-2xl font-display font-bold text-ink-900">{investigation.filename}</h1>
          <div className="flex items-center gap-2 mt-2">
            <SeverityBadge severity={risk?.severity} />
            <span className="text-xs text-ink-500 capitalize">{investigation.status.replace(/_/g, " ")}</span>
            {!isComplete && (
              <span className="flex items-center gap-1 text-xs text-primary-700">
                <LuLoaderCircle className="animate-spin" size={12} /> Analyzing…
              </span>
            )}
          </div>
        </div>
        <Link
          to={`/reports?investigation=${investigation.id}`}
          className="inline-flex items-center gap-2 bg-ink-900 hover:bg-ink-700 text-white text-sm font-semibold px-4 py-2.5 rounded-lg transition-colors"
        >
          <LuDownload size={16} /> Generate Report
        </Link>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-6">
          <FileInfoCard investigation={investigation} />
          <RiskCard risk={risk} />
        </div>
        <div className="lg:col-span-2 space-y-6">
          <StaticAnalysisCard analysis={staticAnalysis} />
          <ThreatIntelCard results={threatIntel} />
          <MitreCard mappings={mitre} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        <div className="lg:col-span-2">
          <IOCCard iocs={iocs} />
        </div>
        <TimelineCard events={investigation.timeline_events} />
      </div>

      <div className="mt-6">
        <AISummaryCard summary={aiSummary} />
      </div>
    </div>
  );
}
