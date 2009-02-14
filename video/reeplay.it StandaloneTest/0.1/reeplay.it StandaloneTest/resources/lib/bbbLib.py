"""
 bbbLib.py

 General functions.

 Cutdown version for reeplay.it
 
"""

import sys, os.path
import xbmc, xbmcgui
import os, re, unicodedata, traceback
from string import strip, replace, find, rjust, capwords
from shutil import rmtree

__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__title__ = "bbbLib"
__author__ = 'BigBellyBilly [BigBellyBilly@gmail.com]'
__date__ = '10-02-2009'
xbmc.output("Imported From: " + __scriptname__ + " title: " + __title__ + " Date: " + __date__)

DIR_HOME = sys.modules[ "__main__" ].DIR_HOME
try:
	DIR_USERDATA = sys.modules[ "__main__" ].DIR_USERDATA
except:
	DIR_USERDATA = DIR_HOME
print "bbbLib() USER_DATA=" + DIR_USERDATA

# KEYPAD CODES
ACTION_UNKNOWN			= 0
ACTION_MOVE_LEFT 	    = 1 	# Dpad
ACTION_MOVE_RIGHT	    = 2		# Dpad
ACTION_MOVE_UP		    = 3		# Dpad
ACTION_MOVE_DOWN	    = 4		# Dpad
ACTION_SCROLL_UP		= 5		# trigger up
ACTION_SCROLL_DOWN		= 6		# trigger down
ACTION_A	            = 7     # A
ACTION_HIGHLIGHT_ITEM	= 8		#
ACTION_B	            = 9     # B
ACTION_BACK	            = 10	# back btn
ACTION_X 	            = 18    # X
ACTION_Y 	            = 34	# Y
ACTION_LEFT_TRIGGER		= 111	# trigger left
ACTION_RIGHT_TRIGGER	= 112	# trigger right
ACTION_WHITE	        = 117	# white button
ACTION_LEFT_STICK       = 85   # left stick clicked in
ACTION_RIGHT_STICK      = 122   # right stick clicked in
ACTION_RIGHT_STICK_UP	= 88
ACTION_RIGHT_STICK_DOWN	= 89
ACTION_RIGHT_STICK_RIGHT= 124
ACTION_RIGHT_STICK_LEFT	= 125

PAD_A                        = 256
PAD_B                        = 257
PAD_X                        = 258
PAD_Y                        = 259
PAD_BLACK                    = 260
PAD_WHITE                    = 261
PAD_LEFT_TRIGGER             = 262
PAD_RIGHT_TRIGGER            = 263
PAD_LEFT_STICK              = 264
PAD_RIGHT_STICK             = 265
PAD_RIGHT_STICK_UP          = 266 # right thumb stick directions
PAD_RIGHT_STICK_DOWN        = 267 # for defining different actions per direction
PAD_RIGHT_STICK_LEFT        = 268
PAD_RIGHT_STICK_RIGHT       = 269
PAD_DPAD_UP                  = 270
PAD_DPAD_DOWN                = 271
PAD_DPAD_LEFT                = 272
PAD_DPAD_RIGHT               = 273
PAD_START                    = 274
PAD_BACK                     = 275
PAD_LEFT_STICK              = 276
PAD_RIGHT_STICK             = 277
PAD_LEFT_ANALOG_TRIGGER      = 278
PAD_RIGHT_ANALOG_TRIGGER    = 279
PAD_LEFT_STICK_UP           = 280 # left thumb stick  directions
PAD_LEFT_STICK_DOWN         = 281 # for defining different actions per direction
PAD_LEFT_STICK_LEFT         = 282
PAD_LEFT_STICK_RIGHT        = 283

ACTION_REMOTE_MENU          = 8
ACTION_REMOTE_PAUSE		    = 25
ACTION_REMOTE_BACK			= 39
ACTION_REMOTE_DISPLAY       = 42
ACTION_REMOTE_STOP		    = 31
ACTION_REMOTE_NEXT_ITEM	    = 32	# remote Skip Next
ACTION_REMOTE_PREV_ITEM	    = 34	# remote Skip Previous
ACTION_REMOTE_LEFT          = 86
ACTION_REMOTE_RIGHT         = 87
ACTION_REMOTE_DOWN          = 88
ACTION_REMOTE_UP            = 89   

REMOTE_LEFT             = (169, 86, )
REMOTE_RIGHT            = (168, 87, )
REMOTE_UP               = (166, 89, )
REMOTE_DOWN             = (167, 88, )
REMOTE_INFO             = (195, 60, )
REMOTE_BACK			    = (216, 39, )
REMOTE_SELECT           = 11
REMOTE_PLAY             = (234, 79, )
REMOTE_TITLE            = (229, 26, )

KEYBOARD_LEFT          = 61477 
KEYBOARD_UP            = 61478 
KEYBOARD_RIGHT         = 61479 
KEYBOARD_DOWN          = 61480
KEYBOARD_PLUS          = 61627 
KEYBOARD_PG_UP         = 61473 
KEYBOARD_PG_DOWN        = 61474
KEYBOARD_INSERT         = 61485
KEYBOARD_X              = 61528
KEYBOARD_A              = 61505
KEYBOARD_B              = 61506
KEYBOARD_Y              = 61529
KEYBOARD_NUM_PLUS       = 61547
KEYBOARD_NUM_MINUS      = 61549
KEYBOARD_ESC            = 61467
KEYBOARD_RETURN         = 61453
KEYBOARD_HOME           = 61476


# CODE GROUPS
CLICK_A = ( ACTION_A, PAD_A, KEYBOARD_A, KEYBOARD_RETURN, REMOTE_SELECT, )
CLICK_B = ( ACTION_B, PAD_B, KEYBOARD_B, ) + REMOTE_BACK
CLICK_X = ( ACTION_X, PAD_X, KEYBOARD_X, )
CLICK_Y = ( ACTION_Y, PAD_Y, KEYBOARD_Y, )
SELECT_ITEM = CLICK_A
EXIT_SCRIPT = ( ACTION_BACK, PAD_BACK, ACTION_REMOTE_MENU, KEYBOARD_ESC, )
CANCEL_DIALOG = CLICK_B
CONTEXT_MENU = ( ACTION_WHITE, PAD_WHITE, KEYBOARD_HOME, ) + REMOTE_INFO
LEFT_STICK_CLICK = (ACTION_LEFT_STICK, PAD_LEFT_STICK, )
RIGHT_STICK_CLICK = (ACTION_RIGHT_STICK, PAD_RIGHT_STICK, )
MOVEMENT_DPAD = ( ACTION_MOVE_LEFT, ACTION_MOVE_RIGHT, ACTION_MOVE_UP, ACTION_MOVE_DOWN, )
MOVEMENT_RIGHT_STICK = (PAD_RIGHT_STICK_UP, PAD_RIGHT_STICK_DOWN, PAD_RIGHT_STICK_LEFT, PAD_RIGHT_STICK_RIGHT, ACTION_RIGHT_STICK_UP,ACTION_RIGHT_STICK_DOWN,ACTION_RIGHT_STICK_LEFT,ACTION_RIGHT_STICK_RIGHT, )
MOVEMENT_LEFT_STICK = (PAD_LEFT_STICK_UP, PAD_LEFT_STICK_DOWN, PAD_LEFT_STICK_LEFT, PAD_LEFT_STICK_RIGHT, )
MOVEMENT_STICKS = MOVEMENT_RIGHT_STICK + MOVEMENT_LEFT_STICK
MOVEMENT_SCROLL_UP = ( ACTION_LEFT_TRIGGER, PAD_LEFT_ANALOG_TRIGGER, ACTION_SCROLL_UP, KEYBOARD_PG_UP, PAD_LEFT_TRIGGER, ACTION_REMOTE_PREV_ITEM, )
MOVEMENT_SCROLL_DOWN = ( ACTION_RIGHT_TRIGGER, PAD_RIGHT_ANALOG_TRIGGER, ACTION_SCROLL_DOWN, KEYBOARD_PG_DOWN, PAD_RIGHT_TRIGGER, ACTION_REMOTE_NEXT_ITEM, )
MOVEMENT_SCROLL = MOVEMENT_SCROLL_UP + MOVEMENT_SCROLL_DOWN
MOVEMENT_KEYBOARD = ( KEYBOARD_LEFT, KEYBOARD_UP, KEYBOARD_RIGHT, KEYBOARD_DOWN, KEYBOARD_PG_UP, KEYBOARD_PG_DOWN, )
MOVEMENT_REMOTE = REMOTE_LEFT + REMOTE_RIGHT + REMOTE_UP + REMOTE_DOWN + (ACTION_REMOTE_NEXT_ITEM, ACTION_REMOTE_PREV_ITEM, )
MOVEMENT_UP = ( ACTION_MOVE_UP, PAD_LEFT_STICK_UP, PAD_RIGHT_STICK_UP, PAD_DPAD_UP, KEYBOARD_UP, ACTION_RIGHT_STICK_UP,) + REMOTE_UP
MOVEMENT_DOWN = ( ACTION_MOVE_DOWN, PAD_LEFT_STICK_DOWN,PAD_RIGHT_STICK_DOWN, PAD_DPAD_DOWN, KEYBOARD_DOWN, ACTION_RIGHT_STICK_DOWN, ) + REMOTE_DOWN
MOVEMENT_LEFT = ( ACTION_MOVE_LEFT, PAD_LEFT_STICK_LEFT, PAD_RIGHT_STICK_LEFT,PAD_DPAD_LEFT, KEYBOARD_LEFT, ACTION_RIGHT_STICK_LEFT,) + REMOTE_LEFT
MOVEMENT_RIGHT = (  ACTION_MOVE_RIGHT, PAD_LEFT_STICK_RIGHT, PAD_RIGHT_STICK_RIGHT, PAD_DPAD_RIGHT, KEYBOARD_RIGHT, ACTION_RIGHT_STICK_RIGHT, ) + REMOTE_RIGHT
MOVEMENT = MOVEMENT_UP + MOVEMENT_DOWN + MOVEMENT_LEFT + MOVEMENT_RIGHT + MOVEMENT_SCROLL + MOVEMENT_KEYBOARD

XBFONT_LEFT       = 0x00000000
XBFONT_RIGHT      = 0x00000001
XBFONT_CENTER_X   = 0x00000002
XBFONT_CENTER_Y   = 0x00000004
XBFONT_TRUNCATED  = 0x00000008

KBTYPE_ALPHA = -1
KBTYPE_NUMERIC = 0
KBTYPE_DATE = 1
KBTYPE_TIME = 2
KBTYPE_IP = 3
KBTYPE_SMB = 4      # not a real kbtype, just a common value
KBTYPE_YESNO = 5    # not a real kbtype, just a common value

# xbmc skin FONT NAMES
FONT10 = 'font10'
FONT11 = 'font11'
FONT12 = 'font12'
FONT13 = 'font13'
FONT14 = 'font14'
FONT16 = 'font16'
FONT18 = 'font18'
FONT_SPECIAL_10 = 'special10'
FONT_SPECIAL_11 = 'special11'
FONT_SPECIAL_12 = 'special12'
FONT_SPECIAL_13 = 'special13'
FONT_SPECIAL_14 = 'special14'
ALL_FONTS = (FONT10,FONT11,FONT12,FONT13,FONT14,FONT16,FONT18,FONT_SPECIAL_10,FONT_SPECIAL_11,FONT_SPECIAL_12,FONT_SPECIAL_13,FONT_SPECIAL_14,)

REGEX_URL_PREFIX = '^((?:http://|www).+?)[/?]'

global dialogProgress
dialogProgress = xbmcgui.DialogProgress()

#######################################################################################################################    
# DEBUG - display indented information
#######################################################################################################################    
DEBUG = True
debugIndentLvl = 0	# current indentation level
def debug( value ):
	global debugIndentLvl
	if (DEBUG and value):
		try:
			if find(value,">") >= 0: debugIndentLvl += 2
			pad = rjust("", debugIndentLvl)
			print pad + str(value)
			if find(value,"<") >= 0: debugIndentLvl -= 2
		except:
			try:
				print value
			except:
				print "Debug() Bad chars in string"

#################################################################################################################
def messageOK(title='', line1='', line2='',line3=''):
#	debug("%s\n%s\n%s\n%s" % (title, line1,line2,line3))
	xbmcgui.Dialog().ok(title ,line1,line2,line3)

#################################################################################################################
def handleException(txt=''):
	try:
		title = "EXCEPTION: " + txt
		e=sys.exc_info()
		list = traceback.format_exception(e[0],e[1],e[2],3)
		text = ''
		for l in list:
			text += l
		traceback.print_exc()
		messageOK(title, text)
	except: pass

#############################################################################################################
def makeDir(dir):
	try:
		d = xbmc.translatePath(dir)
		os.makedirs( d )
		debug("bbbLib.makeDir() " + d)
		return True
	except:
		return False

#############################################################################################################
def removeDir(dir, title="", msg="", msg2="", force=False):
	if force or xbmcgui.Dialog().yesno(title, msg, msg2):
		try:
			d = xbmc.translatePath(dir)
			rmtree(d, ignore_errors=True)
			debug("bbbLib.removeDir() " + d)
		except: pass
	
#################################################################################################################
# delete a single file
def deleteFile(filename):
	try:
		f = xbmc.translatePath(filename)
		os.remove( f )
		debug("bbbLib.deleteFile() " + f)
	except: pass

#################################################################################################################
def readFile(filename):
	try:
		f = xbmc.translatePath(filename)
		debug("bbbLib.readFile() " + f)
		return file(f).read()
	except:
		return ""

#################################################################################################################
def fileExist(filename):
	exists = False
	try:
		f = xbmc.translatePath(filename)
		if os.path.isfile(f) and os.path.getsize(f) > 0:
			exists = True
	except: pass
	debug("bbbLib.fileExist() %s  %s" % (f, exists))
	return exists

##############################################################################################
def doKeyboard(currentValue='', heading='', kbType=KBTYPE_ALPHA, hidden=False):
	debug("doKeyboard() kbType=%s" % kbType)
	if currentValue == None:
		currentValue = ''
	value = currentValue
	if kbType == KBTYPE_ALPHA:
		keyboard = xbmc.Keyboard(currentValue, heading, hidden)
		keyboard.doModal()
		if keyboard.isConfirmed:
			value = keyboard.getText().strip()
		else:
			value = None
	else:
		d = xbmcgui.Dialog()
		value = d.numeric(kbType, heading, currentValue)

	return value

#################################################################################################################
def ErrorCode(e):
	debug("> ErrorCode()")
	print "except=%s" % e
	if hasattr(e, 'code'):
		code = e.code
	else:
		try:
			code = e[0]
		except:
			code = 'Unknown'
	title = 'Error, Code: %s' % code

	if hasattr(e, 'reason'):
		txt = e.reason
	else:
		try:
			txt = e[1]
		except:
			txt = e
	messageOK(title, str(txt))
	debug("< ErrorCode()")

#################################################################################################################
# Convert a text string containing &#x<hex_value> to ascii ch
#################################################################################################################
def urlTextToASCII(text):
	if not text: return ""
	try:
		compile_obj = re.compile('(&#x(.*?);)',  re.IGNORECASE + re.MULTILINE + re.DOTALL)
		match_obj = compile_obj.findall(text)
		for match in match_obj:
			ch = chr(int('0x'+match[1], 16))
			text = text.replace(match[0], ch)

		compile_obj = re.compile('(&#(\d+);)',  re.IGNORECASE + re.MULTILINE + re.DOTALL)
		match_obj = compile_obj.findall(text)
		for match in match_obj:
			ch = chr(int(match[1]))
			text = text.replace(match[0], ch)
	except:
		debug("bbbLib.urlTextToASCII() exception")
	return text


#################################################################################################################
# Thanks to Arboc for this
#################################################################################################################
def unicodeToAscii(text, charset='utf8'):
	if not text: return ""
	try:
		newtxt = text.decode(charset)
		newtxt = unicodedata.normalize('NFKD', newtxt).encode('ASCII','replace')
		return newtxt
	except:
		return text

######################################################################################
def loadFileObj( filename, dataType={} ):
    debug( "loadFileObj() " + filename)
    try:
        file_handle = open( xbmc.translatePath(filename), "r" )
        loadObj = eval( file_handle.read() )
        file_handle.close()
    except:
        # reset to empty according to dataType
        if isinstance(dataType, dict):
            loadObj = {}
        elif isinstance(dataType, list) or isinstance(dataType, tuple):
            loadObj = ()
        else:
            loadObj = None
    return loadObj

######################################################################################
def saveFileObj( filename, saveObj ):
    debug( "saveFileObj() " + filename)
    try:
        file_handle = open( xbmc.translatePath(filename), "w" )
        file_handle.write( repr( saveObj ) )
        file_handle.close()
    except:
        handleException( "_save_file_obj()" )


#################################################################################################################
def getReadmeFilename(home_dir=""):
    debug("> getReadmeFilename() home_dir=" + home_dir)
    filename = "readme.txt"
    base_path, language = getLanguagePath(home_dir)
    fn = bbbTranslatePath( [base_path, language, filename] )
    if not fileExist( fn ):
        fn = bbbTranslatePath( [base_path, "English", filename] )
        if not fileExist( fn ):
            fn = ''
    debug("< getReadmeFilename() %s" % fn)
    return fn

##############################################################################################################    
def getLanguagePath(home_dir=""):
	debug("> getLanguagePath() home_dir=" + home_dir)
	try:
		if not home_dir:
			home_dir = os.getcwd().replace(';','')
		base_path = bbbTranslatePath( [home_dir, 'resources', 'language'] )
		language = capwords(xbmc.getLanguage())
		debug("xbmc language=" + language)
		langPath = "/".join( base_path, language )
		if not os.path.isdir(langPath):
			debug("getLanguagePath() DIR not exist: " + langPath)
			raise
	except:
		traceback.print_exc()
		language = 'English'
	debug("< getLanguagePath() path=%s lang=%s" % ( base_path, language ))
	return base_path, language

#############################################################################################################
# pluginType = music, video, pictures
def installPlugin(pluginType, name='', okMsg="In plugins 'Add Source' to complete installation."):
	debug("> installPlugin() %s %s"  % (pluginType, name))
	install = False
	if not name:
		name = __scriptname__

	try:
		copyFromPath = bbbTranslatePath( [DIR_HOME, "Plugin"] )
		copyFromFile = "/".join( [copyFromPath, 'default.py'] )
		debug("copyFromFile=" + copyFromFile)

		copyToPath = bbbTranslatePath( ["Q:", "plugins", pluginType, name] )
#		copyToPath = bbbTranslatePath( ["special://xbmc", "plugins", pluginType, name] )
		copyToFile = "/".join( [copyToPath, 'default.py'] )
		debug("copyToFile=" + copyToFile)

		# set not exist if; path/file missing or previous installed is older
		copyFromFileSecs = os.path.getmtime(copyFromFile)
		copyToFileSecs = os.path.getmtime(copyToFile)
		debug( "comparing fromSecs %d  toSecs %d"  % (copyFromFileSecs, copyToFileSecs))
		install = (copyFromFileSecs > copyToFileSecs)
	except:
		debug( "dest path not exist" )
		print  str(sys.exc_info()[ 1 ])
		install = True

	if install:
		try:
			from shutil import copytree, rmtree
			try:
				rmtree( copyToPath,ignore_errors=True )
			except: pass
			copytree( copyFromPath, copyToPath )
			debug("Plugin installed OK")
			messageOK(__scriptname__, okMsg, pluginType + ": " + name)
		except:
			traceback.print_exc()
			msg = "Plugin install Failed\n" + str(sys.exc_info()[ 1 ])
			messageOK(__scriptname__, msg)

	debug("< installPlugin() install=%s" % install)
	return install

##############################################################################################################    
def playMedia(source, li=None):
	debug("> playMedia()")
	isPlaying = False

	try:
		if li:
			debug("player source fn/url with li")
			xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(source, li)
		else:
			debug("player source PlayList")
			xbmc.Player().play(source)
		isPlaying = xbmc.Player().isPlaying()
	except:
		traceback.print_exc()
		debug('xbmc.Player().play() failed trying xbmc.PlayMedia() ')
		try:
			cmd = 'xbmc.PlayMedia(%s)' % source
			xbmc.executebuiltin(cmd)
			isPlaying = True
		except:
			handleException('playMedia()')

	debug("< playMedia() isPlaying=%s" % isPlaying)
	return isPlaying

##############################################################################################################    
def logFreeMem(msg=""):
    mem = xbmc.getFreeMem()
    debug( "Freemem=%sMB  %s" % (mem, msg))
    return mem

#################################################################################################################
def searchRegEx(data, regex, flags=re.IGNORECASE):
	try:
		value = re.search(regex, data, flags).group(1)
	except:
		value = ""
	return value

#################################################################################################################
def findAllRegEx(data, regex, flags=re.MULTILINE+re.IGNORECASE+re.DOTALL):
	try:
		matchList = re.compile(regex, flags).findall(data)
	except:
		matchList = []

	if matchList:
		sz = len(matchList)
	else:
		sz = 0
	debug ("findAllRegEx() matches=%s" % sz)
	return matchList

##############################################################################################################
def saveData(data, fn, mode="w"):
    """ Save data to a file """
    if not data or not fn or not mode: return False
    debug("saveData() fn=%s" % fn)
    try:
        f = open(xbmc.translatePath(fn), mode)
        f.write(data)
        f.flush()
        f.close()
        del f
        return True
    except:
        traceback.print_exc()
        return False

######################################################################################
def bbbTranslatePath(partsList):
    return xbmc.translatePath( "/".join(partsList) )