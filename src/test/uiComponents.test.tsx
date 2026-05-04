import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Avatar } from '../components/ui/Avatar';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { StatusBadge } from '../components/ui/StatusBadge';

describe('UI Components', () => {
  describe('Avatar', () => {
    it('renders with initials', () => {
      render(<Avatar init="JD" color="#3b82f6" />);
      expect(screen.getByText('JD')).toBeInTheDocument();
    });

    it('renders with custom size', () => {
      render(<Avatar init="AB" color="#3b82f6" size={60} />);
      const avatar = screen.getByText('AB');
      expect(avatar.parentElement).toHaveStyle({ width: '60px', height: '60px' });
    });

    it('renders with custom color', () => {
      render(<Avatar init="XY" color="#ff0000" />);
      const avatar = screen.getByText('XY');
      expect(avatar.parentElement).toHaveStyle({ backgroundColor: '#ff0000' });
    });
  });

  describe('Badge', () => {
    it('renders children content', () => {
      render(<Badge>Test Badge</Badge>);
      expect(screen.getByText('Test Badge')).toBeInTheDocument();
    });

    it('renders with custom styles', () => {
      render(<Badge style={{ backgroundColor: 'red' }}>Styled Badge</Badge>);
      const badge = screen.getByText('Styled Badge');
      expect(badge).toHaveStyle({ backgroundColor: 'red' });
    });
  });

  describe('Button', () => {
    it('renders with text', () => {
      render(<Button>Click Me</Button>);
      expect(screen.getByText('Click Me')).toBeInTheDocument();
    });

    it('handles click events', () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Click Me</Button>);
      
      screen.getByText('Click Me').click();
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('renders with different sizes', () => {
      render(<Button size="sm">Small Button</Button>);
      const button = screen.getByText('Small Button');
      expect(button).toHaveClass('button-sm');
    });

    it('renders with different variants', () => {
      render(<Button variant="outline">Outline Button</Button>);
      const button = screen.getByText('Outline Button');
      expect(button).toHaveClass('button-outline');
    });

    it('disables button when disabled prop is true', () => {
      render(<Button disabled>Disabled Button</Button>);
      const button = screen.getByText('Disabled Button');
      expect(button).toBeDisabled();
    });
  });

  describe('Card', () => {
    it('renders children content', () => {
      render(<Card>Card Content</Card>);
      expect(screen.getByText('Card Content')).toBeInTheDocument();
    });

    it('renders with custom styles', () => {
      render(<Card style={{ padding: '20px' }}>Styled Card</Card>);
      const card = screen.getByText('Styled Card');
      expect(card.parentElement).toHaveStyle({ padding: '20px' });
    });
  });

  describe('StatusBadge', () => {
    it('renders online status correctly', () => {
      render(<StatusBadge status="online" />);
      const badge = screen.getByText('●');
      expect(badge).toHaveStyle({ color: '#10b981' });
    });

    it('renders offline status correctly', () => {
      render(<StatusBadge status="offline" />);
      const badge = screen.getByText('●');
      expect(badge).toHaveStyle({ color: '#6b7280' });
    });

    it('renders busy status correctly', () => {
      render(<StatusBadge status="busy" />);
      const badge = screen.getByText('●');
      expect(badge).toHaveStyle({ color: '#f59e0b' });
    });

    it('renders away status correctly', () => {
      render(<StatusBadge status="away" />);
      const badge = screen.getByText('●');
      expect(badge).toHaveStyle({ color: '#3b82f6' });
    });

    it('renders with custom size', () => {
      render(<StatusBadge status="online" size={16} />);
      const badge = screen.getByText('●');
      expect(badge).toHaveStyle({ fontSize: '16px' });
    });
  });
});