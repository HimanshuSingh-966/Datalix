import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Upload, Sparkles, FileText, TrendingUp } from 'lucide-react';

interface EmptyStateProps {
  type: 'no-data' | 'no-messages' | 'error';
  onAction?: () => void;
  onExampleDataset?: () => void;
}

export function EmptyState({ type, onAction, onExampleDataset }: EmptyStateProps) {
  if (type === 'no-messages') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] px-6 text-center" data-testid="empty-state-no-messages">
        <h1 className="font-heading text-5xl md:text-6xl mb-4 text-foreground" data-testid="text-welcome-title">
          Welcome to DataLix
        </h1>
        <p className="text-muted-foreground text-lg mb-12 max-w-2xl" data-testid="text-welcome-description">
          Your AI-powered data analysis companion. Upload a dataset and start exploring through natural conversation.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center gap-3 mb-8">
          <Button 
            onClick={() => onAction?.()} 
            size="lg"
            className="min-w-[160px]"
            data-testid="button-upload-dataset"
          >
            <Upload className="h-4 w-4 mr-2" />
            Upload Dataset
          </Button>
          <Button 
            onClick={() => onExampleDataset?.()} 
            variant="outline"
            size="lg"
            className="min-w-[160px]"
            data-testid="button-try-example"
          >
            <FileText className="h-4 w-4 mr-2" />
            Try Example
          </Button>
        </div>

        <div className="mt-4">
          <p className="text-xs text-muted-foreground mb-3">Try asking:</p>
          <div className="flex flex-wrap gap-2 justify-center max-w-xl">
            <span className="text-sm text-foreground/70 px-3 py-1 rounded-full border border-border/50">
              Show me the data quality score
            </span>
            <span className="text-sm text-foreground/70 px-3 py-1 rounded-full border border-border/50">
              Remove outliers
            </span>
            <span className="text-sm text-foreground/70 px-3 py-1 rounded-full border border-border/50">
              Create a correlation heatmap
            </span>
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
