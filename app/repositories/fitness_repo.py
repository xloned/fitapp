from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.fitness import FitnessWorkout, WorkoutSet
import datetime


async def get_day_workout(session: AsyncSession, user_id: int, date: datetime.date):
    result = await session.execute(
        select(FitnessWorkout)
        .where(FitnessWorkout.user_id == user_id)
        .where(FitnessWorkout.date == date)
    )
    return result.scalars().all()

async def delete_workout(session: AsyncSession, entry_id: int):
    await session.execute(
        delete(FitnessWorkout)
        .where(FitnessWorkout.id == entry_id)
    )
    await session.commit()

async def create_workout(session: AsyncSession, user_id: int, date: datetime.date, title: str):
    obj = FitnessWorkout(
        user_id=user_id,
        date=date,
        title=title,
    )
    session.add(obj)
    await session.commit()
    return obj

async def create_set(session, workout_id, exercise, reps, sets_count, weight, done=False):
    obj = WorkoutSet(
        workout_id=workout_id,
        exercise=exercise,
        reps=reps,
        sets_count=sets_count,
        weight=weight,
        done = done,
    )
    session.add(obj)
    await session.commit()
    return obj

async def get_workout_sets(session, workout_id):
    result = await session.execute(
        select(WorkoutSet)
        .where(WorkoutSet.workout_id == workout_id)
    )
    return result.scalars().all()

async def delete_set(session, set_id):
    await session.execute(
        delete(WorkoutSet)
        .where(WorkoutSet.id == set_id)
    )
    await session.commit()