# Casos de Prueba — API Mundial de Fútbol

## Equipos

| # | Operación | Input | Resultado esperado | Status |
|---|---|---|---|---|
| 1 | POST /equipos/ | nombre, pais, grupo, director_tecnico válidos | Objeto creado con id asignado | 200 |
| 2 | GET /equipos/ | Sin parámetros | Lista de equipos con activo=true | 200 |
| 3 | GET /equipos/1 | id existente | Objeto del equipo | 200 |
| 4 | GET /equipos/9999 | id inexistente | {"detail": "Equipo no encontrado"} | 404 |
| 5 | PATCH /equipos/1 | {"director_tecnico": "Nuevo DT"} | Solo ese campo cambia | 200 |
| 6 | DELETE /equipos/3 | id existente | Mensaje de confirmación, activo=false en BD | 200 |
| 7 | DELETE /equipos/9999 | id inexistente | {"detail": "Equipo no encontrado"} | 404 |
| 8 | PATCH /equipos/1 | {} vacío | {"detail": "No se enviaron campos..."} | 400 |

## Jugadores

| # | Operación | Input | Resultado esperado | Status |
|---|---|---|---|---|
| 1 | POST /jugadores/ | nombre, posicion, dorsal, edad, nacionalidad válidos | Objeto creado con id asignado | 200 |
| 2 | GET /jugadores/ | Sin parámetros | Lista de jugadores con activo=true | 200 |
| 3 | GET /jugadores/1 | id existente | Objeto del jugador | 200 |
| 4 | GET /jugadores/9999 | id inexistente | {"detail": "Jugador no encontrado"} | 404 |
| 5 | PATCH /jugadores/1 | {"dorsal": 99} | Solo dorsal cambia | 200 |
| 6 | DELETE /jugadores/3 | id existente | Mensaje de confirmación, activo=false en BD | 200 |
| 7 | DELETE /jugadores/9999 | id inexistente | {"detail": "Jugador no encontrado"} | 404 |
| 8 | PATCH /jugadores/1 | {} vacío | {"detail": "No se enviaron campos..."} | 400 |