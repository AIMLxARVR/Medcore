/**
 * Reviews Routes
 * Handles doctor reviews and ratings
 */

const express = require('express');
const router = express.Router();
const { PrismaClient } = require('@prisma/client');
const { authenticate } = require('../middleware/auth');

const prisma = new PrismaClient();

// POST /api/reviews - Create a new review
router.post('/', authenticate, async (req, res) => {
  try {
    const { appointmentId, doctorId, rating, comment } = req.body;
    
    if (!appointmentId || !doctorId || !rating) {
      return res.status(400).json({ error: 'Appointment ID, doctor ID, and rating are required' });
    }
    
    // Verify the appointment belongs to this user and is completed
    const appointment = await prisma.appointment.findFirst({
      where: {
        id: appointmentId,
        patientId: req.user.id,
        status: 'COMPLETED'
      }
    });
    
    if (!appointment) {
      return res.status(403).json({ error: 'Cannot review this appointment' });
    }
    
    // Check if already reviewed
    const existing = await prisma.review.findUnique({
      where: { appointmentId }
    });
    
    if (existing) {
      return res.status(409).json({ error: 'Appointment already reviewed' });
    }
    
    // Create the review
    const review = await prisma.review.create({
      data: {
        appointmentId,
        doctorId,
        patientId: req.user.id,
        rating: Math.min(5, Math.max(1, rating)), // Clamp between 1-5
        comment: comment || '',
        isVerified: true,
        createdAt: new Date()
      }
    });
    
    // Update doctor's average rating
    const stats = await prisma.review.aggregate({
      where: { doctorId },
      _avg: { rating: true },
      _count: { id: true }
    });
    
    await prisma.doctorProfile.update({
      where: { id: doctorId },
      data: {
        rating: stats._avg.rating || rating,
        totalReviews: stats._count.id
      }
    });
    
    res.status(201).json(review);
  } catch (error) {
    console.error('Create review error:', error);
    res.status(500).json({ error: 'Failed to create review' });
  }
});

// GET /api/reviews/doctor/:id - Get reviews for a doctor
router.get('/doctor/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { limit = 10, offset = 0 } = req.query;
    
    const reviews = await prisma.review.findMany({
      where: { doctorId: id },
      include: {
        patient: {
          select: {
            firstName: true,
            lastName: true
          }
        }
      },
      orderBy: { createdAt: 'desc' },
      take: parseInt(limit),
      skip: parseInt(offset)
    });
    
    // Get average rating
    const stats = await prisma.review.aggregate({
      where: { doctorId: id },
      _avg: { rating: true },
      _count: { id: true }
    });
    
    res.json({
      reviews: reviews.map(r => ({
        ...r,
        patientName: r.patient ? `${r.patient.firstName} ${r.patient.lastName}` : 'Anonymous'
      })),
      averageRating: stats._avg.rating || 0,
      totalReviews: stats._count.id
    });
  } catch (error) {
    console.error('Get doctor reviews error:', error);
    res.status(500).json({ error: 'Failed to get reviews' });
  }
});

// GET /api/reviews/:id - Get a specific review
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const review = await prisma.review.findUnique({
      where: { id },
      include: {
        patient: {
          select: {
            firstName: true,
            lastName: true
          }
        },
        doctor: {
          include: {
            user: {
              select: {
                firstName: true,
                lastName: true
              }
            }
          }
        }
      }
    });
    
    if (!review) {
      return res.status(404).json({ error: 'Review not found' });
    }
    
    res.json(review);
  } catch (error) {
    console.error('Get review error:', error);
    res.status(500).json({ error: 'Failed to get review' });
  }
});

module.exports = router;
