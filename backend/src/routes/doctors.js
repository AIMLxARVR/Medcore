/**
 * Doctor Routes
 * Handles doctor profiles, search, and availability
 */

const express = require('express');
const router = express.Router();
const { PrismaClient } = require('@prisma/client');
const { authenticate, requireRole } = require('../middleware/auth');

const prisma = new PrismaClient();

// GET /api/doctors - List all doctors
router.get('/', async (req, res) => {
  try {
    const { specialty, department, search } = req.query;
    
    const where = {};
    
    if (specialty) {
      where.specialty = specialty;
    }
    
    if (department) {
      where.department = department;
    }
    
    if (search) {
      where.OR = [
        { firstName: { contains: search } },
        { lastName: { contains: search } },
        { specialty: { contains: search } },
      ];
    }

    const doctors = await prisma.doctorProfile.findMany({
      where,
      include: {
        user: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
            phone: true,
          },
        },
      },
      orderBy: { createdAt: 'desc' },
    });

    res.json(doctors);
  } catch (error) {
    console.error('List doctors error:', error);
    res.status(500).json({ error: 'Failed to fetch doctors' });
  }
});

// GET /api/doctors/:id - Get doctor by ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    const doctor = await prisma.doctorProfile.findUnique({
      where: { id },
      include: {
        user: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
            phone: true,
          },
        },
        appointments: {
          where: {
            date: { gte: new Date() },
          },
          orderBy: { date: 'asc' },
          take: 10,
        },
      },
    });

    if (!doctor) {
      return res.status(404).json({ error: 'Doctor not found' });
    }

    res.json(doctor);
  } catch (error) {
    console.error('Get doctor error:', error);
    res.status(500).json({ error: 'Failed to fetch doctor' });
  }
});

// PUT /api/doctors/:id - Update doctor profile (doctor only)
router.put('/:id', authenticate, requireRole('DOCTOR'), async (req, res) => {
  try {
    const { id } = req.params;
    const { title, specialty, department, bio, fee, education, experience, slots } = req.body;

    // Verify the user owns this profile
    const doctor = await prisma.doctorProfile.findUnique({ where: { id } });
    
    if (!doctor || doctor.userId !== req.user.id) {
      return res.status(403).json({ error: 'Not authorized' });
    }

    const updated = await prisma.doctorProfile.update({
      where: { id },
      data: {
        title,
        specialty,
        department,
        bio,
        fee,
        education,
        experience,
        slots,
      },
    });

    res.json(updated);
  } catch (error) {
    console.error('Update doctor error:', error);
    res.status(500).json({ error: 'Failed to update doctor' });
  }
});

// GET /api/doctors/:id/availability - Get available slots
router.get('/:id/availability', async (req, res) => {
  try {
    const { id } = req.params;
    const { date } = req.query;

    const doctor = await prisma.doctorProfile.findUnique({
      where: { id },
    });

    if (!doctor) {
      return res.status(404).json({ error: 'Doctor not found' });
    }

    // Get existing appointments for the date
    const targetDate = date ? new Date(date) : new Date();
    targetDate.setHours(0, 0, 0, 0);
    
    const nextDay = new Date(targetDate);
    nextDay.setDate(nextDay.getDate() + 1);

    const appointments = await prisma.appointment.findMany({
      where: {
        doctorId: id,
        date: {
          gte: targetDate,
          lt: nextDay,
        },
        status: { in: ['CONFIRMED', 'PENDING'] },
      },
      select: { time: true },
    });

    const bookedSlots = appointments.map(a => a.time);

    // Get doctor's available slots for that day
    const dayName = targetDate.toLocaleDateString('en-US', { weekday: 'lowercase' });
    const availableSlots = doctor.slots?.[dayName] || [];

    // Filter out booked slots
    const freeSlots = availableSlots.filter(slot => !bookedSlots.includes(slot));

    res.json({
      date: targetDate.toISOString().split('T')[0],
      slots: freeSlots,
    });
  } catch (error) {
    console.error('Get availability error:', error);
    res.status(500).json({ error: 'Failed to fetch availability' });
  }
});

module.exports = router;
