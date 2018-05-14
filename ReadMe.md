# Parallel TensorFlow DataLoader

This simple project is designed to load data especially video data parallelly to improve the whole system efficiency.The framework is shown following:

![parallel_model][parallel_model]

We fork $K$ threads to load and decode data in CPU and maintain a global FIFO queue to store data. A main task thread is need to train the network in GPU. If the time of loading a batch data is larger than training in GPU, the efficiency will be improved a lot. The simulation experiment results are shown following(The time of loading a batch of data is set to 1 second and time to train in a step is set to 0.2 second):

![s_res]

**fig 1: serially loading data, the cpu usage with only 5.3%**

![p_res]

**fig 2: fork 10 threads to load data, the cpu usage with nearly 30%, almost 6 times than the serial version.**

![p_res_2]

**fig 3: fork 30 threads to load data**

The blog written in Chinese at site https://blog.csdn.net/LoseInVain/article/details/80311534.

[parallel_model]: ./img/parallel_model.png
[p_res_2]: ./img/p_res_2.png
[p_res]: ./img/p_res.png
[s_res]: ./img/s_res.png
[csdn]: https://blog.csdn.net/LoseInVain/article/details/80311534