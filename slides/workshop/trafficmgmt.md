# Istio Traffic Management Basics

- In order to implement Progressive Delivery with Istio
  <br/> we need to use 2 Istio resources:
  
  - [Virtual Service](https://istio.io/docs/reference/config/networking/v1alpha3/virtual-service/)

  - [Destination Rule](https://istio.io/docs/reference/config/networking/v1alpha3/destination-rule/)

---

## Virtual Service

A VirtualService defines a set of traffic routing rules to apply when a host is addressed. Each routing rule defines matching criteria for traffic of a specific protocol. If the traffic is matched, then it is sent to a named destination service (or subset/version of it) defined in the registry.

The source of traffic can also be matched in a routing rule. This allows routing to be customized for specific client contexts.

---

## Virtual Service - path rewriting

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
  - reviews.prod.svc.cluster.local
  http:
  - match:
    - uri:
        prefix: "/wpcatalog"
    - uri:
        prefix: "/consumercatalog"
    rewrite:
      uri: "/newcatalog"
    route:
    - destination:
        host: reviews.prod.svc.cluster.local
```

---

## Virtual Service - header based routing

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: promotions
spec:
  hosts:
  - promotions.prod.svc.cluster.local
  http:
  - match:
    - headers:
        User-Agent:
          regex: ".*Mobile.*"
      uri:
        prefix: "/promotions/mobile"
    route:
    - destination:
        host: promotions-mobile.prod.svc.cluster.local
  - route:
    - destination:
        host: promotions.prod.svc.cluster.local
```

---

## Virtual Service - versioned destinations

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
  - reviews.prod.svc.cluster.local
  http:
  - route:
    - destination:
        host: reviews.prod.svc.cluster.local
        subset: v2
      weight: 25
    - destination:
        host: reviews.prod.svc.cluster.local
        subset: v1
      weight: 75
```
- Wait, where do these `subset`s come from?

---

## Destination Rule

**DestinationRule** defines policies that apply to traffic intended for a service after routing has occurred.
 These rules specify configuration for load balancing, connection pool size from the sidecar, and outlier detection settings to detect and evict unhealthy hosts from the load balancing pool. 

 *Version specific policies* can be specified by defining a named *subset* and overriding the settings specified at the service level. 

 On Kubernetes these subsets can be defined by referencing pod labels.
 
---

## Destination Rule

The following rule uses a round robin load balancing policy for all traffic going to a subset named `testversion` that is composed of endpoints (e.g.: pods) with labels (version:v3).

```yaml
 apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: bookinfo-ratings
spec:
  host: ratings.prod.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
  subsets:
  - name: testversion
    labels:
      version: v3
    trafficPolicy:
      loadBalancer:
        simple: ROUND_ROBIN
```
