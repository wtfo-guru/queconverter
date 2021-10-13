#
#  Copyright (C) 2011-2020 by Ihor E. Novikov
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

import os
import typing as tp

from . import qc3const
from .utils import sconfig
from .utils.mixutils import echo


class QCData:
  app: qc3const.AppHandle
  app_name: str = "QueConverter"
  app_proc: str = "queconverter"
  app_org: str = "wtfo-guru"
  app_domain: str = "wtfo-guru.com"
  app_icon = None
  doc_icon = None
  version: str = qc3const.VERSION
  revision: str = qc3const.REVISION
  build: str = qc3const.BUILD
  app_config: str = ""
  app_config_dir: str = ""
  app_color_profile_dir: str = ""

  def __init__(
    self, app: qc3const.AppHandle, cfgdir: str = "~", check: bool = True
  ) -> None:
    """Creates QC Data instance

    :param app: (QCApplication) QueConverter application handle
    :param cfgdir: (str) parent directory for '.config' folder
    :param check: (bool)
    """
    self.app = app
    self.app_config_dir = os.path.expanduser(os.path.join(cfgdir, ".config", "qc3-py3"))
    self.check_config_dirs() if check else None

  def check_config_dirs(self) -> None:
    """Checks config directories structure. If wrong, fixes them."""
    if not os.path.exists(self.app_config_dir):
      os.makedirs(self.app_config_dir)

    self.app_config = os.path.join(self.app_config_dir, "preferences.cfg")

    # Check color profiles directory
    self.app_color_profile_dir = os.path.join(self.app_config_dir, "profiles")
    if not os.path.exists(self.app_color_profile_dir):
      os.makedirs(self.app_color_profile_dir)

    from .cms import libcms

    for item in qc3const.COLORSPACES + [
      qc3const.COLOR_DISPLAY,
    ]:
      path = os.path.join(self.app_color_profile_dir, "built-in_%s.icm" % item)
      if not os.path.exists(path):
        libcms.cms_save_default_profile(path, item)


LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]

DEFAULT_RGB = "Built-in RGB profile"
DEFAULT_CMYK = "Built-in CMYK profile"
DEFAULT_LAB = "Built-in Lab profile"
DEFAULT_GRAY = "Built-in Grayscale profile"

INTENTS = {
  qc3const.INTENT_PERCEPTUAL: "PERCEPTUAL",
  qc3const.INTENT_RELATIVE_COLORIMETRIC: "RELATIVE_COLORIMETRIC",
  qc3const.INTENT_SATURATION: "SATURATION",
  qc3const.INTENT_ABSOLUTE_COLORIMETRIC: "ABSOLUTE_COLORIMETRIC",
  "PERCEPTUAL": qc3const.INTENT_PERCEPTUAL,
  "RELATIVE_COLORIMETRIC": qc3const.INTENT_RELATIVE_COLORIMETRIC,
  "SATURATION": qc3const.INTENT_SATURATION,
  "ABSOLUTE_COLORIMETRIC": qc3const.INTENT_ABSOLUTE_COLORIMETRIC,
}

BOOL_ATTRS = ("cms_use", "black_point_compensation", "black_preserving_transform")
INTENT_ATTRS = ("cms_rgb_intent", "cms_cmyk_intent")
PROFILES = (
  "cms_rgb_profile",
  "cms_cmyk_profile",
  "cms_lab_profile",
  "cms_gray_profile",
)
PROFILE_DICTS = (
  "cms_rgb_profiles",
  "cms_cmyk_profiles",
  "cms_lab_profiles",
  "cms_gray_profiles",
)

class QCConfig(sconfig.SerializedConfig):
  """Represents QCApplication config"""

  # ============== GENERIC SECTION ===================
  log_level: str = "INFO"

  # ============== COLOR MANAGEMENT SECTION ===================

  cms_use: bool = True
  cms_display_profiles: tp.Dict = {}
  cms_rgb_profiles: tp.Dict = {}
  cms_cmyk_profiles: tp.Dict = {}
  cms_lab_profiles: tp.Dict = {}
  cms_gray_profiles: tp.Dict = {}

  cms_rgb_profile: str = ""
  cms_cmyk_profile: str = ""
  cms_lab_profile: str = ""
  cms_gray_profile: str = ""
  cms_display_profile: str = ""

  cms_use_display_profile: bool = False

  cms_rgb_intent: int = qc3const.INTENT_RELATIVE_COLORIMETRIC
  cms_cmyk_intent: int = qc3const.INTENT_PERCEPTUAL

  cms_flags: int = qc3const.cmsFLAGS_NOTPRECALC
  cms_proofing: bool = False
  cms_gamutcheck: bool = False
  cms_alarmcodes: tp.List[float] = [1.0, 0.0, 1.0]
  cms_proof_for_spot: bool = False
  cms_bpc_flag: bool = False
  cms_bpt_flag: bool = False

  def __init__(self) -> None:
    self.defaults = QCConfig.__dict__.copy()

  def get_defaults(self) -> tp.Dict:
    """Returns default values of QCConfig class

    :return: dict of default field values
    """
    return self.defaults

  @staticmethod
  def to_bool(val):
    return "yes" if val else "no"

  def show(self):
    echo()
    echo("Globall preferences:\n")
    echo("  --log_level=%s" % self.log_level)
    echo()
    echo("Color Picker preferences:\n")
    echo()
    echo("  --cms_use=%s" % self.to_bool(self.cms_use))
    echo('  --cms_rgb_profile="%s"' % (self.cms_rgb_profile or DEFAULT_RGB))
    echo('  --cms_cmyk_profile="%s"' % (self.cms_cmyk_profile or DEFAULT_CMYK))
    echo('  --cms_lab_profile="%s"' % (self.cms_lab_profile or DEFAULT_LAB))
    echo('  --cms_gray_profile="%s"' % (self.cms_gray_profile or DEFAULT_GRAY))
    echo()
    echo('  --cms_rgb_intent="%s"' % INTENTS[self.cms_rgb_intent])
    echo('  --cms_cmyk_intent="%s"' % INTENTS[self.cms_cmyk_intent])
    echo()
    echo("  --black_point_compensation=%s" % self.to_bool(self.cms_bpc_flag))
    echo("  --black_preserving_transform=%s" % self.to_bool(self.cms_bpt_flag))
    echo()

  def change_config(self, options):
    if len(options) < 2:
      echo("Please provide configuration values to change.")
      return
    for key, value in options.items():
      if key in BOOL_ATTRS:
        QCConfig.__dict__[key] = bool(value)
      elif key == "log_level":
        if value in LEVELS:
          QCConfig.log_level = value
      elif key in INTENT_ATTRS:
        if isinstance(value, int) and value in INTENTS:
          QCConfig.__dict__[key] = value
        elif value in INTENTS:
          QCConfig.__dict__[key] = INTENTS[value]
      elif key in PROFILES and isinstance(value, str):
        if not value:
          QCConfig.__dict__[key] = ""
          continue
        cs = qc3const.COLORSPACES[PROFILES.index(key)]
        path = fsutils.normalize_path(value)
        if not fsutils.exists(path):
          echo('ERROR: file "%s" is not found!' % path)
          continue
        profile_name = cms.get_profile_name(path)
        if not profile_name:
          echo('ERROR: file "%s" is not valid color profile!' % path)
          continue
        profile_dir = self.app.appdata.app_color_profile_dir
        dest_path = os.path.join(profile_dir, "%s.icc" % cs)
        if fsutils.exists(dest_path):
          os.remove(dest_path)
        shutil.copy(path, dest_path)
        profile_dict = PROFILE_DICTS[PROFILES.index(key)]
        QCConfig.__dict__[profile_dict] = {profile_name: dest_path}
        QCConfig.__dict__[key] = profile_name
