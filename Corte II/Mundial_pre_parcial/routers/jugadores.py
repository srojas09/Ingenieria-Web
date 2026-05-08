from fastapi import APIRouter, HTTPException
from database import get_connection
from schemas import JugadorCreate, JugadorUpdate, JugadorResponse

router = APIRouter()


# ── CRITERIO 4 — Insertar registro ──────────────────────────────
@router.post("/", response_model=JugadorResponse)
def crear_jugador(jugador: JugadorCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO jugadores (nombre, posicion, dorsal, edad, nacionalidad)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, nombre, posicion, dorsal, edad, nacionalidad, activo
            """,
            (jugador.nombre, jugador.posicion, jugador.dorsal, jugador.edad, jugador.nacionalidad)
        )
        row = cursor.fetchone()
        conn.commit()
        return JugadorResponse(
            id=row[0],
            nombre=row[1],
            posicion=row[2],
            dorsal=row[3],
            edad=row[4],
            nacionalidad=row[5],
            activo=row[6]
        )
    finally:
        cursor.close()
        conn.close()


# ── CRITERIO 5 — Obtener todos los registros activos ────────────
@router.get("/", response_model=list[JugadorResponse])
def obtener_jugadores():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, nombre, posicion, dorsal, edad, nacionalidad, activo FROM jugadores WHERE activo = TRUE"
        )
        rows = cursor.fetchall()
        return [
            JugadorResponse(
                id=row[0],
                nombre=row[1],
                posicion=row[2],
                dorsal=row[3],
                edad=row[4],
                nacionalidad=row[5],
                activo=row[6]
            )
            for row in rows
        ]
    finally:
        cursor.close()
        conn.close()


# ── CRITERIOS 6 y 7 — Obtener un registro por id ────────────────
@router.get("/{jugador_id}", response_model=JugadorResponse)
def obtener_jugador(jugador_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, nombre, posicion, dorsal, edad, nacionalidad, activo FROM jugadores WHERE id = %s AND activo = TRUE",
            (jugador_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return JugadorResponse(
            id=row[0],
            nombre=row[1],
            posicion=row[2],
            dorsal=row[3],
            edad=row[4],
            nacionalidad=row[5],
            activo=row[6]
        )
    finally:
        cursor.close()
        conn.close()


# ── CRITERIO 8 — Actualización parcial ──────────────────────────
@router.patch("/{jugador_id}", response_model=JugadorResponse)
def actualizar_jugador(jugador_id: int, jugador: JugadorUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        campos = jugador.model_dump(exclude_unset=True)

        if not campos:
            raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

        set_clause = ", ".join(f"{campo} = %s" for campo in campos)
        valores = list(campos.values())
        valores.append(jugador_id)

        cursor.execute(
            f"UPDATE jugadores SET {set_clause} WHERE id = %s AND activo = TRUE RETURNING id, nombre, posicion, dorsal, edad, nacionalidad, activo",
            valores
        )
        row = cursor.fetchone()
        conn.commit()

        if row is None:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        return JugadorResponse(
            id=row[0],
            nombre=row[1],
            posicion=row[2],
            dorsal=row[3],
            edad=row[4],
            nacionalidad=row[5],
            activo=row[6]
        )
    finally:
        cursor.close()
        conn.close()


# ── CRITERIOS 9 y 10 — Soft delete ──────────────────────────────
@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE jugadores SET activo = FALSE WHERE id = %s AND activo = TRUE RETURNING id",
            (jugador_id,)
        )
        row = cursor.fetchone()
        conn.commit()

        if row is None:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        return {"mensaje": f"Jugador {jugador_id} eliminado correctamente"}
    finally:
        cursor.close()
        conn.close()