import Papa from 'papaparse';
import * as XLSX from 'xlsx';
import type { DataPreview, ColumnInfo } from '@shared/schema';

export interface ParsedDataset {
  data: Record<string, any>[];
  columns: string[];
  rowCount: number;
  columnCount: number;
}

export async function parseCSV(buffer: Buffer): Promise<ParsedDataset> {
  return new Promise((resolve, reject) => {
    const text = buffer.toString('utf-8');
    
    Papa.parse(text, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true,
      complete: (results) => {
        const data = results.data as Record<string, any>[];
        const columns = results.meta.fields || [];
        
        resolve({
          data,
          columns,
          rowCount: data.length,
          columnCount: columns.length
        });
      },
      error: (error) => reject(error)
    });
  });
}

export function parseExcel(buffer: Buffer): ParsedDataset {
  const workbook = XLSX.read(buffer, { type: 'buffer' });
  const sheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[sheetName];
  
  const jsonData = XLSX.utils.sheet_to_json(worksheet, { defval: null });
  const data = jsonData as Record<string, any>[];
  
  const columns = data.length > 0 ? Object.keys(data[0]) : [];
  
  return {
    data,
    columns,
    rowCount: data.length,
    columnCount: columns.length
  };
}

export function parseJSON(buffer: Buffer): ParsedDataset {
  const text = buffer.toString('utf-8');
  const parsed = JSON.parse(text);
  
  let data: Record<string, any>[];
  
  if (Array.isArray(parsed)) {
    data = parsed;
  } else if (typeof parsed === 'object' && parsed !== null) {
    data = [parsed];
  } else {
    throw new Error('Invalid JSON format. Expected array or object.');
  }
  
  const columns = data.length > 0 ? Object.keys(data[0]) : [];
  
  return {
    data,
    columns,
    rowCount: data.length,
    columnCount: columns.length
  };
}

export async function parseFile(buffer: Buffer, filename: string): Promise<ParsedDataset> {
  const ext = filename.toLowerCase().split('.').pop();
  
  switch (ext) {
    case 'csv':
      return parseCSV(buffer);
    case 'xlsx':
    case 'xls':
      return parseExcel(buffer);
    case 'json':
      return parseJSON(buffer);
    default:
      throw new Error(`Unsupported file format: ${ext}`);
  }
}

export function createDataPreview(dataset: ParsedDataset, maxRows: number = 100): DataPreview {
  const { data, columns, rowCount, columnCount } = dataset;
  
  const columnInfo: ColumnInfo[] = columns.map(col => {
    const values = data.map(row => row[col]);
    const nonNullValues = values.filter(v => v !== null && v !== undefined && v !== '');
    const nullCount = values.length - nonNullValues.length;
    const uniqueValues = new Set(nonNullValues);
    
    const sampleValues = Array.from(uniqueValues).slice(0, 5);
    
    let type = 'string';
    if (nonNullValues.length > 0) {
      const firstValue = nonNullValues[0];
      if (typeof firstValue === 'number') {
        type = Number.isInteger(firstValue) ? 'int64' : 'float64';
      } else if (typeof firstValue === 'boolean') {
        type = 'bool';
      } else if (firstValue instanceof Date) {
        type = 'datetime64';
      }
    }
    
    return {
      name: col,
      type,
      nullCount,
      uniqueCount: uniqueValues.size,
      sampleValues
    };
  });
  
  return {
    columns: columnInfo,
    rows: data.slice(0, maxRows),
    totalRows: rowCount,
    totalColumns: columnCount
  };
}

export function inferDataTypes(data: Record<string, any>[]): Record<string, string> {
  if (data.length === 0) return {};
  
  const types: Record<string, string> = {};
  const columns = Object.keys(data[0]);
  
  for (const col of columns) {
    const values = data.map(row => row[col]).filter(v => v !== null && v !== undefined && v !== '');
    
    if (values.length === 0) {
      types[col] = 'unknown';
      continue;
    }
    
    const allNumbers = values.every(v => typeof v === 'number' || !isNaN(Number(v)));
    const allIntegers = values.every(v => Number.isInteger(Number(v)));
    const allBooleans = values.every(v => typeof v === 'boolean' || v === 'true' || v === 'false');
    
    if (allBooleans) {
      types[col] = 'boolean';
    } else if (allNumbers) {
      types[col] = allIntegers ? 'integer' : 'float';
    } else {
      types[col] = 'string';
    }
  }
  
  return types;
}
