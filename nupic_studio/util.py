from panda3d.core import NodePath
from panda3d.core import TextNode
from panda3d.core import LineSegs


class Color3D:
    BLACK = (0, 0, 0, 1)
    GRAY = (0.5, 0.5, 0.5, 1)
    WHITE = (1, 1, 1, 1)
    RED = (255, 0, 0, 1)
    BLUE = (0, 0, 1, 1)
    YELLOW = (1, 1, 0, 1)
    GREEN_YELLOW = (0.67, 1, 0.18, 1)
    GREEN = (0, 1, 0, 1)


class Texture3D:
    RED = None
    YELLOW = None
    GREEN_YELLOW = None
    GREEN = None
    BLUE = None
    GRAY = None


def createAxesCross(name, size, has_labels):
    def createAxisLine(label, color, draw_to):
        coords.setColor(color)
        coords.moveTo(0, 0, 0)
        coords.drawTo(draw_to)

        # Put the axis' name in the tip
        if label != "":
            text = TextNode(label)
            text.setText(label)
            text.setTextColor(color)
            axis_np = coords_np.attachNewNode(text)
        else:
            axis_np = coords_np.attachNewNode("")
        axis_np.setPos(draw_to)
        return axis_np

    coords_np = NodePath(name)
    coords = LineSegs()
    coords.setThickness(2)
    axis_x_np = createAxisLine("X" if has_labels else "", Color3D.RED, (size, 0, 0))
    axis_y_np = createAxisLine("Y" if has_labels else "", Color3D.GREEN, (0, size, 0))
    axis_z_np = createAxisLine("Z" if has_labels else "", Color3D.BLUE, (0, 0, size))
    np = coords.create(True)
    coords_np.attachNewNode(np)
    return coords_np, axis_x_np, axis_y_np, axis_z_np
