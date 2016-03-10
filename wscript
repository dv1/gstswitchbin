#!/usr/bin/env python


from waflib.Build import BuildContext, CleanContext, InstallContext, UninstallContext, Logs

top = '.'
out = 'build'


def options(opt):
	opt.add_option('--enable-debug', action = 'store_true', default = False, help = 'enable debug build [default: %default]')
	opt.add_option('--with-package-name', action = 'store', default = "Unknown package release", help = 'specify package name to use in plugin [default: %default]')
	opt.add_option('--with-package-origin', action = 'store', default = "Unknown package origin", help = 'specify package origin URL to use in plugin [default: %default]')
	opt.add_option('--plugin-install-path', action = 'store', default = "${PREFIX}/lib/gstreamer-1.0", help = 'where to install the plugin for GStreamer 1.0 [default: %default]')
	opt.load('compiler_c')
	opt.load('gnu_dirs')


def configure(conf):
	import os

	conf.load('compiler_c')
	conf.load('gnu_dirs')

	conf.env['CFLAGS'] += ['-Wextra', '-Wall', '-std=c99', '-fPIC', '-DPIC']
	if conf.options.enable_debug:
		conf.env['CFLAGS'] += ['-O0', '-g3', '-ggdb']
	else:
		conf.env['CFLAGS'] += ['-O2']

	conf.check_cfg(package = 'gstreamer-1.0 >= 1.2.0', uselib_store = 'GSTREAMER', args = '--cflags --libs', mandatory = 1)
	conf.define('GST_PACKAGE_NAME', conf.options.with_package_name)
	conf.define('GST_PACKAGE_ORIGIN', conf.options.with_package_origin)
	conf.define('PACKAGE', "gstswitchbin")
	conf.define('VERSION', '1.0')

	conf.write_config_header('config.h')


def build(bld):
	bld(
		features = ['c', 'cshlib'],
		includes = ['.'],
		defines = ['HAVE_CONFIG_H'],
		uselib = ['GSTREAMER'],
		source = ['plugin.c', 'gstswitchbin.c'],
		target = 'gstswitchbin'
	)
