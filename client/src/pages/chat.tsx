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
import { ExampleDatasetDialog } from '@/components/ExampleDatasetDialog';
import { SettingsDialog } from '@/components/SettingsDialog';
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
    aiProvider,
    addMessage,
    setCurrentDataset,
    setQualityScore,
    setIsLoading,
    clearSession,
  } = useChatStore();

  const [input, setInput] = useState('');
  const [showUploadDialog, setShowUploadDialog] = useState(false);
  const [showExampleDialog, setShowExampleDialog] = useState(false);
  const [showSettingsDialog, setShowSettingsDialog] = useState(false);
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
    if (!sessionId) {
      toast({ description: 'Please upload a dataset first', variant: 'destructive' });
      return;
    }

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
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: input,
          provider: aiProvider
        })
      });

      if (!response.ok) {
        throw new Error('Failed to process message');
      }

      const data = await response.json();

      const assistantMessage: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: data.message,
        timestamp: new Date(),
        functionCalls: data.function_calls,
        chartData: data.chart_data,
        dataPreview: data.data_preview,
        suggestedActions: data.suggested_actions,
      };

      addMessage(assistantMessage);

      // Update dataset if there's a new preview
      if (data.data_preview) {
        setCurrentDataset(data.data_preview);
      }
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
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || 'Upload failed');
      }

      const data = await response.json();

      // Store session ID
      useChatStore.setState({ sessionId: data.sessionId });

      // Set data preview and quality
      setCurrentDataset(data.preview);
      setQualityScore({
        overallScore: data.qualityScore,
        completeness: 0, // Will be populated from issues
        consistency: 0,
        uniqueness: 0,
        validity: 0,
        columnMetrics: [],
        issues: data.issues || [],
        recommendations: []
      });

      const message: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: `✓ Loaded dataset: **${data.datasetInfo.rows} rows × ${data.datasetInfo.columns} columns**\n\nQuality Score: **${Math.round(data.qualityScore)}/100**\n\nI've analyzed your dataset. ${data.issues.length > 0 ? `Found ${data.issues.length} potential issues.` : 'Your data looks good!'} Ask me anything about your data!`,
        timestamp: new Date(),
        dataPreview: data.preview,
        suggestedActions: [
          { label: 'Show Statistics', prompt: 'Show statistical summary' },
          { label: 'Correlation Matrix', prompt: 'Show correlation matrix' },
          { label: 'Create Visualization', prompt: 'Create a scatter plot of the first two numeric columns' },
          ...(data.issues.length > 0 ? [{ label: 'Clean Data', prompt: 'Help me clean this dataset' }] : [])
        ],
      };

      addMessage(message);
      setShowUploadDialog(false);
      toast({ description: 'Dataset uploaded and analyzed!' });
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

  const handleExampleDataset = () => {
    setShowExampleDialog(true);
  };

  const handleExampleDatasetLoaded = (data: any) => {
    useChatStore.setState({ sessionId: data.sessionId });
    setCurrentDataset(data.preview);
    
    const issues = data.issues ?? [];
    setQualityScore({
      overallScore: data.qualityScore,
      completeness: 0,
      consistency: 0,
      uniqueness: 0,
      validity: 0,
      columnMetrics: [],
      issues: issues,
      recommendations: []
    });

    const message: ChatMessage = {
      id: generateId(),
      role: 'assistant',
      content: `✓ Loaded example dataset: **${data.exampleDatasetName}**\n\n**${data.datasetInfo.rows} rows × ${data.datasetInfo.columns} columns**\n\nQuality Score: **${Math.round(data.qualityScore)}/100**\n\nI've loaded a sample dataset for you to explore. ${issues.length > 0 ? `Found ${issues.length} potential issues.` : 'The data looks good!'} Try asking me about the data!`,
      timestamp: new Date(),
      dataPreview: data.preview,
      suggestedActions: [
        { label: 'Show Statistics', prompt: 'Show statistical summary' },
        { label: 'Correlation Matrix', prompt: 'Show correlation matrix' },
        { label: 'Create Visualization', prompt: 'Create a scatter plot' },
        ...(issues.length > 0 ? [{ label: 'Clean Data', prompt: 'Help me clean this dataset' }] : [])
      ],
    };

    addMessage(message);
  };

  const handleSessionHistory = () => {
    toast({ 
      description: 'Session history feature coming soon!',
      variant: 'default'
    });
  };

  const handleSettings = () => {
    setShowSettingsDialog(true);
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      <Header
        onUploadClick={() => setShowUploadDialog(true)}
        onNewSession={handleNewSession}
        onSessionHistory={handleSessionHistory}
        onSettings={handleSettings}
        datasetLoaded={!!currentDataset}
        qualityScore={qualityScore?.overallScore}
      />

      <div className="flex-1 overflow-y-auto flex justify-center">
        <div className="w-full max-w-3xl px-4 py-6">
          {messages.length === 0 ? (
            <EmptyState 
              type="no-messages" 
              onAction={() => setShowUploadDialog(true)} 
              onExampleDataset={handleExampleDataset}
            />
          ) : (
            <div className="space-y-6">
              {messages.map((message) => (
                <div key={message.id} className="space-y-4">
                  <MessageBubble
                    message={message}
                    onRegenerate={() => {
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

      <div className="border-t border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 flex justify-center">
        <div className="w-full max-w-3xl px-4 py-4">
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

      <ExampleDatasetDialog
        open={showExampleDialog}
        onOpenChange={setShowExampleDialog}
        onDatasetLoaded={handleExampleDatasetLoaded}
      />

      <SettingsDialog
        open={showSettingsDialog}
        onOpenChange={setShowSettingsDialog}
      />
    </div>
  );
}
