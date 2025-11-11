import { mean, median, standardDeviation, min, max, quantile } from 'simple-statistics';
import type { StatisticResult, CorrelationMatrix } from '@shared/schema';

export function calculateStatistics(data: Record<string, any>[], columns?: string[]): StatisticResult[] {
  const numericColumns = columns || getNumericColumns(data);
  const results: StatisticResult[] = [];
  
  for (const col of numericColumns) {
    const values = data
      .map(row => row[col])
      .filter(v => typeof v === 'number' && !isNaN(v));
    
    if (values.length === 0) continue;
    
    results.push({
      column: col,
      mean: mean(values),
      median: median(values),
      std: standardDeviation(values),
      min: min(values),
      max: max(values),
      count: values.length,
      q25: quantile(values, 0.25),
      q75: quantile(values, 0.75)
    });
  }
  
  return results;
}

export function calculateCorrelation(data: Record<string, any>[], columns?: string[]): CorrelationMatrix {
  const numericColumns = columns || getNumericColumns(data);
  
  const matrix: number[][] = [];
  
  for (const col1 of numericColumns) {
    const row: number[] = [];
    const values1 = data.map(r => r[col1]).filter(v => typeof v === 'number' && !isNaN(v));
    
    for (const col2 of numericColumns) {
      const values2 = data.map(r => r[col2]).filter(v => typeof v === 'number' && !isNaN(v));
      
      if (values1.length === 0 || values2.length === 0) {
        row.push(0);
        continue;
      }
      
      const corr = pearsonCorrelation(values1, values2);
      row.push(corr);
    }
    
    matrix.push(row);
  }
  
  return {
    columns: numericColumns,
    matrix
  };
}

function pearsonCorrelation(x: number[], y: number[]): number {
  const n = Math.min(x.length, y.length);
  if (n === 0) return 0;
  
  const meanX = mean(x.slice(0, n));
  const meanY = mean(y.slice(0, n));
  
  let numerator = 0;
  let sumSqX = 0;
  let sumSqY = 0;
  
  for (let i = 0; i < n; i++) {
    const dx = x[i] - meanX;
    const dy = y[i] - meanY;
    numerator += dx * dy;
    sumSqX += dx * dx;
    sumSqY += dy * dy;
  }
  
  const denominator = Math.sqrt(sumSqX * sumSqY);
  
  if (denominator === 0) return 0;
  
  return numerator / denominator;
}

function getNumericColumns(data: Record<string, any>[]): string[] {
  if (data.length === 0) return [];
  
  const columns = Object.keys(data[0]);
  return columns.filter(col => {
    const values = data.map(row => row[col]);
    return values.some(v => typeof v === 'number');
  });
}

export function describeDataset(data: Record<string, any>[]): Record<string, any> {
  const columns = data.length > 0 ? Object.keys(data[0]) : [];
  const numericCols = getNumericColumns(data);
  
  return {
    shape: [data.length, columns.length],
    columns: columns,
    numericColumns: numericCols,
    dtypes: columns.reduce((acc, col) => {
      const values = data.map(row => row[col]).filter(v => v !== null && v !== undefined);
      if (values.length === 0) {
        acc[col] = 'unknown';
      } else if (values.every(v => typeof v === 'number')) {
        acc[col] = 'number';
      } else if (values.every(v => typeof v === 'boolean')) {
        acc[col] = 'boolean';
      } else {
        acc[col] = 'string';
      }
      return acc;
    }, {} as Record<string, string>),
    statistics: calculateStatistics(data, numericCols)
  };
}
