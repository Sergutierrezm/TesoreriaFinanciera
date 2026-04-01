from dataclasses import dataclass
from typing import Optional

@dataclass
class RegistroTesoreria:
    anio: int
    mes: str
    capital_liquido: float
    inversion: float
    id: Optional[int] = None


    @property
    def total (self) -> float:
        return self.capital_liquido + self.inversion