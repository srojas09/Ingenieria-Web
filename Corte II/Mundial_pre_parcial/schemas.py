from pydantic import BaseModel, ConfigDict
from typing import Optional


# ───────────────────────────────
# TABLA 1 - Equipos
# ───────────────────────────────

class EquipoBase(BaseModel):
    nombre: str
    pais: str
    grupo: Optional[str] = None
    director_tecnico: Optional[str] = None


class EquipoCreate(EquipoBase):
    pass


class EquipoUpdate(BaseModel):
    nombre: Optional[str] = None
    pais: Optional[str] = None
    grupo: Optional[str] = None
    director_tecnico: Optional[str] = None


class EquipoResponse(EquipoBase):
    id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)


# ───────────────────────────────
# TABLA 2 - Jugadores
# ───────────────────────────────

class JugadorBase(BaseModel):
    nombre: str
    posicion: Optional[str] = None
    dorsal: Optional[int] = None
    edad: Optional[int] = None
    nacionalidad: Optional[str] = None


class JugadorCreate(JugadorBase):
    pass


class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    posicion: Optional[str] = None
    dorsal: Optional[int] = None
    edad: Optional[int] = None
    nacionalidad: Optional[str] = None


class JugadorResponse(JugadorBase):
    id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)