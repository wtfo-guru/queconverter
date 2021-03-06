# -*- coding: utf-8 -*-
#
#  Copyright (C) 2013-2015 by Ihor E. Novikov
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
from qc3.formats.sk2.sk2_config import SK2_Config
from qc3.formats.sk2.sk2_methods import create_new_doc, SK2_Methods
from qc3.formats.sk2.sk2_filters import SK2_Loader, SK2_Saver


class SK2_Presenter(TextModelPresenter):
  cid = qc3const.SK2

  config = None
  doc_file = ""
  resources = None
  cms = None
  app = None
  active_page = None
  doc_name = ""

  def __init__(self, appdata, cnf=None, filepath=None):
    cnf = cnf or {}
    self.config = SK2_Config()
    config_file = os.path.join(appdata.app_config_dir, "sk2_config.xml")
    self.config.load(config_file)
    self.config.update(cnf)
    self.appdata = appdata
    self.app = self.appdata.app
    self.cms = self.appdata.app.default_cms
    self.loader = SK2_Loader()
    self.saver = SK2_Saver()
    self.methods = SK2_Methods(self)
    self.resources = {}
    if filepath is None:
      self.new()
    else:
      self.load(filepath)

  def new(self):
    self.model = create_new_doc(self.config)
    self.update()

  def update(self, action=False):
    TextModelPresenter.update(self, action)
    if self.model is not None:
      self.methods.update()
