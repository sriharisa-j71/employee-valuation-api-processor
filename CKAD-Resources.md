# CKAD (Certified Kubernetes Application Developer) - Study Resources

## About CKAD

The Certified Kubernetes Application Developer (CKAD) exam certifies your ability to design, build, configure, and deploy cloud-native applications for Kubernetes.

- **Exam Duration**: 2 hours
- **Passing Score**: 66%
- **Format**: Performance-based, hands-on command-line tasks
- **Access**: Open book - Official Kubernetes documentation allowed

## Official Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [CKAD Certification Page](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/)
- [CNCF CKAD Information](https://www.cncf.io/training/certification/ckad/)
- [CKAD Curriculum (PDF)](https://github.com/cncf/curriculum/blob/master/CKAD_Curriculum_v1.31.pdf)
- [CKAD Curriculum Path (PDF)](https://training.linuxfoundation.org/wp-content/uploads/2024/10/CKAD_CurriculumPath.pdf)

---

## Domains & Competencies Breakdown

### 1. Application Design and Build (20%)

#### Container Images
- [Images - Kubernetes Docs](https://kubernetes.io/docs/concepts/containers/images/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Building Container Images](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)

#### Workload Resources
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
- [DaemonSets](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [ReplicaSets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)

#### Multi-Container Patterns
- [Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
- [Sidecar Containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)
- [Ephemeral Containers](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/)
- [Container Lifecycle Hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/)

#### Storage
- [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Persistent Volume Claims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- [Ephemeral Volumes](https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/)

---

### 2. Application Deployment (20%)

#### Deployment Strategies
- [Deployments - Rolling Updates](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
- [Rollback Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment)
- [Blue/Green Deployment Strategy](https://kubernetes.io/blog/2018/04/30/zero-downtime-deployment-kubernetes-jenkins/)
- [Canary Deployments](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#canary-deployments)

#### Package Management
- [Helm - Package Manager](https://helm.sh/docs/)
- [Helm Charts](https://helm.sh/docs/topics/charts/)
- [Helm Values Files](https://helm.sh/docs/chart_template_guide/values_files/)
- [Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- [Managing Resources with Kubectl](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/)

#### Rollout Management
- [Deployment Rollout Status](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#checking-rollout-history-of-a-deployment)
- [Pausing and Resuming Rollouts](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#pausing-and-resuming-a-deployment)

---

### 3. Application Observability and Maintenance (15%)

#### Probes and Health Checks
- [Liveness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-liveness-command)
- [Readiness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes)
- [Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-startup-probes)
- [Container Probes](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)

#### Monitoring and Logging
- [Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- [kubectl logs Command](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
- [kubectl top Command](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#top)
- [Monitoring Resources](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-usage-monitoring/)
- [Events](https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/)

#### Debugging and Troubleshooting
- [Debugging Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Debugging Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
- [Troubleshooting Applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
- [Debugging Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [kubectl debug Command](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container)

#### API Deprecations
- [Deprecated API Migration Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/)
- [API Versioning](https://kubernetes.io/docs/reference/using-api/)

---

### 4. Application Environment, Configuration, and Security (25%)

#### Configuration Management
- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Configure Pods with ConfigMaps](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Distribute Credentials Securely](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)

#### Resource Management
- [Resource Requests and Limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/)
- [Pod Priority and Preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/)

#### Security
- [SecurityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
- [Seccomp Profiles](https://kubernetes.io/docs/tutorials/security/seccomp/)
- [AppArmor](https://kubernetes.io/docs/tutorials/security/apparmor/)
- [ServiceAccounts](https://kubernetes.io/docs/concepts/security/service-accounts/)
- [Managing Service Accounts](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

#### RBAC and Authorization
- [RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Role and ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole)
- [RoleBinding and ClusterRoleBinding](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#rolebinding-and-clusterrolebinding)
- [Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

#### Custom Resources
- [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- [CustomResourceDefinitions (CRDs)](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
- [Operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)

---

### 5. Services and Networking (20%)

#### Services
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Service Types (ClusterIP, NodePort, LoadBalancer)](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)
- [Headless Services](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)
- [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)
- [Connecting Applications with Services](https://kubernetes.io/docs/tutorials/services/connect-applications-service/)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

#### Ingress
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
- [Set up Ingress](https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/)

#### Network Policies
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Declare Network Policy](https://kubernetes.io/docs/tasks/administer-cluster/declare-network-policy/)
- [Network Policy Recipes](https://github.com/ahmetb/kubernetes-network-policy-recipes)

#### Troubleshooting Networking
- [Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
- [Debugging DNS Resolution](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/)

---

## Additional Learning Resources

### Practice Environments
- [Killer.sh CKAD Simulator](https://killer.sh/ckad) - Realistic exam simulator (included with exam registration)
- [KodeKloud CKAD Course](https://kodekloud.com/courses/certified-kubernetes-application-developer-ckad/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)
- [Minikube](https://minikube.sigs.k8s.io/docs/) - Local Kubernetes setup

### Courses and Training
- [Linux Foundation LFD259: Kubernetes for Developers](https://training.linuxfoundation.org/training/kubernetes-for-developers/)
- [Udemy - CKAD Course by Mumshad Mannambeth](https://www.udemy.com/course/certified-kubernetes-application-developer/)
- [A Cloud Guru - CKAD Course](https://acloudguru.com/course/certified-kubernetes-application-developer-ckad)

### Books
- "Kubernetes Up & Running" by Kelsey Hightower
- "Cloud Native DevOps with Kubernetes" by John Arundel & Justin Domingus
- "Kubernetes Patterns" by Bilgin Ibryam & Roland Huß

### Practice Repositories
- [CKAD Exercises - GitHub](https://github.com/dgkanatsios/CKAD-exercises)
- [CKAD Practice Questions](https://github.com/lucassha/CKAD-resources)

### kubectl Resources
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [kubectl Quick Reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [kubectl Commands Reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)
- [kubectl Conventions](https://kubernetes.io/docs/reference/kubectl/conventions/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)

### Community Resources
- [Kubernetes Slack](https://slack.k8s.io/)
- [Kubernetes Forum](https://discuss.kubernetes.io/)
- [CNCF YouTube Channel](https://www.youtube.com/c/cloudnativefdn)

---

## Exam Tips

1. **Bookmark Important Pages**: Create bookmarks for frequently used Kubernetes documentation pages before the exam
2. **Use Imperative Commands**: Master `kubectl create`, `kubectl run`, `kubectl expose` with `--dry-run=client -o yaml`
3. **Set Up Aliases**: Configure `alias k=kubectl` and enable bash autocompletion
4. **Practice Time Management**: Allocate time based on question weights; skip difficult questions and return later
5. **Validate Your Work**: Always verify your resources are running correctly before moving to the next question
6. **Context Switching**: Remember to switch context/namespace as specified in each question
7. **Use `kubectl explain`**: Quickly reference resource specs during the exam (`kubectl explain pod.spec.containers --recursive`)
8. **Master YAML formatting**: Use `--dry-run=client -o yaml` extensively to generate templates
9. **Understand question scope**: Some questions may not require creating resources, just inspecting
10. **Label everything**: Good labeling helps with selection and management
11. **Practice with vim/nano**: Get comfortable with the terminal editor you'll use
12. **Use `kubectl api-resources`**: Quickly find resource short names and API groups

---

## Important kubectl Commands to Master

```bash
# Imperative commands with dry-run
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deployment.yaml
kubectl expose deployment nginx --port=80 --target-port=8080 --dry-run=client -o yaml > service.yaml
kubectl create configmap my-config --from-literal=key1=value1 --dry-run=client -o yaml > configmap.yaml
kubectl create secret generic my-secret --from-literal=password=secret123 --dry-run=client -o yaml > secret.yaml

# Quick edits
kubectl edit deployment nginx
kubectl set image deployment/nginx nginx=nginx:1.18

# Scaling
kubectl scale deployment nginx --replicas=5
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80

# Troubleshooting
kubectl logs pod-name
kubectl logs pod-name -c container-name
kubectl logs pod-name --previous  # logs from previous container instance
kubectl logs -f pod-name  # follow logs
kubectl describe pod pod-name
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get events --sort-by=.lastTimestamp

# Debugging with ephemeral containers (NEW - important for exam)
kubectl debug pod-name -it --image=busybox
kubectl debug pod-name -it --image=busybox --target=container-name
kubectl debug node/node-name -it --image=busybox

# Explain resources (CRITICAL for exam when you forget YAML structure)
kubectl explain pod.spec.containers --recursive
kubectl explain deployment.spec.strategy
kubectl explain service.spec
kubectl explain pod.spec.securityContext

# Rollout management
kubectl rollout status deployment/nginx
kubectl rollout history deployment/nginx
kubectl rollout history deployment/nginx --revision=2
kubectl rollout undo deployment/nginx
kubectl rollout undo deployment/nginx --to-revision=2
kubectl rollout restart deployment/nginx
kubectl rollout pause deployment/nginx
kubectl rollout resume deployment/nginx

# JSON path queries (useful for complex filtering)
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'

# Port forwarding (important for testing services)
kubectl port-forward pod/nginx 8080:80
kubectl port-forward service/nginx 8080:80
kubectl port-forward deployment/nginx 8080:80

# Execute commands in containers
kubectl exec -it pod-name -- /bin/bash
kubectl exec -it pod-name -c container-name -- /bin/sh
kubectl exec pod-name -- env
kubectl exec pod-name -- ls -la /app

# Copy files to/from containers
kubectl cp pod-name:/path/to/file ./local-file
kubectl cp ./local-file pod-name:/path/to/file
kubectl cp pod-name:/path/to/file ./local-file -c container-name

# Context and namespace
kubectl config get-contexts
kubectl config use-context context-name
kubectl config set-context --current --namespace=namespace-name
kubectl config view

# Force delete stuck resources
kubectl delete pod pod-name --grace-period=0 --force
kubectl delete pod pod-name --now

# Get all resources in namespace
kubectl get all -n namespace-name
kubectl api-resources --verbs=list --namespaced -o name

# Patch resources
kubectl patch deployment nginx -p '{"spec":{"replicas":3}}'
kubectl patch pod nginx -p '{"spec":{"containers":[{"name":"nginx","image":"nginx:1.19"}]}}'

# Create resource and expose in one go
kubectl run nginx --image=nginx --port=80 --expose

# Watch resources
kubectl get pods -w
kubectl get pods -w -o wide

# Show labels and label selection
kubectl get pods --show-labels
kubectl get pods -L app,tier,version
kubectl get pods -l app=nginx
kubectl get pods -l 'env in (prod,staging)'

# Field selector (faster than grep)
kubectl get pods --field-selector status.phase=Running
kubectl get pods --field-selector metadata.namespace=default,status.phase=Running
kubectl get events --field-selector involvedObject.kind=Pod

# Resource usage
kubectl top nodes
kubectl top pods
kubectl top pods --containers
kubectl top pods -n namespace-name --sort-by=memory

# Service and endpoint inspection
kubectl get endpoints
kubectl get svc -o wide

# RBAC inspection
kubectl auth can-i create deployments
kubectl auth can-i delete pods --as=user@example.com
kubectl auth can-i '*' '*' --all-namespaces
```

---

## Key Changes in This Update

### Fixed Issues
- **Updated CKAD Curriculum PDF link**: Changed from generic GitHub repository link to direct PDF link (`https://github.com/cncf/curriculum/blob/master/CKAD_Curriculum_v1.31.pdf`)
- **Added CKAD Curriculum Path PDF**: New official resource from Linux Foundation (`https://training.linuxfoundation.org/wp-content/uploads/2024/10/CKAD_CurriculumPath.pdf`)
- **Removed outdated content**: Eliminated 2015 blog link for multi-container patterns that is no longer maintained

### New Content Added

#### Application Design and Build
- **Ephemeral Containers**: Modern debugging technique for troubleshooting running pods
- **Container Lifecycle Hooks**: PostStart and PreStop hooks for container management

#### Application Deployment
- **Helm Values Files**: Essential for managing Helm chart configurations

#### Application Observability and Maintenance
- **kubectl debug Command**: Critical new debugging tool using ephemeral containers

#### Application Environment, Configuration, and Security
- **Pod Security Admission**: Replaced deprecated PodSecurityPolicy with modern admission controller
- **Seccomp Profiles**: Secure computing mode for restricting system calls
- **AppArmor**: Mandatory access control framework for application security

#### Services and Networking
- **Headless Services**: Services without cluster IP for direct pod access
- **EndpointSlices**: Scalable alternative to Endpoints for large clusters

#### kubectl Resources
- **kubectl Conventions**: Best practices for using kubectl
- **Kubernetes API Reference**: Complete API documentation

### Enhanced Sections

#### Exam Tips (6 new tips added)
- Using `kubectl explain` for quick reference
- Mastering YAML generation with dry-run
- Understanding question scope
- Importance of labeling
- Terminal editor proficiency
- Finding resource short names with `kubectl api-resources`

#### kubectl Commands (Significant expansion)
- **Imperative commands**: Added ConfigMap and Secret creation
- **Debugging**: Ephemeral container debugging for pods and nodes
- **Resource inspection**: kubectl explain with recursive flag
- **Rollout management**: Complete rollout command suite
- **JSONPath queries**: Advanced filtering and formatting
- **Port forwarding**: Testing services locally
- **Container operations**: Exec and cp commands
- **Resource management**: Patching, force deletion, watching
- **Label and field selectors**: Efficient resource filtering
- **RBAC inspection**: Authorization checking commands

### Documentation Quality Improvements
- All links verified to point to official Kubernetes documentation
- Maintained consistent markdown formatting
- Preserved existing helpful sections (Practice Environments, Courses, Books, etc.)
- Added modern Kubernetes 1.31 features and best practices

---

Good luck with your CKAD certification! 🚀
