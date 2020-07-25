import os
import time
import shutil
import psutil
import socket
import platform
import pymemcache
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import ClockObject
from panda3d.core import loadPrcFileData
from panda3d.core import Filename
from panda3d.core import MultiplexStream
from panda3d.core import Notify
from panda3d.core import Point2
from panda3d.core import Point3
from panda3d.core import TextNode
from panda3d.core import BamCache
from panda3d.core import GraphicsOutput, Texture, Vec3
from panda3d.core import LineSegs
from panda3d.core import TextureStage
from panda3d.core import TexGenAttrib
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from nupic_studio import REPO_DIR
from nupic_studio.util import createAxesCross, Color3D, Texture3D

VIEW_RADIUS = 1000

# Redirect output to log file
# TODO: When implement project uncomment
#log_file = os.path.join(REPO_DIR, "output.log")
#if os.path.exists(log_file):
#    os.remove(log_file)
#nout = MultiplexStream()
#Notify.ptr().setOstreamPtr(nout, 0)
#nout.addFile(Filename(log_file))

# Disable any caching
cache = BamCache.get_global_ptr()
cache.set_active(False)


class Simulation(ShowBase):

    def __init__(self, project, project_path):

        # Set Panda3D configuration flags
        loadPrcFileData("", "window-type offscreen")
        loadPrcFileData("", "model-cache-dir")
        # TODO: When implement project uncomment
        #if project['logging']:
        #    print("Enabling full logging...")
        #    loadPrcFileData("", "notify-level spam")
        #    loadPrcFileData("", "default-directnotify-level info")
        #else:
        #    loadPrcFileData("", "notify-level warning")
        #    loadPrcFileData("", "default-directnotify-level warning")

        ShowBase.__init__(self)
        self.project = project
        self.project_path = project_path
        self.last_bit_idx = 0
        self.last_cell_idx = 0
        self.last_segment_idx = 0
        self.last_synapse_idx = 0

        # Clear the record folder
        # TODO: When implement project uncomment
        #if self.project['playback']:
        #    self.record_dir = os.path.join(self.project_path, "record")
        #    if os.path.exists(self.record_dir):
        #        shutil.rmtree(self.record_dir)
        #    os.mkdir(self.record_dir)
        #else:
        #    self.record_dir = None

        # Enable physics
        print("Enabling physics...")
        self.physics_manager = BulletWorld()
        self.physics_manager.setGravity((0, 0, 0))

        # Allow AI entities as much time as they need to think
        self.frame_rate = 60
        print("Configuring frame rate (" + str(self.frame_rate) + ")...")
        global globalClock
        globalClock.setMode(ClockObject.M_forced)
        globalClock.setFrameRate(self.frame_rate)
        globalClock.reset()

        # Turn on debug wireframes for every object in this simulation
        print("Enabling debug...")
        self.debug_senses_nps = []
        debug_node = BulletDebugNode("Debug")
        self.debug_np = self.render.attachNewNode(debug_node)
        self.physics_manager.setDebugNode(self.debug_np.node())
        #self.debug_np.show()

        # Necessary for scene visualization
        self.mouse_feature = ""
        self.start_mouse_work_fn = None
        self.stop_mouse_work_fn = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_steps = None

        # Instead of a window, we put the graphics to a texture which can be handled by other 3rd software like QT
        self.screen_texture = Texture()
        self.win.addRenderTexture(self.screen_texture, GraphicsOutput.RTMCopyRam)
        # TODO: When implement project uncomment
        #if self.project['playback']:
        #    prefix = str(Filename.from_os_specific(os.path.join(self.record_dir, 'main_camera')))
        #    max_frames = 99999999
        #    self.movie(namePrefix=prefix, duration=(max_frames / self.frame_rate), fps=self.frame_rate, format='png', sd=8, source=self.win)

        # Run memcached program to share neural images with other client softwares
        # TODO: When implement project uncomment
        #if self.project['shared']:
        #    system = platform.system().lower()
        #    ip = self.getIp()
        #    port = 11211
        #    if not self.processExists("memcached"):
        #        raise Exception("Memcached service is not runnning!")
        #    self.memcached_client = pymemcache.client.base.Client((ip, port))
        #    print("Sharing objects in " + ip + ":" + str(port) + " ...")

        # Load the color textures
        print("Loading textures...")
        Texture3D.RED = self.loader.loadTexture(Filename.from_os_specific(os.path.join(REPO_DIR, "models", "tex_red.png")))
        Texture3D.YELLOW = self.loader.loadTexture(Filename.from_os_specific(os.path.join(REPO_DIR, "models", "tex_yellow.png")))
        Texture3D.GREEN_YELLOW = self.loader.loadTexture(Filename.from_os_specific(os.path.join(REPO_DIR, "models", "tex_green_yellow.png")))
        Texture3D.Green = self.loader.loadTexture(Filename.from_os_specific(os.path.join(REPO_DIR, "models", "tex_green.png")))
        Texture3D.BLUE = self.loader.loadTexture(Filename.from_os_specific(os.path.join(REPO_DIR, "models", "tex_blue.png")))
        Texture3D.GRAY = self.loader.loadTexture(Filename.from_os_specific(os.path.join(REPO_DIR, "models", "tex_gray.png")))

        print("Adjusting lights...")
        directional_light_1 = DirectionalLight('directional_light_1')
        directional_light_1.setColor(Color3D.WHITE)
        self.directional_light_1_np = self.render.attachNewNode(directional_light_1)
        self.directional_light_1_np.setHpr(200, -20, 0)
        self.render.setLight(self.directional_light_1_np)
        directional_light_2 = DirectionalLight('directional_light_2')
        directional_light_2.setColor(Color3D.WHITE)
        self.directional_light_2_np = self.render.attachNewNode(directional_light_2)
        self.directional_light_2_np.setHpr(20, -20, 0)
        self.render.setLight(self.directional_light_2_np)

        # Adjust the scene elements
        print("Adjusting camera position...")
        self.disable_mouse()
        self.cam.setPos(0, -VIEW_RADIUS*0.99, 0)
        self.cam.lookAt(0, 0, 0)
        self.camera_pivot_np = self.render.attachNewNode("camera_pivot")
        #self.camera_pivot_np.setPos(self.getPointFromCamLens((0, 0))[1])
        self.camera_pivot_np.setPos(0, 0, 0)
        self.cam_pos = None
        self.cam_hpr = None
        # TODO: When implement project uncomment
        #if self.project["use_last_camera_view"] and self.project["last_camera_pos"] is not None:
        #    self.cam.setPos(self.project["last_camera_pos"])
        #    self.cam.setHpr(self.project["last_camera_hpr"])
        #    self.cam_pos = self.project["last_camera_pos"]
        #    self.cam_hpr = self.project["last_camera_hpr"]
        #else:
        #    self.cam.setPos(self.project["camera_pos"])
        #    self.cam.lookAt(self.project["camera_look_at"])
        self.cam.reparentTo(self.camera_pivot_np)

        # Create the coords widget for indicating axes directions
        self.coords_np, self.axis_x_np, self.axis_y_np, self.axis_z_np, self.cam_label_np, self.cam_pos_np, self.cam_hpr_np, \
        self.touched_label_np, self.touched_object_np, self.touched_pos_np = self.createScreenWidgets()

        self.is_simulating = True
        print("Simulation running!")
        print("(See 'output.log' to more details)")

        # Put "update" function to be executed at every frame
        self.start = time.time()
        self.taskMgr.add(self.update, "update")

    def processExists(self, process_name):
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def destroy(self):
        print("Cleaning memory...")
        self.is_simulating = False
        ShowBase.destroy(self)
        print("Simulation stopped!")

    def update(self, task):
        # Don't update if simulating is stopping! Risk of null objects raise exceptions.
        if self.is_simulating:
            self.updateCamera()
            time_per_frame = self.getTimePerFrame()
            self.physics_manager.doPhysics(time_per_frame)
        return Task.cont

    def getIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def getTimePerFrame(self):
        return globalClock.getDt()

    def startMouseWork(self, feature, start_mouse_work_fn, stop_mouse_work_fn):
        self.mouse_feature = feature
        self.start_mouse_work_fn = start_mouse_work_fn
        self.stop_mouse_work_fn = stop_mouse_work_fn
        self.cam_label_np.show()
        self.cam_pos_np.show()
        self.cam_hpr_np.show()
        self.touched_label_np.show()
        self.touched_object_np.show()
        self.touched_pos_np.show()

        # Pick a position to act as pivot to the camera
        if self.mouse_feature == "zoom":
            target_pos = (self.mouse_x, self.mouse_y)
        else:
            target_pos = (0, 0)
        self.touched_object, self.touched_pos = self.getPointFromCamLens(target_pos)
        if self.touched_pos is None:
            self.touched_object = None
            self.touched_pos = (0, 0, 0)

        # Move camera pivot to touched position
        cam_pos = self.cam.getPos(self.render)
        self.cam.reparentTo(self.render)
        self.camera_pivot_np.setPos(self.touched_pos)
        self.cam.reparentTo(self.camera_pivot_np)
        self.cam.setPos(self.render, cam_pos)

        self.start_mouse_work_fn()

    def stopMouseWork(self):
        self.mouse_feature = ""
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.cam_label_np.hide()
        self.cam_pos_np.hide()
        self.cam_hpr_np.hide()
        self.touched_label_np.hide()
        self.touched_object_np.hide()
        self.touched_pos_np.hide()

        self.stop_mouse_work_fn()

    def resetCamera(self):
        self.camera_pivot_np.setPos(0, 0, 0)
        self.camera_pivot_np.setHpr(0, 0, 0)
        self.cam.setPos(self.render, (0, -VIEW_RADIUS*0.99, 0))

    def updateCamera(self):
        """
        Use mouse input to turn/move the camera.
        """
        if self.mouse_feature != "":
            diff_x = (self.last_mouse_x - self.mouse_x) if self.last_mouse_x is not None else 0
            diff_y = (self.last_mouse_y - self.mouse_y) if self.last_mouse_y is not None else 0
            self.last_mouse_x = self.mouse_x
            self.last_mouse_y = self.mouse_y
            if self.mouse_feature == "rotate":
                offset = 5000 * self.getTimePerFrame()
                self.camera_pivot_np.setH(self.camera_pivot_np.getH() + diff_x * offset)    # horizontal plane
                self.camera_pivot_np.setP(self.camera_pivot_np.getP() - diff_y * offset)    # vertical plane
            elif self.mouse_feature == "pan":
                offset = 15000 * self.getTimePerFrame()
                self.camera_pivot_np.setZ(self.cam, self.camera_pivot_np.getZ(self.cam) + diff_y * offset)    # horizontal plane
                self.camera_pivot_np.setX(self.cam, self.camera_pivot_np.getX(self.cam) + diff_x * offset)    # vertical plane
            elif self.mouse_feature == "zoom":
                offset = 0.1 * self.getTimePerFrame()
                diff = self.cam.getPos(self.render) - self.camera_pivot_np.getPos(self.render)
                self.cam.setPos(self.render, self.cam.getPos(self.render) - diff * self.mouse_steps * offset)
                self.stopMouseWork()

            # Format the camera info text
            self.cam_pos = tuple([round(n, 2) for n in self.cam.getPos(self.render)])
            self.cam_hpr = tuple([round(n, 2) for n in self.cam.getHpr(self.render)])
            cam_pos_text = "XYZ: ({:d}, {:d}, {:d})".format(int(self.cam_pos[0]), int(self.cam_pos[1]), int(self.cam_pos[2]))
            cam_hpr_text = "HPR: ({:d}, {:d}, {:d})".format(int(self.cam_hpr[0]), int(self.cam_hpr[1]), int(self.cam_hpr[2]))

            # Update coordinates widget
            hpr = self.render.getHpr(self.cam)
            self.coords_np.setHpr(hpr)
            hpr = self.cam.getHpr(self.render)
            self.axis_x_np.setHpr(hpr)
            self.axis_y_np.setHpr(hpr)
            self.axis_z_np.setHpr(hpr)

            # Show camera position and rotation
            self.cam_pos_np.node().setText(cam_pos_text)
            self.cam_hpr_np.node().setText(cam_hpr_text)

            # Format the touch info text showing object and point touched by the cross
            touched_object_text = ""
            touched_pos_text = ""
            if self.touched_object is not None:
                touched_object_text = "Name: " + self.touched_object.getParent(0).getName()
            if self.touched_pos is not None:
                touched_pos_text = "XYZ: ({:d}, {:d}, {:d})".format(int(self.touched_pos[0]), int(self.touched_pos[1]), int(self.touched_pos[2]))
            self.touched_object_np.node().setText(touched_object_text)
            self.touched_pos_np.node().setText(touched_pos_text)

    def getPointFromCamLens(self, target_pos):

        # Get to and from pos in camera coordinates and transform to global coordinates
        p_from, p_to = Point3(), Point3()
        self.camLens.extrude(Point2(target_pos), p_from, p_to)
        p_from = self.render.getRelativePoint(self.cam, p_from)
        p_to = self.render.getRelativePoint(self.cam, p_to)

        # Get the target coordinates which correspond to mouse coordinates and walk the camera to this direction
        result = self.physics_manager.rayTestClosest(p_from, p_to)
        if result.hasHit():
            return result.getNode(), result.getHitPos()
        else:
            return None, None

    def createScreenWidgets(self):

        # Pin the coords in left-bottom of the screen
        origin = [-1.4, 5, -0.85]
        coords_np, axis_x_np, axis_y_np, axis_z_np = createAxesCross("coords", 3, True)
        coords_np.reparentTo(self.cam)
        coords_np.setPos(self.cam, tuple(origin))
        coords_np.setScale(0.1)

        # Put the camera label ('observer') text in the left-bottom corner
        origin = [-1.7, 5, -1.1]
        text = TextNode("cam_label")
        text.setText("Observer")
        text.setTextColor(Color3D.YELLOW)
        cam_label_np = self.cam.attachNewNode(text)
        cam_label_np.setPos(self.cam, tuple(origin))
        cam_label_np.setScale(0.07)

        # Put the camera position in the left-bottom corner
        origin = [-1.7, 5, -1.2]
        text = TextNode("cam_pos")
        text.setText("XYZ:")
        text.setTextColor(Color3D.YELLOW)
        cam_pos_np = self.cam.attachNewNode(text)
        cam_pos_np.setPos(self.cam, tuple(origin))
        cam_pos_np.setScale(0.07)

        # Put the camera rotation in the left-bottom corner
        origin = [-1.7, 5, -1.3]
        text = TextNode("cam_hpr")
        text.setText("HPR:")
        text.setTextColor(Color3D.YELLOW)
        cam_hpr_np = self.cam.attachNewNode(text)
        cam_hpr_np.setPos(self.cam, tuple(origin))
        cam_hpr_np.setScale(0.07)

        # Put the touch label text in the right-bottom corner
        origin = [0.8, 5, -1.1]
        text = TextNode("touched_label")
        text.setText("Touched Object")
        text.setTextColor(Color3D.YELLOW)
        touched_label_np = self.cam.attachNewNode(text)
        touched_label_np.setPos(self.cam, tuple(origin))
        touched_label_np.setScale(0.07)

        # Put the touched objected in the right-bottom corner
        origin = [0.8, 5, -1.2]
        text = TextNode("touched_object")
        text.setText("Name:")
        text.setTextColor(Color3D.YELLOW)
        touched_object_np = self.cam.attachNewNode(text)
        touched_object_np.setPos(self.cam, tuple(origin))
        touched_object_np.setScale(0.07)

        return coords_np, axis_x_np, axis_y_np, axis_z_np, cam_label_np, cam_pos_np, cam_hpr_np, touched_label_np, touched_object_np, touched_object_np

    def createElement(self, name, type, start, end=None):
        if type == "cell":
            model_file = "sphere.dae"
        elif type == "bit":
            model_file = "box.dae"
        elif type == "segment" or type == "synapse":
            model_file = "cylinder.dae"

        # Create the rigid body
        body_node = BulletRigidBodyNode(name)
        body_node.setDeactivationEnabled(False)
        body_np = self.render.attachNewNode(body_node)
        body_np.setName(name)

        if type == "segment" or type == "synapse":
            # Calculate the linear distance between the start and the end position of the segment.
            length = (Point3(start) - Point3(end)).length()

            body_np.setPos(start)
            body_np.lookAt(end)
            body_np.setScale(1, length/2, 1)
        else:
            body_np.setPos(start)

        # Load the 3d model file using the asset folder relative path and attach the geom node to rigid body
        object_np = self.loader.loadModel(Filename.from_os_specific(os.path.join(REPO_DIR, "models", model_file)))
        object_np.reparentTo(body_np)
        object_np.setPosHpr((0, 0, 0), (0, 0, 0))
        object_np.setName(name + "_geom")
        object_np.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)

        # Apply any transforms from modelling sotware to gain performance
        object_np.flattenStrong()

        # Create the shape used for collisions
        geom_nodes = object_np.findAllMatches("**/+GeomNode")
        mesh = BulletTriangleMesh()
        for geom in geom_nodes[0].node().getGeoms():
            mesh.addGeom(geom)
        shape = BulletTriangleMeshShape(mesh, dynamic=True)
        body_node.addShape(shape)

        self.physics_manager.attachRigidBody(body_node)
        return body_np

    def createBit(self, position):
        name = "bit_" + str(self.last_bit_idx)
        self.last_bit_idx += 1
        return self.createElement(name, "bit", position)

    def createCell(self, position):
        name = "cell_" + str(self.last_cell_idx)
        self.last_cell_idx += 1
        return self.createElement(name, "cell", position)

    def createSegment(self, start, end):
        name = "segment_" + str(self.last_segment_idx)
        self.last_segment_idx += 1
        return self.createElement(name, "segment", start, end)

    def createSynapse(self, start, end):
        name = "synapse_" + str(self.last_synapse_idx)
        self.last_synapse_idx += 1
        return self.createElement(name, "synapse", start, end)

    def removeElement(self, element_np):
        if len(element_np.children) > 0:
            geo_np = element_np.children[0]
            geo_np.detachNode()
            del geo_np
        element_np.detachNode()
        del element_np
