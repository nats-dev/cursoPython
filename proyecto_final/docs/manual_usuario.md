# Manual de usuario

## Crear un hábito

1. Pulsa **Nuevo** en la barra inferior.
2. Escribe un **nombre** (obligatorio, hasta 60 caracteres) y, si quieres, una descripción.
3. Elige la **frecuencia**:
   - *Todos los días*: la racha cuenta días seguidos.
   - *N veces por semana*: la racha cuenta semanas seguidas (de lunes a domingo) en las que alcanzas ese objetivo.
4. Pulsa **Guardar**.

## Registrar el día

En **Hoy** toca el círculo de cada hábito para marcarlo. Vuelve a tocarlo para desmarcarlo.
La barra superior muestra cuántos llevas de los que *tocan* hoy. Un hábito semanal cuyo objetivo
ya has cumplido esta semana deja de contar: hoy toca descansar.

## Corregir días anteriores

Entra en un hábito (toca su nombre) y usa el **calendario de las últimas semanas**: toca un día para
marcarlo o desmarcarlo. Los días futuros están bloqueados.

## Entender las cifras

| Cifra | Significado |
|-------|-------------|
| **Racha actual** | Días (o semanas) seguidos cumpliendo. No se rompe por no haber marcado todavía hoy |
| **Mejor racha** | La racha más larga de tu historial |
| **Veces en total** | Todas las veces que lo has cumplido |
| **Últimos 28 días** | % del objetivo que has cumplido en las últimas cuatro semanas |

## Estadísticas

La pestaña **Estadísticas** muestra el cumplimiento por hábito, la evolución semanal, los días de la
semana en que más cumples y una tabla resumen. Se activa cuando hay al menos un registro.

## Editar, archivar y eliminar

- **Editar:** desde el detalle del hábito. Cambiar la frecuencia recalcula las rachas con la nueva regla.
- **Archivar:** el hábito deja de aparecer en «Hoy» y en las estadísticas, pero conserva su historial.
- **Restaurar:** desde **Hábitos → Archivados**.
- **Eliminar:** solo para hábitos archivados; borra el hábito y todos sus registros y **no se puede deshacer**.

## Copia de seguridad

Tus datos son los ficheros `datos/habitos.csv` y `datos/registros.csv`. Copiarlos es hacer una copia
de seguridad; pegarlos en otra instalación los restaura.

## Problemas frecuentes

| Problema | Causa y solución |
|----------|------------------|
| «Problema con los datos» al abrir la app | Un CSV se ha editado a mano con un error. El mensaje indica el fichero y la línea |
| No puedo abrirla desde el móvil | Comprueba que ambos están en la misma wifi, que arrancaste con `HOST=0.0.0.0` y que el cortafuegos permite el puerto 5000 |
| «Ya tienes un hábito llamado…» | Los nombres no se pueden repetir entre hábitos activos (no distingue mayúsculas) |
