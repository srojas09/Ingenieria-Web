#!/bin/bash

#Funcion: crear un archivo con la fecha

FECHA=$(date +%H%M)
echo $FECHA

touch file_$FECHA.txt

echo "su archivo fue creado"


