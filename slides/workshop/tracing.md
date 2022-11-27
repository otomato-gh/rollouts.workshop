# Distributed tracing with Jaeger
.exercise[

- Generate some traffic by reloading `front` in your browser.

- Look at the traces in Jaeger

- Is one of the backends slower than the other one?

]

--

- Looks like `beth` is taking too slow to respond...

---

## What makes distributed tracing possible?

Although Istio proxies are able to automatically send spans, they need some hints to tie together the entire trace. Applications need to propagate the appropriate HTTP headers so that when the proxies send span information, the spans can be correlated correctly into a single trace.

In `front/front.py` line 17:

```python
    incoming_headers = [ 'x-request-id',
                         'x-b3-traceid',
                         'x-b3-spanid',
                         'x-b3-parentspanid',
                         'x-b3-sampled',
                         'x-b3-flags',
                         'x-ot-span-context'
    ]
```

Each service needs to pass these headers to its downstream connections.

---

## Let's fix the problem!

- We've found slowness in `beth` responses

- Let's see what's causing this:

.exercise[
- Look at `beth/api.py`, line 33

- A-ha, looks like someone forgot to remove some testing code...
]

- Let's fix the issue, build a new version and redeploy.