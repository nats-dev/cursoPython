# Guía de Git y entrega

## Opción A: dentro del repositorio del curso (recomendada si el profe lo pide así)

```bash
# Desde la raíz de tu repositorio del curso
cp -r /ruta/a/habit-tracker ./proyecto_final      # o copia la carpeta con el explorador
cd proyecto_final
git status
```

Antes de nada comprueba que **no** se suben tus datos personales ni el entorno virtual:

```bash
git status --ignored | head -20      # datos/*.csv y .venv deben salir como ignorados
```

## Opción B: repositorio propio

```bash
cd habit-tracker
git init -b main
git remote add origin https://github.com/TU_USUARIO/habit-tracker.git
```

## Historial por hitos

Subir el trabajo en pasos pequeños y con mensajes claros es parte de la rúbrica de calidad.
Una forma natural de ordenarlo (comprueba que los tests pasan en cada paso):

```bash
git add .gitignore LICENSE requirements*.txt pytest.ini
git commit -m "chore: estructura inicial, dependencias y .gitignore"

git add habitos/__init__.py habitos/excepciones.py habitos/rachas.py tests/conftest.py tests/test_rachas.py
git commit -m "feat: excepciones propias y cálculo de rachas con tests"

git add habitos/modelo.py tests/test_modelo.py
git commit -m "feat: dataclass Habito con validación, registros y cumplimiento"

git add habitos/gestor.py tests/test_gestor.py
git commit -m "feat: GestorHabitos (altas, ediciones, duplicados, progreso de hoy)"

git add habitos/almacen.py tests/test_almacen.py
git commit -m "feat: persistencia en CSV con escritura atómica y errores claros"

git add habitos/analisis.py habitos/graficos.py tests/test_analisis.py tests/test_graficos.py
git commit -m "feat: análisis con pandas y gráficos con Matplotlib"

git add web run.py tests/test_web.py
git commit -m "feat: interfaz web con Flask, mobile-first y API JSON"

git add scripts datos/.gitkeep
git commit -m "feat: script de datos de demostración"

git add README.md docs
git commit -m "docs: README, arquitectura, manual de usuario y guía de Git"
```

Después, si usas la opción B:

```bash
git push -u origin main
```

y con la opción A, un `git push` normal.

## Lista de comprobación antes de entregar

- [ ] `pytest` pasa completo en tu máquina
- [ ] `python run.py` arranca y puedes crear un hábito y marcarlo
- [ ] Has sustituido `[TU NOMBRE]` y `[URL DEL REPOSITORIO]` en `README.md` y `LICENSE`
- [ ] Has añadido tus capturas en `docs/img/` y enlazado en el README
- [ ] En GitHub el README se ve bien (los diagramas Mermaid de `docs/arquitectura.md` se renderizan solos)
- [ ] No hay datos personales (`datos/*.csv`) ni `.venv` en el repositorio
- [ ] Puedes explicar, con tus palabras, qué hace cada capa y por qué
