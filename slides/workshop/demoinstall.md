# The Demo Installation

- microk8s installs the so-called _evaluation_ or _demo_ install of Istio

- It includes additional components:

  - Prometheus - for monitoring

  - Grafana - for dashboards

  - Jaeger - for tracing (see the istio-tracing-.. pod)

  - Kiali - the Istio UI 

---
## The mixer pods

- We can see pilot, galley, citadel... But where is the mixer?

.exercise[
```bash
kubectl get pod -n istio-system -l=istio=mixer
```
]

- Mixer has 2 functions: defining traffic policy and exposing traffic telemetry. 

- Therefore - 2 pods.

---
## The sidecars

- Now, where are the Envoys?

- Let's look at the Pilot pod:

.exercise[
```bash
kubectl describe pod -n istio-system -l istio=pilot
```
]
--

```
Containers:
  discovery:
...
    Image:         docker.io/istio/pilot:1.0.5
...
  istio-proxy:
...
    Image:         docker.io/istio/proxyv2:1.0.5
```
---

### The sidecars

- But how do the sidecars get into our own pods?

- Let's deploy a service.

.exercise[
```bash
kubectl create deployment httpbin --image=kennethreitz/httpbin
```
]

- And look at the pod: 

.exercise[
```bash
kubectl describe pod -l=app=httpbin
```
]

- There's only one container. The sidecar proxy isn't there...

---

## The sidecar injection

- How do we inject the proxy into our pod?

- Do we need to edit our deployment ourselves?!

- There should be some magic somewhere!

- Remember when we looked at Istio pods there was that *sidecar-injector* pod?

- So why didn't it work?

---

## The sidecar injection

From Istio docs:
"When you deploy your application using kubectl apply, the Istio sidecar injector will automatically inject Envoy containers into your application pods if they are started in namespaces labeled with **istio-injection=enabled**."

- Let's label our namespace and redeploy:

.exercise[
```bash
kubectl label namespace default istio-injection=enabled
kubectl delete pod -l=app=httpbin
```
]
--

- Recreating that pod took a whole lotta time, didn't it?!

---

## The sidecar injection

- Look at our new pod:

.exercise[
```bash
kubectl describe pod -l=app=httpbin
```
]

- Now we have two containers and there was an [init-container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)!

- The istio-init container is run before the other containers are started and it's responsible for setting up the iptables rules so that all inbound/outbound traffic will go through Envoy

  - For a deep dive into what istio-init does - read this [blog post](https://medium.com/faun/understanding-how-envoy-sidecar-intercept-and-route-traffic-in-istio-service-mesh-20fea2a78833)

---

## Let's cleanup the default namespace

- We just learned that automated istio-proxy injection is enabled per namespace.

- We will be using a special namespace for our deployments today.

- We don't want istio injection enabled on our `default` namespace, so let's clean it up:

.exercise[
```bash
kubectl label ns default --overwrite  istio-injection=disabled
```
]

