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

from qc3.formats.skp.skp_const import SKP_ID
from qc3.formats.skp.skp_presenter import SKP_Presenter
from qc3.utils.fsutils import get_fileptr
from qc3.utils.mixutils import merge_cnf


def skp_loader(
  appdata, filename=None, fileptr=None, translate=True, convert=False, cnf=None, **kw
):
  cnf = merge_cnf(cnf, kw)
  doc = SKP_Presenter(appdata, cnf)
  doc.load(filename, fileptr)
  return doc


def skp_saver(
  doc, filename=None, fileptr=None, translate=True, convert=False, cnf=None, **kw
):
  doc.save(filename, fileptr)


def check_skp(path):
  fileptr = get_fileptr(path, binary=False)
  string = fileptr.read(len(SKP_ID))
  fileptr.close()
  return string == SKP_ID
