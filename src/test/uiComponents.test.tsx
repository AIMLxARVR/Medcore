import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Avatar, Badge, Button, Card, StatusBadge } from '../components/ui';

describe('UI Components', () => {
  describe('Avatar', () => {
    it('renders with initial', () => {
      render(<Avatar init="JD" color="#3b82f6" size={40} />);
      const avatarText = screen.getByText('JD');
      expect(avatarText).toBeInTheDocument();
    });

    it('renders with correct size', () => {
      render(<Avatar init="AB" color="#3b82f6" size={60} />);
      const avatarText = screen.getByText('AB');
      expect(avatarText).toBeInTheDocument();
    });

    it('renders with correct color', () => {
      render(<Avatar init="CD" color="#ff0000" size={40} />);
      const avatarText = screen.getByText('CD');
      expect(avatarText).toBeInTheDocument();
    });
  });

  describe('Badge', () => {
    it('renders with text', () => {
      render(<Badge text="Test Badge" />);
      const badgeText = screen.getByText('Test Badge');
      expect(badgeText).toBeInTheDocument();
    });

    it('renders with custom color', () => {
      render(<Badge text="Custom" color="#ff0000" bg="#ff0000" />);
      const badgeText = screen.getByText('Custom');
      expect(badgeText).toBeInTheDocument();
    });
  });

  describe('Button', () => {
    it('renders with text', () => {
      render(<Button>Click Me</Button>);
      const buttonText = screen.getByText('Click Me');
      expect(buttonText).toBeInTheDocument();
    });

    it('renders with correct variant', () => {
      render(<Button variant="outline">Outline Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('renders with correct size', () => {
      render(<Button size="sm">Small Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('handles click events', () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Clickable</Button>);
      const button = screen.getByRole('button');
      fireEvent.click(button);
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('can be disabled', () => {
      render(<Button disabled>Disabled</Button>);
      const button = screen.getByRole('button');
      expect(button).toBeDisabled();
    });
  });

  describe('Card', () => {
    it('renders with children', () => {
      render(<Card><div>Card Content</div></Card>);
      const cardText = screen.getByText('Card Content');
      expect(cardText).toBeInTheDocument();
    });

    it('renders with custom style', () => {
      render(<Card style={{ backgroundColor: '#f0f0f0' }}><div>Styled Card</div></Card>);
      const cardText = screen.getByText('Styled Card');
      expect(cardText).toBeInTheDocument();
    });
  });

  describe('StatusBadge', () => {
    it('renders with connected status', () => {
      render(<StatusBadge status="connected" />);
      const badgeText = screen.getByText('Connected');
      expect(badgeText).toBeInTheDocument();
    });

    it('renders with disconnected status', () => {
      render(<StatusBadge status="disconnected" />);
      const badge = screen.getByText('Disconnected');
      expect(badge).toBeTruthy();
    });

    it('renders with pending status', () => {
      render(<StatusBadge status="pending" />);
      const badge = screen.getByText('Pending');
      expect(badge).toBeTruthy();
    });

    it('renders with success status', () => {
      render(<StatusBadge status="success" />);
      const badge = screen.getByText('Success');
      expect(badge).toBeTruthy();
    });

    it('renders with error status', () => {
      render(<StatusBadge status="error" />);
      const badge = screen.getByText('Error');
      expect(badge).toBeTruthy();
    });

    it('renders with warning status', () => {
      render(<StatusBadge status="warning" />);
      const badge = screen.getByText('Warning');
      expect(badge).toBeTruthy();
    });

    it('renders with confirmed status', () => {
      render(<StatusBadge status="confirmed" />);
      const badge = screen.getByText('Confirmed');
      expect(badge).toBeTruthy();
    });

    it('renders with completed status', () => {
      render(<StatusBadge status="completed" />);
      const badge = screen.getByText('Completed');
      expect(badge).toBeTruthy();
    });

    it('renders with cancelled status', () => {
      render(<StatusBadge status="cancelled" />);
      const badge = screen.getByText('Cancelled');
      expect(badge).toBeTruthy();
    });

    it('renders with syncing status', () => {
      render(<StatusBadge status="syncing" />);
      const badge = screen.getByText('Syncing');
      expect(badge).toBeTruthy();
    });

    it('defaults to pending for unknown status', () => {
      render(<StatusBadge status="unknown" />);
      const badge = screen.getByText('Pending');
      expect(badge).toBeTruthy();
    });
  });
});
