# panim - Paradoxical ANIMation

## Overview

`panim` is a personal Python-based animation tool designed for exploring the intersection of mathematics and coding. It allows users to create mathematical animations, generative art, and simulate various systems. The philosophy behind `panim` is learning through implementation, providing a hands-on approach to understanding complex concepts by building them from scratch.

## Features

*   **L-System Engine:** Generate and animate intricate fractal patterns using Lindenmayer systems.
    *   Supports standard L-Systems and Branched L-Systems.
    *   Customizable axioms, rules, angles, and iterations.
*   **Various Animators:** Pre-built animators for common simulations and effects:
    *   Rain simulation
    *   Pendulum dynamics (e.g., Double Pendulum)
    *   Generative art patterns (e.g., spirals, vanishing pixels)
*   **Transformation System:** Apply transformations to animations:
    *   **ZoomTransformer:** Zoom in or out of the scene.
    *   **RotationTransformer:** Rotate the scene.
    *   **TransformerPipeline:** Chain multiple transformations together.
*   **Combined Animations:** Render multiple independent animations within the same scene.
*   **Save Animations:** Export animations as MP4 video files.
*   **Customizable:** Flexible framework for creating new types of animations and visual effects.

## Installation and Setup

1.  **Prerequisites:**
    *   Python 3.x
    *   `matplotlib`: For plotting and animation.
    *   `numpy`: For numerical operations.
    *   `loguru`: For logging.
    *   `ffmpeg`: Required by `matplotlib` to save animations as MP4 files. Ensure it's installed and accessible in your system's PATH.

    You can typically install the Python libraries using pip:
    ```bash
    pip install matplotlib numpy loguru
    ```
    Installation of `ffmpeg` depends on your operating system (e.g., `sudo apt-get install ffmpeg` on Debian/Ubuntu, `brew install ffmpeg` on macOS).

2.  **Get the Code:**
    Clone this repository to your local machine:
    ```bash
    git clone https://github.com/USERNAME/panim.git # Replace USERNAME/panim with the actual repo path if different
    cd panim
    ```

3.  **Running Examples:**
    The `examples/` directory contains various scripts showcasing different features of `panim`. To run an example, navigate to its directory and execute the Python script:
    ```bash
    cd examples/lsystems
    python tree.py
    ```
    Animations will typically be saved in an `out/` directory created within the main `panim` project directory or within specific subdirectories (e.g., `out/trees/`).

## Core Concepts

### Animators (`AbstractAnimator`)

The `panim.animator.AbstractAnimator` class is the cornerstone of all animations in `panim`. It provides the fundamental structure for:

*   **Animation Loop:** Managing the frame-by-frame progression of the animation.
*   **Canvas Setup:** Initializing the `matplotlib` figure and axes for drawing.
*   **Frame Update Logic:** Subclasses must implement the `update(i)` method, which defines what calculations or changes occur at each frame `i`. This method should return the data required to draw the current frame.
*   **Rendering:** Handling the drawing of data onto the canvas for each frame.
*   **Saving:** Providing functionality to save the completed animation to a video file (typically MP4).

Specific animators (like `LSystemAnimator`, `RainAnimator`, etc.) inherit from `AbstractAnimator` and implement their unique animation logic.

### L-Systems

L-Systems (Lindenmayer Systems) are a mathematical formalism for describing the growth of simple multicellular organisms or generating fractal structures. In `panim`:

*   **`panim.lsystem.LSystem`:** This class is responsible for generating the L-System string. You provide it with:
    *   `axiom`: The initial string (e.g., "F").
    *   `rule`: A dictionary of production rules (e.g., `{"F": "F+F--"}`).
    *   `iteration`: The number of times the rules are applied to the axiom to generate the final string.
    *   `turn_angle`: The angle (in degrees) used for '+' (turn right) and '-' (turn left) commands.
    The class then processes these rules to produce a long string that represents the structure.
*   **`panim.lsystem.LSystemAnimator`:** Takes an `LSystem` instance (or its parameters) and animates the drawing of the L-system based on its generated string. It translates symbols like 'F' (draw forward), '+' (turn right), '-' (turn left) into graphical operations.
*   **`panim.lsystem.BranchedLSystemAnimator`:** An extension for L-Systems that use branching symbols like '[' (save current state) and ']' (restore state). This allows for more complex, tree-like structures.

### Transformers

Transformers (`panim.transformers.Transformer`) are special animators that modify the output of another animator. They take an existing animator object and apply transformations to its coordinate data on each frame.

*   **`ZoomTransformer`:** Scales the coordinates to create a zoom-in or zoom-out effect.
*   **`RotationTransformer`:** Rotates the coordinates around the origin.
*   **`TransformerPipeline`:** Allows you to chain multiple transformers together, applying them sequentially to an animator's output.

## Getting Started: Creating Your First Animation

Let's create a simple fractal tree animation using `BranchedLSystemAnimator`.

1.  **Create a Python file** (e.g., `my_first_animation.py`) in the root directory of the `panim` project (or ensure `panim` is in your Python path).

2.  **Add the following Python code:**

    ```python
    #!/usr/bin/env python3

    # Ensure panim is in the Python path if running from outside the root directory
    # import sys
    # from pathlib import Path
    # path = str(Path().absolute().parent) # Assuming this script is in an 'examples' like folder
    # if path not in sys.path:
    #     sys.path.insert(0, path)

    from panim.lsystem import BranchedLSystemAnimator

    def create_simple_tree():
        # 1. Define L-System Parameters
        axiom = "F"  # The starting symbol
        rules = {
            "F": "FF[++F][-F]"  # Rule: 'F' becomes 'FF', then branch right, then branch left
                                # '[', ']' are for branching
                                # '+' turns right, '-' turns left
        }
        iterations = 3  # How many times to apply the rules
        angle = 25.0    # Angle for turns in degrees

        # 2. Instantiate the Animator
        # We use BranchedLSystemAnimator because our rule uses '[' and ']'
        animator = BranchedLSystemAnimator(
            axiom=axiom,
            rule=rules,
            iteration=iterations,
            turn_angle=angle,
            start_position=(0, -30),  # Start drawing from (x=0, y=-30)
            nlimit=40,                # Sets the plot limits (e.g., x from -40 to 40)
            interval=50,              # Delay between frames in milliseconds
            color=(0.2, 1.0, 0.2),    # Line color (RGB tuple, green-ish)
            line_width=2,
            title="My First Fractal Tree"
        )

        # 3. Run the Animation
        # The number of frames is determined by the length of the generated L-system coordinates
        num_frames = len(animator.coords)
        animator.animate(num_frames=num_frames, fps=24) # fps can be specified here

        # 4. Save the Animation
        output_filename = "out/my_simple_tree.mp4"
        print(f"Saving animation to {output_filename}...")
        animator.save(output_filename, fps=24, dpi=150) # fps and dpi for saving
        print("Animation saved!")

    if __name__ == "__main__":
        create_simple_tree()
    ```

3.  **Run the script:**
    ```bash
    python my_first_animation.py
    ```
    This will display the animation and then save it to `out/my_simple_tree.mp4`.

This example demonstrates the basic workflow: define parameters, instantiate an animator, run the animation, and save it.

## Examples Gallery

Here are some animations rendered using `panim`:

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

## API Reference (Summary)

Detailed API documentation is embedded as docstrings within the source code. Key modules and classes include:

*   **`panim.animator`**:
    *   `AbstractAnimator`: The base class for all animators.
    *   `CombinedAnimator`: Combines multiple animators into one scene.
    *   `AbstractImageAnimator`: Base for animations based on image array manipulations.
*   **`panim.lsystem`**:
    *   `LSystem`: Core class for L-System string generation.
    *   `BranchedLSystem`: Extends `LSystem` for branching structures.
    *   `LSystemAnimator`: Animates standard L-Systems.
    *   `BranchedLSystemAnimator`: Animates branched L-Systems.
*   **`panim.transformers`**:
    *   `Transformer`: Base class for all transformers.
    *   `ZoomTransformer`: Applies zoom transformations.
    *   `RotationTransformer`: Applies rotation transformations.
    *   `TransformerPipeline`: Chains multiple transformers.
*   Other modules like `panim.rain`, `panim.pendulum`, `panim.spirals`, etc., contain specialized animators.

Please refer to the docstrings in each module and class for detailed information on parameters and methods.

## Disclaimer

The code is experimental and primarily a personal project. While it's not intended to cause harm, rendering very high-resolution animations (e.g., 4K) with high FPS might be resource-intensive. Optimizations are an ongoing consideration.

There are many excellent animation libraries available; `panim` is a tool for personal exploration and learning.

## TO-DO

*   Add PanTransformer to pan the animation scene.
*   Optimize the renderer by culling points outside the screen context.
*   Add a transformer to make old points vanish as rendering progresses.
*   Add more artistic animation objects (e.g., circle, rectangle primitives).
*   Introduce the concept of a camera for more complex scene manipulation.
*   Refactor project structure for better organization.
*   Implement BOID for flocking behavior simulation.
*   Enhance documentation and add more examples.
