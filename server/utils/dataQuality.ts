import type { DataQuality, QualityIssue, ColumnMetric } from '@shared/schema';

export function analyzeDataQuality(data: Record<string, any>[]): DataQuality {
  if (data.length === 0) {
    return {
      overallScore: 0,
      completeness: 0,
      consistency: 0,
      uniqueness: 0,
      validity: 0,
      columnMetrics: [],
      issues: [],
      recommendations: ['Upload a dataset to begin analysis']
    };
  }
  
  const columns = Object.keys(data[0]);
  const totalCells = data.length * columns.length;
  
  // Calculate completeness
  let totalMissing = 0;
  const columnMetrics: ColumnMetric[] = [];
  
  for (const col of columns) {
    const values = data.map(row => row[col]);
    const missingCount = values.filter(v => v === null || v === undefined || v === '').length;
    const nonNullValues = values.filter(v => v !== null && v !== undefined && v !== '');
    const uniqueValues = new Set(nonNullValues);
    
    totalMissing += missingCount;
    
    const dataType = inferColumnType(nonNullValues);
    
    columnMetrics.push({
      column: col,
      missingPercentage: (missingCount / data.length) * 100,
      uniqueValues: uniqueValues.size,
      dataType,
      sampleValues: Array.from(uniqueValues).slice(0, 3)
    });
  }
  
  const completeness = 1 - (totalMissing / totalCells);
  
  // Calculate consistency
  let consistencyScore = 1.0;
  const typeInconsistencies: string[] = [];
  
  for (const col of columns) {
    const values = data.map(row => row[col]).filter(v => v !== null && v !== undefined && v !== '');
    const types = new Set(values.map(v => typeof v));
    
    if (types.size > 1) {
      consistencyScore -= 0.1;
      typeInconsistencies.push(col);
    }
  }
  
  const consistency = Math.max(0, consistencyScore);
  
  // Calculate uniqueness
  const duplicateRows = findDuplicateRows(data);
  const uniqueness = 1 - (duplicateRows / data.length);
  
  // Calculate validity
  const validity = 0.9; // Simplified for now
  
  // Overall score (weighted average)
  const overallScore = Math.round(
    completeness * 0.4 +
    consistency * 0.3 +
    uniqueness * 0.2 +
    validity * 0.1
  ) * 100;
  
  // Detect issues
  const issues: QualityIssue[] = [];
  
  // Missing values
  const highMissingCols = columnMetrics.filter(m => m.missingPercentage > 20);
  if (highMissingCols.length > 0) {
    issues.push({
      type: 'missing_values',
      severity: 'high',
      count: highMissingCols.length,
      description: `${highMissingCols.length} columns have >20% missing values: ${highMissingCols.map(c => c.column).join(', ')}`
    });
  }
  
  // Duplicates
  if (duplicateRows > 0) {
    issues.push({
      type: 'duplicates',
      severity: duplicateRows > data.length * 0.1 ? 'high' : 'medium',
      count: duplicateRows,
      description: `Found ${duplicateRows} duplicate rows (${((duplicateRows / data.length) * 100).toFixed(1)}%)`
    });
  }
  
  // Type inconsistencies
  if (typeInconsistencies.length > 0) {
    issues.push({
      type: 'inconsistency',
      severity: 'medium',
      count: typeInconsistencies.length,
      description: `${typeInconsistencies.length} columns have mixed data types: ${typeInconsistencies.join(', ')}`
    });
  }
  
  // Outliers detection
  const numericColumns = columnMetrics.filter(m => m.dataType === 'integer' || m.dataType === 'float');
  for (const col of numericColumns) {
    const values = data.map(row => row[col.column]).filter(v => typeof v === 'number');
    const outliers = detectOutliersIQR(values);
    
    if (outliers.length > 0) {
      issues.push({
        type: 'outliers',
        severity: 'low',
        column: col.column,
        count: outliers.length,
        description: `${outliers.length} potential outliers in ${col.column}`
      });
    }
  }
  
  // Generate recommendations
  const recommendations: string[] = [];
  
  if (highMissingCols.length > 0) {
    recommendations.push(`Handle missing values in: ${highMissingCols.map(c => c.column).slice(0, 3).join(', ')}`);
  }
  
  if (duplicateRows > 0) {
    recommendations.push(`Remove ${duplicateRows} duplicate rows to improve data quality`);
  }
  
  if (typeInconsistencies.length > 0) {
    recommendations.push(`Standardize data types in columns: ${typeInconsistencies.slice(0, 3).join(', ')}`);
  }
  
  if (issues.length === 0) {
    recommendations.push('Your data quality is excellent! You can proceed with analysis.');
  }
  
  return {
    overallScore,
    completeness,
    consistency,
    uniqueness,
    validity,
    columnMetrics,
    issues,
    recommendations
  };
}

function inferColumnType(values: any[]): string {
  if (values.length === 0) return 'unknown';
  
  const allNumbers = values.every(v => typeof v === 'number');
  const allIntegers = values.every(v => Number.isInteger(v));
  const allBooleans = values.every(v => typeof v === 'boolean');
  
  if (allBooleans) return 'boolean';
  if (allNumbers) return allIntegers ? 'integer' : 'float';
  return 'string';
}

function findDuplicateRows(data: Record<string, any>[]): number {
  const seen = new Set<string>();
  let duplicates = 0;
  
  for (const row of data) {
    const key = JSON.stringify(row);
    if (seen.has(key)) {
      duplicates++;
    } else {
      seen.add(key);
    }
  }
  
  return duplicates;
}

function detectOutliersIQR(values: number[]): number[] {
  if (values.length < 4) return [];
  
  const sorted = [...values].sort((a, b) => a - b);
  const q1 = sorted[Math.floor(sorted.length * 0.25)];
  const q3 = sorted[Math.floor(sorted.length * 0.75)];
  const iqr = q3 - q1;
  
  const lowerBound = q1 - 1.5 * iqr;
  const upperBound = q3 + 1.5 * iqr;
  
  return values.filter(v => v < lowerBound || v > upperBound);
}
