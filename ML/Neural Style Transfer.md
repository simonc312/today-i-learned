### NST (Neural Style Transfer)


2017

DiscoGANs 

https://deepai.org/publication/learning-to-discover-cross-domain-relations-with-generative-adversarial-networks

or 

https://arxiv.org/pdf/1703.05192.pdf

The DiscoGAN does not require supervised human labeling/annotation or by another algorithm between two cross domain image sets. It can self discover relations between the sets.

It uses 2 different GANs to develop the cross domain relations. It applies the constraint of one to one mapping - bijective. The goal is to minimize the distance between the applying the function encoding and decoding mappings between the two domains. There are 2 types of losses in this GAN network: reconstruction loss from A -> B -> A and standard GAN loss from assessing A -> B. The total GAN loss is the sum of the reconstruction and standard losses from the 2 partial models. The failure case occurs in the model when 2 different images from set A can be mapped to the same image from set B. The failure case occurs during model reconstruction loss when the same image from set A can map to multiple images from set B.

In each real domain experiment, all input images and translated images were of size 64×64×3. For training the Adam Optimizer was used. Batch Normalization was used for all the convolutional and deconvolutional layers except the first and last with a mean parameter of 0.5 and a standard deviation parameter of 0.999. The experiments were run with an Nvidea Titan X GPU - 336 GB/s bandwidth, 384-bit interface width, 1000 MHz base and 1075 MHz boosted clock.

It's possible to generate images from sketches to color images if the model has been trained with that mapping even though it's a one to many mapping. 

Other approaches to generative images have been explored:
- https://machinelearningmastery.com/what-is-cyclegan/
- https://arxiv.org/abs/1703.10593 (original publication 2017)
- application of DiscoGAN and CycleGAN for designing novel Korean hanbok style dresses
    - http://www.irphouse.com/ijert19/ijertv12n12_130.pdf

![disco-gan-sketch](https://images.deepai.org/converted-papers/1703.05192/x14.png)

Companies offering NST services:
- https://deepart.io
    - 69 Euros + shipping for 75x50 cm poster with watermark...
    - 299 Euros on acrylic glass without watermark
    - 19 Euros for just the file (1300x1300)
    - 500x500px free tier
    - https://deepart.io/pricing/
- https://deepai.org/machine-learning-model/fast-style-transfer
  - free to use api that takes input content and style url or files
  - as expected quality of output is poor
  - not ready for commerical usage

Different from simple style transfer as a painting filters.
Because it applies to all the pixels of the input dataset.
Instead of being able to identify the object itself within the image to selectively apply style.

2 encoder and decoder pairs form the GAN.

Common reasons GANs fail:
- not enough datasets 
- poor loss function 


