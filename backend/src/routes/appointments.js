/**
 * Appointment Routes
 * Handles appointment booking, management, and status
 */

const express = require('express');
const router = express.Router();
const { PrismaClient } = require('@prisma/client');
const { authenticate, requireRole } = require('../middleware/auth');

const prisma = new PrismaClient();

// GET /api/appointments - List user's appointments
router.get('/', authenticate, async (req, res) => {
  try {
    const { status, from, to } = req.query;
    
    const where = {
      OR: [
        { patientId: req.user.id },
        { doctor: { userId: req.user.id } },
      ],
    };
    
    if (status) {
      where.status = status;
    }
    
    if (from || to) {
      where.date = {};
      if (from) where.date.gte = new Date(from);
      if (to) where.date.lte = new Date(to);
    }

    const appointments = await prisma.appointment.findMany({
      where,
      include: {
        patient: {
          include: {
            user: {
              select: { firstName: true, lastName: true, email: true, phone: true },
            },
          },
        },
        doctor: {
          include: {
            user: {
              select: { firstName: true, lastName: true },
            },
          },
        },
      },
      orderBy: { date: 'desc' },
    });

    res.json(appointments);
  } catch (error) {
    console.error('List appointments error:', error);
    res.status(500).json({ error: 'Failed to fetch appointments' });
  }
});

// GET /api/appointments/:id - Get appointment by ID
router.get('/:id', authenticate, async (req, res) => {
  try {
    const { id } = req.params;
    
    const appointment = await prisma.appointment.findUnique({
      where: { id },
      include: {
        patient: {
          include: {
            user: {
              select: { firstName: true, lastName: true, email: true, phone: true },
            },
          },
        },
        doctor: {
          include: {
            user: {
              select: { firstName: true, lastName: true, email: true, phone: true },
            },
          },
        },
        payment: true,
      },
    });

    if (!appointment) {
      return res.status(404).json({ error: 'Appointment not found' });
    }

    // Check authorization
    const isOwner = appointment.patientId === req.user.id ||
      appointment.doctor?.userId === req.user.id ||
      req.user.role === 'ADMIN';

    if (!isOwner) {
      return res.status(403).json({ error: 'Not authorized' });
    }

    res.json(appointment);
  } catch (error) {
    console.error('Get appointment error:', error);
    res.status(500).json({ error: 'Failed to fetch appointment' });
  }
});

// POST /api/appointments - Create new appointment
router.post('/', authenticate, async (req, res) => {
  try {
    const { doctorId, date, time, notes } = req.body;

    // Verify doctor exists
    const doctor = await prisma.doctorProfile.findUnique({
      where: { id: doctorId },
    });

    if (!doctor) {
      return res.status(404).json({ error: 'Doctor not found' });
    }

    // Check slot availability
    const existing = await prisma.appointment.findFirst({
      where: {
        doctorId,
        date: new Date(date),
        time,
        status: { in: ['CONFIRMED', 'PENDING'] },
      },
    });

    if (existing) {
      return res.status(409).json({ error: 'Slot already booked' });
    }

    // Get patient profile
    const patient = await prisma.patientProfile.findUnique({
      where: { userId: req.user.id },
    });

    if (!patient) {
      return res.status(400).json({ error: 'Patient profile not found' });
    }

    // Create appointment
    const appointment = await prisma.appointment.create({
      data: {
        patientId: patient.id,
        doctorId,
        date: new Date(date),
        time,
        notes,
        status: 'PENDING',
        serial: await getNextSerial(doctorId, date),
      },
      include: {
        doctor: {
          include: { user: { select: { firstName: true, lastName: true } } },
        },
      },
    });

    res.status(201).json(appointment);
  } catch (error) {
    console.error('Create appointment error:', error);
    res.status(500).json({ error: 'Failed to create appointment' });
  }
});

// PATCH /api/appointments/:id - Update appointment status
router.patch('/:id', authenticate, async (req, res) => {
  try {
    const { id } = req.params;
    const { status, notes } = req.body;

    const appointment = await prisma.appointment.findUnique({
      where: { id },
    });

    if (!appointment) {
      return res.status(404).json({ error: 'Appointment not found' });
    }

    // Check authorization
    const isOwner = appointment.patientId === req.user.id ||
      appointment.doctor?.userId === req.user.id ||
      req.user.role === 'ADMIN';
    
    const canCancel = status === 'CANCELLED' && (isOwner || req.user.role === 'ADMIN');
    const canComplete = status === 'COMPLETED' && (appointment.doctor?.userId === req.user.id || req.user.role === 'ADMIN');

    if (!canCancel && !canComplete) {
      return res.status(403).json({ error: 'Not authorized' });
    }

    // Check cancellation fee applies (< 24 hours)
    if (status === 'CANCELLED') {
      const hoursUntil = (new Date(appointment.date) - new Date()) / (1000 * 60 * 60);
      if (hoursUntil < 24) {
        // Would apply cancellation fee in production
        console.log('Cancellation fee applies');
      }
    }

    const updated = await prisma.appointment.update({
      where: { id },
      data: { status, notes },
    });

    res.json(updated);
  } catch (error) {
    console.error('Update appointment error:', error);
    res.status(500).json({ error: 'Failed to update appointment' });
  }
});

// Helper: Get next serial number
async function getNextSerial(doctorId, date) {
  const day = new Date(date);
  day.setHours(0, 0, 0, 0);
  const nextDay = new Date(day);
  nextDay.setDate(nextDay.getDate() + 1);

  const last = await prisma.appointment.findFirst({
    where: {
      doctorId,
      date: { gte: day, lt: nextDay },
    },
    orderBy: { serial: 'desc' },
  });

  return (last?.serial || 0) + 1;
}

module.exports = router;
