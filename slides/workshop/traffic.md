# Traffic Management

- Controlling the amount of traffic by the number of pods is very limited

- Modern proxies allow us to have weighted load-balancing 

- Kubernetes ingress controllers and service meshes can be configured to do weighted load balancing even with one pod per app version

- Argo Rollouts can be integrated with multiple service meshes and ingress controllers

---

## Ingress Controller in Our Cluster


- In our k3d cluster the Traefik ingress controller is installed

- It's mapped to port 80 of our host machine

- It creates routes based on standard kubernetes Ingress resources

- Or based on its own CRDs - for smarter traffic control

- Argo Rollouts integrates with Traefik CRDS

---

## Explore the Traefik CRDs

.exercise[
  ```bash
  kubectl get crd | grep traefik
  ```
]

- See the *IngressRoute* and the *TraefikService* resources?

- These are the ones we will be using

---

## Create the Traefik Ingress

- Let's start with creating the ingress and the weighted load-balancing

- We will need:
  - A DNS record for our ingress (see next slide)
  - an additional Service for the canary access
  - a TraefikService to load balance between the stable and the canary service
  - an IngressRoute to route ingress traffic to the application


---

## Setting up DNS 

- We will use nip.io for DNS

- In order to do that we'll need to edit the IngressRoute definition:

- Replace `<MY_IP>` in the `code/ingressroute.yaml` with the IP of your lab machine:

```yaml
  - kind: Rule
    match: Host(`demo.<MY_IP>.nip.io`)  #replace <MY_IP> with your machine public IP
```

.exercise[
  ```bash
  MY_IP=$(dig +short myip.opendns.com @resolver1.opendns.com)
  sed -i s/\<MY_IP\>/$MY_IP/ ~/rollouts.workshop/code/ingressroute.yaml
  ```
]

---

## Creating the Ingress

- Let's create the ingress resources:

.exercise[
  ```bash
  kubectl apply -f ~/rollouts.workshop/code/rolloutscanaryservice.yaml
  kubectl apply -f ~/rollouts.workshop/code/traefikservice.yaml
  kubectl apply -f ~/rollouts.workshop/code/ingressroute.yaml
  ```
]

- Check by going to demo.`your.machine.ip`.nip.io in browser

---

## Updating our rollout

- We want to see canary Traefik(!) management in action

- Let's update our rollout to define traffic management

.exercise[
  ```bash
  kubectl apply -f ~/rollouts.workshop/code/rollout-weighted.yaml
  ```
]

- Watch it scale down to 1 replica instead of 5 (we don't need multiple replicas if we use traffic management)

---

## Updating the Rollout with Traffic Management

- We will deploy a new version, promote it and see its progress in Web UI


.exercise[

- Update the version:
  ```bash
  kar set image rollouts-demo rollouts-demo=argoproj/rollouts-demo:yellow
  ```

- Watch the progress in rollouts console
  ```bash
  kar get rollout rollouts-demo -w
  ```

- Promote the canary to the second stage:
  ```bash
  kar promote rollouts-demo
  ```
]

- Watch the demo UI to see the canary progress
