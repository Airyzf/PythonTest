import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

mnist=input_data.read_data_sets('MNIST_data',one_hot=True)

def add_layer(inputs,in_size,out_size,activation_function=None):
    Weight=tf.Variable(tf.random_normal([in_size,out_size]))
    biases=tf.Variable(tf.zeros([1,out_size])+0.1)
    Wx_plus_b=tf.matmul(inputs,Weight)+biases
    if activation_function is None:
        outputs=Wx_plus_b
    else:
        outputs=activation_function(Wx_plus_b)
    return outputs

def compute_accuracy(v_xs,v_ys):
    global prediction
    y_pre=sess.run(prediction,feed_dict={xs:v_xs})
    correct_prediction=tf.equal(tf.argmax(y_pre,1),tf.argmax(v_ys,1))
    accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    result=sess.run(accuracy,feed_dict={xs:v_xs,ys:v_ys})
    return result

def weight_variable(shape):
    initial=tf.truncated_normal(shape,stddev=1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial=tf.constant(0.1,shape=shape)
    return tf.Variable(initial)

def conv2d(x,W):
    #strides=[1,x_movestep,y_movestep,1],
    # strides[0]=strides[3]=1 规定的
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

def max_pol_2x2(x):
    # strides[0]=strides[3]=1 规定的
    #strides=[1,2,2,1] 2x2把图片缩小了
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

# x_data=np.linspace(-1,1,300)[:,np.newaxis]
# noise=np.random.normal(0,0.05,x_data.shape)
# y_data=np.square(x_data)-0.5
#
# xs=tf.placeholder(tf.float32,[None,1])
# ys=tf.placeholder(tf.float32,[None,1])
# l1=add_layer(xs,1,10,activation_function=tf.nn.relu)
# prediction=add_layer(l1,10,1,activation_function=None)
#
# loss=tf.reduce_mean(tf.reduce_sum(np.square(
#     ys-prediction),reduction_indices=[1]))
# train_step=tf.train.GradientDescentOptimizer(0.1).minimize(loss)

xs=tf.placeholder(tf.float32,[None,784])#28x28
ys=tf.placeholder(tf.float32,[None,10])
keep_prob=tf.placeholder(tf.float32)
x_image=tf.reshape(xs,[-1,28,28,1])#[n_sample,28,28,1(颜色通道)]

##conv1 layer
W_conv1=weight_variable([5,5,1,32])#5x5大小抽取,输入时是1个高度，输出32个高度
b_conv1=bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)#因为Padding="SAME" 所以大小不变，28x28x32
h_pool1=max_pol_2x2(h_conv1)#strides=[1,2,2,1] 2x2 池化大小变了 14x14x32

##conv2 layer
W_conv2=weight_variable([5,5,32,64])#5x5大小抽取，输入32个高度，输出64个高度
b_conv2=bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)#因为Padding="SAME" 所以大小不变，28x28x64
h_pool2=max_pol_2x2(h_conv2)#strides=[1,2,2,1] 2x2 池化大小变了 7x7x64

##func1
W_fc1=weight_variable([7*7*64,1024])
b_fc1=bias_variable([1024])
#[n_sample,7,7,64]变成[n_sample,7*7*64]
h_pool2_flat=tf.reshape(h_pool2,[-1,7*7*64])
h_fc1=tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)
h_fc1_drop=tf.nn.dropout(h_fc1,keep_prob)

##func2
W_fc2=weight_variable([1024,10])
b_fc2=bias_variable([10])
prediction=tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)

# prediction=add_layer(xs,784,10,activation_function=tf.nn.softmax)
#
cross_entropy=tf.reduce_mean(-tf.reduce_sum(ys*tf.log(prediction),
                                            reduction_indices=[1]))
train_step=tf.train.AdadeltaOptimizer(1e-4).\
    minimize(cross_entropy)

inti=tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(inti)
    for i in range(1000):
        batch_xs,batch_ys=mnist.train.next_batch(100)
        sess.run(train_step,feed_dict={xs:batch_xs,ys:batch_ys})
        if i % 50 == 0:
            print(compute_accuracy(
                mnist.test.images,mnist.test.labels))
