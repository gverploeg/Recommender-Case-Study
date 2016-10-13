# Setting up GraphLab

## Sign up for an academic license. 

1. Visit [Turi](https://turi.com/download/academic.html), and sign up for an academic license (*not* the free trial).

2. Take note of your Product key after you are done signing up. 

## Install GraphLab Create and set up your license. 

1. Install `graphlab-create` using `pip`: 

```bash 
pip install graphlab-create
```

2.) Create a configuration file so that `graphlab-create` will have your product key (fill in 1234 below with your product key): 

```bash 
export GRAPHLAB_KEY=1234
mkdir -p ~/.graphlab && echo -e "[Product]\nproduct_key=${GRAPHLAB_KEY}" > ~/.graphlab/config \
&& echo "Configuration file written" || echo "Configuration file not written"
```
