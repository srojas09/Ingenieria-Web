#!/bin/bash

#Funcionalidad: Verificar archivos

echo "============================================================="

echo "Verificador de Archivos"

echo "============================================================="


if [ -d "files" ]; then
	echo "existe la carpeta files"
else 
	echo "NO existe la carpeta files"
	echo "creando directorio"
	$(mkdir files)
fi

if [ -f "Clase.txt" ]; then 
	echo "el archivo Clase.txt existen dentro del directorio $(pwd)"
else
	echo "el archivo NO existe"
fi


