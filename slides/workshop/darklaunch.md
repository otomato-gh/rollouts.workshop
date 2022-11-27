# Launching Darkly

- Our existing deployments already have a version label:

```yaml
      labels:
        app: beth
        version: v01
```

.exercise[
- Create a new deployment for `beth` in file `deployments/beth-v03.yaml` labeled as:

```yaml
version: v03
```

- Don't forget to also update deployment name and image name

- Deploy

```bash
kubectl apply -f  deployments/beth-v03.yaml -n staging
```
]

---

## Did This Work As Planned?

- Try reloading front UI in your browser

- Hmm, we get both versions intermittently. Not what we wanted!

- Let's fix our virtual service.

.exercise[ 
```bash
kubectl apply -f istio/dark-launch.yaml
```
]

- Look at `istio/dark-launch.yaml`
---

## Privileged Access

- Back in you browser - sign in as user `developer` (the `Sign in` button is at top right)

- You should be consistently getting version 0.3

- Sign out now.

- Are you getting the older version again?

