# panim
Paradoxical ANIMation

## What?
Yes. Nothing much. Just my personal "mathematical" animation tool.
I intend to use this as a zone where my love for mathematics and coding meets. 

As Feynman said:
> I learned very early the difference between knowing the name of something and knowing something.


For me this is only possible by implementing "things" from scratch.

## So?
Yeah. For now it can render "things" like:
- L-Systems
- Rain
- Generative Arts
- Double Pendulum
- Zooming In and Out (Transformer)
- Scene Rotation (Transformer)
- Pipeline for transformers
- Random L-System
- Multiple Combined Animation

## Animation Renedered From Panim

### L-Systems
- [Hilbert Curve](https://www.youtube.com/watch?v=YmBgv_ttd4o)
- [Simple Fractal Tree - Branched L System](https://www.youtube.com/watch?v=v_XYCuwM1lQ)
- [Binary Fractal Tree](https://www.youtube.com/watch?v=qzYDGGJ6tH4)
- [Dragon Curve](https://www.youtube.com/watch?v=ZkI2Dg7yZo0)
- [Simple Fractal Flower](https://www.youtube.com/watch?v=WvZ4rlcGFvs)
- [Complex Tree](https://www.youtube.com/watch?v=PW8Vq2VeYa4)
- [Tiles](https://www.youtube.com/watch?v=n2surTrThXk)
- [Crystals](https://www.youtube.com/watch?v=VVgVbBwdybw)
- [Square Spiral](https://www.youtube.com/watch?v=zCrNb2teSkA)

### Random L-System
- [Random Sphere-like Branched L-System](https://www.youtube.com/watch?v=M20CyhPMbKU)

### Combined Animators for Random L-System
- [Combined Animation](https://www.youtube.com/watch?v=ZD2eDmWKgV4)
- [Combined Animation with 25 Randomly Generated L-System](https://www.youtube.com/watch?v=CesihF7eVt)
- [Random Psychedelic Animation with N=75 Animators combined](https://www.youtube.com/watch?v=Cc8_EhgjVv0)


### Rain
- [Rain Animation](https://www.youtube.com/watch?v=mUZdfECU09A)
- [Rain Drops](https://www.youtube.com/watch?v=kK2ZekDgocw)


### Pendulum
- [Double Pendulum](https://www.youtube.com/watch?v=Jv21HIJOANE)
- [Double Pendulum with Tip Tracking](https://www.youtube.com/watch?v=y_JSQc1tqF4)

### Generative Arts
- [Psychedelic Spiral](https://www.youtube.com/watch?v=dyrQ81b2DxY)
- [Vanishing Pixels](https://www.youtube.com/watch?v=r0Rw-ix-5PY)
- [Simple Water Flow](https://www.youtube.com/watch?v=wMujrvugwIk)
- [White Voids](https://www.youtube.com/watch?v=Q_KM3v3K3_I)


## Disclaimer
The code is experimental. But does not do harm to your system (if I am to be more optimistic than usual).
Unless you are rendering a high resolution animation (for example 4K) with high FPS, the code works fine! 
In case your machine lags while rendering, I am sure you have absurdly higher number of frames being rendered. 
I will try to optimize in future times to come. Till then, have a look at the To-Do list.

I am sure there are many other better tools to perform similar tasks. This is solely for my own personal experiments.

## TO-DO
Following are the things I have in my mind but I am too much lost in my own mind-cave that I have to find time to implement. :/

- ~~Add ZoomTransformer~~
- ~~Add RotationTransformer~~
- ~~Add TransformerPipeline~~
- Add PanTransformer to pan the animation scene
- Optimize the renderer by removing points out the screen context.
- Add a transformer to make old points vanish into the oblivion as redering progresses
- Add artistic animation objects like circle, rectangle
- Add the concept of camera
- Refactor project structure
