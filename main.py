from sim.render import App, init_glfw





if __name__ == "__main__":
    w = init_glfw()
    r =App(w)
    r.launch()
