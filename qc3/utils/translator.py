# -*- coding: utf-8 -*-
#
#  Copyright (C) 2018 by Ihor E. Novikov
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

import gettext
import os


class MsgTranslator(object):
    translate = None

    def __init__(self):
        self.translate = self.dummy_translate

    def dummy_translate(self, msg):
        return msg

    def set_locale(self, textdomain, msgs_path, locale='system'):
        msgs_path = msgs_path.decode('utf8') \
            if not (msgs_path, unicode) else msgs_path
        if locale == 'en' or not os.path.exists(msgs_path):
            return
        if locale and not locale == 'system':
            os.environ['LANGUAGE'] = locale
        gettext.bindtextdomain(textdomain, msgs_path)
        gettext.textdomain(textdomain)
        self.translate = gettext.gettext

    def __call__(self, msg):
        return self.translate(msg)
