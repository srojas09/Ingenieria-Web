#!/bin/bash

#Funcionalidad: Saludar a tu flete

HORA=$(date +%H)

echo " la hora es: $HORA:$(date +%H)"

if [ $HORA -lt 12 ]; then 
	echo "hola el reye, buenos dias"
fi

if [ $HORA -ge 6 ] && [ $HORA -lt 18 ]; then
	echo "Buenas tardes princeso"
fi

if [ $HORA -ge 18 ]; then 
	echo "venga le doy su buena noche"
fi

