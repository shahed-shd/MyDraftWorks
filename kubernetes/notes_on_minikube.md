## Prerequisite
- **Docker**: Installed and running (for building images). Verify: `docker --version`.
- **kubectl**: Minikube bundles it, no separate install needed.
- **Hypervisor**: For Minikube's VM (Docker Desktop works on macOS/Windows; VirtualBox or KVM2 on Linux).

## Installation
- install `minikube`:
  </br>
  On Mac:
  ```bash
  brew install minikube
  ```
- Verify installation:
  ```bash
  minikube version
  ```

## Start Minikube Cluster
```bash
minikube start --driver=docker
```
N.B.: Use `--driver=virtualbox` on Linux if Docker isn't a hypervisor

- **What happens**: Downloads Kubernetes (latest stable) if not downloaded, starts a single-node cluster.
- **Verify**: `kubectl get nodes` (shows `minikube` as `Ready`).
- **Dashboard** (optional): `minikube dashboard` (opens browser UI).


## Build and Load Docker Image into Minikube
- ### Point docker CLI to minikubes own docker daemon:
  
  Minikube uses its own Docker daemon. To point docker client to minikube's docker daemon:
    
    ```bash
    eval $(minikube docker-env)
    ```
  Or, to a specific profile:

  - To get a list of all Minikube clusters (which Minikube calls *profiles*):
    ```bash
    minikube profile list
    ```
  - then
    ```bash
    eval $(minikube -p <profile-name> docker-env)
    ```

  **What happens:** Points docker client to minikube's docker daemon by setting environment variables like `DOCKER_HOST`, `DOCKER_CERT_PATH` etc. Affects the current terminal session. If we open a new terminal, default to point to the system's (host) Docker daemon.
  </br>
  Also, can be unset in current terminal by:
  ```bash
  eval $(minikube docker-env --unset)
  ```

- ### Build the image inside Minikube:
  ```bash
  docker build -t <image-name:tag> -f <docker-file-path> <context-path>
  ```
  Example:
  ```bash
  docker build -t hello-service -f cicd/Dockerfile .
  ```
  **Verify:** `docker images` wil show the image.

## Create Kubernetes Manifests
Create YAML files in the project root for
- *Deployment* (manages Pods)
- *Service* (exposes the Pod).

Sample `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-deployment
  labels:
    app: hello-service
spec:
  replicas: 1  # Scale as needed
  selector:
    matchLabels:
      app: hello-service
  template:
    metadata:
      labels:
        app: hello-service
    spec:
      containers:
      - name: hello-container
        image: hello-service    # The local image
        imagePullPolicy: Never  # `Never` skips remote pulls (ideal for local/Minikube to use pre-loaded images); alternatives: `IfNotPresent` (default) or `Always`.
        ports:
        - containerPort: 9001   # Application (Spring Boot, FastAPI etc) port
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"  # 0.25 cores
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /actuator/health  # Use Actuator health (or /hello)
            port: 9001
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /actuator/health
            port: 9001
          initialDelaySeconds: 30
          periodSeconds: 10
```

Sample `service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-service
spec:
  type: ClusterIP  # Internal; change to NodePort for quick external access
  selector:
    app: hello-service
  ports:
  - port: 9001
    targetPort: 9001
    protocol: TCP
```

## Deploy to Kubernetes
From the root:
```bash
kubectl apply -f <file path to deployment.yaml>
```
**What happens**: Creates *Deployment* (Pod starts).
</br>
**Verify**:
  - `kubectl get deployments` (shows list of deployments)
  - `kubectl describe deployment <deployment-name>` (shows details)
  - `kubectl logs deployment/<deployment-name>` (shows pod logs, like applicaion start-up logs)
  - `kubectl get pods` (shows list of pods)

Then
```bash
kubectl apply -f <file path to service.yaml>
```
**What happens**: Creates *Service*.
</br>
**Verify**:
  - `kubectl get services` (shows list of services)
  - `kubectl describe service <service-name>` (shows details)

## Access the Application
- **Port-Forward** (easiest for local testing):
  ```bash
  kubectl port-forward service/<service-name> <local-port>:<remote-hport>
  ```
- Or, NodePort for direct Minikube IP:
  - Update `service.yaml` to `type: NodePort` and re-apply by `kubectl apply -f <file path to service.yaml>`
  - Get URL by `minikube service <service-name> --url`

## Cleanup
- Stop port-forward: `Ctrl+C`.
- Delete resources: `kubectl delete -f <file-path-to-deployment.yaml> -f <file-path-to-service.yaml>`
- Stop Minikube: `minikube stop`
- Delete cluster: `minikube delete` (full reset).