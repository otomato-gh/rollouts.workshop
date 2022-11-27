# Our First Rollout

Rollouts replace the Deployments in our K8s cluster.

To deploy our very first version we will deploy a Rollout and a matching Service to access it.




---
## Deploy our first rollout
.exercise[
- Deploy the Rollout
  ```bash
  kubectl apply ~/rollouts.workshop/code/rollout.yml
  ```
- Deploy the Service
  ```bash
  kubectl apply ~/rollouts.workshop/code/service.yml
  ```
]
--



---
## Exploring Istio on K8s

 - Ok, that's where config is stored. But where are the processes?

```bash
kubectl get pod
```
 - Nothing here... Are they in kube-system?

```bash
kubectl get pod -n kube-system
```
 - Not here too!
---

## Exploring Istio on K8s

 - Let's look somewhere else

```bash
kubectl get ns
```
 - Hey, there's an *istio-system* namespace

```bash
kubectl get pod -n istio-system
```

- Now we're talking!

- But why so many?!

