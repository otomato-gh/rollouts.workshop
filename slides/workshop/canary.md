# Rolling out to Production with Canary

- The new version seems to behave fine

- It's time to release it

- But we still want to be on the safe side

- We want stress-free releases

.warning[
    Forty-three percent of all adults suffer adverse health effects from **stress**.
]

- Canary to the rescue

---

## Giving some traffic to our new version

.exercise[
- Look at istio/canary.yaml:

```yaml
http:
  - route:
    - destination:
        host: beth
        port:
          number: 80
        subset: v01
      weight: 99
    - destination:
        host: beth
        port:
          number: 80
        subset: v03
      weight: 1
```
]

---

## Giving some traffic to our new version

.exercise[
```bash
kubectl apply -f istio/canary.yaml
```
]

- We don't want to test this through the UI, do we?

- Let's run curl in a loop and see what we get

---

## Running a curl pod

.exercise[
```bash
kubectl create -n staging -f - <<EOF
apiVersion: v1
kind: Pod
metadata:  
  name: curl
spec:
  containers:
  - args:
    - sleep
    - "100000"
    image: otomato/alpine-curl
    name: curl
EOF
```
]

---

## Curling Our Service

.exercise[
```bash
kubectl exec -it -n staging curl sh
```
- Inside the container:
```bash
while true; do curl http://beth/version; done
```
]

- Are you getting any `0.3` versions?

- Leave this running 

---
## Releasing the Canary

.exercise[
- Edit VirtualService `beth` to gradually release more traffic to v03
```bash 
kubectl edit virtualservice -n staging beth 
```
]
- Once we see only 0.3 getting returned by our curler (and our browser) - 
  <br/> we're done. Version v01 can now be deleted.





