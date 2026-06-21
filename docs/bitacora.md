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


## 2026-06-20 — Fase 1: máquinas virtuales
- Instalado VirtualBox y descargada la ISO de Ubuntu Server 24.04 LTS.
- Configurada la red Host-Only `192.168.56.0/24` (anfitrión en `.1`, DHCP desactivado).
- Creada la VM `k3s-server` (2 vCPU, 4 GB, 25 GB) con dos adaptadores: NAT + Host-Only.
- Instalado Ubuntu Server a mano con OpenSSH activado e IP fija `192.168.56.10`.
- **Problema:** al reiniciar tras instalar apareció "failed unmounting cdrom.mount".
  **Solución:** era inofensivo; apagué la VM y quité la ISO de la unidad óptica.
- Clonadas `k3s-agent-1` (`.11`) y `k3s-agent-2` (`.12`); ajustados hostname e IP en cada una.
- Configurado acceso por clave SSH sin contraseña desde Windows y atajos en `~/.ssh/config`.
- Añadidas las entradas de los tres nodos en `/etc/hosts`.
- **Resultado:** 3 nodos accesibles por SSH y comunicados entre sí. Fase 1 completada.


## 2026-06-21 — Fase 2: clúster Kubernetes (k3s)
- Instalado k3s (v1.35.5+k3s1) en `k3s-server` como control-plane, forzando la red Host-Only y
  desactivando Traefik y servicelb (se usarán MetalLB + Ingress-NGINX en la Fase 3).
- Unidos `k3s-agent-1` y `k3s-agent-2` como workers con el token del servidor.
- **Problema:** al unir el primer worker, el servicio `k3s-agent` falló porque al pegar el token se
  coló un salto de línea (token inválido).
  **Solución:** capturar el token con `read -r TOKEN` (ignora el salto de línea) y relanzar con `K3S_TOKEN="$TOKEN"`.
- Instalado `kubectl` en Windows, copiado el kubeconfig por `scp` y ajustado el campo `server:`.
- **Resultado:** 3 nodos `Ready` y clúster manejable desde Windows. Fase 2 completada.