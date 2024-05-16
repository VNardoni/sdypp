## PART II 

Desarrolle este proceso de manera distribuida donde se debe partir la
imagen en n pedazos, y asignar la tarea de aplicar la máscara a N procesos
distribuidos. Después deberá unificar los resultados.
A partir de ambas implementaciones, comente los resultados de performance
dependiendo de la cantidad de nodos y tamaño de imagen.

## PART III

Mejore la aplicación del punto anterior para que, en caso de que un proceso
distribuido (al que se le asignó parte de la imagen a procesar - WORKER) se caiga y no responda, el proceso principal detecte esta situación y pida este
cálculo a otro proceso.

![](grafico/diagrama.png)

