/**
 * Admin Routes
 * Handles admin dashboard statistics, audit logs, and data export
 */

const express = require('express');
const router = express.Router();
const { PrismaClient } = require('@prisma/client');
const { authenticate, requireRole } = require('../middleware/auth');

const prisma = new PrismaClient();

// GET /api/admin/stats - Dashboard statistics (admin only)
router.get('/stats', authenticate, requireRole('ADMIN'), async (req, res) => {
  try {
    // Get appointment stats
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const [
      todayAppointments,
      totalAppointments,
      totalPatients,
      totalDoctors,
      pendingAppointments,
      completedToday
    ] = await Promise.all([
      prisma.appointment.count({
        where: {
          date: {
            gte: today,
            lt: tomorrow
          }
        }
      }),
      prisma.appointment.count(),
      prisma.user.count({ where: { role: 'PATIENT', isActive: true } }),
      prisma.doctorProfile.count({ where: { isActive: true } }),
      prisma.appointment.count({ where: { status: 'PENDING' } }),
      prisma.appointment.count({
        where: {
          date: { gte: today, lt: tomorrow },
          status: 'COMPLETED'
        }
      })
    ]);
    
    // Get weekly appointment data
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    
    const weeklyAppointments = await prisma.appointment.groupBy({
      by: ['date'],
      where: {
        date: { gte: weekAgo }
      },
      _count: { id: true }
    });
    
    // Get ETL sync stats
    const etlLastSync = await prisma.etlSyncLog.findFirst({
      orderBy: { timestamp: 'desc' }
    });
    
    res.json({
      appointments: {
        today: todayAppointments,
        total: totalAppointments,
        pending: pendingAppointments,
        completedToday,
        weekly: weeklyAppointments.map(w => ({
          date: w.date,
          count: w._count.id
        }))
      },
      users: {
        patients: totalPatients,
        doctors: totalDoctors
      },
      etl: {
        lastSync: etlLastSync?.timestamp || null,
        status: etlLastSync?.status || 'never'
      }
    });
  } catch (error) {
    console.error('Get admin stats error:', error);
    res.status(500).json({ error: 'Failed to get statistics' });
  }
});

// GET /api/admin/audit-logs - Get audit logs (admin only)
router.get('/audit-logs', authenticate, requireRole('ADMIN'), async (req, res) => {
  try {
    const { limit = 50, offset = 0, type } = req.query;
    
    const where = {};
    if (type) {
      where.type = type;
    }
    
    const logs = await prisma.auditLog.findMany({
      where,
      orderBy: { timestamp: 'desc' },
      take: parseInt(limit),
      skip: parseInt(offset),
      include: {
        user: {
          select: {
            email: true,
            firstName: true,
            lastName: true
          }
        }
      }
    });
    
    res.json(logs.map(log => ({
      ...log,
      userEmail: log.user?.email || 'System'
    })));
  } catch (error) {
    console.error('Get audit logs error:', error);
    res.status(500).json({ error: 'Failed to get audit logs' });
  }
});

// POST /api/admin/export - Export data (admin only)
router.post('/export', authenticate, requireRole('ADMIN'), async (req, res) => {
  try {
    const { type, format = 'json' } = req.body;
    
    let data = [];
    let filename = '';
    
    switch (type) {
      case 'appointments':
        data = await prisma.appointment.findMany({
          include: {
            patient: {
              select: { firstName: true, lastName: true, email: true }
            },
            doctor: {
              include: {
                user: {
                  select: { firstName: true, lastName: true }
                }
              }
            }
          }
        });
        filename = 'appointments';
        break;
        
      case 'patients':
        data = await prisma.user.findMany({
          where: { role: 'PATIENT' },
          select: {
            id: true,
            email: true,
            firstName: true,
            lastName: true,
            phone: true,
            createdAt: true
          }
        });
        filename = 'patients';
        break;
        
      case 'doctors':
        data = await prisma.doctorProfile.findMany({
          include: {
            user: {
              select: { firstName: true, lastName: true, email: true }
            },
            specialization: true
          }
        });
        filename = 'doctors';
        break;
        
      default:
        return res.status(400).json({ error: 'Invalid export type' });
    }
    
    // Format the output
    if (format === 'csv') {
      if (data.length === 0) {
        return res.status(404).json({ error: 'No data to export' });
      }
      
      const headers = Object.keys(data[0]);
      const csv = [
        headers.join(','),
        ...data.map(row => 
          headers.map(h => JSON.stringify(row[h] || '')).join(',')
      );
      
      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', `attachment; filename=${filename}.csv`);
      return res.send(csv.join('\n'));
    }
    
    // Default to JSON
    res.json({
      exportedAt: new Date(),
      type,
      count: data.length,
      data
    });
  } catch (error) {
    console.error('Export error:', error);
    res.status(500).json({ error: 'Failed to export data' });
  }
});

// GET /api/admin/users - Manage users (admin only)
router.get('/users', authenticate, requireRole('ADMIN'), async (req, res) => {
  try {
    const { role, isActive, limit = 50, offset = 0 } = req.query;
    
    const where = {};
    if (role) where.role = role;
    if (isActive !== undefined) where.isActive = isActive === 'true';
    
    const users = await prisma.user.findMany({
      where,
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        phone: true,
        role: true,
        isActive: true,
        createdAt: true
      },
      orderBy: { createdAt: 'desc' },
      take: parseInt(limit),
      skip: parseInt(offset)
    });
    
    res.json(users);
  } catch (error) {
    console.error('Get users error:', error);
    res.status(500).json({ error: 'Failed to get users' });
  }
});

// PATCH /api/admin/users/:id - Update user status (admin only)
router.patch('/users/:id', authenticate, requireRole('ADMIN'), async (req, res) => {
  try {
    const { id } = req.params;
    const { isActive } = req.body;
    
    // Prevent self-deactivation
    if (id === req.user.id) {
      return res.status(403).json({ error: 'Cannot modify your own account' });
    }
    
    const user = await prisma.user.update({
      where: { id },
      data: { isActive },
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        isActive: true
      }
    });
    
    // Log the action
    await prisma.auditLog.create({
      data: {
        userId: req.user.id,
        action: isActive ? 'USER_ACTIVATED' : 'USER_DEACTIVATED',
        targetId: id,
        timestamp: new Date()
      }
    });
    
    res.json(user);
  } catch (error) {
    console.error('Update user error:', error);
    res.status(500).json({ error: 'Failed to update user' });
  }
});

module.exports = router;
