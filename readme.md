# Infraestructura empresarial containerizada con CI/CD y monitorización

**Proyecto Final · Ciclo Formativo de Grado Superior — Administración de Sistemas Informáticos en Red (ASIR)**

- **Autor:** Francisco Sierra de la Rosa
- **Curso:** 2025/2026

---

## Objetivo

Diseñar, desplegar y mantener desde cero un entorno de producción simulado que demuestre
el dominio de la infraestructura moderna de extremo a extremo —virtualización, contenedores,
orquestación, automatización (CI/CD) y monitorización— **sin intervención manual en producción**.

## ¿Qué se construye?

- Un **clúster de Kubernetes de 3 nodos** (1 control-plane + 2 workers) sobre máquinas virtuales.
- Una **aplicación real con varios servicios**, accesible desde el exterior mediante **HTTPS**.
- Un **pipeline de CI/CD** que despliega automáticamente en cada `push` al repositorio.
- Un **sistema de monitorización** completo: métricas, paneles (dashboards) y alertas.

## Arquitectura (resumen)

| Capa | Tecnología |
|------|------------|
| Virtualización | A confirmar (VirtualBox / Proxmox / nube) |
| Sistema operativo | Ubuntu Server LTS |
| Orquestación | Kubernetes (k3s) |
| Red del clúster | CNI + MetalLB + Ingress-NGINX |
| HTTPS | cert-manager + Let's Encrypt |
| Aplicación | A confirmar |
| CI/CD | GitHub Actions + Argo CD (GitOps) |
| Monitorización | Prometheus + Grafana + Alertmanager |

> Diagrama y detalle completo en [`docs/arquitectura.md`](docs/arquitectura.md).

## Estructura del repositorio

├── docs/ → Documentación, diagramas y bitácora
├── infra/ → Aprovisionamiento de las máquinas virtuales (Fase 1)
├── kubernetes/ → Manifiestos del clúster (Fases 2–4)
├── app/ → Código de la aplicación (Fase 4)
├── ci-cd/ → Pipelines y configuración GitOps (Fase 5)
└── monitoring/ → Prometheus, Grafana y alertas (Fase 6)


## Fases del proyecto

| Fase | Contenido | Estado |
|------|-----------|--------|
| 0 | Diseño, repositorio y documentación | 🟢 En curso |
| 1 | Despliegue de las 3 máquinas virtuales | ⏳ |
| 2 | Instalación del clúster Kubernetes | ⏳ |
| 3 | Red, acceso externo y HTTPS | ⏳ |
| 4 | Despliegue de la aplicación | ⏳ |
| 5 | Pipeline de CI/CD | ⏳ |
| 6 | Monitorización | ⏳ |

## Documentación

- [Arquitectura](docs/arquitectura.md)
- [Decisiones técnicas (ADR)](docs/decisiones.md)
- [Bitácora de trabajo](docs/bitacora.md)