# MedCore Styling Guide

## Overview

This document outlines the styling architecture and best practices for the MedCore application. We have migrated from inline styles to CSS Modules following industry best practices.

## Architecture

### CSS Modules

All UI components now use CSS Modules for styling. This approach provides:
- **Scoped Styles**: Class names are locally scoped to avoid conflicts
- **Better Performance**: Styles are processed at build time
- **Maintainability**: Styles are co-located with components
- **Type Safety**: TypeScript integration for better developer experience

### File Structure

```
src/
├── components/
│   └── ui/
│       ├── Avatar.tsx
│       ├── Avatar.module.css
│       ├── Badge.tsx
│       ├── Badge.module.css
│       ├── Button.tsx
│       ├── Button.module.css
│       ├── Card.tsx
│       ├── Card.module.css
│       ├── StatusBadge.tsx
│       └── StatusBadge.module.css
└── styles/
    ├── variables.css      # CSS custom properties (design tokens)
    └── global.css         # Global styles and utilities
```

## Design Tokens

### CSS Variables

All design tokens are defined in `src/styles/variables.css` as CSS custom properties:

```css
:root {
  /* Primary Colors */
  --color-primary: #0C4A6E;
  --color-primary-mid: #0369A1;
  --color-primary-light: #E0F2FE;

  /* Semantic Colors */
  --color-green: #059669;
  --color-red: #DC2626;
  --color-amber: #B45309;

  /* Neutral Colors */
  --color-bg: #F0F4F8;
  --color-card: #FFFFFF;
  --color-border: #E2E8F0;
  --color-text: #0F172A;
  --color-muted: #64748B;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

### Usage in CSS

```css
.my-component {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}
```

## Component Styling Patterns

### 1. Avatar Component

**Props:**
- `init`: string - Initials to display
- `color`: string - Custom color (optional)
- `size`: 'sm' | 'md' | 'lg' | 'xl' | number - Size variant or custom pixel value

**Example:**
```tsx
import { Avatar } from './components/ui';

// Using predefined sizes
<Avatar init="JD" color="#3b82f6" size="md" />

// Using custom size
<Avatar init="AB" color="#ff0000" size={60} />
```

### 2. Badge Component

**Props:**
- `text`: string - Badge text
- `color`: string - Custom text color (optional)
- `bg`: string - Custom background color (optional)
- `size`: 'sm' | 'md' | 'lg' - Size variant
- `variant`: 'primary' | 'success' | 'warning' | 'error' - Color variant

**Example:**
```tsx
import { Badge } from './components/ui';

// Using variant
<Badge text="Success" variant="success" size="md" />

// Using custom colors
<Badge text="Custom" color="#ff0000" bg="#ff0000" />
```

### 3. Button Component

**Props:**
- `children`: React.ReactNode - Button content
- `onClick`: () => void - Click handler
- `variant`: 'primary' | 'outline' | 'ghost' | 'success' | 'danger' | 'purple'
- `size`: 'sm' | 'md' | 'lg'
- `full`: boolean - Full width
- `disabled`: boolean
- `type`: 'button' | 'submit' | 'reset'

**Example:**
```tsx
import { Button } from './components/ui';

<Button variant="primary" size="md" onClick={handleClick}>
  Click Me
</Button>

<Button variant="outline" size="sm" disabled>
  Disabled
</Button>
```

### 4. Card Component

**Props:**
- `children`: React.ReactNode
- `size`: 'sm' | 'md' | 'lg'
- `variant`: 'default' | 'interactive' | 'bordered' | 'elevated'
- `onClick`: () => void - For interactive variant
- `style`: React.CSSProperties - Additional inline styles

**Example:**
```tsx
import { Card } from './components/ui';

<Card size="md" variant="elevated">
  <h3>Card Title</h3>
  <p>Card content</p>
</Card>

<Card variant="interactive" onClick={handleClick}>
  Clickable Card
</Card>
```

### 5. StatusBadge Component

**Props:**
- `status`: 'connected' | 'disconnected' | 'pending' | 'success' | 'warning' | 'error' | 'confirmed' | 'completed' | 'cancelled' | 'syncing'
- `showIndicator`: boolean - Show status indicator dot

**Example:**
```tsx
import { StatusBadge } from './components/ui';

<StatusBadge status="connected" />
<StatusBadge status="syncing" showIndicator={true} />
```

## Best Practices

### 1. Component Styling

**DO:**
```tsx
// Use CSS Modules
import styles from './MyComponent.module.css';

<div className={styles.container}>
  <h2 className={styles.title}>Title</h2>
</div>
```

**DON'T:**
```tsx
// Avoid inline styles for static properties
<div style={{ padding: '20px', borderRadius: '8px' }}>
  <h2 style={{ fontSize: '24px' }}>Title</h2>
</div>
```

### 2. Dynamic Styles

**DO:**
```tsx
// Use CSS variables for dynamic values
<div style={{ 
  '--dynamic-color': userColor 
} as React.CSSProperties}>
  Content
</div>
```

**DON'T:**
```tsx
// Avoid complex inline style objects
<div style={{ 
  padding: `${size * 2}px`,
  margin: `${spacing}px ${spacing * 1.5}px`,
  borderRadius: `${radius}px`
}}>
  Content
</div>
```

### 3. Responsive Design

**DO:**
```css
/* In CSS Module */
.container {
  padding: var(--spacing-md);
}

@media (min-width: 768px) {
  .container {
    padding: var(--spacing-lg);
  }
}
```

### 4. Theme Support

The application supports both light and dark themes through CSS variables:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #0F172A;
    --color-card: #1E293B;
    --color-text: #F1F5F9;
  }
}
```

## Testing

### Testing Styled Components

When testing components with CSS Modules:

```tsx
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct variant class', () => {
    render(<Button variant="outline">Click</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('outline');
  });

  it('renders with correct size class', () => {
    render(<Button size="sm">Click</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('sm');
  });
});
```

## Migration Notes

### From Inline Styles to CSS Modules

**Before:**
```tsx
const Button = ({ variant, size }) => {
  const variants = {
    primary: { background: '#0C4A6E', color: '#fff' },
    outline: { background: 'transparent', color: '#0C4A6E' }
  };
  const sizes = {
    sm: { padding: '5px 11px', fontSize: '12px' },
    md: { padding: '8px 16px', fontSize: '13px' }
  };

  return (
    <button style={{ ...variants[variant], ...sizes[size] }}>
      {children}
    </button>
  );
};
```

**After:**
```tsx
import styles from './Button.module.css';

const Button = ({ variant, size }) => {
  return (
    <button className={`${styles.button} ${styles[variant]} ${styles[size]}`}>
      {children}
    </button>
  );
};
```

## Performance Considerations

1. **CSS Modules are processed at build time** - No runtime style calculations
2. **Minimal inline styles** - Only use for dynamic values
3. **CSS variables for theming** - Efficient theme switching
4. **Avoid style thrashing** - Group related style changes

## Accessibility

### Color Contrast

All color combinations meet WCAG AA standards:
- Normal text: 4.5:1 contrast ratio
- Large text: 3:1 contrast ratio
- Interactive elements: 3:1 contrast ratio

### Focus States

All interactive elements have visible focus states:
```css
.button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

## Future Enhancements

1. **Consider CSS-in-JS** for complex theming needs
2. **Add Storybook** for component documentation
3. **Implement design system tokens** in JavaScript for runtime access
4. **Add animation utilities** for consistent motion design
5. **Create responsive grid system** for layouts

## Resources

- [CSS Modules Documentation](https://github.com/css-modules/css-modules)
- [CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)
