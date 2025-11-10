import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Upload, Sparkles, FileText, TrendingUp } from 'lucide-react';

interface EmptyStateProps {
  type: 'no-data' | 'no-messages' | 'error';
  onAction?: () => void;
}

export function EmptyState({ type, onAction }: EmptyStateProps) {
  if (type === 'no-messages') {
    return (
      <div className="flex flex-col items-center justify-center py-20 px-6 text-center" data-testid="empty-state-no-messages">
        <div className="p-6 rounded-full bg-primary/10 mb-6">
          <Sparkles className="h-12 w-12 text-primary" data-testid="icon-welcome" />
        </div>
        <h2 className="text-2xl font-semibold mb-2" data-testid="text-welcome-title">Welcome to DataLix AI!</h2>
        <p className="text-muted-foreground mb-6 max-w-md" data-testid="text-welcome-description">
          Upload a dataset and start analyzing with natural language. Clean, transform, visualize, and export your data—all through conversation.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl w-full">
          <Card className="p-6 text-left hover-elevate cursor-pointer transition-all" onClick={() => onAction?.()}>
            <div className="flex items-start gap-4">
              <div className="p-3 rounded-lg bg-chart-1/10">
                <Upload className="h-6 w-6 text-chart-1" />
              </div>
              <div>
                <h3 className="font-semibold mb-1">Upload Data</h3>
                <p className="text-sm text-muted-foreground">
                  Start by uploading your CSV, Excel, JSON, or Parquet file
                </p>
              </div>
            </div>
          </Card>

          <Card className="p-6 text-left hover-elevate cursor-pointer transition-all">
            <div className="flex items-start gap-4">
              <div className="p-3 rounded-lg bg-chart-2/10">
                <FileText className="h-6 w-6 text-chart-2" />
              </div>
              <div>
                <h3 className="font-semibold mb-1">Example Datasets</h3>
                <p className="text-sm text-muted-foreground">
                  Try with sample data to explore features
                </p>
              </div>
            </div>
          </Card>
        </div>

        <div className="mt-8 p-4 bg-muted/50 rounded-lg max-w-md">
          <p className="text-xs text-muted-foreground mb-2">Try asking:</p>
          <div className="space-y-1">
            <p className="text-sm">• "Show me the data quality score"</p>
            <p className="text-sm">• "Remove outliers from the price column"</p>
            <p className="text-sm">• "Create a correlation heatmap"</p>
          </div>
        </div>
      </div>
    );
  }

  if (type === 'no-data') {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-6 text-center" data-testid="empty-state-no-data">
        <div className="p-6 rounded-full bg-muted mb-4">
          <TrendingUp className="h-10 w-10 text-muted-foreground" />
        </div>
        <h3 className="text-xl font-semibold mb-2">No data loaded</h3>
        <p className="text-muted-foreground mb-4 max-w-sm">
          Upload a dataset to start analyzing and visualizing your data
        </p>
        {onAction && (
          <Button onClick={onAction} data-testid="button-upload-data">
            <Upload className="h-4 w-4 mr-2" />
            Upload Dataset
          </Button>
        )}
      </div>
    );
  }

  if (type === 'error') {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-6 text-center" data-testid="empty-state-error">
        <div className="p-6 rounded-full bg-destructive/10 mb-4">
          <FileText className="h-10 w-10 text-destructive" />
        </div>
        <h3 className="text-xl font-semibold mb-2">Something went wrong</h3>
        <p className="text-muted-foreground mb-4 max-w-sm">
          We encountered an error. Please try again or contact support if the problem persists.
        </p>
        {onAction && (
          <Button onClick={onAction} variant="outline" data-testid="button-retry">
            Try Again
          </Button>
        )}
      </div>
    );
  }

  return null;
}
