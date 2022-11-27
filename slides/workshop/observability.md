# Istio Observability Features

- Observability (or o11y) is an important concept in microservice-based approach

- Observability of our systems is composed of three main components:

  - Logs

  - Metrics

  - Traces

- Istio makes inter-service networking observable by:

  - Collecting request metrics

  - Collecting distributed traces
---
## Istio and Observability

.trivia[
*Question*:

- What Istio component is responsible for collecting telemetry in Istio?
]

--

*Answer*:

- Mixer is responsible for collecting and shipping telemetry 

---

class: pic

## Mixer and its Adapters

- Mixer is pluggable. Mixer Adapters allow us to post to multiple backends:

![Mixer](images/adapters.svg)

---

## Observability Add-Ons in Our Istio Installation

- Let's see what observability services we have in our installation.

.exercise[
    ```bash
    kubectl get svc -n istio-system
    ```
]

- We have: 

  - **Prometheus**: for network telemetry
  - **Grafana**: to visualize Prometheus data
  - **Kiali**: to visualize the connections between our services
  - **Jaeger** (it's the service named `tracing`): to store and visualize distributed traces
  - **Zipkin**: another option to store and visualize distributed traces

---

## Explore the Telemetry

.exercise[
- Let's expose Jaeger, Grafana and Servicegraph on NodePort

```bash
for service in tracing grafana kiali; do
    kubectl patch svc -n istio-system $service --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'
done;
```
- Get the ports for the exposed services:

```bash
kubectl get svc grafana  -n istio-system  -o jsonpath='{ .spec.ports[0].nodePort }{"\n"}'
```

- Do the same for `kiali` and `tracing` services
- Browse to http://your-node-ip:3XXXX (replace with actual service port) 
    
]

