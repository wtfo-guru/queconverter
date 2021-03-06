# -*- coding: utf-8 -*-
#
#  Copyright (C) 2015 by Igor E. Novikov
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

from qc3 import qc3const, cms
from qc3.formats.generic import TextModelPresenter
from qc3.formats.soc.soc_config import SOC_Config
from qc3.formats.soc.soc_filters import SOC_Loader, SOC_Saver
from qc3.formats.soc.soc_model import SOC_Palette
from qc3.qc3const import COLOR_RGB


class SOC_Presenter(TextModelPresenter):
  cid = qc3const.SOC

  config = None
  doc_file = ""
  resources = None
  cms = None

  def __init__(self, appdata, cnf=None, filepath=None):
    cnf = cnf or {}
    self.config = SOC_Config()
    config_file = os.path.join(appdata.app_config_dir, self.config.filename)
    self.config.load(config_file)
    self.config.update(cnf)
    self.appdata = appdata
    self.cms = self.appdata.app.default_cms
    self.loader = SOC_Loader()
    self.saver = SOC_Saver()
    self.new()
    if filepath:
      self.load(filepath)

  def new(self):
    self.model = SOC_Palette(self.config.source)
    self.update()

  def update(self, action=False):
    pass

  def convert_from_skp(self, skp_doc):
    skp_model = skp_doc.model
    soc = self.model
    soc.name = skp_model.name
    soc.columns = skp_model.columns
    soc.comments = ""
    if skp_model.source:
      soc.comments += "Palette source: " + skp_model.source + "\n"
    soc.comments += skp_model.comments
    soc.comments = soc.comments
    for item in skp_model.colors:
      color = self.cms.get_rgb_color(item)[1]
      rgb = cms.rgb_to_hexcolor(color)
      soc.colors.append([rgb, item[3]])

  def convert_to_skp(self, skp_doc):
    skp_model = skp_doc.model
    if self.doc_file:
      skp_model.name = os.path.basename(self.doc_file).replace(".soc", "")
      skp_model.name += " palette"
    else:
      skp_model.name = "SOC palette"
    skp_model.source = self.model.source
    skp_model.columns = self.model.columns
    skp_model.comments = self.model.comments
    if self.doc_file:
      filename = os.path.basename(self.doc_file)
      if skp_model.comments:
        skp_model.comments += "n"
      skp_model.comments += "Converted from %s" % filename

    for item in self.model.colors:
      rgb, name = item
      clr = cms.hexcolor_to_rgb(rgb)
      skp_model.colors.append([COLOR_RGB, clr, 1.0, name])
