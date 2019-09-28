
LAB1 SQUAD TRAINING - PYTHON  
---  

### Fundamentals  
  
Before we start working on **Storify**, our store management application, we need to review the basics of _Python_ to make sure that everyone has the minimum required to get started.  

The way we are going to learn and practice some _Python_ concepts in this chapter is by working with a [Jupyter Notebook](https://jupyter4edu.github.io/jupyter-edu-book/index.html).  
  
#### Jupyter Notebook  
  
The _Jupyter Notebook_ is a web application that allows you to create and share interactive documents that contain live code, equations, visualizations and explanatory text (markdown, latex...). Jupyter Notebook supports over 100 programming languages through its [kernels](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels). Jupyter comes with **IPython** kernel as default.  

Let's pick up from where we left it last chapter, and install Jupyter

The uses of Jupyter are generally related to data science and scientific computing such as : _Data cleaning and transformation, numerical simulation, statistical modeling, machine learning..._ So the recommended way of using it is through **Anaconda distribution** because it provides all the necessary packages out of the box. However, we are going to install Jupyter the _pythonic_ way  

First to isolate Jupyter packages, we are going to create a dedicated _venv_ for it. Run commands:

```shell script
python -m venv jptrenv
source jptrenv/bin/activate
```

Result:
<pre>
(jptrenv) Project $
</pre>

Next, run command:

```shell script
pip install jupyter  
ls jptrenv/bin
```  

Result (file system):  
<pre>  
.  
├── ...  
├── iptest  
├── iptest3  
├── ipython  
├── ipython3  
├── jsonschema  
├── jupyter  
├── jupyter-bundlerextension  
├── jupyter-console  
├── jupyter-kernel  
├── jupyter-kernelspec  
├── jupyter-migrate  
├── jupyter-nbconvert  
├── jupyter-nbextension  
├── jupyter-notebook  
├── jupyter-qtconsole  
├── jupyter-run  
├── jupyter-serverextension  
├── jupyter-troubleshoot  
├── jupyter-trust  
├── ...  
</pre>  
  
All that is left to do is run Jupyter Notebook:  

```shell script
jupyter notebook  
``` 

Result:  
<pre>  
[I 16:17:01.705 NotebookApp] Serving notebooks from local directory: /home/user/Playground/squad-lab1-store  
[I 16:17:01.705 NotebookApp] The Jupyter Notebook is running at:  
[I 16:17:01.705 NotebookApp] http://localhost:8888/?token=a0bbfe62e863264c032f723e211d35c3131f58638be00a59  
[I 16:17:01.706 NotebookApp]  or http://127.0.0.1:8888/?token=a0bbfe62e863264c032f723e211d35c3131f58638be00a59  
[I 16:17:01.706 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).  
[C 16:17:01.730 NotebookApp]  
  
    To access the notebook, open this file in a browser:  
        file:///home/user/.local/share/jupyter/runtime/nbserver-21829-open.html  
    Or copy and paste one of these URLs:  
        http://localhost:8888/?token=a0bbfe62e863264c032f723e211d35c3131f58638be00a59  
     or http://127.0.0.1:8888/?token=a0bbfe62e863264c032f723e211d35c3131f58638be00a59  
</pre>  
  
As you can see, the printed output presents us with _URLs_ to open the notebook web application
  
This chapter comes with a folder with notebooks that we are going to explore together. So let's switch to our notebook app!
