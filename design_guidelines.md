# DataLix AI Design Guidelines

## Design Approach

**System**: Hybrid approach drawing from Linear's clean professionalism, ChatGPT's conversational interface, and Observable's data visualization clarity.

**Core Principles**:
- Information density balanced with breathing room
- Data-first presentation with minimal chrome
- Conversational interface that feels professional, not playful
- Clarity and scannability for complex data operations
- Consistent, predictable interaction patterns

---

## Typography System

**Font Stack**:
- **Interface**: Inter (primary) - clean, readable at all sizes
- **Data/Code**: JetBrains Mono - for tables, code snippets, technical content

**Hierarchy**:
- **Page Headers**: text-2xl, font-semibold (main app title)
- **Section Headers**: text-lg, font-semibold (data quality score, chart titles)
- **Body Text**: text-base, font-normal (AI responses, descriptions)
- **Metadata**: text-sm, font-medium (timestamps, row counts, data types)
- **Captions**: text-xs, font-normal (hints, secondary info)
- **Data Values**: text-sm, font-mono (table cells, statistics)

---

## Layout System

**Spacing Primitives**: Tailwind units of 2, 4, 6, and 8 for consistency
- Component padding: p-4 or p-6
- Section spacing: space-y-6 or space-y-8
- Inline element gaps: gap-2 or gap-4
- Page margins: px-6 or px-8

**Grid Structure**:
- Single column chat layout (max-w-4xl centered for readability)
- Two-column layouts for data comparisons (before/after)
- Three-column grids for statistics cards
- Full-width for data tables and visualizations

---

## Core Components

### Chat Interface

**Message Structure**:
- User messages: right-aligned, max-w-2xl, rounded-2xl, distinct treatment
- AI messages: left-aligned, max-w-3xl, rounded-2xl, includes avatar
- Message spacing: space-y-4 between message groups
- Padding within bubbles: px-4 py-3 for text, px-6 py-4 for data-rich content

**Message Elements**:
- Avatar: 8×8 rounded-full for AI, user initials for users
- Timestamp: text-xs below message, subtle
- Actions toolbar: appears on hover, right-aligned icons
- Markdown rendering: proper heading hierarchy, code blocks with syntax highlighting

**Input Area**:
- Textarea: auto-expanding with max-h-32, rounded-xl border
- Attachment button: left-aligned icon button
- Send button: prominent, rounded-lg, min-w-12 for touch targets
- Example prompts: horizontal pills below input, text-sm, interactive

### Data Preview Tables

**Structure**:
- Compact density: text-sm throughout
- Header row: font-semibold with data type indicators (subtle badges)
- Cell padding: px-3 py-2 for readability
- Borders: subtle horizontal rules between rows
- Null highlighting: distinct visual treatment without distracting
- Expandable: initial 5 rows, "Show more" trigger
- Metadata bar: row/column count, file size above table

**Presentation**:
- Monospace font for numeric data
- Right-align numbers, left-align text
- Truncate long strings with ellipsis, tooltip on hover
- Sticky header on scroll
- Zebra striping for rows (subtle alternation)

### Data Visualizations

**Chart Container**:
- Full-width responsive (w-full)
- Aspect ratio maintained (aspect-video for most charts)
- Border and subtle elevation for separation
- Title: text-lg font-semibold above chart
- Legend: positioned appropriately per chart type
- Export button: top-right corner, icon only

**Chart Types Layout**:
- Small multiples: grid-cols-2 on desktop for comparisons
- Single large chart: full container width
- Chart + statistics: two-column layout (60/40 split)

### Quality Score Display

**Presentation**:
- Large prominent score: text-4xl font-bold
- Progress ring or bar visualization
- Breakdown metrics: grid of 4 cards showing sub-scores
- Issue list: vertical stack with severity indicators
- Recommendations: actionable cards with clear CTAs

### Suggested Actions

**Layout**:
- Horizontal scrolling container
- Pills: rounded-full px-4 py-2, font-medium text-sm
- Gap: gap-2 between pills
- Icons: leading icons for visual scanning
- Maximum 5 visible, scroll for more

### Statistics Cards

**Grid Layout**:
- grid-cols-3 on desktop, grid-cols-2 on tablet, grid-cols-1 on mobile
- Card structure: rounded-xl border, p-6
- Metric value: text-3xl font-bold
- Metric label: text-sm above value
- Trend indicator: small chart or arrow if applicable

### File Upload Modal

**Structure**:
- Center-aligned modal, max-w-2xl
- Drag zone: min-h-64, dashed border, rounded-xl
- Large icon and helper text centered
- File list: vertical stack below drop zone
- Progress bars: full-width per file
- Actions: right-aligned buttons at bottom

### Header Bar

**Layout**:
- Full-width, sticky top, border-b
- Logo + title: left-aligned
- Dataset indicator: center (when active)
- Actions + user menu: right-aligned
- Height: h-16 for consistent top bar
- Padding: px-6 horizontal

### Navigation Elements

**Session Management**:
- Sidebar toggle or dropdown menu
- Session list: vertical stack with timestamps
- Active session: distinct visual treatment
- New session button: prominent placement

### Empty States

**Structure**:
- Center-aligned content, py-12 or py-20
- Large icon or illustration
- Headline: text-xl font-semibold
- Description: text-base, max-w-prose
- Suggested actions: grid of action cards below
- Action cards: 2-column grid, border, rounded-lg, p-4, hover state

### Loading States

**Patterns**:
- Typing indicator: 3 dots, bouncing animation, within message bubble
- Skeleton loaders: match data table structure with subtle pulse
- Spinner: centered for full-screen operations
- Progress bar: linear, indeterminate or determinate

### Error States

**Display**:
- Inline errors: within message bubble, distinct treatment
- Banner errors: top of viewport, dismissible
- Error details: expandable accordion
- Retry button: always present, clear affordance

---

## Responsive Behavior

**Breakpoints**:
- Mobile: single column, stacked components
- Tablet: selective two-column layouts for data
- Desktop: full multi-column, max utilization

**Mobile Considerations**:
- Touch targets: minimum 44×44 for all interactive elements
- Simplified tables: horizontal scroll or card view
- Collapsible sections: conserve vertical space
- Bottom-aligned input area: fixed position

---

## Micro-interactions

**Minimal Animation Philosophy**:
- Message sending: smooth scroll to bottom
- Table expand/collapse: height transition
- Chart rendering: fade-in once data loaded
- No decorative animations
- Focus on instant feedback for actions

---

## Component Density

**Information Hierarchy**:
- Generous whitespace around major sections (space-y-8)
- Tight grouping within related elements (space-y-2)
- Data tables: compact but scannable
- Chat messages: comfortable reading distance

---

## Accessibility

**Focus States**: 
- Visible focus rings on all interactive elements (ring-2 ring-offset-2)
- Keyboard navigation: logical tab order throughout
- Skip links: for main content areas

**Content**:
- Sufficient contrast ratios for all text
- Alt text for icons and charts
- ARIA labels for complex interactions
- Screen reader announcements for dynamic content updates