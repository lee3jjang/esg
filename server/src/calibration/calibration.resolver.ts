import { Args, ID, Mutation, Query, Resolver } from '@nestjs/graphql';
import { CalibrationService } from './calibration.service';
import { CalibrationType, CreateCalibrationInputType } from './types';

@Resolver()
export class CalibrationResolver {
  constructor(private readonly calibrationService: CalibrationService) {}

  @Query(() => CalibrationType, { name: 'calibration' })
  getCaliration(
    @Args('calibrationId', { type: () => ID }) calibrationId: string,
  ): CalibrationType {
    return this.calibrationService.getCalibration(calibrationId);
  }

  @Query(() => [CalibrationType], { name: 'calibrationList' })
  getCalibrationList(): CalibrationType[] {
    return this.calibrationService.getCalibrationList();
  }

  @Mutation(() => CalibrationType, { name: 'createCalibration' })
  createCalibration(
    @Args('createCalibrationInput')
    createCalibrationInput: CreateCalibrationInputType,
  ): CalibrationType {
    return this.calibrationService.createCalibration(createCalibrationInput);
  }
}
