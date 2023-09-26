from typing import List

import datetime

import numpy as np
import pandas as pd
from workalendar.america.brazil import Brazil

from settings import Settings
from apps.models import PolynomialRegressionDataModel
from src.model_loader import ModelLoader
from src.logger import create_logger
from src.exceptions import (
    InvalidDate,
    InvalidDateRange,
)


settings = Settings()
logger = create_logger(settings.LOGGER)


class PolynomialRegressionService:
    """
    Service to serve a polynomial regression model
    """

    async def predict(self, symbol: str, from_date: str, to_date: str) -> dict:
        """
        Perform predictions

        Args:
            symbol (str): ticker name, i.e PETR4
            from_date (str): date to start prediction
            to_date (str): date to end prediction

        Raises:
            InvalidDateRange: Date range provided is not valid
            InvalidDate: Date string is not valid

        Returns:
            dict: Predictions
        """
        model_loader = ModelLoader.get_instance()
        model_descriptor = PolynomialRegressionDataModel(
            **model_loader.load_model(f"polynomial_regression_{symbol.lower()}")
        )

        try:
            from_date = datetime.datetime.strptime(from_date, "%y-%m-%d")
            to_date = datetime.datetime.strptime(
                f"{to_date} 23:59:59", "%y-%m-%d %H:%M:%S"
            )
            if from_date.date() > to_date.date():
                raise InvalidDateRange
        except ValueError as err:
            raise InvalidDate from err

        pred_start_index = model_descriptor.pred_start_index
        pred_start_date = model_descriptor.pred_start_date
        pred_start_date = datetime.datetime.strptime(
            pred_start_date, "%y-%m-%d %H:%M:%S"
        )

        prediction_hours = self.get_working_hours_between(
            from_date=from_date,
            to_date=to_date,
        )

        adjusted_pred_start_index = self.adjust_pred_start_index(
            from_date=from_date,
            pred_start_date=pred_start_date,
            pred_start_index=pred_start_index,
        )

        model = model_descriptor.artifact

        predictions = model.predict(
            np.array(
                list(
                    range(
                        adjusted_pred_start_index,
                        adjusted_pred_start_index + len(prediction_hours),
                    )
                )
            ).reshape(-1, 1)
        )

        predictions = {
            hour: f"{prediction:.3f}"
            for hour, prediction in zip(prediction_hours, predictions.flatten())
        }
        return predictions, adjusted_pred_start_index

    def get_working_hours_between(self, from_date: str, to_date: str) -> List[str]:
        """
        Generate a list of working hours for a date range

        Args:
            from_date (str): Working hours start
            to_date (str): Working hours end

        Returns:
            List[str]: A list of dates
        """
        cal = Brazil()
        # Filter working days and market open hours
        days = pd.date_range(start=from_date, end=to_date, freq="H")
        days_df = pd.DataFrame({"date": days})
        days_df_filtered = days_df[
            (days_df["date"].dt.time >= pd.to_datetime("10:00:00").time())
            & (days_df["date"].dt.time <= pd.to_datetime("16:00:00").time())
        ]
        days_df_filtered["working_day"] = days_df_filtered["date"].apply(
            cal.is_working_day
        )
        days_df_filtered["date"] = days_df_filtered["date"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        working_days = list(
            days_df_filtered[days_df_filtered["working_day"] == True]["date"]
        )

        return working_days

    def adjust_pred_start_index(
        self,
        from_date: datetime.datetime,
        pred_start_date: datetime.datetime,
        pred_start_index: int,
    ) -> int:
        """
        The polynomial regression model is a function of time so the prediciton
        index is just a numeric representation of that time in the function itself
        This helper function adjusts that index in order to generate correct predictions
        for a given time period

        Args:
            from_date (datetime.datetime): Inital date
            pred_start_date (datetime.datetime): The model's reference date
            pred_start_index (int): Index representing pred_start_date on the model

        Returns:
            int: Adjusted index
        """
        cal = Brazil()

        working_days = cal.get_working_days_delta(from_date, pred_start_date)
        working_days_diff = (
            working_days if from_date >= pred_start_date else -working_days
        )
        adjusted_index = pred_start_index + working_days_diff * 7

        return adjusted_index
