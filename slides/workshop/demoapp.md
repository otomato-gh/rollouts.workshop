# Deploying the Application

- Our purpose today is to learn how Istio allows us to implement *progressive delivery* techniques

- We'll do that by deploying a demo application - an *alphabeth* system :)

- It's just a frontend service that speaks to 2 backends (aleph and beth)

- All the services are bare-bones Python Flask apps

---

class: pic
## The Sample App 
![diagram](images/demoapp.png)

---

## What's on the menu?

In this part, we will:

- **build** images for our app,

- **ship** these images with a registry,

- **run** deployments using these images,

- expose these deployments so they can communicate with each other,

- expose the web UI so we can access it from outside.

---

## The plan

- Build our images using Docker

- Tag images so that they are named `$REGISTRY/servicename`

- Upload them to a registry

- Create deployments using the images

- Expose (with a ClusterIP) the services that need to communicate

- Expose (with a NodePort) the WebUI

---

## Which registry do we want to use?

- We could use the Docker Hub

- Or a service offered by our cloud provider (GCR, ECR...)

- Or we could just self-host that registry

*We'll self-host the registry because it's the most generic solution for this workshop.*

---

## Using the open source registry

- We need to run a `registry:2` container
  <br/>(make sure you specify tag `:2` to run the new version!)

- It will store images and layers to the local filesystem
  <br/>(but you can add a config file to use S3, Swift, etc.)

- Docker *requires* TLS when communicating with the registry

  - unless for registries on `127.0.0.0/8` (i.e. `localhost`)

  - or with the Engine flag `--insecure-registry`

- Our strategy: publish the registry container on a NodePort,
  <br/>so that it's available through `127.0.0.1:32000` on our single node
  
.warning[We're choosing port 32000 because it's the default port for an insecure registry on microk8s]

---

# Deploying a self-hosted registry

- We will deploy a registry container, and expose it with a NodePort 32000


.exercise[

- Create the registry service:
  ```bash
  kubectl create deployment registry --image=registry:2
  ```

- Expose it on a NodePort:
  ```bash
  kubectl create service nodeport registry --tcp=5000 --node-port=32000
  ```

]

---

## Testing our registry

- A convenient Docker registry API route to remember is `/v2/_catalog`

.exercise[

- View the repositories currently held in our registry:
  ```bash
  REGISTRY=localhost:32000
  curl $REGISTRY/v2/_catalog
  ```

]

--

We should see:
```json
{"repositories":[]}
```

---

## Testing our local registry

- We can retag a small image, and push it to the registry

.exercise[

- Make sure we have the busybox image, and retag it:
  ```bash
  docker pull busybox
  docker tag busybox $REGISTRY/busybox
  ```

- Push it:
  ```bash
  docker push $REGISTRY/busybox
  ```

]

---

## Checking again what's on our local registry

- Let's use the same endpoint as before

.exercise[

- Ensure that our busybox image is now in the local registry:
  ```bash
  curl $REGISTRY/v2/_catalog
  ```

]

The curl command should now output:
```json
{"repositories":["busybox"]}
```

---

## Building and pushing our images

- We are going to use a convenient feature of Docker Compose

.exercise[

- Go to the `alephbeth` directory:
  ```bash
  cd ~/istio.workshop/alephbeth
  ```

- Build and push the images:
  ```bash
  export REGISTRY
  docker-compose build
  docker-compose push
  ```

]

Let's have a look at the `docker-compose.yaml` file while this is building and pushing.

---

```yaml
services:
  front:
    build: front
    image: ${REGISTRY}/front:${TAG-0.3}  
  aleph:
    build: aleph
    image: ${REGISTRY}/aleph:${TAG-0.3}
  beth:
    build: beth
    image: ${REGISTRY}/beth:${TAG-0.3}
  mongo:
    image: mongo
```

---

## Deploying all the things

- We can now deploy our code 

- We will create a new namespace 'staging' and enable istio sidecar injection on it

.exercise[

- We have kubernetes yamls ready for the first version of our app in `deployments` dir:
  ```bash
  cd deployments
  kubectl create ns staging
  kubectl label ns staging istio-injection=enabled
  kubectl apply -f aleph.yaml  -f front.yaml -f beth.yaml  -n staging 
  ```
]
---

## Is this working?

- After waiting for the deployment to complete, let's look at the logs!

  (Hint: use `kubectl get deploy -w` to watch deployment events)

.exercise[

- Look at some logs:
  ```bash
  kubectl logs -n staging deploy/front
  ```
- Hmm, that didn't work. We need to specify the container name!
  ```bash
  kubectl logs -n staging deploy/front front
  kubectl logs -n staging deploy/front istio-proxy
  ```
]

---

## Accessing the web UI

- Our `front` service is exposed on a NodePort.

- Let's look at it and see if it works:

.exercise[

- Get the port of the `front` service

```bash
kubectl get svc -n staging front -o=jsonpath='{ .spec.ports[0].nodePort }{"\n"}'
```
- Open the web UI in your browser (http://node-ip-address:3xxxx/)

<!-- ```open http://node-ip-address:3xxxx/``` -->

]

--

*You should see the frontend application showing the versions of both its backends*