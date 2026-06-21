# Fase 2 — Clúster Kubernetes (k3s)

Clúster k3s de 3 nodos instalado sobre las VMs de la Fase 1.

## Topología

| Nodo | Rol | IP | Componente |
|------|-----|-----|-----------|
| `k3s-server` | control-plane | 192.168.56.10 | k3s server |
| `k3s-agent-1` | worker | 192.168.56.11 | k3s agent |
| `k3s-agent-2` | worker | 192.168.56.12 | k3s agent |

- **Versión:** k3s v1.35.5+k3s1 (Kubernetes 1.35)
- **Runtime de contenedores:** containerd
- **Red de pods (CNI):** Flannel sobre la interfaz Host-Only (`enp0s8`)

## Instalación del control-plane

```bash
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server \
  --node-ip 192.168.56.10 --advertise-address 192.168.56.10 \
  --flannel-iface enp0s8 --tls-san 192.168.56.10 \
  --write-kubeconfig-mode 644 --disable traefik --disable servicelb" sh -
```

Flags clave:
- `--node-ip` / `--advertise-address` → fuerzan el uso de la red interna Host-Only.
- `--flannel-iface enp0s8` → la red de pods va por la interfaz interna.
- `--tls-san 192.168.56.10` → certificado válido para el acceso remoto con kubectl.
- `--disable traefik --disable servicelb` → se desactivan los componentes por defecto;
  en la Fase 3 se instalan MetalLB + Ingress-NGINX.

## Unión de los workers

En cada worker (cambiando `--node-ip` a `.11` o `.12`):

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://192.168.56.10:6443 \
  K3S_TOKEN="<token-del-servidor>" \
  INSTALL_K3S_EXEC="--node-ip 192.168.56.11 --flannel-iface enp0s8" sh -
```

El token se obtiene en el control-plane:
`sudo cat /var/lib/rancher/k3s/server/node-token`

## Acceso desde el equipo anfitrión (Windows)

1. `kubectl` instalado en Windows.
2. `kubeconfig` copiado por scp: `scp k3s-server:/etc/rancher/k3s/k3s.yaml ~/.kube/config`
3. Editar el campo `server:` para que apunte a `https://192.168.56.10:6443`.
4. `kubectl get nodes` → los 3 nodos en estado `Ready`.