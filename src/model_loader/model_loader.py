from __future__ import annotations

import pickle


class ModelLoader:
    _instance = None

    @classmethod
    def get_instance(cls) -> ModelLoader:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.models_dir = "artifacts/models"
        self.loaded_models = {}

    def load_model(self, model: str) -> object:
        """
        Load models into memory

        Args:
            model (str): The model's name

        Returns:
            object: The model desciption object
        """
        if model not in self.loaded_models:
            with open(f"{self.models_dir}/{model}.pickle", "rb") as file:
                model_obj = pickle.load(file)
            self.loaded_models[model] = model_obj

        return self.loaded_models[model]
