import { Injectable } from '@nestjs/common';
import { v4 as uuidv4 } from 'uuid';
import { CalibrationType, CreateCalibrationInputType } from './types';
import * as dayjs from 'dayjs';

@Injectable()
export class CalibrationService {
  private calibrationList: CalibrationType[] = [
    {
      id: '1',
      title: '연습용 캘리브레이션',
      baseDate: '2023-12-31',
      createdAt: '2023-12-24 10:52',
    },
    {
      id: '2',
      title: '실전용 캘리브레이션',
      baseDate: '2023-09-30',
      createdAt: '2023-12-25 17:23',
    },
  ];
  getCalibration(calibrationId: string): CalibrationType {
    return this.calibrationList.filter(({ id }) => id === calibrationId)[0];
  }

  getCalibrationList(): CalibrationType[] {
    return this.calibrationList;
  }

  createCalibration({
    title,
    baseDate,
  }: CreateCalibrationInputType): CalibrationType {
    const id = uuidv4();
    const createdAt = dayjs().format('YYYY-MM-DD HH:mm');
    const calibration = {
      id,
      title,
      baseDate,
      createdAt,
    };
    this.calibrationList.push(calibration);
    return calibration;
  }
}
