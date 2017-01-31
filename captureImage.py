import cozmo
import asyncio
import pygame
from Common.woc import WOC
from Instagram.InstagramAPI import InstagramAPI
from Common.colors import Colors

try:
    import numpy as np
except ImportError:
    sys.exit("Cannot import numpy: Do `pip3 install --user numpy` to install")

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

'''
@class CaptureImage
Cozmo takes a picture and uploads the image to Instagram
@author - Wizards of Coz
'''

class CaptureImage(WOC):
    def __init__(self, *a, **kw):
        WOC.__init__(self)

        cozmo.setup_basic_logging()
        cozmo.connect(self.run)

    async def run(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self.coz = await coz_conn.wait_for_robot()

        asyncio.ensure_future(self.start_program());

        while not self.exit_flag:
            await asyncio.sleep(0)
        self.coz.abort_all_actions()

    async def calc_pixel_threshold(self, image: Image):
        grayscale_image = image.convert('L')
        mean_value = np.mean(grayscale_image.getdata())
        return mean_value

    async def start_program(self):
        self.coz.camera.image_stream_enabled = True;
        await self.coz.set_lift_height(0).wait_for_completed();
        await self.coz.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE/4).wait_for_completed()
        self.cubes = None
        look_around = self.coz.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

        try:
            self.cubes = await self.coz.world.wait_until_observe_num_objects(3, object_type = cozmo.objects.LightCube,timeout=60)
        except asyncio.TimeoutError:
            print("Didn't find a cube :-(")
            return
        finally:
            look_around.stop()
            await self.coz.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE, in_parallel= True).wait_for_completed()
            self.cubes[0].set_lights(Colors.GREEN);
            self.cubes[1].set_lights(Colors.GREEN);
            self.cubes[2].set_lights(Colors.GREEN);
            self.coz.world.add_event_handler(cozmo.objects.EvtObjectTapped, self.on_object_tapped)

            self.face_dimensions = cozmo.oled_face.SCREEN_WIDTH, cozmo.oled_face.SCREEN_HALF_HEIGHT
            self.image_taken = False;
            while self.image_taken == False:
                latest_image = self.coz.world.latest_image
                if latest_image is not None:
                    duration_s = 0.1
                    await self.showImageOnFace(latest_image, duration_s);

                await asyncio.sleep(duration_s)

    async def showImageOnFace(self, image, duration_s):
        resized_image = image.raw_image.resize(self.face_dimensions, Image.BICUBIC)
        resized_image = resized_image.transpose(Image.FLIP_LEFT_RIGHT)
        pixel_threshold = await self.calc_pixel_threshold(resized_image)
        screen_data = cozmo.oled_face.convert_image_to_screen_data(resized_image, pixel_threshold=pixel_threshold)

        self.coz.display_oled_face_image(screen_data, duration_s * 1000.0)

    async def on_object_tapped(self, event, *, obj, tap_count, tap_duration, **kw):
        # print("Received	a	tap	event", event)
        # print("Received	a	tap	event", obj.object_id)
        self.image_taken = True;

        i = 0;
        while i < 3:
            for cube in self.cubes:
                cube.set_lights(cozmo.lights.green_light);
            await asyncio.sleep(0.2);
            for cube in self.cubes:
                cube.set_lights_off();
            await asyncio.sleep(0.2);
            i += 1

        await asyncio.sleep(1);

        for cube in self.cubes:
            cube.set_lights(cozmo.lights.red_light);

        image = self.coz.world.latest_image
        while image is None:
            await asyncio.sleep(0.1)
            image = self.coz.world.latest_image


        await self.showImageOnFace(image, 5);

        r_image = image.raw_image;
        img = r_image.convert('L')
        img.save("output.jpg")

        im = Image.open("output.jpg")
        pix = im.load()
        newImage = im.convert('RGB');
        pix2 = newImage.load();
        for i in range(0,im.width):
            for j in range(0,im.height):
                if pix[i,j] < 128:
                    pix2[i, j] = (0,0,255)
                else:
                    pix2[i, j] = (0, 0, 0)
        newImage.save("new.jpg");

        insta = InstagramAPI("wizardsofcoz", "Wizards!!")
        insta.login() # login
        insta.uploadPhoto("output.jpg");

        for cube in self.cubes:
            cube.set_lights(cozmo.lights.green_light)

        self.exit_flag = True;

if __name__ == '__main__':
    CaptureImage()
