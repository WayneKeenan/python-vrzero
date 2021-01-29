import os
import threading
import time
import math
import pi3d
from .hmd import OpenHMD
from . import Gamepad

# Greetings programs...

# Created By User: Wayne Keenan
# ( wayne@thebubbleworks.com  /  https://twitter.com/wkeenan  /  https://github.com/WayneKeenan )


DEBUG = False

DEFAULT_TARGET_FPS = 60

# Oculus DK2 HMD resolution (also need to update /boot/config.txt)
#DEFAULT_HMD_SCREEN_WIDTH=1920
#DEFAULT_HMD_SCREEN_HEIGHT=1080

# PSVR Resolution chosen by Pi "best for display"
DEFAULT_HMD_SCREEN_WIDTH=1824
DEFAULT_HMD_SCREEN_HEIGHT=984


DEFAULT_AVATAR_EYE_HEIGHT = 6.0
DEFAULT_AVATAR_MOVEMENT_SPEED = 1.0
DEFAULT_AVATAR_VIEW_SPEED = 1.0

DEFAULT_HMD_EYE_SEPERATION=0.65
DEFAULT_HMD_VIEW_SCALE = 2.0

DEFAULT_JOYPAD_VIEW_SCALE = 4.0
DEFAULT_JOYPAD_MOVE_SCALE = 4.0
DEFAULT_KEYBOARD_MOVE_SCALE = 4.0
DEFAULT_MOUSE_MOVE_SCALE=10.0


DEFAULT_MOUSE_BUTTON_ACTION = pi3d.event.Event.key_to_code('BTN_MOUSE')
DEFAULT_MOUSE_BUTTON_JUMP = pi3d.event.Event.key_to_code('BTN_RIGHT')

DEFAULT_KEY_FORWARD = pi3d.event.Event.key_to_code('KEY_W')
DEFAULT_KEY_BACKWARD = pi3d.event.Event.key_to_code('KEY_S')
DEFAULT_KEY_STRAFE_LEFT = pi3d.event.Event.key_to_code('KEY_A')
DEFAULT_KEY_STRAFE_RIGHT = pi3d.event.Event.key_to_code('KEY_D')
DEFAULT_KEY_JUMP = pi3d.event.Event.key_to_code('KEY_SPACE')
DEFAULT_KEY_ACTION = pi3d.event.Event.key_to_code('KEY_ENTER')

DEFAULT_KEY_SCREENSHOT = pi3d.event.Event.key_to_code('KEY_P')
DEFAULT_KEY_QUIT = pi3d.event.Event.key_to_code('KEY_ESC')

DEFAULT_JOYPAD_BUTTON_ACTION = pi3d.event.Event.key_to_code('BTN_A')
DEFAULT_JOYPAD_BUTTON_JUMP = pi3d.event.Event.key_to_code('BTN_B')

DEFAULT_JOYPAD_BUTTON_QUIT = pi3d.event.Event.key_to_code('BTN_SELECT')

class Engine:
    """
    Represents a Virtual Realtiy engine that handles the movement of an avatar and 3D stereo projection of
    a 3D Scene created using Pi3D.

    Movement of the avatar can be controlled by any (optionally) attached keyboard, mouse or joypad.
    Rotational sensor readings from an Oculus Rift head mounted display will update the camera view.

    .. note::
        Only internal data is set at object creation time, OpenGL ES display and input event setup for keyboard,
        joystick, mouse and Head Mounted Display (HMD) is deferred until ``init()`` is called.

    """

    def __init__(self, **kwargs):
        self.debug = DEBUG
        self.keep_running = True

        self.is_forward_pressed = False
        self.is_backward_pressed = False
        self.is_strafe_left_pressed = False
        self.is_strafe_right_pressed = False
        self.is_action_pressed = False
        self.is_jump_pressed = False

        self._avatar_position = [0.0, 0.0, 0.0]
        self.avatar_body_rotation = [0.0, 0.0, 0.0]
        self.avatar_head_rotation = [0.0, 0.0, 0.0]
        self._avatar_eye_height = DEFAULT_AVATAR_EYE_HEIGHT
        self._avatar_movement_speed = DEFAULT_AVATAR_MOVEMENT_SPEED
        self.avatar_view_speed = DEFAULT_AVATAR_VIEW_SPEED

        self.joypad_view_scale = DEFAULT_JOYPAD_VIEW_SCALE
        self.joypad_move_scale = DEFAULT_JOYPAD_MOVE_SCALE
        self.mouse_move_scale = DEFAULT_MOUSE_MOVE_SCALE
        self.keyboard_move_scale = DEFAULT_KEYBOARD_MOVE_SCALE

        self.camera_position = [0.0, 0.0, 0.0]
        self.camera_rotation = [0.0, 0.0, 0.0]

        self.joystick_h_axis_pos = 0.0
        self.joystick_v_axis_pos = 0.0
        self.joystick_right_h_axis_pos = 0.0
        self.joystick_right_v_axis_pos = 0.0

        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.mouse_dx = 0.0
        self.mouse_dy = 0.0

        self.screenshot_count = 1

        self.hmd_screen_width = DEFAULT_HMD_SCREEN_WIDTH
        self.hmd_screen_height = DEFAULT_HMD_SCREEN_HEIGHT
        self.hmd_eye_seperation = DEFAULT_HMD_EYE_SEPERATION
        self.target_fps = DEFAULT_TARGET_FPS

        self.use_framebuffer = False

        self.show_stats = True
        self.tick = 0
        self.next_time = time.time() + 1.0

        self.use_simple_display=False
        self.use_crosseyed_method=False

    def stats(self):
        if not self.show_stats:
            return

        if time.time() > self.next_time:
            self.next_time = time.time() + 1.0
            print("FPS: {}", self.tick)
            self.tick = 0
        self.tick += 1

    def init(self):
        if self.use_framebuffer:
            os.putenv('SDL_FBDEV', '/dev/fb0')
            os.putenv('SDL_VIDEODRIVER', 'fbcon')

        self.DISPLAY = pi3d.Display.create(w=self.hmd_screen_width, h=self.hmd_screen_height,
                                           #display_config=pi3d.DISPLAY_CONFIG_HIDE_CURSOR | pi3d.DISPLAY_CONFIG_MAXIMIZED,
                                           use_glx=True)

        self.DISPLAY.set_background(0.0,0.0,0.0,1)
        self.DISPLAY.frames_per_second = self.target_fps

        shader_name = "barrel" if not self.use_simple_display else "uv_flat"
        if self.use_crosseyed_method:
            self.hmd_eye_seperation = -self.hmd_eye_seperation
        #self.CAMERA = pi3d.StereoCam(separation=self.hmd_eye_seperation, interlace=0, shader="shaders/"+shader_name)
        self.CAMERA = pi3d.StereoCam(separation=self.hmd_eye_seperation, interlace=0)

        # Setup Inputs

        #self.inputs = pi3d.InputEvents(self.key_handler_func, self.mouse_handler_func, self.joystick_handler_func)
        if Gamepad.available():
            self.gamepad = Gamepad.PS4()
            self.gamepad.startBackgroundUpdates()
        else:
            print('Controller not connected :(')


        self.hmd = OpenHMD()

    def mouse_handler_func(self, sourceType, sourceIndex, delta_x, delta_y, v, h):
        if self.debug:
            print("Relative[%d] (%d, %d), (%d, %d)" %(sourceIndex, delta_x, delta_y, v, h))
        self.mouse_dx = delta_x/DEFAULT_MOUSE_MOVE_SCALE
        self.mouse_dy = delta_y/DEFAULT_MOUSE_MOVE_SCALE
        self.mouse_x += delta_x/DEFAULT_MOUSE_MOVE_SCALE
        self.mouse_y += delta_y/DEFAULT_MOUSE_MOVE_SCALE

        # Mouse Updates  (Avatart body rotation, not the head)
        self.avatar_body_rotation[0] = -self.mouse_y
        self.avatar_body_rotation[1] = -self.mouse_x

    def joystick_handler_func(self, sourceType, sourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty):
        if self.debug:
            print("Absolute[%d] (%6.3f, %6.3f, %6.3f), (%6.3f, %6.3f, %6.3f), (%2.0f, %2.0f)" %(sourceIndex, x1, y1, z1, x2, y2, z2, hatx, haty))
        self.joystick_v_axis_pos = x1 if x1 is not None else 0.0
        self.joystick_h_axis_pos = y1 if y1 is not None else 0.0
        self.joystick_right_v_axis_pos = x2 if x2 is not None else 0.0
        self.joystick_right_h_axis_pos = y2 if y2 is not None else 0.0

    def key_handler_func(self, sourceType, sourceIndex, key, value):
        if self.debug:
            print("key="+str(key), pi3d.event.Event.code_to_key(key),"[",sourceIndex,"] =",value)

        if DEFAULT_KEY_FORWARD == key:
            self.is_forward_pressed = value > 0

        elif DEFAULT_KEY_BACKWARD == key:
            self.is_backward_pressed = value > 0

        elif DEFAULT_KEY_STRAFE_RIGHT == key:
            self.is_strafe_right_pressed = value > 0

        elif DEFAULT_KEY_STRAFE_LEFT == key:
            self.is_strafe_left_pressed = value > 0


        elif ( (DEFAULT_KEY_ACTION == key) or (DEFAULT_JOYPAD_BUTTON_ACTION == key) or (DEFAULT_MOUSE_BUTTON_ACTION == key)):
            if value == 0:
                self.on_action_released()
            elif value == 1:
                self.on_action_pressed()

        elif ( (DEFAULT_KEY_JUMP == key) or (DEFAULT_JOYPAD_BUTTON_JUMP == key) or (DEFAULT_MOUSE_BUTTON_JUMP == key)):
            if value == 0:
                self.on_jump_released()
            elif value == 1:
                self.on_jump_pressed()

        elif DEFAULT_KEY_SCREENSHOT == key and value == 1:
            pi3d.screenshot("vr_screenshot_"+str(self.screenshot_count)+".jpg")
            self.screenshot_count += 1

        elif DEFAULT_KEY_QUIT == key or DEFAULT_JOYPAD_BUTTON_QUIT == key:
            self.stop()

    def poll_inputs(self):
        #self.inputs.do_input_events()
        left_x = self.gamepad.axis("LEFT-X")
        left_y = self.gamepad.axis("LEFT-Y")
        right_x = self.gamepad.axis("RIGHT-X")
        right_y = self.gamepad.axis("RIGHT-Y")
        #print(left_x, left_y, right_x, right_y)
        self.joystick_handler_func(self, None, None, left_x, left_y, None, right_x, right_y, None, None)

    def update_avatar(self):
        self.hmd.poll()
        #HMD Updates (Avatar head rotation)
        self.avatar_head_rotation = ( math.degrees(self.hmd.rotation[0])*DEFAULT_HMD_VIEW_SCALE,
                              math.degrees(self.hmd.rotation[1])*DEFAULT_HMD_VIEW_SCALE,
                              math.degrees(self.hmd.rotation[2])*DEFAULT_HMD_VIEW_SCALE)



        # Mouse view updates are done in the event handler, because of viewpoint reseting

        y_rotation = self.avatar_body_rotation[1]
        keyboard_speed = self.keyboard_move_scale*self.avatar_movement_speed
        joypad_speed = self.joypad_move_scale*self.avatar_movement_speed
        joypad_view_speed = self.joypad_view_scale*self.avatar_view_speed

        # Joypad update - Looking
        if math.fabs(self.joystick_right_v_axis_pos) > 0.1:
            self.avatar_body_rotation[0] += -self.joystick_right_v_axis_pos*joypad_view_speed

        if math.fabs(self.joystick_right_h_axis_pos) > 0.1:
            self.avatar_body_rotation[1] += -self.joystick_right_h_axis_pos*joypad_view_speed


        # Keyboard updates
        if self.is_forward_pressed:
            self.avatar_position[0] -= math.sin(math.radians(y_rotation))*keyboard_speed
            self.avatar_position[2] += math.cos(math.radians(y_rotation))*keyboard_speed

        if self.is_backward_pressed:
            self.avatar_position[0] += math.sin(math.radians(y_rotation))*keyboard_speed
            self.avatar_position[2] -= math.cos(math.radians(y_rotation))*keyboard_speed

        if self.is_strafe_left_pressed:
            self.avatar_position[0] -= math.cos(math.radians(-y_rotation))*keyboard_speed
            self.avatar_position[2] += math.sin(math.radians(-y_rotation))*keyboard_speed

        if self.is_strafe_right_pressed:
            self.avatar_position[0] += math.cos(math.radians(-y_rotation))*keyboard_speed
            self.avatar_position[2] -= math.sin(math.radians(-y_rotation))*keyboard_speed


        # Joypad update - Movement
        if math.fabs(self.joystick_v_axis_pos) > 0.1:
            self.avatar_position[0] -= math.sin(math.radians(y_rotation))*-self.joystick_v_axis_pos*joypad_speed
            self.avatar_position[2] += math.cos(math.radians(y_rotation))*-self.joystick_v_axis_pos*joypad_speed

        if math.fabs(self.joystick_h_axis_pos) > 0.1:
            self.avatar_position[0] -= math.cos(math.radians(-y_rotation))*-self.joystick_h_axis_pos*joypad_speed
            self.avatar_position[2] += math.sin(math.radians(-y_rotation))*-self.joystick_h_axis_pos*joypad_speed

    def update_camera(self):
        self.camera_position = list(self.avatar_position)
        self.camera_position[1] += self.avatar_eye_height

        # Combining Head and Body rotations for the camera.
        self.camera_rotation[0] = self.avatar_body_rotation[0] + self.avatar_head_rotation[0]
        self.camera_rotation[1] = self.avatar_body_rotation[1] + self.avatar_head_rotation[1]
        self.camera_rotation[2] = self.avatar_body_rotation[2] + self.avatar_head_rotation[2]

    def render_stereo_scene(self, render_callback):
        self.CAMERA.move_camera(self.camera_position,
                                self.camera_rotation[1], self.camera_rotation[0], -self.camera_rotation[2])

        for i in range(2):
            self.CAMERA.start_capture(i)
            render_callback()
            self.CAMERA.end_capture(i)
        self.CAMERA.draw()



    def start(self, **kwargs):

        self.on_start()
        while self.DISPLAY.loop_running() or self.keep_running:
            self.poll_inputs()
            self.update_avatar()
            self.on_update()
            self.update_camera()
            self.render_stereo_scene(self.on_render)
            self.stats()
        self.on_stop()

    def stop(self):
        self.hmd.close()
        self.DISPLAY.destroy()
        self.keep_running = False;

    # To be overriden by user. (all optional)
    def on_start(self):
        pass

    def on_render(self):
        pass

    def on_update(self):
        pass

    def on_action_pressed(self):
        pass

    def on_action_released(self):
        pass

    def on_jump_pressed(self):
        pass

    def on_jump_released(self):
        pass

    def on_stop(self):
        pass

    # Utilities
    def get_keycode(self, key):
        return pi3d.event.Event.key_to_code(key)


    # The VR Zero API for the fun stuff...

    @property
    def avatar_movement_speed(self):
        return self._avatar_movement_speed

    @avatar_movement_speed.setter
    def avatar_movement_speed(self, speed):
        self._avatar_movement_speed = speed

    @property
    def avatar_position(self):
        return self._avatar_position

    @avatar_position.setter
    def avatar_position(self, position):
        self._avatar_position = position

    @property
    def avatar_eye_height(self):
        return self._avatar_eye_height

    @avatar_eye_height.setter
    def avatar_eye_height(self, height):
        self._avatar_eye_height = height


    @property
    def avatar_y_pos(self):
        return self._avatar_position[1]

    @avatar_y_pos.setter
    def avatar_y_pos(self, y):
        self._avatar_position[1] = y


