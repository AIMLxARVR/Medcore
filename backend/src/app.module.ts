import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';
import { DoctorsModule } from './doctors/doctors.module';
import { AppointmentsModule } from './appointments/appointments.module';
import { PaymentsModule } from './payments/payments.module';
import { ReviewsModule } from './reviews/reviews.module';
import { PrismaModule } from './common/prisma.module';

@Module({
  imports: [
    // Load .env file
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),
    
    // Prisma module for database
    PrismaModule,
    
    // Feature modules
    AuthModule,
    UsersModule,
    DoctorsModule,
    AppointmentsModule,
    PaymentsModule,
    ReviewsModule,
  ],
})
export class AppModule {}
