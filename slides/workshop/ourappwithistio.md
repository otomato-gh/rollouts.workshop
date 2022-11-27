# Our App with Istio

- Ok, time to start managing our app with Istio

- The first thing to do is create VirtualService entities for each of our services

- I've prepared a definition for front service in alephbeth/istio/front-vs.yaml

.exercise[

```bash
kubectl apply -f alephbeth/istio/front-vs.yaml -n staging
```
]

Note: you won't notice a change. We're only accessing the service from outside of the cluster.

Controlling traffic to the `front` service would require defining a [Gateway](https://istio.io/docs/reference/config/networking/v1alpha3/gateway/) object. But that is out of the scope of our training today.

---

## VirtualServices for Everyone

- Now create virtual services for `aleph` and `beth`

.exercise[
- Create yaml definitions for both services

- Apply them to your cluster

```bash
kubectl apply -f alephbeth/istio/aleph-vs.yaml -n staging
kubectl apply -f alephbeth/istio/beth-vs.yaml -n staging
```

- Verify
```bash
kubectl get virtualservice -n staging
```
]

- Is everything still working?

---

## Let's build a New Version

- Remember that `beth` wasn't displaying the version right?

- Let's fix that and deploy a new version.

- But this time we'll launch darkly!

.exercise[
- In `beth/api.py` change the version on line 12:
```python
    'version': '0.3',
```
- Build a new docker image and push it to local registry

- Don't update your existing `beth` deployment. We will launch darkly!
]

