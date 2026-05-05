import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Avatar from '../components/ui/Avatar';
import Badge from '../components/ui/Badge';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import StatusBadge from '../components/ui/StatusBadge';

describe('UI Components', () => {
  describe('Avatar', () => {
    it('renders with initial', () => {
      render(<Avatar init="JD" color="#3b82f6" size={40} />);
      expect(screen.getByText('JD')).toBeInTheDocument();
    });

    it('renders with correct size', () => {
      render(<Avatar init="AB" color="#3b82f6" size={60} />);
      const avatar = screen.getByText('AB').parentElement;
      expect(avatar).toHaveStyle({ width: '60px', height: '60px' });
    });

    it('renders with correct color', () => {
      render(<Avatar init="CD" color="#ff0000" size={40} />);
      const avatar = screen.getByText('CD').parentElement;
      expect(avatar).toHaveStyle({ backgroundColor: '#ff0000' });
    });
  });

  describe('Badge', () => {
    it('renders with text', () => {
      render(<Badge text="Test Badge" />);
      expect(screen.getByText('Test Badge')).toBeInTheDocument();
    });

    it('renders with custom color', () => {
      render(<Badge text="Custom" color="#ff0000" bg="#ff0000" />);
      const badge = screen.getByText('Custom');
      expect(badge).toHaveStyle({ backgroundColor: '#ff0000' });
    });
  });

  describe('Button', () => {
    it('renders with text', () => {
      render(<Button>Click Me</Button>);
      expect(screen.getByText('Click Me')).toBeInTheDocument();
    });

    it('renders with correct variant', () => {
      render(<Button variant="outline">Outline Button</Button>);
      const button = screen.getByText('Outline Button');
      expect(button).toHaveStyle({ backgroundColor: 'transparent' });
    });

    it('renders with correct size', () => {
      render(<Button size="sm">Small Button</Button>);
      const button = screen.getByText('Small Button');
      expect(button).toHaveStyle({ fontSize: '12px', padding: '5px 11px' });
    });

    it('handles click events', () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Clickable</Button>);
      fireEvent.click(screen.getByText('Clickable'));
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('can be disabled', () => {
      render(<Button disabled>Disabled</Button>);
      const button = screen.getByText('Disabled');
      expect(button).toBeDisabled();
    });
  });

  describe('Card', () => {
    it('renders with children', () => {
      render(<Card><div>Card Content</div></Card>);
      expect(screen.getByText('Card Content')).toBeInTheDocument();
    });

    it('renders with custom style', () => {
      render(<Card style={{ backgroundColor: '#f0f0f0' }}><div>Styled Card</div></Card>);
      const card = screen.getByText('Styled Card').closest('div');
      expect(card).toHaveStyle({ backgroundColor: '#f0f0f0' });
    });
  });

  describe('StatusBadge', () => {
    it('renders with connected status', () => {
      render(<StatusBadge status="connected" />);
      expect(screen.getByText('Connected')).toBeInTheDocument();
    });

    it('renders with disconnected status', () => {
      render(<StatusBadge status="disconnected" />);
      expect(screen.getByText('Disconnected')).toBeInTheDocument();
    });

    it('renders with pending status', () => {
      render(<StatusBadge status="pending" />);
      expect(screen.getByText('Pending')).toBeInTheDocument();
    });

    it('renders with success status', () => {
      render(<StatusBadge status="success" />);
      expect(screen.getByText('Success')).toBeInTheDocument();
    });

    it('renders with error status', () => {
      render(<StatusBadge status="error" />);
      expect(screen.getByText('Error')).toBeInTheDocument();
    });

    it('renders with warning status', () => {
      render(<StatusBadge status="warning" />);
      expect(screen.getByText('Warning')).toBeInTheDocument();
    });

    it('renders with confirmed status', () => {
      render(<StatusBadge status="confirmed" />);
      expect(screen.getByText('Confirmed')).toBeInTheDocument();
    });

    it('renders with completed status', () => {
      render(<StatusBadge status="completed" />);
      expect(screen.getByText('Completed')).toBeInTheDocument();
    });

    it('renders with cancelled status', () => {
      render(<StatusBadge status="cancelled" />);
      expect(screen.getByText('Cancelled')).toBeInTheDocument();
    });

    it('renders with syncing status', () => {
      render(<StatusBadge status="syncing" />);
      expect(screen.getByText('Syncing')).toBeInTheDocument();
    });

    it('defaults to pending for unknown status', () => {
      render(<StatusBadge status="unknown" />);
      expect(screen.getByText('Pending')).toBeInTheDocument();
    });
  });
});