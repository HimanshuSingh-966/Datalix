import type { StatisticResult } from '@shared/schema';
import { Card } from '@/components/ui/card';
import { formatNumber } from '@/lib/utils';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface StatisticsCardsProps {
  statistics: StatisticResult[];
}

export function StatisticsCards({ statistics }: StatisticsCardsProps) {
  if (statistics.length === 0) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" data-testid="statistics-cards">
      {statistics.map((stat) => (
        <Card key={stat.column} className="p-6" data-testid={`stat-card-${stat.column}`}>
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm text-muted-foreground mb-1" data-testid="label-stat-column">Column</p>
              <h3 className="text-lg font-semibold font-mono" data-testid={`text-column-name-${stat.column}`}>{stat.column}</h3>
            </div>
            <div className="p-2 rounded-lg bg-primary/10">
              <TrendingUp className="h-5 w-5 text-primary" data-testid="icon-stat-trend" />
            </div>
          </div>

          <div className="space-y-3">
            {stat.mean !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Mean</span>
                <span className="text-sm font-semibold font-mono">{formatNumber(stat.mean)}</span>
              </div>
            )}

            {stat.median !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Median</span>
                <span className="text-sm font-semibold font-mono">{formatNumber(stat.median)}</span>
              </div>
            )}

            {stat.std !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Std Dev</span>
                <span className="text-sm font-semibold font-mono">{formatNumber(stat.std)}</span>
              </div>
            )}

            {stat.min !== undefined && stat.max !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Range</span>
                <span className="text-sm font-semibold font-mono">
                  {formatNumber(stat.min)} - {formatNumber(stat.max)}
                </span>
              </div>
            )}

            {stat.count !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Count</span>
                <span className="text-sm font-semibold font-mono">{formatNumber(stat.count, 0)}</span>
              </div>
            )}

            {stat.q25 !== undefined && stat.q75 !== undefined && (
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">IQR</span>
                <span className="text-sm font-semibold font-mono">
                  {formatNumber(stat.q25)} - {formatNumber(stat.q75)}
                </span>
              </div>
            )}
          </div>
        </Card>
      ))}
    </div>
  );
}
