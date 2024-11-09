import unittest
import json
from profiler_app import ProfileApp

class TestProfileApp(unittest.TestCase):
    def setUp(self):
        self.app = ProfileApp()
        self.app.update()

    def test_get_installed_software(self):
        software = self.app.get_installed_software()
        self.assertIsInstance(software, list)
        self.assertTrue(all(isinstance(item, dict) for item in software))

    def test_get_printers(self):
        printers = self.app.get_printers()
        self.assertIsInstance(printers, list)

    def test_get_windows_info(self):
        windows_info = self.app.get_windows_info()
        self.assertIsInstance(windows_info, dict)
        self.assertIn("windows_version", windows_info)

    def test_diff_profiles(self):
        current_profile = {"software": [{"name": "TestApp", "version": "1.0"}]}
        comparison_profile = {"software": [{"name": "TestApp", "version": "2.0"}]}
        diff = self.app.get_diff(current_profile, comparison_profile)
        self.assertIn("values_changed", diff)

    def test_save_profile(self):
        profile_data = {"software": [{"name": "TestApp", "version": "1.0"}]}
        file_path = "test_profile.json"
        with open(file_path, "w") as file:
            json.dump(profile_data, file)
        with open(file_path, "r") as file:
            loaded_data = json.load(file)
        self.assertEqual(profile_data, loaded_data)

    def tearDown(self):
        self.app.destroy()

if __name__ == "__main__":
    unittest.main()
