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

## ADR-003 — Distribución de Kubernetes: k3s ✅
**Fecha:** 2026-06-16
**Decisión:** Usar k3s como distribución de Kubernetes.
**Motivo:** Kubernetes certificado pero ligero y fiable; arranque rápido y bajo consumo, lo que
reduce el riesgo de fallos el día de la defensa y permite centrar el esfuerzo en lo que más valor
aporta (CI/CD y monitorización).
**Alternativa descartada:** kubeadm (Kubernetes "puro": más dominio técnico pero más laborioso y
frágil). Se contempla como entorno adicional si sobra tiempo.

## ADR-004 — Base de virtualización: VirtualBox en local ✅
**Fecha:** 2026-06-16
**Decisión:** Desplegar las 3 VMs con VirtualBox en el equipo local (32 GB de RAM).
**Motivo:** Encaja con las competencias de ASIR (se administra la virtualización y la red); total
fiabilidad y disponibilidad sin internet el día de la defensa; sin coste ni riesgo de suspensión de
cuenta. El acceso HTTPS externo se resolverá con un túnel (Cloudflare Tunnel) o DuckDNS + apertura
de puerto en el router.
**Alternativa descartada:** nube gratuita (Oracle Free Tier). Se menciona como línea de mejora futura.

## ADR-005 — Aplicación a desplegar 🟡
**Opciones en evaluación:** app propia de 3 capas · app open source real · demo de microservicios (Online Boutique).
**Pendiente:** confirmar.

## ADR-006 — CI/CD: GitHub Actions + Argo CD (GitOps) ✅
**Decisión:** GitHub Actions para construir la imagen y Argo CD para desplegarla siguiendo el modelo GitOps.
**Motivo:** Cumple el objetivo de "cero intervención manual en producción": el clúster se sincroniza solo con lo que diga el repositorio.

## ADR-007 — Monitorización: kube-prometheus-stack ✅
**Decisión:** Prometheus + Grafana + Alertmanager mediante el chart `kube-prometheus-stack`.
**Motivo:** Estándar de facto; integra métricas, dashboards y alertas en una sola instalación.