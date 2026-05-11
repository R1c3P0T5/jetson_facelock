from uuid import UUID

from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import FaceVectorLimitExceededError, FaceVectorNotFoundError
from src.faces.models import FaceVector


MAX_FACE_VECTORS_PER_USER = 100


async def list_face_vectors(
    user_id: UUID,
    session: AsyncSession,
    skip: int = 0,
    limit: int = MAX_FACE_VECTORS_PER_USER,
) -> tuple[int, list[FaceVector]]:
    total = (
        await session.exec(
            select(func.count())
            .select_from(FaceVector)
            .where(FaceVector.user_id == user_id)
        )
    ).one()
    faces = list(
        (
            await session.exec(
                select(FaceVector)
                .where(FaceVector.user_id == user_id)
                .offset(skip)
                .limit(limit)
            )
        ).all()
    )
    return total, faces


async def add_face_vector(
    user_id: UUID,
    embedding: bytes,
    label: str | None,
    session: AsyncSession,
) -> FaceVector:
    count = (
        await session.exec(
            select(func.count())
            .select_from(FaceVector)
            .where(FaceVector.user_id == user_id)
        )
    ).one()
    if count >= MAX_FACE_VECTORS_PER_USER:
        raise FaceVectorLimitExceededError()
    fv = FaceVector(user_id=user_id, embedding=embedding, label=label)
    session.add(fv)
    await session.commit()
    await session.refresh(fv)
    return fv


async def delete_face_vector(
    face_id: UUID,
    user_id: UUID,
    session: AsyncSession,
) -> None:
    fv = await session.get(FaceVector, face_id)
    if fv is None or fv.user_id != user_id:
        raise FaceVectorNotFoundError()
    await session.delete(fv)
    await session.commit()
