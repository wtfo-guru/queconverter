# -*- coding: utf-8 -*-
#
#  Copyright (C) 2015-2016 by Igor E. Novikov
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
from qc3.formats.generic import TaggedModelPresenter
from qc3.formats.xml_.xml_config import XML_Config
from qc3.formats.xml_.xml_filters import XML_Loader, XML_Saver
from qc3.formats.xml_.xml_model import XMLObject


class XML_Presenter(TaggedModelPresenter):

  cid = qc3const.XML

  config = None
  doc_file = ""
  resources = None
  cms = None

  def __init__(self, appdata, cnf={}, filepath=None):
    self.doc_file = ""
    self.resources = None
    self.config = XML_Config()
    config_file = os.path.join(appdata.app_config_dir, self.config.filename)
    self.config.load(config_file)
    self.config.update(cnf)
    self.appdata = appdata
    self.cms = self.appdata.app.default_cms
    self.loader = XML_Loader()
    self.saver = XML_Saver()
    if filepath is None:
      self.new()
    else:
      self.load(filepath)

  def new(self):
    self.model = XMLObject("root")
