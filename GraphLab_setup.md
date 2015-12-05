# Setting up GraphLab

### Sign up for the free trial. 

1.) Visit [GraphLab's website](https://dato.com/), and sign up for the free
trial by clicking in the upper right corner.  

2.) You can put in Galvanize for the organization and Data Science Fellow
for your Job Title.   

3.) Take note of your Product key after you are done signing up. 

### Pip install and set up a configuration file.  

1.) Pip install graphlab-create: 

```bash 
pip install graphlab-create
```

2.) Create a configuration file so that graphlab-create will know where
to look to find your product key (fill in 1234 below with your product key): 

```bash 
mkdir -p ~/.graphlab && echo -e "[Product]\nproduct_key=1234" > ~/.graphlab/config \
&& echo "Configuration file written" || echo "Configuration file not written"
```
