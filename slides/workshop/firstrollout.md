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

- We can see from the plugin output that the Rollout is in a paused state, and now has 1 of 5 replicas running the new version of the pod template, and 4 of 5 replicas running the old version. 

- This equates to the 20% canary weight as defined by the `setWeight: 20` step.

- When a Rollout reaches a pause step with no duration, it will remain in a paused state indefinitely until it is resumed/promoted. To manually promote a rollout to the next step, run the promote command of the plugin:

.exercise[
  ```bash
  kar promote rollouts-demo
  ```
]

- Watch the Rollout as it proceeds to execute the remaining steps.

---

## Aborting a Rollout

- Sometimes a canary doesn't satisfy our quality requirements and we decide to abort it.

- Let's see how.

- First - let's deploy a new version:

.exercise[
  ```bash
  kar set image rollouts-demo rollouts-demo=argoproj/rollouts-demo:red
  ```
]

---

## Aborting the Rollout

- Watch the Rollout reach the paused state and roll back to the previous stable:

.exercise[
  ```bash
  kar abort rollouts-demo
  ```
]

- When a rollout is aborted, it will scale up the "stable" version of the ReplicaSet (in this case the `yellow` image), and scale down any other versions. Although the stable version of the ReplicaSet may be running and is healthy, the overall rollout is still considered Degraded, since the desired version (the red image) is not the version which is actually running.

---

## Going Back to Healthy

- In order to make Rollout considered `Healthy` again and not `Degraded`, it is necessary to change the desired state back to the previous, stable version. This typically involves running `kubectl apply` against the previous Rollout spec. In our case, we can simply re-run the set image command using the previous, "yellow" image.

.exercise[
```bash
kar set image rollouts-demo rollouts-demo=argoproj/rollouts-demo:yellow
```
]

- After running this command, you should notice that the Rollout immediately becomes `Healthy`, and there is no activity with regards to new ReplicaSets becoming created.