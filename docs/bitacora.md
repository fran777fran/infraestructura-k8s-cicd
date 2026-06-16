# Bitácora de trabajo

Diario del proyecto. Cada entrada: fecha · qué se hizo · problemas y soluciones.

## 2026-06-16 — Fase 0: arranque del proyecto
- Configurada la identidad de Git (`user.name`, `user.email`) y la rama por defecto `main`.
- Creada la estructura de carpetas del proyecto.
- Inicializado el repositorio Git local y realizado el primer commit.
- Creado el repositorio en GitHub y subido el proyecto con `git push`.
- **Problema:** añadí el remoto `origin` con la URL de ejemplo (`tu-usuario`) por error.
  **Solución:** lo eliminé con `git remote remove origin` y lo volví a añadir con mi URL real
  (`https://github.com/fran777fran/...`). Verificado con `git remote -v`.
- Redactada la documentación inicial: README, decisiones técnicas (ADR) y esta bitácora.