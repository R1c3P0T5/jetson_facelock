from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import FaceVectorNotFoundError
from src.faces.models import FaceVector


async def list_face_vectors(user_id: UUID, session: AsyncSession) -> list[FaceVector]:
    result = await session.exec(select(FaceVector).where(FaceVector.user_id == user_id))
    return list(result.all())


async def add_face_vector(
    user_id: UUID,
    embedding: bytes,
    label: str | None,
    session: AsyncSession,
) -> FaceVector:
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
