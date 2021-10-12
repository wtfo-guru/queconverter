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

from qc3 import qc3const
from qc3.formats.generic import TextModelPresenter
from qc3.formats.skp.skp_config import SKP_Config
from qc3.formats.skp.skp_filters import SKP_Loader, SKP_Saver
from qc3.formats.skp.skp_model import SK1Palette


class SKP_Presenter(TextModelPresenter):
  cid = qc3const.SKP

  config = None
  doc_file = ""
  resources = None
  cms = None

  def __init__(self, appdata, cnf=None, filepath=None):
    cnf = cnf or {}
    self.config = SKP_Config()
    config_file = os.path.join(appdata.app_config_dir, self.config.filename)
    self.config.load(config_file)
    self.config.update(cnf)
    self.appdata = appdata
    self.cms = self.appdata.app.default_cms
    self.loader = SKP_Loader()
    self.saver = SKP_Saver()
    self.new()
    if filepath:
      self.load(filepath)

  def new(self):
    self.model = SK1Palette()
    self.update()

  def update(self, action=False):
    TextModelPresenter.update(self, action)

  def translate_from_sk2(self, sk2_doc):
    pass

  def translate_to_sk2(self, sk2_doc):
    pass
