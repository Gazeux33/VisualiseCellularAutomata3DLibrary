# 3D visualisation Library for Cellular Automata

This project consists of a library designed for the visualisation of cellular automata, created in Python and using OpenGL. This library allows users to simulate and visualise various cellular automata behaviours in an interactive graphical environment. By taking advantage of OpenGL's rendering capabilities, your tool offers a fluid and detailed visual experience, making it easier to understand and analyse complex cellular automata models.


## Example of Using the Library ( see examples folder for more examples): 



```py
class PerlinNoiseVisualisation(BaseApp): # Inherit from BaseApp (3D visualisation library)
    def __init__(self) -> None:
        super().__init__()
        self.noise_map = None
        self.set_window_title("PerlinNoise") # Set window title
        self.set_window_size(WindowSize(1000, 800)) # Set window size
        self.matrix_size = 100 # Size of the matrix
        self.need_to_generate = True
        self.add_event_key_callback(self.regenerate_matrix, GLFW_CONSTANTS.GLFW_KEY_R) # Add key callback

    def update(self) -> None:
        if self.need_to_generate:
            self.noise_map = self.generate_noise_map()
            self.create_cube_from_noise_map()
            self.renderer.update_instance_buffer(self.scene.cubes)
            self.renderer.prepare_instance_data()
            self.need_to_generate = False

    def regenerate_matrix(self) -> None:
        self.scene.delete_all_cubes()
        self.noise_map = self.generate_noise_map()
        self.create_cube_from_noise_map()
        self.renderer.update_instance_buffer(self.scene.cubes)
        self.renderer.prepare_instance_data()

    def generate_noise_map(self) -> np.ndarray:
        noise = PerlinNoise(octaves=2.3, seed=self.seed)
        lin = np.linspace(0, 1, self.matrix_size, endpoint=False)
        x, y = np.meshgrid(lin, lin)
        pic = np.zeros((self.matrix_size, self.matrix_size))
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                pic[i][j] = noise([x[i][j], y[i][j]])
        return pic

    def create_cube_from_noise_map(self) -> None:
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
               # Add cube to the scene
                self.scene.add_cube(i, j, self.noise_map[i, j] * self.matrix_size,texture_name="pastel.png")

# create an instance of the class and launch the application
g = PerlinNoiseVisualisation()
g.launch()
```

![Perlin noise](https://github.com/Gazeux33/VisualiseCellularAutomata3DLibrary/blob/master/assets/noise1.png)



## Techical Details

 * **Instance Rendering** : Renders multiple instances of an object with a single draw call to improve performance
 * **Shaders (Vertex and Fragment)**: Programs on the GPU that process vertices and pixels to define the visual output.
 * **Transformation Matrices**: 
    * **View Matrix**: Transforms world coordinates to camera coordinates.
    * **Projection Matrix**: Transforms camera coordinates to screen coordinates.
    * **Model Matrix**: Transforms object coordinates to world coordinates.
 * **Depth Buffering**: Uses a buffer to store pixel depth for accurate object visibility based on distance.

 * **Texture Mapping**: Applies images to 3D models to add detail without increasing polygons.

 * **Blending and Alpha Blending**: Combines fragment colors for transparency and overlay effects.

 * **Culling (Frustum and Back-Face)**: Skips rendering of objects or faces not visible to the camera to enhance performance.

 * **Vertex Buffer Objects (VBOs) and Vertex Array Objects (VAOs)**: Store vertex data on the GPU for efficient access and rendering.

 * **Instanced Geometry Buffering**: Stores transformation matrices for rendering multiple instances of a model efficiently.

# Acknowledgment


https://www.youtube.com/playlist?list=PLn3eTxaOtL2PDnEVNwOgZFm5xYPr4dUoR

https://cs.brown.edu/courses/cs195v/projects/life/edwallac/index.html
