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

## ADR-006 — CI/CD: GitHub Actions + Argo CD (GitOps)
**Decisión:** GitHub Actions para construir la imagen y Argo CD para desplegarla siguiendo el modelo GitOps.
**Motivo:** Cumple el objetivo de "cero intervención manual en producción": el clúster se sincroniza solo con lo que diga el repositorio.

## ADR-007 — Monitorización: kube-prometheus-stack
**Decisión:** Prometheus + Grafana + Alertmanager mediante el chart `kube-prometheus-stack`.
**Motivo:** Estándar de facto; integra métricas, dashboards y alertas en una sola instalación.

## ADR-008 — Acceso externo: Cloudflare Tunnel
**Fecha:** 2026-06-23
**Decisión:** Exponer el clúster a internet mediante **Cloudflare Tunnel** (`cloudflared`
desplegado como Deployment dentro del propio clúster, con 2 réplicas), usando un dominio propio
(`proyecto-asir.xyz`) registrado en Porkbun y delegado a Cloudflare.
**Motivo:** Permite acceso externo real con HTTPS **sin abrir puertos** en el router ni depender de
una IP pública (funciona incluso detrás de CGNAT). La conexión la inicia `cloudflared` **de dentro
hacia fuera**, por lo que no se expone ningún puerto entrante → más seguro. Las 2 réplicas dan
alta disponibilidad al túnel.
**Alternativa descartada:** DuckDNS + reenvío de puertos + Let's Encrypt HTTP-01 → exige acceso al
router e IP pública (no válido con CGNAT) y expone el servicio directamente. También se descartó
dejar el acceso solo en local, porque no cumpliría el objetivo de "accesible desde el exterior".

## ADR-009 — Certificados HTTPS: cert-manager + Let's Encrypt (DNS-01)
**Fecha:** 2026-06-23
**Decisión:** Emitir y renovar los certificados HTTPS automáticamente con **cert-manager** y
**Let's Encrypt**, usando el desafío **DNS-01** a través de la API de Cloudflare (token con
permisos mínimos: `Zone:DNS:Edit` + `Zone:Zone:Read`).
**Motivo:** El desafío DNS-01 **no necesita** que el clúster sea accesible desde internet (solo crea
un registro TXT temporal vía API), lo que encaja perfecto con un clúster privado detrás de un túnel.
Además permite certificados *wildcard*. Se probó primero con el emisor `staging` para no agotar los
límites del entorno de producción, y luego se pasó a `prod`.
**Alternativa descartada:** desafío HTTP-01 → requiere que Let's Encrypt alcance el servidor por el
puerto 80, inviable en una red privada. Certificados autofirmados → provocan aviso de seguridad en
el navegador.