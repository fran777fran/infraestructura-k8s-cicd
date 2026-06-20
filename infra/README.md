# Fase 1 — Infraestructura: máquinas virtuales

Las tres máquinas virtuales que forman el clúster, creadas con VirtualBox sobre el PC anfitrión.

## Máquinas

| VM | Rol | vCPU | RAM | Disco | IP (Host-Only) |
|----|-----|------|-----|-------|----------------|
| `k3s-server` | control-plane | 2 | 4 GB | 25 GB | 192.168.56.10 |
| `k3s-agent-1` | worker | 2 | 4 GB | 25 GB | 192.168.56.11 |
| `k3s-agent-2` | worker | 2 | 4 GB | 25 GB | 192.168.56.12 |

- **Sistema operativo:** Ubuntu Server 24.04 LTS
- **Red:** dos adaptadores por VM
  - *Adaptador 1 — NAT:* salida a internet (descargas).
  - *Adaptador 2 — Host-Only* (`192.168.56.0/24`): comunicación interna del clúster
    y acceso SSH desde el anfitrión (`192.168.56.1`).

## Cómo se creó

1. Instalación manual de Ubuntu Server en `k3s-server`, con servidor **OpenSSH** activado.
2. IP fija configurada en **netplan** sobre la interfaz host-only (`enp0s8`).
3. `k3s-agent-1` y `k3s-agent-2` creadas **clonando** `k3s-server` (clon completo, MAC regeneradas).
4. En cada clon se ajustó el hostname (`hostnamectl`) y la IP.
5. Acceso por **clave SSH** (sin contraseña) desde el anfitrión y resolución de nombres por `/etc/hosts`.

## Acceso

Desde el PC anfitrión (atajos en `~/.ssh/config`):

```bash
ssh k3s-server
ssh k3s-agent-1
ssh k3s-agent-2
```