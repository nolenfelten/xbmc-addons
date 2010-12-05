## PyDocs Printer

import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import resources.lib.pydoc as pydoc


def _get_browse_dialog( default="", heading="", dlg_type=3, shares="files", mask="", use_thumbs=False, treat_as_folder=False ):
    """ 
        shows a browse dialog and returns a value
        - 0 : ShowAndGetDirectory
        - 1 : ShowAndGetFile
        - 2 : ShowAndGetImage
        - 3 : ShowAndGetWriteableDirectory
    """
    dialog = xbmcgui.Dialog()
    value = dialog.browse( dlg_type, heading, shares, mask, use_thumbs, treat_as_folder, default )
    return value

if ( __name__ == "__main__" ):
    # get Addon object
    Addon = xbmcaddon.Addon( id=os.path.basename( os.getcwd() ) )
    # get user prefered save location
    doc_path = Addon.getSetting( "doc_path" )
    # get location if none set
    if ( not doc_path ):
        doc_path = _get_browse_dialog( doc_path, Addon.getLocalizedString( 30110 ) )
    # if doc_path create html docs
    if ( doc_path ):
        # show feedback
        pDialog = xbmcgui.DialogProgress()
        pDialog.create( Addon.getAddonInfo( "Name" ) )
        # set the doc_path setting incase the browse dialog was used
        Addon.setSetting( "doc_path", doc_path )
        # get our document object
        doc = pydoc.HTMLDoc()
        # modules
        modules = [ "xbmc", "xbmcgui", "xbmcplugin", "xbmcaddon" ]
        # enumerate thru and print our help docs
        for count, module in enumerate( modules ):
            # set correct path
            _path = xbmc.validatePath( xbmc.translatePath( os.path.join( doc_path, "%s.html" % ( module, ) ) ) )
            # update dialog
            pDialog.update( count * ( 100 / len( modules ) ), Addon.getLocalizedString( 30711 ) % ( module + ".html PyDoc", ), Addon.getLocalizedString( 30712 ) % ( _path, ) )
            # print document
            try:
                open( _path, "w" ).write( doc.document( eval( module ) ) )
            except Exception, e:
                # oops
                xbmc.log( "An error occurred saving %s! (%s)" % ( module, e, ), xbmc.LOGERROR )
        #close dialog
        pDialog.update( 100 )
        pDialog.close()