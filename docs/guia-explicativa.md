# Guía explicativa del proyecto (Fases 0–3)

> Documento de apoyo para entender —y saber defender— cada pieza de la infraestructura
> construida hasta ahora. Pensado para leerse de principio a fin.

---

## 1. ¿Qué estás construyendo? (la idea en una frase)

Estás montando, **desde cero y sobre tu propio PC**, un entorno de producción como el de una
empresa: varios servidores que forman un **clúster de Kubernetes**, sobre el que corre una
aplicación accesible **desde internet con HTTPS**, que se desplegará **sola** al subir cambios al
repositorio (CI/CD) y que estará **monitorizada**.

Una analogía: es como construir un **polígono industrial completo**. Primero el terreno y las naves
(las máquinas virtuales), luego un sistema que coloca y vigila la mercancía automáticamente
(Kubernetes), después la entrada con seguridad y carretera de acceso (red + HTTPS), y por último
una cinta transportadora que mete producto nuevo sin parar la fábrica (CI/CD) y unas cámaras de
control (monitorización).

---

## 2. Conceptos base (para entender todo lo demás)

| Concepto | Qué es, en cristiano |
|----------|----------------------|
| **Virtualización** | Crear "ordenadores dentro de tu ordenador". Cada uno (una **máquina virtual** o VM) cree que es un PC de verdad. Aquí usas **VirtualBox** para crear 3. |
| **Contenedor** | Una "caja" que lleva dentro una aplicación **y todo lo que necesita** para funcionar (librerías, dependencias). Se ejecuta igual en cualquier sitio. |
| **Imagen** | La "plantilla" de un contenedor (como un molde). De una imagen se crean muchos contenedores idénticos. |
| **Kubernetes (K8s)** | El "director de orquesta": decide en qué servidor corre cada contenedor, los reinicia si fallan, reparte la carga, etc. Tú le dices *qué* quieres, él se ocupa del *cómo*. |
| **k3s** | Una versión **ligera** de Kubernetes (un solo programa), ideal para equipos modestos. Es Kubernetes de verdad, certificado. |
| **Nodo** | Cada servidor (VM) que forma parte del clúster. |
| **Control-plane** | El nodo "**cerebro**": toma las decisiones y guarda el estado del clúster. En tu caso, `k3s-server`. |
| **Worker** | Los nodos "**obreros**" donde se ejecutan de verdad las aplicaciones. En tu caso, `k3s-agent-1` y `k3s-agent-2`. |

### Los 4 objetos de Kubernetes que ya has usado

- **Pod** → la unidad mínima: uno (o varios) contenedores que viven juntos. Es lo que de verdad
  "se ejecuta".
- **Deployment** → el "**gerente**" de los pods: tú le dices "quiero 2 copias de esta app" y él se
  encarga de que **siempre** haya 2 vivas (si una se cae, la recrea).
- **Service** → la "**centralita**": da una dirección **interna y estable** a un grupo de pods y
  reparte el tráfico entre ellos. (Los pods cambian de IP al recrearse; el Service no.)
- **Ingress** → el "**recepcionista**": recibe el tráfico web de fuera y lo envía al Service
  correcto **según la URL** que pidan.

- **Helm** → el "**instalador de aplicaciones**" de Kubernetes (como el `apt` de Linux). Instala
  componentes complejos con un solo comando. Lo usaste para MetalLB, Ingress, cert-manager...

---

## 3. Lo que has montado, fase por fase

### Fase 0 — Repositorio y documentación

**Qué hiciste:** creaste un repositorio **Git** (control de versiones) y lo subiste a **GitHub**,
con una estructura de carpetas por áreas (`infra/`, `kubernetes/`, `ci-cd/`...).

**Por qué importa:** ese repositorio es la **fuente única de verdad** del proyecto. En la Fase 5,
el sistema desplegará automáticamente *lo que diga el repositorio* (a eso se le llama **GitOps**).
Además, documentar desde el día 1 (README, decisiones ADR, bitácora) es lo que distingue un
proyecto profesional.

### Fase 1 — Las máquinas virtuales

**Qué hiciste:** con VirtualBox creaste 3 VMs con **Ubuntu Server**, cada una con **dos tarjetas de
red**, y las dejaste accesibles por **SSH** sin contraseña.

| VM | Rol | IP interna |
|----|-----|------------|
| `k3s-server` | control-plane | 192.168.56.10 |
| `k3s-agent-1` | worker | 192.168.56.11 |
| `k3s-agent-2` | worker | 192.168.56.12 |

**Las dos tarjetas de red (clave para entender el resto):**
- **NAT** → da **salida a internet** a la VM (para descargar paquetes). Es como un teléfono que
  llama hacia fuera pero no recibe llamadas.
- **Host-Only** (`192.168.56.0/24`) → una **red privada** entre tu PC y las 3 VMs, para que hablen
  entre ellas y para que tú entres por SSH. Tu PC está en esa red como `192.168.56.1`.

**SSH y claves:** en vez de entrar por la ventanita de VirtualBox, te conectas por **SSH** (terminal
remota) desde Windows. Con **claves SSH** entras sin escribir contraseña: tienes una clave *privada*
(secreta, en tu PC) y una *pública* (copiada a los servidores). Es el estándar profesional.

### Fase 2 — El clúster Kubernetes (k3s)

**Qué hiciste:** instalaste **k3s** en el control-plane y uniste los 2 workers, formando un clúster
de 3 nodos. Luego lo manejas con **`kubectl`** desde Windows.

**Detalles importantes de la instalación (por si te preguntan):**
- `--node-ip` / `--flannel-iface enp0s8` → forzaste a k3s a usar la **red Host-Only** para
  comunicarse, no la NAT. Sin esto, los workers no encontrarían al servidor.
- `--tls-san 192.168.56.10` → metiste esa IP en el **certificado** del clúster, para poder
  controlarlo desde Windows sin errores de seguridad.
- `--disable traefik --disable servicelb` → **desactivaste** el balanceador y el ingress que k3s
  trae por defecto, porque ibas a instalar los tuyos (MetalLB + Ingress-NGINX) en la Fase 3.

**`kubectl` desde Windows:** copiaste el archivo de credenciales (`kubeconfig`) del servidor a tu PC
y cambiaste la dirección a `192.168.56.10`. Desde entonces, das órdenes al clúster desde tu
terminal, como un administrador real.

### Fase 3 — Red, acceso externo y HTTPS

Aquí abriste el clúster al mundo. Son varias piezas que encajan:

**MetalLB** → el "**repartidor de IPs**". En la nube, cuando pides un servicio accesible, el
proveedor te da una IP automáticamente. En tu clúster casero no hay nadie que lo haga... salvo
MetalLB, que reparte IPs de un rango que le diste (`192.168.56.200–250`). Gracias a él, tu
Ingress tiene una IP fija accesible.

**Ingress-NGINX** → el "**portero/recepcionista**" del clúster. Es el único punto de entrada del
tráfico web; mira la URL y lo manda al Service correcto. MetalLB le asignó la IP `192.168.56.200`.

**cert-manager + Let's Encrypt** → el "**gestor de candados**". cert-manager pide certificados HTTPS
de forma automática a **Let's Encrypt** (una autoridad que los emite **gratis**) y los **renueva
solo** antes de que caduquen.

- **Desafío DNS-01:** para darte el certificado, Let's Encrypt necesita comprobar que el dominio es
  tuyo. El método DNS-01 lo hace **creando un registro DNS temporal** a través de la API de
  Cloudflare (con un token de permisos mínimos). Lo elegiste porque **no necesita** que tu clúster
  sea accesible desde fuera — perfecto para una red privada.
- **staging vs prod:** primero probaste con el emisor de *pruebas* (staging, sin límites) y, al ver
  que funcionaba, pasaste al *real* (prod), que da el candado de confianza.

**Cloudflare Tunnel** → el "**túnel al exterior**". Tu clúster está en una red privada; nadie de
internet puede entrar directamente. **cloudflared** (un pequeño programa que corre **dentro de tu
clúster**, con 2 réplicas) abre una conexión **de dentro hacia fuera** hacia Cloudflare. Como la
conexión la inicia él, **no hace falta abrir ningún puerto** en tu router (más seguro y funciona
detrás de cualquier conexión).

**El dominio:** registraste `proyecto-asir.xyz` en Porkbun y lo **delegaste a Cloudflare**
(cambiando los *nameservers*), que es quien gestiona su DNS y por donde entra el túnel.

---

## 4. El viaje de una petición (cómo encaja TODO)

Cuando alguien abre `https://hello.proyecto-asir.xyz` desde su móvil, ocurre esto:

1. **Navegador → Cloudflare:** la petición llega a Cloudflare (porque el DNS del dominio apunta
   allí). Cloudflare pone el **HTTPS** de cara al usuario.
2. **Cloudflare → Túnel:** Cloudflare envía la petición por el **túnel cifrado** hasta tu
   `cloudflared`, que está dentro del clúster.
3. **cloudflared → Ingress-NGINX:** cloudflared se la pasa al **Ingress** (usando tu certificado
   Let's Encrypt en esa conexión interna).
4. **Ingress → Service:** el Ingress mira la URL (`hello.proyecto-asir.xyz`) y la manda al
   **Service** `hello`.
5. **Service → Pod:** el Service elige uno de los **pods** y le pasa la petición.
6. **Vuelta:** la respuesta hace el camino inverso hasta el navegador.

Por eso, en la página de prueba, el "Server name" es el **nombre del pod** que te atendió: estás
viendo el final del viaje. 🎯

```
Internet → Cloudflare (HTTPS) → Túnel → cloudflared → Ingress-NGINX → Service → Pod
```

---

## 5. Glosario rápido

- **VM:** ordenador virtual dentro de tu PC.
- **Contenedor:** caja con una app y sus dependencias.
- **Clúster:** conjunto de nodos (servidores) que trabajan como uno.
- **Control-plane / worker:** cerebro / obreros del clúster.
- **Pod:** lo que de verdad se ejecuta (contenedor[es]).
- **Deployment:** mantiene N copias de un pod vivas.
- **Service:** dirección interna fija que reparte entre pods.
- **Ingress:** puerta de entrada web según la URL.
- **MetalLB:** asigna IPs accesibles a los servicios.
- **cert-manager:** pide y renueva certificados HTTPS solo.
- **Let's Encrypt:** autoridad que emite certificados gratis.
- **Cloudflare Tunnel:** conexión segura del clúster a internet sin abrir puertos.
- **Helm:** instalador de componentes de Kubernetes.
- **kubectl:** la herramienta para dar órdenes al clúster.
- **GitOps:** desplegar automáticamente lo que diga el repositorio Git.

---

## 6. Estado actual y lo que viene

**Ya tienes (Fases 0–3):** repositorio + documentación, 3 VMs, clúster k3s de 3 nodos, red interna,
balanceador (MetalLB), entrada web (Ingress), HTTPS automático (cert-manager + Let's Encrypt) y
acceso externo seguro (Cloudflare Tunnel). **Una aplicación real, accesible desde internet con
candado válido.**

**Lo que falta:**
- **Fase 4 — La aplicación de verdad:** sustituir la app de prueba por una aplicación con varios
  servicios.
- **Fase 5 — CI/CD:** que cada `git push` construya y despliegue la app **sin tocar nada** a mano.
- **Fase 6 — Monitorización:** métricas, paneles (Grafana) y alertas (Prometheus + Alertmanager).
