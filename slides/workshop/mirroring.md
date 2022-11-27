# Traffic Mirroring

- Rolling out the app to internal users is great.

- It allows us to test features in isolation.

- But this still isn't the real traffic.

- Let's replicate *all* the traffic to the new version and see how it behaves. 

---

## Let's mirror all traffic to v03:

.exercise[
```bash
kubectl apply -n staging -f - <<EOF
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: beth
spec:
  hosts:
    - beth
  http:
  - route:
    - destination:
        host: beth
        subset: v01
    mirror:
      host: beth
      subset: v03
EOF
```
]

---

## Traffic Mirroring

- In UI check the version of `beth` you're now getting

- Check the logs of `beth-03` pod to make sure it's getting all incoming requests

.exercise[
```bash
kubectl logs deploy/beth-03 -n staging -f beth
```
- In a new shell
```bash
kubectl logs deploy/beth -n staging -f beth
```
]

- You should see all your requests arriving to both versions

