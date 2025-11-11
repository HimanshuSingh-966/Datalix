import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Badge } from '@/components/ui/badge';
import { AIProviderSelector } from '@/components/AIProviderSelector';
import { Upload, Plus, User, LogOut, Settings, History } from 'lucide-react';
import { useAuthStore } from '@/lib/store';

interface HeaderProps {
  onUploadClick?: () => void;
  onNewSession?: () => void;
  onSessionHistory?: () => void;
  onSettings?: () => void;
  datasetLoaded?: boolean;
  qualityScore?: number;
}

export function Header({ onUploadClick, onNewSession, onSessionHistory, onSettings, datasetLoaded, qualityScore }: HeaderProps) {
  const { user, logout } = useAuthStore();

  const getQualityBadgeVariant = (score?: number): 'default' | 'secondary' | 'destructive' => {
    if (!score) return 'secondary';
    if (score >= 75) return 'default';
    if (score >= 50) return 'secondary';
    return 'destructive';
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center justify-between px-6">
        {/* Logo and Title */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-chart-1 flex items-center justify-center" data-testid="logo-icon">
              <span className="text-lg font-bold text-white">D</span>
            </div>
            <div>
              <h1 className="text-xl font-bold" data-testid="text-app-title">DataLix AI</h1>
              <p className="text-xs text-muted-foreground" data-testid="text-app-subtitle">AI-Powered Data Analysis</p>
            </div>
          </div>

          {/* Dataset Status */}
          {datasetLoaded && (
            <div className="hidden md:flex items-center gap-2 ml-6 pl-6 border-l border-border" data-testid="dataset-status">
              <span className="text-sm text-muted-foreground" data-testid="text-dataset-loaded">Dataset loaded</span>
              {qualityScore !== undefined && (
                <Badge variant={getQualityBadgeVariant(qualityScore)} data-testid="badge-quality-score">
                  Score: {Math.round(qualityScore)}/100
                </Badge>
              )}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          <AIProviderSelector />
          
          <Button
            variant="outline"
            size="sm"
            onClick={onUploadClick}
            data-testid="button-header-upload"
          >
            <Upload className="h-4 w-4 mr-2" />
            <span className="hidden sm:inline">Upload</span>
          </Button>

          <Button
            variant="default"
            size="sm"
            onClick={onNewSession}
            data-testid="button-new-session"
          >
            <Plus className="h-4 w-4 mr-2" />
            <span className="hidden sm:inline">New Session</span>
          </Button>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" data-testid="button-user-menu">
                <User className="h-5 w-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <div className="px-2 py-1.5">
                <p className="text-sm font-medium" data-testid="text-user-name">{user?.username || 'User'}</p>
                <p className="text-xs text-muted-foreground" data-testid="text-user-email">{user?.email || 'user@example.com'}</p>
              </div>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => onSessionHistory?.()} data-testid="menu-history">
                <History className="h-4 w-4 mr-2" />
                Session History
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onSettings?.()} data-testid="menu-settings">
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={logout} data-testid="menu-logout">
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
