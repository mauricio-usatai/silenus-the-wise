import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from settings import Settings
from apps.services import PolynomialRegressionService
from src.logger import create_logger
from src.exceptions import (
    InvalidDate,
    InvalidDateRange,
)


router = APIRouter(
    prefix="/api/v0/predict",
    tags=["predict"],
)

settings = Settings()
logger = create_logger(settings.LOGGER)


@router.get("/polynomial-regression/{symbol}")
async def preg_predict(symbol: str, from_date: str, to_date: str) -> JSONResponse:
    """
    Polinomyal Regression prediction route

    Args:
        symbol (str): The name of the ticker
        from_date (str): Start date
        to_date (str): End date

    Returns:
        JSONResponse: Api response
    """
    preg = PolynomialRegressionService()
    try:
        prediction = await preg.predict(
            symbol=symbol,
            from_date=from_date,
            to_date=to_date,
        )
    except InvalidDate as err:
        logger.error(err)
        return JSONResponse(status_code=400, content={"error": "Invalid date"})
    except InvalidDateRange as err:
        logger.error(err)
        return JSONResponse(status_code=400, content={"error": "Invalid date range"})
    except Exception as err:
        logger.error("%s\n%s", err, traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": "unknown server error"})

    return JSONResponse(status_code=200, content={"prediction": prediction})
