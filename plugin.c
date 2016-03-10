#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "gstswitchbin.h"


static gboolean plugin_init(GstPlugin *plugin)
{
	gboolean ret = TRUE;
	ret = ret && gst_element_register(plugin, "switchbin", GST_RANK_NONE, gst_switch_bin_get_type());
	return ret;
}


GST_PLUGIN_DEFINE(
	GST_VERSION_MAJOR,
	GST_VERSION_MINOR,
	switchbin,
	"switchbin",
	plugin_init,
	VERSION,
	"LGPL",
	GST_PACKAGE_NAME,
	GST_PACKAGE_ORIGIN
)
