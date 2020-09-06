### [Fast Arbitrary Style Transfer][0]

<img src="./assets/fast_style_transfer_model_architecture.png" 
alt="model_architecture" height="400" />

A model trained on 80k paintings and 6k visual textures can generalize to new painting styles.

Previous models excelled at quickly generating a limited set of styles.

The model architecture consists of a style transfer network that takes content image 
and style vector output from style prediction network. The content image, stylized image, and style image are input to
the image classification network to calculate style and content loss.

The style transfer network is a convolutional neural network with a encoder/decoder architecture.
Training a new network is inefficient because painting styles share commonalities. 
The improvement from single to N (32) fast styles came from using a linear transformation that 
outputs a 3000 dimension vector representing a painting style.

The paper authors used the [Kaggle Painters By Numbers][1] dataset of nearly 80k labeled paintings as training style images and the [ImageNet dataset][2] for training content images.
They use the [Describable Textures Dataset (DTD)][3] that categorizes 5.6k images into 47 textures (ex bubbly) to supplement the training style images.

From the 1024 new unobserved painting styles the average distribution of losses was comparable to the observed styles.
They found that training more styles helps until reaching 16k styles where then it marginally hits limit for reducing style loss.
Also, they found that increasing the number of paintings (in same styles) in training content set did not improve reduction of content loss. 

> The style transfer model represents all paintings and textures in a style embedding vector~S that is 2758 dimensional.
> The  style  prediction  network  predicts ~S from a lower dimensional representation (i.e.,bottleneck) containing only 100 dimensions. 

<img src="./assets/fast_style_transfer_prediction_network_visualization.png" 
alt="DTD-textures-low-dimensional-style-embedding" height="400" />

> (T)he style prediction network has learned a representation for artistic styles that is largely organized based on our perception of visual and semantic similarity without any explicit supervision.
> Importantly, we can now interpolate between the identity stylization and arbitrary (in this case, unobserved) painting in order to effectively dial in the weight of thepainting style.

<img src="./assets/fast_style_transfer_interpolation.png" 
alt="style-interpolation" height="160" />

Style Prediction Network:

- 256x256 px style images were used.
- Inception-v3 neural network was used with 17x17 spatial dimensions and 768 filter depth. Read [guide to inception network][4] for more details.
- The [Adam Optimizer][5] was used with hyper parameters alpha = 0.001 (learning rate), beta1 = 0.9 (momentum) and beta2 = 0.999 (RMSprop) as recommended by authors of the Adam paper because it has demonstrated to work well for many domains.
- Isotropic gaussian weight initialization was used because. Read [deep learning initialization][6] for more details.

Style Transfer Network:
- same Adam Optimizer paramters
- same Isotropic gaussian weight initialization
- The [ReLU activation function][7] was used to avoid the vanishing gradient problem, is easy to optimize/generalize/train due to linear behavior, and has become the default for deep convolutional neural networks (CNNs).

[0]: https://arxiv.org/pdf/1705.06830.pdf
[1]: https://www.kaggle.com/c/painter-by-numbers/data
[2]: http://image-net.org/
[3]: https://www.robots.ox.ac.uk/%7Evgg/data/dtd/index.html
[4]: https://towardsdatascience.com/a-simple-guide-to-the-versions-of-the-inception-network-7fc52b863202
[5]: https://towardsdatascience.com/adam-optimization-algorithm-1cdc9b12724a
[6]: https://www.deeplearning.ai/ai-notes/initialization/
[7]: https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/