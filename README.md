# MedCore - Medical AI Assistant Application

## Overview

MedCore is a modern medical AI assistant application built with React, TypeScript, and Vite. It provides patients with AI-powered health consultations, appointment booking, doctor search, and portal access.

## 🚀 Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Vitest** - Testing framework
- **CSS Modules** - Component styling
- **Lucide React** - Icon library

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Basic UI components (Button, Card, etc.)
│   └── shared/         # Shared components (NavBar, TypingDots)
├── features/           # Feature-specific components
│   ├── admin/          # Admin dashboard
│   ├── ai-clinical/    # AI clinical assistant
│   ├── booking/        # Appointment booking
│   ├── chatbot/        # AI chatbot interface
│   ├── doctors/        # Doctor listings
│   ├── etl/            # ETL operations
│   ├── home/           # Home page
│   └── portal/         # Patient portal
├── hooks/              # Custom React hooks
├── services/           # External service integrations
├── styles/             # Global styles and design tokens
├── types/              # TypeScript type definitions
└── test/               # Test files
```

## 🎨 Styling Architecture

### CSS Modules

All components use CSS Modules for styling. This provides:
- Scoped styles to avoid conflicts
- Better performance through build-time processing
- Co-located styles with components
- TypeScript integration

### Design Tokens

Design tokens are defined in `src/styles/variables.css` as CSS custom properties:

```css
:root {
  --color-primary: #0C4A6E;
  --color-green: #059669;
  --spacing-md: 1rem;
  --radius-lg: 12px;
  /* ... more tokens */
}
```

### Usage Example

```tsx
// Component.tsx
import styles from './Component.module.css';

function Component() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Title</h1>
    </div>
  );
}
```

```css
/* Component.module.css */
.container {
  padding: var(--spacing-md);
  background-color: var(--color-card);
}

.title {
  font-size: 24px;
  color: var(--color-text);
}
```

## 🧩 Component Library

### UI Components

#### Avatar
```tsx
<Avatar init="JD" color="#3b82f6" size="md" />
```

#### Badge
```tsx
<Badge text="Success" variant="success" size="md" />
```

#### Button
```tsx
<Button variant="primary" size="md" onClick={handleClick}>
  Click Me
</Button>
```

#### Card
```tsx
<Card size="md" variant="elevated">
  Content
</Card>
```

#### StatusBadge
```tsx
<StatusBadge status="connected" showIndicator={true} />
```

### Shared Components

#### NavBar
```tsx
<NavBar view="home" onNav={handleNav} />
```

#### TypingDots
```tsx
<TypingDots size="md" color="primary" label="Thinking" />
```

## 📝 Type Definitions

Common types are centralized in `src/types/index.ts`:

```typescript
export type ViewType = 'home' | 'chatbot' | 'doctors' | ...;

export interface Doctor {
  id: string;
  name: string;
  specialty: string;
  // ...
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:ui

# Run tests with coverage
npm run test:coverage

# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration
```

### Testing Components

```tsx
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct variant class', () => {
    render(<Button variant="outline">Click</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('outline');
  });
});
```

## 🏗️ Development

### Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Code Quality

```bash
# Run linter
npm run lint

# Type check
npm run typecheck
```

## 📚 Best Practices

### Component Development

1. **Use CSS Modules** for all component styling
2. **Define TypeScript interfaces** for props
3. **Follow naming conventions**:
   - Component files: PascalCase (e.g., `Button.tsx`)
   - Style files: `ComponentName.module.css`
   - Test files: `ComponentName.test.tsx`

4. **Co-locate styles** with components
5. **Use design tokens** instead of hardcoded values
6. **Write tests** for all components

### Styling Guidelines

**DO:**
```tsx
import styles from './MyComponent.module.css';

<div className={styles.container}>
  Content
</div>
```

**DON'T:**
```tsx
<div style={{ padding: '20px', borderRadius: '8px' }}>
  Content
</div>
```

### Type Safety

**DO:**
```tsx
interface Props {
  title: string;
  count: number;
  onAction: () => void;
}

function Component({ title, count, onAction }: Props) {
  // ...
}
```

**DON'T:**
```tsx
function Component(props: any) {
  // ...
}
```

## 🎯 Features

- **AI Chatbot**: Interactive health consultation
- **Doctor Search**: Find and book appointments
- **Patient Portal**: Access health records
- **AI Clinical**: AI-powered clinical analysis
- **ETL Hub**: Data management
- **Admin Dashboard**: System administration

## 🔐 Security Considerations

- All API calls should be authenticated
- Patient data must be encrypted
- Follow HIPAA compliance guidelines
- Regular security audits recommended

## 📖 Documentation

- [Styling Guide](./STYLING_GUIDE.md) - Detailed styling architecture
- [Refactoring Summary](./REFACTORING_SUMMARY.md) - Recent changes and improvements

## 🤝 Contributing

1. Follow the established code style
2. Write tests for new features
3. Update documentation
4. Submit pull requests for review

## 📄 License

[Add your license information here]

## 📞 Support

For support and questions, please contact [your support contact].

---

Built with ❤️ for better healthcare
