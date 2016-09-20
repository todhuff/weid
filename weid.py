#!/usr/bin/python
#
# Simple program to display security cameras.

# I could import from packages and save some typing, but I prefer to
# have code that anyone can look at, and know what package a function,
# class, object, etc. is from sight. You'll thank me later.
import pygame, urllib2, StringIO, sys, os, datetime, base64, configobj, multiprocessing, time

def str2bool(i):
  return i.lower() in ("yes", "true", "t", "y", "1")

class Camera(pygame.sprite.Sprite):
  """Each camera is a sprite, so we can manipulate it in later revisions"""
  def __init__(
        self, screen, img_filename,
        username, password, authentication,
        scale, scale_x, scale_y, pos_x, pos_y,
        enabled, sleep, show_errors ):
    """ Create a new Camera object.

         screen:
            The screen on which the camera lives (must be a
            pygame Surface object, such as pygame.display)

        img_filaneme:
            Image file (URL) for the camera.
    """
    pygame.sprite.Sprite.__init__(self)
    self.img_filename = img_filename
    self.password = password
    self.username = username
    self.authentication = authentication
    self.image = pygame.image.load(error_image)
    self.image = self.image.convert()
    self.scale = scale
    self.scale_x = scale_x
    self.scale_y = scale_y
    self.screen = screen
    self.oldimage = ''
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.enabled = enabled
    self.sleep = sleep
    self.show_errors = show_errors
    
  def update(self, counter, f):
    """ Update the camera.
    """
    self.oldimage = self.image
    try:
      self.image = pygame.image.load(f[counter])
    except pygame.error, message:
      print ("Pygame Error: Cannot load image: Camera %d" % counter)
      print ("Resource: {0}".format(self.img_filename))
      #print ("Username: {0}".format(self.username))
      #print ("Password: {0}".format(self.password))
      #print (" ")
      if self.show_errors:
        self.image = pygame.image.load(error_image)
      else:
        self.image = self.oldimage

    if self.scale:
      self.image = pygame.transform.scale(self.image, (self.scale_x, self.scale_y))
    self.image = self.image.convert()
    self.image_w, self.image_h = self.image.get_size()
    bounds_rect = self.screen.get_rect().inflate(-self.image_w, -self.image_h)
    if self.pos_x < bounds_rect.left:
        self.pos_x = bounds_rect.left
    elif self.pos_x > bounds_rect.right:
        self.pos_x = bounds_rect.right
    elif self.pos_y < bounds_rect.top:
        self.pos_y = bounds_rect.top
    elif self.pos_y > bounds_rect.bottom:
        self.pos_y = bounds_rect.bottom

  def loadimage(self,i):
    try:
      f = self.image
      #print ("URL = %s" % self.img_filename)
      request = urllib2.Request(self.img_filename)
      if self.authentication:
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
    except:
      print (" ")
      print ("Unknown error setting up request")
      print ("Resource: {0}".format(self.img_filename))
      print ("Username: {0}".format(self.username))
      print ("Password: (Hidden)")
      print (" ")
      if self.show_errors:
        f = pygame.image.load(error_image)
    try:
      f = StringIO.StringIO(urllib2.urlopen(request,None,5).read())
    except urllib2.URLError, e:
      print ("URLError: Cannot load image:", e.reason)
      print ("Resource: {0}".format(self.img_filename))
      print ("Username: {0}".format(self.username))
      print ("Password: (Hidden)")
      print (" ")
      if self.show_errors:
        f = pygame.image.load(error_image)
    except urllib2.HTTPError, e:
      print ("HTTPError: Cannot load image:", e.code)
      print ("Resource: {0}".format(self.img_filename))
      print ("Username: {0}".format(self.username))
      print ("Password: (Hidden)")
      print (" ")
      if self.show_errors:
        f = pygame.image.load(error_image)
    except:
      print ("Unknown error loading image")
      print ("Resource: {0}".format(self.img_filename))
      print ("Username: {0}".format(self.username))
      print ("Password: (Hidden)")
      print (" ")
      if self.show_errors:
        f = pygame.image.load(error_image)
    return(f)
  
  def blitter(self, draw_box):
      """ Blit the camera onto the screen that was provided in
          the constructor.
      """
      # The camera image is placed at self.pos.
      # To allow for smooth movement even when the camera rotates
      # and the image size changes, its placement is always
      # centered.
      #
      draw_pos = self.image.get_rect().move(
          self.pos_x - self.image_w / 2, 
          self.pos_y - self.image_h / 2)
      self.screen.blit(self.image, draw_pos)
      if draw_box :
        pygame.draw.rect(screen, (255,88,88),
        ((self.pos_x - self.image_w / 2),
        (self.pos_y - self.image_h / 2),
        self.image_w,self.image_h),1)

  #------------------ PRIVATE PARTS ------------------#

def _worker(i, mycamera, ns):
  while ns.is_running is True:
    image = mycamera.loadimage(i)
    f = ns.f
    f[i] = image
    ns.f = f
    time.sleep(mycamera.sleep)
  # Exit here.

if __name__ == '__main__':
  if not pygame.font: print ('Warning, fonts disabled')
  if not pygame.mixer: print ('Warning, sound disabled')
  pygame.init()
  pygame.mouse.set_visible(0)
  options = configobj.ConfigObj(r"/etc/weid/options", stringify = False)
  cameras_config = configobj.ConfigObj(r"/etc/weid/cameras")#, stringify = False)
  camera_names = cameras_config['Active']['Cameras']
  print ("Cameras: {0}".format(camera_names))
  cameras = []
  cameras_x = []
  cameras_y = []
  cameras_authentication = []
  cameras_user = []
  cameras_password = []
  cameras_scale = []
  cameras_scale_x = []
  cameras_scale_y = []
  cameras_enabled = []
  cameras_sleep = []
  cameras_show_errors = []
  for i in camera_names:
    cameras.append(str(cameras_config[i]['URL']))
    cameras_x.append(int(cameras_config[i]['X_Position']))
    cameras_y.append(int(cameras_config[i]['Y_Position']))
    cameras_authentication.append(bool(str2bool(cameras_config[i]['Authentication'])))
    cameras_user.append(str(cameras_config[i]['Username']))
    cameras_password.append(str(cameras_config[i]['Password']))
    cameras_scale.append(bool(str2bool(cameras_config[i]['Scaled'])))
    cameras_scale_x.append(int(cameras_config[i]['X_Scale']))
    cameras_scale_y.append(int(cameras_config[i]['Y_Scale']))
    cameras_enabled.append(bool(str2bool(cameras_config[i]['Enabled'])))
    cameras_sleep.append(float(cameras_config[i]['Sleep']))
    cameras_show_errors.append(bool(str2bool(cameras_config[i]['Show_Errors'])))
  # Variables used for camera selection and manipulation
  selected = 0 # Current camera bein manipulated
  edit_mode = 0

  clock = pygame.time.Clock()
  state = 1
  BG_COLOR = 1
  # Tagline config
  if options['Tagline']['Enabled']:
    font = pygame.font.Font(options['Tagline']['Font'], int(options['Tagline']['Font_Size']))
    tagline_text = font.render(options['Tagline']['Format'], True, map(int, options['Tagline']['Colour']))
  # Date / Time config
  if options['Time']['Enabled']:
    time_font = pygame.font.Font(options['Time']['Font'], int(options['Time']['Font_Size']))
  error_image = options['Defaults']['Error_Image']
  # Are we running under X?
  disp_no = os.getenv('DISPLAY')
  if disp_no:
    print ("Running under X. DISPLAY = {0}".format(disp_no))
  # Load the first / best available display driver.
  drivers = ['directfb', 'fbcon', 'svgalib']
  for driver in drivers:
    if not os.getenv('SDL_VIDEODRIVER'):
      os.putenv('SDL_VIDEODRIVER',driver)
    try:
      pygame.display.init()
    except pygame.error:
      print ("Driver {0} failed to load.".format(driver))
      continue
    found = True
    break
  if not found:
    raise Exception('No suitable video driver available!')
  size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
  screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
  camera_url = []
  manage = multiprocessing.Manager()
  ns = manage.Namespace()
  ns.is_running = True
  num_cameras=cameras.__len__()
  f = []
  for i in range(num_cameras):
    f.append(0)
  ns.f = f
  pool = multiprocessing.Pool(num_cameras)
  for i in range(cameras.__len__()):
    camera_url.append(Camera(screen,
      cameras[i],
      cameras_user[i],
      cameras_password[i],
      cameras_authentication[i],
      cameras_scale[i],
      cameras_scale_x[i],
      cameras_scale_y[i],
      cameras_x[i],
      cameras_y[i],
      cameras_enabled[i],
      cameras_sleep[i],
      cameras_show_errors[i]))
      
    pool.apply_async(_worker, args = (i,camera_url[i],ns,))
  
  print ("Entering main loop...")
  screen.fill(BG_COLOR)
  time.sleep(2)
  while True:
    for event in pygame.event.get() :
      if event.type == pygame.QUIT :
        print ("Quitting.")
        ns.is_running = False
        pool.close()
        pool.join()
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYUP : 
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q :
          print ("Exiting.")
          ns.is_running = False
          pool.close()
          pool.join()
          pygame.quit()
          sys.exit()
        elif event.key == pygame.K_KP_PLUS and edit_mode == 1 :
          selected = selected + 1
          if selected > len(camera_url)-1 :
            selected = 0
        elif event.key == pygame.K_KP_MINUS and edit_mode == 1 :
          selected = selected - 1
          if selected < 0 :
            selected = len(camera_url)-1
        elif event.key == pygame.K_RIGHT and edit_mode == 1 :
          camera_url[selected].pos_x = camera_url[selected].pos_x + 15
        elif event.key == pygame.K_LEFT and edit_mode == 1 :
          camera_url[selected].pos_x = camera_url[selected].pos_x - 15
        elif event.key == pygame.K_UP and edit_mode == 1 :
          camera_url[selected].pos_y = camera_url[selected].pos_y - 15
        elif event.key == pygame.K_DOWN and edit_mode == 1 :
          camera_url[selected].pos_y = camera_url[selected].pos_y + 15
        elif event.key ==pygame.K_e:
          edit_mode = 1 - edit_mode      
    # Redraw the background
    screen.fill(BG_COLOR)
    # Update and redraw all cameras
    counter = -1
    for i in camera_url:
      counter = counter + 1
      draw_box = 0
      if counter == selected and edit_mode == 1:
        draw_box = 1
      i.update(counter,ns.f)
      i.blitter(draw_box)
    # Tagline
    if options['Tagline']['Enabled']:
      screen.blit(tagline_text, (int(options['Tagline']['X_Position']), int(options['Tagline']['Y_Position'])))
    # Time / date display
    if options['Time']['Enabled']:
      current_time = datetime.datetime.now()
      time_text = time_font.render(current_time.strftime(options['Time']['Format']), True, map(int, options['Time']['Colour']))
      screen.blit(time_text, (int(options['Time']['X_Position']), int(options['Time']['Y_Position'])))
    pygame.display.flip()
