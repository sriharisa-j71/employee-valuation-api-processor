# CKAD 4-Day Intensive Study Plan

## Overview

This intensive 4-day study plan is designed for individuals who have some Kubernetes experience and need to prepare quickly for the CKAD exam. Each day focuses on specific exam domains with hands-on practice.

**Prerequisites:**
- Basic Kubernetes knowledge
- Access to a Kubernetes cluster (Minikube, kind, or cloud-based)
- kubectl installed and configured
- 6-8 hours available per day

**Daily Structure:**
- Morning (3 hours): Theory and Documentation Review
- Afternoon (2-3 hours): Hands-on Practice
- Evening (1-2 hours): Mock Questions and Review

---

## Day 1: Application Design and Build + Deployment

**Focus Areas:**
- Application Design and Build (20%)
- Application Deployment (20%)

### Morning Session (3 hours)

#### 1. Container Images and Pod Design (60 min)
- [ ] Review [Images documentation](https://kubernetes.io/docs/concepts/containers/images/)
- [ ] Study [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [ ] Learn multi-container patterns: [Init Containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) and [Sidecar](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)
- [ ] Review pod lifecycle and restart policies

**Practice Tasks:**
```bash
# Create a simple pod
kubectl run nginx --image=nginx

# Create pod with resource limits
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml
# Edit to add resource requests/limits

# Multi-container pod with sidecar
# Create YAML with multiple containers
```

#### 2. Workload Resources (90 min)
- [ ] Study [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [ ] Review [Jobs and CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [ ] Learn [DaemonSets](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
- [ ] Review [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)

**Key Commands:**
```bash
kubectl create deployment nginx --image=nginx --replicas=3
kubectl create job hello --image=busybox -- echo "Hello World"
kubectl create cronjob hello --image=busybox --schedule="*/1 * * * *" -- echo "Hello"
```

#### 3. Storage (30 min)
- [ ] Review [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
- [ ] Study [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [ ] Learn about emptyDir, hostPath, and PVCs

### Afternoon Practice (2-3 hours)

**Hands-on Exercises:**

1. **Pod Creation (30 min)**
   - [ ] Create a pod with specific image and labels
   - [ ] Create a pod with environment variables
   - [ ] Create a pod with resource limits
   - [ ] Create a multi-container pod with init container

2. **Deployment Management (45 min)**
   - [ ] Create a deployment with 3 replicas
   - [ ] Update deployment image
   - [ ] Scale deployment up and down
   - [ ] Perform rolling update
   - [ ] Rollback a deployment
   - [ ] Check rollout history

3. **Jobs and CronJobs (30 min)**
   - [ ] Create a Job that runs to completion
   - [ ] Create a Job with parallelism
   - [ ] Create a CronJob with specific schedule
   - [ ] List and delete completed jobs

4. **Storage (45 min)**
   - [ ] Create a pod with emptyDir volume
   - [ ] Create a PersistentVolumeClaim
   - [ ] Mount PVC in a pod
   - [ ] Create pod with hostPath volume

### Evening Review (1-2 hours)

- [ ] Complete 10-15 practice questions on Day 1 topics
- [ ] Review mistakes and understand why
- [ ] Create personal notes/cheat sheet
- [ ] Watch [CKAD Deployment video tutorial](https://www.youtube.com/results?search_query=ckad+deployment)

**Recommended Practice:**
- KodeKloud: Pods and Deployments sections
- CKAD Exercises: Application Design questions

---

## Day 2: Configuration, Security, and Environment

**Focus Areas:**
- Application Environment, Configuration, and Security (25%)

### Morning Session (3 hours)

#### 1. ConfigMaps and Secrets (60 min)
- [ ] Study [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [ ] Review [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [ ] Learn to inject as environment variables and volumes

**Key Commands:**
```bash
# ConfigMap creation
kubectl create configmap my-config --from-literal=key1=value1 --from-literal=key2=value2
kubectl create configmap my-config --from-file=config.txt

# Secret creation
kubectl create secret generic my-secret --from-literal=password=secretpass
kubectl create secret docker-registry regcred --docker-server=<server> --docker-username=<user>
```

#### 2. Resource Management (45 min)
- [ ] Review [Resource Requests and Limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [ ] Study [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [ ] Learn [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/)

#### 3. Security Contexts and ServiceAccounts (75 min)
- [ ] Study [SecurityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [ ] Review [ServiceAccounts](https://kubernetes.io/docs/concepts/security/service-accounts/)
- [ ] Learn about [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [ ] Study [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

### Afternoon Practice (2-3 hours)

**Hands-on Exercises:**

1. **ConfigMaps (30 min)**
   - [ ] Create ConfigMap from literals
   - [ ] Create ConfigMap from file
   - [ ] Mount ConfigMap as environment variables
   - [ ] Mount ConfigMap as volume
   - [ ] Update pod to use ConfigMap

2. **Secrets (30 min)**
   - [ ] Create generic secret
   - [ ] Create docker-registry secret
   - [ ] Use secret as environment variable
   - [ ] Mount secret as volume
   - [ ] Create pod with imagePullSecret

3. **Resource Management (30 min)**
   - [ ] Create pod with resource requests and limits
   - [ ] Create ResourceQuota for namespace
   - [ ] Create LimitRange for namespace
   - [ ] Test quota enforcement

4. **Security (60 min)**
   - [ ] Create pod with SecurityContext (runAsUser, fsGroup)
   - [ ] Create pod with read-only root filesystem
   - [ ] Create ServiceAccount
   - [ ] Assign ServiceAccount to pod
   - [ ] Create Role and RoleBinding
   - [ ] Create NetworkPolicy to restrict traffic

### Evening Review (1-2 hours)

- [ ] Complete 15-20 practice questions on Day 2 topics
- [ ] Review ConfigMap vs Secret usage patterns
- [ ] Practice RBAC verb and resource combinations
- [ ] Update personal cheat sheet

**Security Practice Focus:**
- Practice writing NetworkPolicy YAML from scratch
- Understand pod-to-pod, namespace-to-namespace restrictions
- Review common SecurityContext settings

---

## Day 3: Observability, Services, and Networking

**Focus Areas:**
- Application Observability and Maintenance (15%)
- Services and Networking (20%)

### Morning Session (3 hours)

#### 1. Probes and Health Checks (60 min)
- [ ] Study [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [ ] Understand different probe types: httpGet, tcpSocket, exec
- [ ] Learn about probe timing parameters

**Probe YAML Example:**
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 3
  periodSeconds: 3

readinessProbe:
  tcpSocket:
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

#### 2. Monitoring and Debugging (60 min)
- [ ] Master [kubectl logs](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
- [ ] Learn [kubectl top](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#top)
- [ ] Study [Debugging Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [ ] Review events and describe commands

**Essential Debug Commands:**
```bash
kubectl logs pod-name
kubectl logs pod-name -c container-name --previous
kubectl describe pod pod-name
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl top pod
kubectl top node
```

#### 3. Services and Networking (60 min)
- [ ] Study [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [ ] Review service types: ClusterIP, NodePort, LoadBalancer
- [ ] Learn [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [ ] Study [DNS for Services](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

**Service Commands:**
```bash
kubectl expose pod nginx --port=80 --target-port=80
kubectl expose deployment webapp --type=NodePort --port=8080
kubectl create service clusterip my-svc --tcp=80:8080
```

### Afternoon Practice (2-3 hours)

**Hands-on Exercises:**

1. **Probes (45 min)**
   - [ ] Create pod with liveness probe (httpGet)
   - [ ] Create pod with readiness probe (tcpSocket)
   - [ ] Create pod with startup probe
   - [ ] Create pod with exec probe
   - [ ] Test probe failure scenarios

2. **Monitoring and Troubleshooting (45 min)**
   - [ ] View logs from running pod
   - [ ] View logs from multi-container pod
   - [ ] View previous container logs
   - [ ] Use kubectl describe to debug failed pod
   - [ ] Check events for troubleshooting
   - [ ] Use kubectl top to view resource usage

3. **Services (45 min)**
   - [ ] Create ClusterIP service for deployment
   - [ ] Create NodePort service
   - [ ] Test service connectivity with busybox
   - [ ] Verify service endpoints
   - [ ] Create headless service
   - [ ] Test DNS resolution

4. **Ingress (30 min)**
   - [ ] Create Ingress resource
   - [ ] Configure host-based routing
   - [ ] Configure path-based routing
   - [ ] Test Ingress access

### Evening Review (1-2 hours)

- [ ] Complete 15-20 practice questions on Day 3 topics
- [ ] Practice debugging scenarios
- [ ] Review service selector and label matching
- [ ] Update cheat sheet with debug commands

**Focus Areas:**
- Speed up log viewing and pod debugging
- Practice creating services imperatively
- Understand service DNS naming convention

---

## Day 4: Full Mock Exams and Review

**Focus:** Timed practice and weak area improvement

### Morning Session (3 hours)

#### First Mock Exam (2 hours)
- [ ] Take a full-length timed mock exam (Killer.sh or similar)
- [ ] Simulate real exam conditions
- [ ] Switch contexts and namespaces for each question
- [ ] Practice time management
- [ ] Don't look up answers - try to solve everything yourself

**After Mock Exam (1 hour):**
- [ ] Review all questions
- [ ] Identify weak areas
- [ ] Note questions you couldn't complete
- [ ] Review correct solutions
- [ ] Update notes with mistakes

### Afternoon Practice (2-3 hours)

#### Targeted Practice Based on Weak Areas

**If weak in Deployments:**
- [ ] Practice rollout, rollback, and update strategies
- [ ] Create deployments with different strategies
- [ ] Practice scaling operations

**If weak in ConfigMaps/Secrets:**
- [ ] Create multiple ConfigMaps with different methods
- [ ] Practice mounting as both env vars and volumes
- [ ] Combine multiple ConfigMaps in single pod

**If weak in Networking:**
- [ ] Create various service types
- [ ] Practice Ingress configuration
- [ ] Create and test NetworkPolicies

**If weak in Security:**
- [ ] Practice SecurityContext configurations
- [ ] Create ServiceAccounts and RBAC resources
- [ ] Test pod-level and container-level security

#### Speed Practice (30 min)
Focus on speed for common tasks:
- [ ] Create pod with specific requirements (30 seconds)
- [ ] Create deployment and expose as service (1 minute)
- [ ] Create ConfigMap and mount in pod (1 minute)
- [ ] Debug failed pod (30 seconds)

### Evening Session (2 hours)

#### Second Mock Exam (2 hours)
- [ ] Take another full-length mock exam
- [ ] Apply lessons learned from first mock
- [ ] Focus on time management
- [ ] Validate all answers before moving on

**After Second Mock:**
- [ ] Review performance
- [ ] Compare scores with first mock
- [ ] Identify any remaining weak areas

### Final Preparation (30-60 min)

#### Create Your Exam Day Cheat Sheet
Essential commands and patterns you'll use:

```bash
# Aliases
alias k=kubectl
alias kn='kubectl config set-context --current --namespace'

# Quick pod creation
kubectl run NAME --image=IMAGE --dry-run=client -o yaml > pod.yaml

# Quick deployment
kubectl create deployment NAME --image=IMAGE --replicas=N --dry-run=client -o yaml > deploy.yaml

# Expose service
kubectl expose deployment NAME --port=PORT --target-port=PORT --type=TYPE

# ConfigMap/Secret
kubectl create configmap NAME --from-literal=key=value
kubectl create secret generic NAME --from-literal=key=value

# Resource management
kubectl set resources deployment NAME --limits=cpu=200m,memory=512Mi --requests=cpu=100m,memory=256Mi

# Rollout
kubectl rollout status deployment NAME
kubectl rollout history deployment NAME
kubectl rollout undo deployment NAME

# Debugging
kubectl logs POD [-c CONTAINER]
kubectl describe pod POD
kubectl get events --sort-by=.metadata.creationTimestamp

# Context switching
kubectl config use-context CONTEXT
kubectl config set-context --current --namespace=NAMESPACE
```

#### Review Checklist
- [ ] Common YAML patterns memorized
- [ ] Imperative commands muscle memory
- [ ] Know where to find docs quickly
- [ ] Confident with Vim basics
- [ ] Understand time management strategy
- [ ] Know how to validate answers quickly

---

## Day 5 (Exam Day)

### Before the Exam (1-2 hours before)

**Don't:**
- ❌ Cram new information
- ❌ Take a practice exam
- ❌ Study complex topics
- ❌ Stress or panic

**Do:**
- ✅ Review your personal cheat sheet briefly
- ✅ Review common mistakes to avoid
- ✅ Get some light exercise or fresh air
- ✅ Eat a good meal
- ✅ Stay hydrated
- ✅ Relax and trust your preparation

### During Exam Setup (15 minutes)

**System Check:**
- [ ] Test webcam and microphone
- [ ] Close all unnecessary applications
- [ ] Clear desk area (check proctor requirements)
- [ ] Have ID ready

**Browser Setup:**
- [ ] Bookmark essential Kubernetes doc pages
  - kubectl cheat sheet
  - API reference
  - Common workload pages (pods, deployments, services)
- [ ] Test copy-paste functionality

**Terminal Setup:**
- [ ] Set up kubectl alias: `alias k=kubectl`
- [ ] Enable autocompletion: `source <(kubectl completion bash)`
- [ ] Configure Vim if needed

### During the Exam (2 hours)

**Strategy:**

**First 5 minutes:**
- [ ] Scan all questions quickly
- [ ] Note easy vs difficult questions
- [ ] Identify high-value questions

**First Pass (60-70 minutes):**
- [ ] Complete all easy/medium questions
- [ ] Flag difficult questions
- [ ] Verify each answer before moving on

**Second Pass (30-40 minutes):**
- [ ] Tackle flagged difficult questions
- [ ] Start with highest point value

**Final Review (10-20 minutes):**
- [ ] Review flagged questions
- [ ] Double-check context/namespace for each question
- [ ] Verify critical resources are running
- [ ] Fix any obvious errors

**Remember:**
- Switch context/namespace FIRST for each question
- Read question requirements carefully
- Validate your work (kubectl get, describe, logs)
- Don't spend too long on any single question
- Stay calm and confident

---

## Additional Resources for 4-Day Plan

### Day 1 Resources
- [CKAD Exercises - Pods and Deployments](https://github.com/dgkanatsios/CKAD-exercises#core-concepts)
- KodeKloud: Core Concepts and Configuration sections

### Day 2 Resources
- [CKAD Exercises - ConfigMaps and Secrets](https://github.com/dgkanatsios/CKAD-exercises#configuration)
- KodeKloud: Security section

### Day 3 Resources
- [CKAD Exercises - Services](https://github.com/dgkanatsios/CKAD-exercises#services)
- [Network Policy Recipes](https://github.com/ahmetb/kubernetes-network-policy-recipes)

### Day 4 Resources
- [Killer.sh CKAD Simulator](https://killer.sh/ckad)
- [KodeKloud Mock Exams](https://kodekloud.com/courses/certified-kubernetes-application-developer-ckad/)

---

## Daily Time Summary

| Day | Morning | Afternoon | Evening | Total |
|-----|---------|-----------|---------|-------|
| 1   | 3h      | 2.5h      | 1.5h    | 7h    |
| 2   | 3h      | 2.5h      | 1.5h    | 7h    |
| 3   | 3h      | 2.5h      | 1.5h    | 7h    |
| 4   | 3h      | 2.5h      | 2h      | 7.5h  |

**Total Study Time: ~29 hours**

---

## Success Tips

1. **Consistency:** Follow the schedule strictly
2. **Hands-on First:** Prioritize practice over theory
3. **Speed Matters:** Practice typing commands quickly
4. **Validate Everything:** Always check your work
5. **Learn from Mistakes:** Review every error carefully
6. **Stay Calm:** Confidence comes from preparation

---

## After Completing the Plan

**If you have more time:**
- Take additional mock exams
- Practice weak areas identified in mocks
- Review Kubernetes documentation structure
- Join study groups or forums

**Final 24 Hours:**
- Light review only
- No new topics
- Rest well
- Stay confident

---

**You're ready! Trust your preparation and go ace that CKAD exam! 🚀**
