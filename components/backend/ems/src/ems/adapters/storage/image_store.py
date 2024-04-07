import asyncio
import io
from typing import Optional
from uuid import UUID

import aiofiles
import PIL.Image
from ems.adapters.storage import Settings
from ems.application.interfaces import IImage, IImageStore


class Image(IImage):
    __config: Settings
    image_id: UUID
    size: int
    path: str

    def __init__(self, config: Settings, image_id: UUID, size: int, path: str):
        self.__config = config
        self.image_id = image_id
        self.size = size
        self.path = path


class ImageStore(IImageStore):
    __config: Settings

    def __init__(self, config: Settings):
        self.__config = config

    @staticmethod
    def _load_from_bytes(data: bytes) -> PIL.Image:
        return PIL.Image.open(io.BytesIO(data))

    @staticmethod
    def _convert(image: PIL.Image) -> bytes:
        rgb_image = image.convert("RGB")
        converted = io.BytesIO()
        rgb_image.save(converted, "JPEG")
        return converted.getvalue()

    async def save(
        self, data: bytes, image_id: UUID, subdir: Optional[str] = None
    ) -> Image:
        loop = asyncio.get_running_loop()
        image = await loop.run_in_executor(None, self._load_from_bytes, data)
        converted = await loop.run_in_executor(None, self._convert, image)

        path = f"{self.__config.PUBLIC_DIR_PATH}/images"
        if subdir is not None:
            path += f"/{subdir}/{image_id}.jpeg"
        else:
            path += f"/{image_id}.jpeg"
        async with aiofiles.open(path, "w+b") as output:
            await output.write(converted)

        stored = Image(self.__config, image_id, image.size, path)
        return stored
