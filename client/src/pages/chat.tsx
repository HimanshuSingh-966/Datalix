import { useEffect, useRef, useState } from 'react';
import { Header } from '@/components/Header';
import { MessageBubble } from '@/components/MessageBubble';
import { DataPreview } from '@/components/DataPreview';
import { ChartDisplay } from '@/components/ChartDisplay';
import { QualityScore } from '@/components/QualityScore';
import { SuggestedActions } from '@/components/SuggestedActions';
import { FileUpload } from '@/components/FileUpload';
import { TypingIndicator } from '@/components/LoadingStates';
import { EmptyState } from '@/components/EmptyStates';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useChatStore } from '@/lib/store';
import { generateId } from '@/lib/utils';
import { Send, Paperclip } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import type { ChatMessage } from '@shared/schema';

export default function ChatPage() {
  const {
    sessionId,
    messages,
    currentDataset,
    qualityScore,
    isLoading,
    addMessage,
    setCurrentDataset,
    setQualityScore,
    setIsLoading,
    clearSession,
  } = useChatStore();

  const [input, setInput] = useState('');
  const [showUploadDialog, setShowUploadDialog] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { toast } = useToast();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 128)}px`;
    }
  }, [input]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    addMessage(userMessage);
    setInput('');
    setIsLoading(true);

    try {
      // TODO: Replace with actual API call in backend integration
      await new Promise(resolve => setTimeout(resolve, 1500));

      const assistantMessage: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: 'I received your message! Once the backend is integrated, I\'ll be able to process your data operations using Groq and Gemini AI.',
        timestamp: new Date(),
        suggestedActions: [
          { label: 'Show Statistics', prompt: 'Show statistical summary' },
          { label: 'Create Visualization', prompt: 'Create a correlation heatmap' },
          { label: 'Export Data', prompt: 'Export as CSV' },
        ],
      };

      addMessage(assistantMessage);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: error instanceof Error ? error.message : 'An error occurred',
        timestamp: new Date(),
        error: true,
      };
      addMessage(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
    if (e.key === 'k' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      setInput('');
    }
  };

  const handleUpload = async (file: File) => {
    try {
      // TODO: Replace with actual API call in backend integration
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Mock response
      const mockDataPreview = {
        columns: [
          { name: 'id', type: 'int64', nullCount: 0, uniqueCount: 100, sampleValues: [1, 2, 3, 4, 5] },
          { name: 'name', type: 'object', nullCount: 5, uniqueCount: 95, sampleValues: ['Alice', 'Bob', 'Charlie', null, 'Diana'] },
          { name: 'age', type: 'int64', nullCount: 10, uniqueCount: 45, sampleValues: [25, 30, null, 35, 40] },
          { name: 'salary', type: 'float64', nullCount: 2, uniqueCount: 98, sampleValues: [50000, 60000, 75000, null, 90000] },
        ],
        rows: [
          { id: 1, name: 'Alice', age: 25, salary: 50000 },
          { id: 2, name: 'Bob', age: 30, salary: 60000 },
          { id: 3, name: 'Charlie', age: null, salary: 75000 },
          { id: 4, name: null, age: 35, salary: null },
          { id: 5, name: 'Diana', age: 40, salary: 90000 },
        ],
        totalRows: 100,
        totalColumns: 4,
        fileName: file.name,
      };

      const mockQuality = {
        overallScore: 67.5,
        completeness: 0.85,
        consistency: 0.92,
        uniqueness: 0.88,
        validity: 0.95,
        columnMetrics: [],
        issues: [
          { type: 'missing_values' as const, severity: 'medium' as const, column: 'name', count: 5, description: '5 missing values in name column' },
          { type: 'missing_values' as const, severity: 'medium' as const, column: 'age', count: 10, description: '10 missing values in age column' },
          { type: 'outliers' as const, severity: 'low' as const, column: 'salary', count: 3, description: '3 outliers detected in salary column' },
        ],
        recommendations: [
          'Impute missing values in age column using median',
          'Impute missing values in name column using mode or custom value',
          'Review outliers in salary column before removal',
        ],
      };

      setCurrentDataset(mockDataPreview);
      setQualityScore(mockQuality);

      const message: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: `✓ Loaded dataset: **${mockDataPreview.totalRows} rows × ${mockDataPreview.totalColumns} columns**\n\nQuality Score: **${Math.round(mockQuality.overallScore)}/100**\n\nI've analyzed your dataset. You can see the data preview and quality metrics below.`,
        timestamp: new Date(),
        dataPreview: mockDataPreview,
        suggestedActions: [
          { label: 'Clean Dataset', prompt: 'Clean the dataset and remove outliers' },
          { label: 'Show Statistics', prompt: 'Show statistical summary' },
          { label: 'Create Chart', prompt: 'Create a correlation heatmap' },
        ],
      };

      addMessage(message);
      setShowUploadDialog(false);
      toast({ description: 'Dataset uploaded successfully!' });
    } catch (error) {
      toast({ 
        description: error instanceof Error ? error.message : 'Upload failed', 
        variant: 'destructive' 
      });
    }
  };

  const handleSuggestedAction = (prompt: string) => {
    setInput(prompt);
    textareaRef.current?.focus();
  };

  const handleNewSession = () => {
    if (messages.length > 0) {
      if (confirm('Start a new session? This will clear the current conversation.')) {
        clearSession();
        toast({ description: 'New session started' });
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      <Header
        onUploadClick={() => setShowUploadDialog(true)}
        onNewSession={handleNewSession}
        datasetLoaded={!!currentDataset}
        qualityScore={qualityScore?.overallScore}
      />

      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-6">
          {messages.length === 0 ? (
            <EmptyState type="no-messages" onAction={() => setShowUploadDialog(true)} />
          ) : (
            <div className="space-y-6">
              {messages.map((message) => (
                <div key={message.id} className="space-y-4">
                  <MessageBubble
                    message={message}
                    onRegenerate={() => {
                      // TODO: Implement regenerate
                      toast({ description: 'Regenerate feature coming soon!' });
                    }}
                  />

                  {message.dataPreview && (
                    <div className="ml-11">
                      <DataPreview data={message.dataPreview} />
                    </div>
                  )}

                  {message.chartData && (
                    <div className="ml-11">
                      <ChartDisplay chartData={message.chartData} />
                    </div>
                  )}

                  {message.suggestedActions && message.suggestedActions.length > 0 && (
                    <div className="ml-11">
                      <SuggestedActions
                        actions={message.suggestedActions}
                        onSelect={handleSuggestedAction}
                      />
                    </div>
                  )}
                </div>
              ))}

              {isLoading && (
                <TypingIndicator />
              )}

              <div ref={messagesEndRef} />
            </div>
          )}

          {qualityScore && currentDataset && (
            <div className="mt-8">
              <QualityScore quality={qualityScore} />
            </div>
          )}
        </div>
      </div>

      <div className="border-t border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-end gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setShowUploadDialog(true)}
              data-testid="button-attach-file"
            >
              <Paperclip className="h-5 w-5" />
            </Button>

            <div className="flex-1 relative">
              <Textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type your message... (Shift+Enter for new line)"
                className="resize-none min-h-[44px] max-h-32 pr-12"
                rows={1}
                disabled={isLoading}
                data-testid="input-chat-message"
              />
            </div>

            <Button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              size="icon"
              data-testid="button-send-message"
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>

          <div className="mt-3 flex items-center gap-2 text-xs text-muted-foreground" data-testid="container-examples">
            <span>Examples:</span>
            <button
              className="text-primary hover:underline"
              onClick={() => handleSuggestedAction('Show correlation matrix')}
              data-testid="example-correlation"
            >
              Show correlation
            </button>
            <span>•</span>
            <button
              className="text-primary hover:underline"
              onClick={() => handleSuggestedAction('Export as CSV')}
              data-testid="example-export"
            >
              Export as CSV
            </button>
            <span>•</span>
            <button
              className="text-primary hover:underline"
              onClick={() => handleSuggestedAction('Create a histogram of age')}
              data-testid="example-histogram"
            >
              Create histogram
            </button>
          </div>
        </div>
      </div>

      <Dialog open={showUploadDialog} onOpenChange={setShowUploadDialog}>
        <DialogContent className="sm:max-w-2xl">
          <DialogHeader>
            <DialogTitle>Upload Dataset</DialogTitle>
          </DialogHeader>
          <FileUpload onUpload={handleUpload} />
        </DialogContent>
      </Dialog>
    </div>
  );
}
