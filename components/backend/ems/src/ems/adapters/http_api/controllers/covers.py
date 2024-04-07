from typing import Annotated, Any

from annotated_types import Gt
from ems.adapters.http_api.auth import get_auth_payload
from ems.adapters.http_api.dependencies import get_event_service
from ems.application.services import EventService
from ems.application.services.event_service import CoverDownloadStatus
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

router = APIRouter(
    prefix="/covers",
    tags=["Обложки"],
)


@router.get(
    path="/{cover_id}",
    status_code=200,
    responses={
        200: {
            "description": "Изображение скачано.",
            "content": {"image/jpeg"},
        },
        404: {"description": "Обложка не найдена."},
    },
)
async def download_cover(
    cover_id: Annotated[int, Gt(0)],
    event_service: Annotated[EventService, Depends(get_event_service)],
    _auth_claims: Annotated[dict[str, Any], Depends(get_auth_payload)],
):
    match await event_service.download_cover(cover_id=cover_id):
        case _, CoverDownloadStatus.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No cover with such id.",
            )
        case img_bytes, CoverDownloadStatus.OK:
            return Response(content=img_bytes, media_type="image/jpeg")
