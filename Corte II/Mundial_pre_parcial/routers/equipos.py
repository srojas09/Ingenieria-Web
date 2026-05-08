from fastapi import APIRouter, HTTPException
from database import get_connection
from schemas import EquipoCreate, EquipoUpdate, EquipoResponse

router = APIRouter()


# ── CRITERIO 4 — Insertar registro ──────────────────────────────
@router.post("/", response_model=EquipoResponse)
def crear_equipo(equipo: EquipoCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO equipos (nombre, pais, grupo, director_tecnico)
            VALUES (%s, %s, %s, %s)
            RETURNING id, nombre, pais, grupo, director_tecnico, activo
            """,
            (equipo.nombre, equipo.pais, equipo.grupo, equipo.director_tecnico)
        )
        row = cursor.fetchone()
        conn.commit()
        return EquipoResponse(
            id=row[0],
            nombre=row[1],
            pais=row[2],
            grupo=row[3],
            director_tecnico=row[4],
            activo=row[5]
        )
    finally:
        cursor.close()
        conn.close()


# ── CRITERIO 5 — Obtener todos los registros activos ────────────
@router.get("/", response_model=list[EquipoResponse])
def obtener_equipos():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, nombre, pais, grupo, director_tecnico, activo FROM equipos WHERE activo = TRUE"
        )
        rows = cursor.fetchall()
        return [
            EquipoResponse(
                id=row[0],
                nombre=row[1],
                pais=row[2],
                grupo=row[3],
                director_tecnico=row[4],
                activo=row[5]
            )
            for row in rows
        ]
    finally:
        cursor.close()
        conn.close()


# ── CRITERIOS 6 y 7 — Obtener un registro por id ────────────────
@router.get("/{equipo_id}", response_model=EquipoResponse)
def obtener_equipo(equipo_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, nombre, pais, grupo, director_tecnico, activo FROM equipos WHERE id = %s AND activo = TRUE",
            (equipo_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        return EquipoResponse(
            id=row[0],
            nombre=row[1],
            pais=row[2],
            grupo=row[3],
            director_tecnico=row[4],
            activo=row[5]
        )
    finally:
        cursor.close()
        conn.close()


# ── CRITERIO 8 — Actualización parcial ──────────────────────────
@router.patch("/{equipo_id}", response_model=EquipoResponse)
def actualizar_equipo(equipo_id: int, equipo: EquipoUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        campos = equipo.model_dump(exclude_unset=True)

        if not campos:
            raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

        set_clause = ", ".join(f"{campo} = %s" for campo in campos)
        valores = list(campos.values())
        valores.append(equipo_id)

        cursor.execute(
            f"UPDATE equipos SET {set_clause} WHERE id = %s AND activo = TRUE RETURNING id, nombre, pais, grupo, director_tecnico, activo",
            valores
        )
        row = cursor.fetchone()
        conn.commit()

        if row is None:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        return EquipoResponse(
            id=row[0],
            nombre=row[1],
            pais=row[2],
            grupo=row[3],
            director_tecnico=row[4],
            activo=row[5]
        )
    finally:
        cursor.close()
        conn.close()


# ── CRITERIOS 9 y 10 — Soft delete ──────────────────────────────
@router.delete("/{equipo_id}")
def eliminar_equipo(equipo_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE equipos SET activo = FALSE WHERE id = %s AND activo = TRUE RETURNING id",
            (equipo_id,)
        )
        row = cursor.fetchone()
        conn.commit()

        if row is None:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        return {"mensaje": f"Equipo {equipo_id} eliminado correctamente"}
    finally:
        cursor.close()
        conn.close()