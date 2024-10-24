# minikube
minikube status     # Display status
minikube service <service-name>     # Open a service
minikube service list               # Lists service URLs in local cluster
minikube profile list               # Lists all profiles

# kubectl
kubectl version         # Display versions

# debug
kubectl logs <pod-name>     # Logging
kubectl describe <resource-type> <resource-name>    # Describe
kubectl exec -it <pod-name> -- /bin/bash  # Execute a command in a container

# generic
kubectl api-resources                               # List supported API resources
kubectl get all                                     # List all resources
kubectl get <resource-type>                         # List
kubectl delete <resource-type> <resource-name>      # Delete
kubectl apply -f <file-path>
kubectl delete -f <file-path>
kubectl cluster-info

# node
kubectl get nodes       # List nodes

# pod
kubectl get pods                    # List pods
kubectl get pods -A                 # List pods across all namespaces
kubectl get pods -o wide            # List pods with more info
kubectl describe pod <pod-name>     # Describe a pod

# service
kubectl get services                        # List services
kubectl describe service <service-name>     # Describe a service

# deployment
kubectl get deployments    # List deployments
kubectl create deployment <deployment-name> --image=<image-name>    # Create

# replicaset
kubectl get replicasets

# secret
kubectl get secrets
kubectl describe secret <secret-name>

# namespace
kubectl get namespaces
kubectl create namespace <namespace-name>
