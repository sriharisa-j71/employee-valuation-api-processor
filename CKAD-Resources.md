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
- [CKAD Curriculum (PDF)](https://github.com/cncf/curriculum)

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
- [Multi-Container Pod Patterns](https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns/)

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

---

## Important kubectl Commands to Master

```bash
# Imperative commands with dry-run
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deployment.yaml
kubectl expose deployment nginx --port=80 --target-port=8080 --dry-run=client -o yaml > service.yaml

# Quick edits
kubectl edit deployment nginx
kubectl set image deployment/nginx nginx=nginx:1.18

# Scaling
kubectl scale deployment nginx --replicas=5

# Troubleshooting
kubectl logs pod-name
kubectl logs pod-name -c container-name
kubectl describe pod pod-name
kubectl get events --sort-by=.metadata.creationTimestamp

# Context and namespace
kubectl config get-contexts
kubectl config use-context context-name
kubectl config set-context --current --namespace=namespace-name
```

---

Good luck with your CKAD certification! 🚀
