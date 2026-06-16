# Registro de decisiones técnicas (ADR)

Recoge las decisiones importantes del proyecto y su justificación.
Estados: ✅ Aceptada · 🟡 Propuesta (a confirmar) · ❌ Descartada

---

## ADR-001 — Control de versiones: Git + GitHub ✅
**Fecha:** 2026-06-16
**Decisión:** Git como control de versiones y GitHub como repositorio remoto central.
**Motivo:** Estándar de la industria. Además, GitHub será la *fuente de verdad* para el flujo GitOps de la Fase 5.

## ADR-002 — Estructura del repositorio por fases ✅
**Decisión:** Un único repositorio con una carpeta por área (infra, kubernetes, app, ci-cd, monitoring).
**Motivo:** Refleja la hoja de ruta, facilita la navegación y prepara el terreno para GitOps.

## ADR-003 — Distribución de Kubernetes: k3s 🟡
**Decisión propuesta:** k3s.
**Motivo:** Kubernetes certificado pero ligero; bajo consumo de RAM y arranque rápido, ideal para VMs limitadas.
**Alternativa:** kubeadm (Kubernetes "puro": más dominio técnico, pero más laborioso y frágil).
**Pendiente:** confirmar según los recursos de hardware disponibles.

## ADR-004 — Base de virtualización 🟡
**Opciones en evaluación:** VirtualBox local · Proxmox en equipo dedicado · Nube (Oracle Free Tier / Hetzner).
**Pendiente:** confirmar según la RAM/CPU del equipo disponible.

## ADR-005 — Aplicación a desplegar 🟡
**Opciones en evaluación:** app propia de 3 capas · app open source real · demo de microservicios (Online Boutique).
**Pendiente:** confirmar.

## ADR-006 — CI/CD: GitHub Actions + Argo CD (GitOps) ✅
**Decisión:** GitHub Actions para construir la imagen y Argo CD para desplegarla siguiendo el modelo GitOps.
**Motivo:** Cumple el objetivo de "cero intervención manual en producción": el clúster se sincroniza solo con lo que diga el repositorio.

## ADR-007 — Monitorización: kube-prometheus-stack ✅
**Decisión:** Prometheus + Grafana + Alertmanager mediante el chart `kube-prometheus-stack`.
**Motivo:** Estándar de facto; integra métricas, dashboards y alertas en una sola instalación.