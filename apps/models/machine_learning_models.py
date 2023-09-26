from pydantic import BaseModel


class PolynomialRegressionDataModel(BaseModel):
    artifact: object
    pred_start_index: int
    pred_start_date: str
