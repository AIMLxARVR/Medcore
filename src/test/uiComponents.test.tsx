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
      const avatar = avatarText.parentElement;
      expect(avatar).toBeInTheDocument();
      // For custom numeric size, check inline styles
      expect(avatar).toHaveStyle({ 
        width: '60px', 
        height: '60px',
        fontSize: '18px'
      });
    });

    it('renders with correct color', () => {
      render(<Avatar init="CD" color="#ff0000" size={40} />);
      const avatarText = screen.getByText('CD');
      const avatar = avatarText.parentElement;
      expect(avatar).toBeInTheDocument();
      // Check that custom color is applied via inline styles
      expect(avatar).toHaveStyle({ 
        backgroundColor: expect.stringContaining('#ff000022'),
        borderColor: expect.stringContaining('#ff000044'),
        color: '#ff0000'
      });
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
      // Check that custom colors are applied via inline styles
      expect(badgeText).toHaveStyle({ 
        color: '#ff0000', 
        backgroundColor: '#ff0000' 
      });
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
      // Check variant via computed styles since CSS Modules uses hashed class names
      expect(button).toHaveStyle({
        backgroundColor: 'transparent',
        borderColor: 'var(--color-primary)',
        color: 'var(--color-primary)'
      });
    });

    it('renders with correct size', () => {
      render(<Button size="sm">Small Button</Button>);
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
      // Check size via computed styles
      expect(button).toHaveStyle({
        padding: '5px 11px',
        fontSize: '12px'
      });
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
      const card = cardText.parentElement;
      expect(card).toHaveStyle({ backgroundColor: '#f0f0f0' });
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
      const badgeElement = screen.getByText('Disconnected').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('renders with pending status', () => {
      render(<StatusBadge status="pending" />);
      const badgeElement = screen.getByText('Pending').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('renders with success status', () => {
      render(<StatusBadge status="success" />);
      const badgeElement = screen.getByText('Success').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('renders with error status', () => {
      render(<StatusBadge status="error" />);
      const badgeElement = screen.getByText('Error').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('renders with warning status', () => {
      render(<StatusBadge status="warning" />);
      const badgeElement = screen.getByText('Warning').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('renders with confirmed status', () => {
      render(<StatusBadge status="confirmed" />);
      const badgeElement = screen.getByText('Confirmed').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('renders with completed status', () => {
      render(<StatusBadge status="completed" />);
      const badgeElement = screen.getByText('Completed').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('renders with cancelled status', () => {
      render(<StatusBadge status="cancelled" />);
      const badgeElement = screen.getByText('Cancelled').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('renders with syncing status', () => {
      render(<StatusBadge status="syncing" />);
      const badgeElement = screen.getByText('Syncing').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });

    it('defaults to pending for unknown status', () => {
      render(<StatusBadge status="unknown" />);
      const badgeElement = screen.getByText('Pending').parentElement;
      expect(badgeElement).toBeInTheDocument();
    });
  });
});