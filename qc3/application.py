# -*- coding: utf-8 -*-
#
#  Copyright (C) 2012-2017 by Ihor E. Novikov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os
import sys
import argparse
import textwrap
import typing as tp

import qc3
from . import app_cms, events, msgconst, configure, translate
from .app_palettes import PaletteManager
from .qc3conf import QCData, QCConfig
from .utils.mixutils import echo, config_logging

LOG = logging.getLogger(__name__)

LOG_MAP: tp.Dict[int, tp.Callable] = {
  msgconst.JOB: LOG.info,
  msgconst.INFO: LOG.info,
  msgconst.OK: LOG.info,
  msgconst.WARNING: LOG.warning,
  msgconst.ERROR: LOG.error,
  msgconst.STOP: lambda *args: args,
}


class QCApplication:
  """Represents QueConverter application.
  The object exists during translation process only.
  """

  path: str
  config: QCConfig
  appdata: QCData
  default_cms: app_cms.AppColorManager
  palettes: PaletteManager
  log_filepath: str
  do_verbose: bool = False

  def __init__(self, path: str = "", cfgdir: str = "~", check: bool = True) -> None:
    """Creates QueConverter application instance.

    :param path: (str) current application path
    :param cfgdir: (str) path to '.config'
    :param check: (bool) config directory check flag
    """
    self.path = path
    cfgdir = os.path.expanduser(cfgdir)
    self.config = QCConfig()
    self.config.app = self
    self.appdata = QCData(self, cfgdir, check=check)
    self.config.load(self.appdata.app_config)
    self.log_filepath = os.path.join(self.appdata.app_config_dir, "qc3.log")
    setattr(qc3, "config", self.config)
    setattr(qc3, "appdata", self.appdata)

  def verbose(self, *args: tp.Union[int, str]) -> None:
    """Logging callable to write event message records

    :param args: (list) event message args
    """
    status = msgconst.MESSAGES[args[0]]
    LOG_MAP[args[0]](args[1])
    if self.do_verbose or args[0] in (msgconst.ERROR, msgconst.STOP):
      indent = " " * (msgconst.MAX_LEN - len(status))
      echo("%s%s| %s" % (status, indent, args[1]))
    if args[0] == msgconst.STOP:
      echo("For details see logs: %s\n" % self.log_filepath)

  def __mk_options(self) -> tp.Dict:
    options = {}
    options['dry-run'] = self.args.dry_run
    options['verbose'] = self.args.verbose > 0
    options['verbose-short'] = self.args.verbose_short
    options['recursive'] = self.args.recursive
    return options

  def __parse_args(self) -> tp.Optional[tp.NoReturn]:
    parser = argparse.ArgumentParser(
      prog="queconverter",
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent(
        """\
        Example: queconverter drawing.cgm drawing.svg
        """
      ),
    )
    parser.add_argument("files", nargs='*', default=[], help="specify files to convert")
    parser.add_argument(
      "-d",
      "--debug",
      action="count",
      dest="debug",
      default=0,
      help="increment debug level",
    )
    parser.add_argument(
      "--dry-run",
      action="store_true",
      dest="dry_run",
      default=False,
      help="specify dry run",
    )
    parser.add_argument(
      "--parts",
      "--components",
      action="store_true",
      dest="parts",
      default=False,
      help="show parts/components",
    )
    parser.add_argument(
      "--show-log",
      action="store_true",
      dest="show_log",
      default=False,
      help="show previous log",
    )
    parser.add_argument(
      "--package-dir",
      "--pkg-dir",
      action="store_true",
      dest="showdir",
      default=False,
      help="show package directory",
    )
    parser.add_argument(
      "--format",
      action="store",
      dest="format",
      default='',
      help="specify format of saved output",
    )
    parser.add_argument(
      "--log",
      "--log-level",
      action="store",
      dest="log_level",
      default=self.config.log_level, # TODO: add validation
      help="set log level",
    )
    parser.add_argument(
      "-r", "--recursive",
      action="store_true",
      dest="recursive",
      default=False,
      help="show config",
    )
    parser.add_argument(
      "--show-config",
      "--show-prefs",
      action="store_true",
      dest="showcfg",
      default=False,
      help="show config",
    )
    parser.add_argument(
      "--verbose-short",
      action="store_true",
      dest="verbose_short",
      default=False,
      help="specify short verbose wtf?",
    )
    parser.add_argument(
      "-v",
      "--verbose",
      action="count",
      dest="verbose",
      default=0,
      help="increment verbosity level",
    )
    parser.add_argument(
      "-V",
      "--version",
      action="store_true",
      dest="version",
      default=False,
      help="show version and exit",
    )

    self.args = parser.parse_args()

  def check_sys_args(self, current_dir: tp.Optional[str]) -> tp.Optional[tp.NoReturn]:
    """Checks system arguments before translation executed

    :param current_dir: (str|None) directory path where QueConverter command executed
    """
    self.__parse_args()

    if self.args.version:
      dt = self.appdata
      mark = "" if not dt.build else " build %s" % dt.build
      msg = "%s %s%s%s\n" % (dt.app_name, dt.version, dt.revision, mark)
      self.__show_short_help(msg)
      sys.exit(0)
    elif self.args.parts:
      self.__show_parts(self.appdata)
      sys.exit(0)
    elif self.args.show_log:
      log_filepath = os.path.join(self.appdata.app_config_dir, "qc3.log")
      with open(log_filepath, "r") as fileptr:
        echo(fileptr.read())
      sys.exit(0)
    elif self.args.showdir:
      echo(os.path.dirname(os.path.dirname(__file__)))
      sys.exit(0)
    elif self.args.showcfg:
      configure.show_config()
      sys.exit(0)
    # TODO: write configure support
    # elif cmds.check_args(cmds.CONFIG_CMDS):
    #   options = cmds.parse_cmd_args(current_dir)[1]
    #   cmds.normalize_options(options)
    #   cmds.change_config(options)
    #   self.config.save()
    #   sys.exit(0)

  def __reconcile_files(self, current_dir: tp.Optional[str]) -> tp.List[str]:
    files = []
    for item in self.args.files:
      if current_dir:
        if not os.path.dirname(item) or item.startswith('.'):
          item = os.path.join(current_dir, item)
      if item.startswith('~'):
        item = os.path.expanduser(item)
      files.append(os.path.abspath(item))
    if len(files) == 0:
      return None
    return files

  def get_translation_args(
    self,
    current_dir: tp.Optional[str],
  ) -> tp.Union[tp.NoReturn, tp.Tuple[tp.Callable, tp.List[str], tp.Dict]]:
    """Prepares QueConverter execution command, options, targets and destinations

    :param current_dir: (str|None) directory path where QueConverter command executed
    """
    current_dir = current_dir or os.getcwd()
    # files, options = cmds.parse_cmd_args(current_dir)
    files = self.__reconcile_files(current_dir)

    if not files:
      self.__show_short_help("File names are not provided!")
      sys.exit(1)
    elif len(files) == 1:
      msg = "Destination directory or file name is not provided!"
      self.__show_short_help(msg)
      sys.exit(1)

    options = self.__mk_options()
    if any(["*" in files[0], "?" in files[0]]):
      translate.wildcard_convert(self.appdata, files, options)
      if os.path.exists(files[1]):
        if not os.path.isdir(files[1]):
          msg = 'Destination directory "%s" is not a directory!'
          self.__show_short_help(msg % files[1])
          sys.exit(1)
      else:
        os.makedirs(files[1])
    elif len(files) > 2:
      translate.multiple_convert(self.appdata, files, options)
      if os.path.exists(files[-1]):
        if not os.path.isdir(files[-1]):
          msg = 'Destination directory "%s" is not a directory!'
          self.__show_short_help(msg % files[-1])
          sys.exit(1)
      else:
        os.makedirs(files[-1])
    elif not os.path.exists(files[0]):
      self.__show_short_help('Source file "%s" is not found!' % files[0])
      sys.exit(1)
    else:
      translate.convert(self.appdata, files, options)

  def __call__(self, current_dir: tp.Optional[str] = None) -> tp.NoReturn:
    """QueConverter translation callable.

    :param current_dir: (str|None) directory path where QueConverter command executed
    """
    self.check_sys_args(current_dir=current_dir)

    self.do_verbose = self.args.verbose > 0

    events.connect(events.MESSAGES, self.verbose)
    config_logging(
      filepath=self.log_filepath, level=self.args.log_level
    )

    self.default_cms = app_cms.AppColorManager(self)
    self.palettes = PaletteManager(self)

    # ------------ EXECUTION ----------------
    status = 0
    # noinspection PyBroadException
    try:
      self.get_translation_args(current_dir=current_dir)
    except Exception as ex:
      msg = str(ex)
      print(msg)
      LOG.error(msg)
      status = 1

    echo() if self.do_verbose else None
    sys.exit(status)

  @staticmethod
  def __show_short_help(msg):
    echo()
    echo(msg)
    echo("USAGE: queconverter [OPTIONS] [INPUT FILE] [OUTPUT FILE]")
    echo("Use --help for more details.")

  @staticmethod
  def __show_part(name, value):
    ALIGNMENT = 25
    value = value.replace("\n", "")
    msg = " " * 4 + name + "." * (ALIGNMENT - len(name)) + "[ %s ]" % value
    echo(msg)

  @staticmethod
  def __show_parts(appdata):
    echo()
    mark = "" if not appdata.build else " build %s" % appdata.build
    app_name = "%s %s%s%s" % (appdata.app_name, appdata.version, appdata.revision, mark)
    echo("%s components:\n" % app_name)
    part = ""
    try:
      part = "Python"
      QCApplication.__show_part(part, sys.version)

      part = "LCMS"
      from qc3 import cms

      QCApplication.__show_part(part, cms.libcms.get_version())

    except Exception as e:
      QCApplication.__show_part(part, "FAIL")
      echo("Reason: %s" % str(e))
    echo()

  @staticmethod
  def show_config():
    config = qc3.config
    echo()
    echo("Color Picker preferences:\n")
    echo("  --log_level=%s" % config.log_level)
    echo()
    echo("  --cms_use=%s" % to_bool(config.cms_use))
    echo('  --cms_rgb_profile="%s"' % (config.cms_rgb_profile or DEFAULT_RGB))
    echo('  --cms_cmyk_profile="%s"' % (config.cms_cmyk_profile or DEFAULT_CMYK))
    echo('  --cms_lab_profile="%s"' % (config.cms_lab_profile or DEFAULT_LAB))
    echo('  --cms_gray_profile="%s"' % (config.cms_gray_profile or DEFAULT_GRAY))
    echo()
    echo('  --cms_rgb_intent="%s"' % INTENTS[config.cms_rgb_intent])
    echo('  --cms_cmyk_intent="%s"' % INTENTS[config.cms_cmyk_intent])
    echo()
    echo("  --black_point_compensation=%s" % to_bool(config.cms_bpc_flag))
    echo("  --black_preserving_transform=%s" % to_bool(config.cms_bpt_flag))
    echo()
