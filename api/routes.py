from fastapi import APIRouter
from datetime import datetime
from fastapi import HTTPException
from service.package_versions import get_package_versions
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/versions")
async def get_versions(name: str):
    logger.info(f"Request received to get versions for package {name}.")
    try:
        package_versions = get_package_versions(name)

        if package_versions:
            formatted_response = {
                "name": name,
                "versions": package_versions,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            logger.info(f"Versions for package {name} fetched successfully")
            return formatted_response
        else:
            error_message = f"Failed to fetch vulnerability data for package {name}."
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        error_message = f"An error occurred while processing the request: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
