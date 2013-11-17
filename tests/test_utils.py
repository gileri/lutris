from unittest import TestCase
from lutris.util import system
from lutris.util import steam


class TestFileUtils(TestCase):
    def test_file_ids_are_correctly_transformed(self):
        file_id = 'foo-bar'
        self.assertEqual(system.python_identifier(file_id), 'foo-bar')

        file_id = '${foo-bar}'
        self.assertEqual(system.python_identifier(file_id), '${foo_bar}')

        file_id = '${foo-bar} ${a-b}'
        self.assertEqual(system.python_identifier(file_id), '${foo_bar} ${a_b}')

        file_id = '${foo-bar} a-b'
        self.assertEqual(system.python_identifier(file_id), '${foo_bar} a-b')

        file_id = '${foo-bar-bang}'
        self.assertEqual(system.python_identifier(file_id), '${foo_bar_bang}')

        file_id = '${foo-bar bang}'
        self.assertEqual(system.python_identifier(file_id), '${foo-bar bang}')

    def test_file_ids_are_substitued(self):
        fileid = '${foo-bar}'
        _files = {
            'foo-bar': "/foo/bar"
        }
        self.assertEqual(system.substitute(fileid, _files), "/foo/bar")


class TestSteamUtils(TestCase):
    def test_dict_to_vdf(self):
        dict_data = {
            'AppState': {
                'appID': '13240',
                'StateFlags': '4',
                'UserConfig': {
                    "name": "Unreal Tournament",
                    "gameid": "13240"
                }
            }
        }
        expected_vdf = """"AppState"
{
\t"UserConfig"
\t{
\t\t"gameid"\t\t"13240"
\t\t"name"\t\t"Unreal Tournament"
\t}
\t"StateFlags"\t\t"4"
\t"appID"\t\t"13240"
}"""
        vdf_data = steam.to_vdf(dict_data)
        self.assertEqual(vdf_data.strip(), expected_vdf.strip())
