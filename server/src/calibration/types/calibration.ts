import { Field, ObjectType } from '@nestjs/graphql';

@ObjectType()
export class CalibrationType {
  @Field(() => String)
  id: string;

  @Field()
  title: string;

  @Field()
  baseDate: string;

  @Field()
  createdAt: string;
}
