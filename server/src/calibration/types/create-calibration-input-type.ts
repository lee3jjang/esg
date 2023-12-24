import { Field, InputType } from '@nestjs/graphql';

@InputType()
export class CreateCalibrationInputType {
  @Field()
  title: string;

  @Field()
  baseDate: string;
}
