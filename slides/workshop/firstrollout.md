# Our First Rollout

Rollouts replace the Deployments in our K8s cluster.

To deploy our very first version we will deploy a Rollout and a matching Service to access it.




---
## Deploy our first rollout
.exercise[
- Deploy the Rollout
  ```bash
  kubectl apply -f ~/rollouts.workshop/code/rollout.yaml
  ```
- Deploy the Service
  ```bash
  kubectl apply -f ~/rollouts.workshop/code/service.yaml
  ```
]
--



---
## What did we roll out?

 - Let's look at rollout.yaml

```yaml
spec:
  replicas: 5
  strategy:
    canary:     # The strategy is Canary Deployment
      steps:
      - setWeight: 20 # We first send 20% to the canary
      - pause: {}     # We wait for a manual promotion
      - setWeight: 40 # Promote canary to 40%
      - pause: {duration: 10} # Wait 10 sec
      - setWeight: 60 # Promote canary to 60%
      - pause: {duration: 10}
      - setWeight: 80 # Promote canary to 80%
      - pause: {duration: 10} # Wait 10 sec
      # Finally canary replaces previous version
```

---

## Watching the Rollout

Initial creations of any Rollout will immediately scale up the replicas to 100% (skipping any canary upgrade steps, analysis, etc...) since there was no upgrade that occurred.

The Argo Rollouts **kubectl plugin** allows you to visualize the Rollout, its related resources (ReplicaSets, Pods, AnalysisRuns), and presents live state changes as they occur. To watch the rollout as it deploys, run the get rollout --watch command from plugin:

.exercise[
```bash
kubectl argo rollouts get rollout rollouts-demo --watch
 # or rather
kar get rollout rollouts-demo --watch
```
]

---

## Updating the Rollout

- Now let's update the Rollout and see the magic of the staged deployment in action:

.exercise[
  ```bash
  # Run in a new shell while "watch" is running
  kar set image rollouts-demo rollouts-demo=argoproj/rollouts-demo:yellow
  ```
]

- Go back to the first shell to watch the rollout progress

---
## Promoting the Rollout

We can see from the plugin output that the Rollout is in a paused state, and now has 1 of 5 replicas running the new version of the pod template, and 4 of 5 replicas running the old version. 

This equates to the 20% canary weight as defined by the `setWeight: 20` step.

