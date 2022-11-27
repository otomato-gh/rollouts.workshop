## Introduction

- This presentation was created by [Ant Weiss](https://twitter.com/antweiss) to support 
  instructor-led workshops.

- We included as much information as possible in these slides

- Most of the information this workshop is based on is public knowledge and can also be accessed through [Argo Rollouts official documents and tutorials](https://argoproj.github.io/argo-rollouts/)

![image alt ><](images/argo-rollouts.png)
---

## Training environment

- This is a hands-on training with exercises and examples

- We assume that you have access to a Kubernetes cluster

- The training labs for today's session were generously sponsored by [Otomato Software Delivery](https://otomato.io)
- We will be using [k3d](https://k3d.io) to run these clusters 


---

## Getting started

- Get the source code and the slides for this workshop:

.exercise[

- On your Strigo VM:

  ```bash
  git clone https://github.com/otomato-gh/rollouts.workshop.git 
  cd rollouts.workshop
  ./prepare-vms/setup_rollouts.sh
  # enter new shell for kubectl completion
  sudo su - ${USER}
  ```

]

- This will install the Argo Rollouts controller in your k3d cluster