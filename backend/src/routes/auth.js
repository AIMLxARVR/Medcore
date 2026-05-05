/**
 * Auth Routes
 * Handles authentication: register, login, refresh token
 */

const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const { PrismaClient } = require('@prisma/client');
const { authenticate } = require('../middleware/auth');

const prisma = new PrismaClient();

// POST /api/auth/register
router.post('/register', async (req, res) => {
  try {
    const { email, password, firstName, lastName, phone, role } = req.body;

    // Check if user exists
    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      return res.status(409).json({ error: 'Email already registered' });
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, 10);

    // Create user
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        firstName,
        lastName,
        phone,
        role: role || 'PATIENT',
      },
    });

    // Generate tokens
    const tokens = generateTokens(user);

    res.status(201).json(tokens);
  } catch (error) {
    console.error('Register error:', error);
    res.status(500).json({ error: 'Registration failed' });
  }
});

// POST /api/auth/login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find user
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Verify password
    const isValid = await bcrypt.compare(password, user.passwordHash);
    if (!isValid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    if (!user.isActive) {
      return res.status(401).json({ error: 'Account is deactivated' });
    }

    // Generate tokens
    const tokens = generateTokens(user);

    res.json(tokens);
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Login failed' });
  }
});

// POST /api/auth/refresh
router.post('/refresh', async (req, res) => {
  try {
    const { refreshToken } = req.body;
    
    const payload = jwt.verify(
      refreshToken, 
      process.env.JWT_SECRET || 'medcore_secret_key'
    );

    const user = await prisma.user.findUnique({ where: { id: payload.sub } });
    if (!user || !user.isActive) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    const tokens = generateTokens(user);
    res.json(tokens);
  } catch (error) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});

// Helper: Generate JWT tokens
function generateTokens(user) {
  const payload = {
    sub: user.id,
    email: user.email,
    role: user.role,
  };

  const secret = process.env.JWT_SECRET || 'medcore_secret_key';
  const accessToken = jwt.sign(payload, secret, { 
    expiresIn: process.env.JWT_EXPIRES_IN || '15m' 
  });
  const refreshToken = jwt.sign(payload, secret, { 
    expiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d' 
  });

  return {
    accessToken,
    refreshToken,
    user: {
      id: user.id,
      email: user.email,
      firstName: user.firstName,
      lastName: user.lastName,
      role: user.role,
    },
  };
}

// POST /api/auth/logout
// In production, you'd blacklist the token. For now, we just acknowledge the request.
// The client should discard the token from local storage.
router.post('/logout', authenticate, async (req, res) => {
  try {
    // Log the logout action for audit purposes
    console.log(`User ${req.user.email} logged out`);
    
    // In a production system, you would:
    // 1. Add the access token to a blacklist in Redis
    // 2. Remove the refresh token from the database
    // For MVP, we just acknowledge successful logout
    
    res.json({ message: 'Logged out successfully' });
  } catch (error) {
    console.error('Logout error:', error);
    res.status(500).json({ error: 'Logout failed' });
  }
});

// GET /api/auth/me - Get current user profile
router.get('/me', authenticate, async (req, res) => {
  try {
    const user = await prisma.user.findUnique({
      where: { id: req.user.id },
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        phone: true,
        role: true,
        bloodGroup: true,
        dateOfBirth: true,
        createdAt: true,
      },
    });
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    // Get additional profile data based on role
    let profile = null;
    if (user.role === 'DOCTOR') {
      profile = await prisma.doctorProfile.findUnique({
        where: { userId: user.id },
      });
    } else if (user.role === 'PATIENT') {
      profile = await prisma.patientProfile.findUnique({
        where: { userId: user.id },
      });
    }
    
res.json({ ...user, profile });
  } catch (error) {
    console.error('Get profile error:', error);
    res.status(500).json({ error: 'Failed to get profile' });
  }
});

// PATCH /api/auth/me - Update current user profile
router.patch('/me', authenticate, async (req, res) => {
  try {
    const { firstName, lastName, phone, bloodGroup, dateOfBirth } = req.body;
    
    // Build update data - only allow specific fields to be updated
    const updateData = {};
    if (firstName !== undefined) updateData.firstName = firstName;
    if (lastName !== undefined) updateData.lastName = lastName;
    if (phone !== undefined) updateData.phone = phone;
    if (bloodGroup !== undefined) updateData.bloodGroup = bloodGroup;
    if (dateOfBirth !== undefined) updateData.dateOfBirth = new Date(dateOfBirth);
    
    const user = await prisma.user.update({
      where: { id: req.user.id },
      data: updateData,
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        phone: true,
        role: true,
        bloodGroup: true,
        dateOfBirth: true,
        updatedAt: true,
      },
    });
    
    res.json(user);
  } catch (error) {
    console.error('Update profile error:', error);
    res.status(500).json({ error: 'Failed to update profile' });
  }
});

module.exports = router;
