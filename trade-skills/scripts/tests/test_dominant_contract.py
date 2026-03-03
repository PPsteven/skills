#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for DominantContractManager
"""

import sys
import unittest
import os
import json
import tempfile
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from trade_utils import DominantContractManager


class TestDominantContractManager(unittest.TestCase):
    """Test dominant contract management functionality"""

    def setUp(self):
        """Create temporary config file for testing"""
        self.temp_fd, self.temp_config = tempfile.mkstemp(suffix='.json')
        self.test_config = {
            "rb": "rb2505",
            "hc": "hc2505",
            "i": "i2505",
            "j": "j2505"
        }
        with open(self.temp_config, 'w', encoding='utf-8') as f:
            json.dump(self.test_config, f, ensure_ascii=False, indent=2)

        self.manager = DominantContractManager(self.temp_config)

    def tearDown(self):
        """Clean up temporary files"""
        os.close(self.temp_fd)
        if os.path.exists(self.temp_config):
            os.unlink(self.temp_config)

    def test_get_dominant_existing(self):
        """Test getting dominant contract for existing variety"""
        result = self.manager.get_dominant("rb")
        self.assertEqual(result, "rb2505")

    def test_get_dominant_not_found(self):
        """Test getting dominant contract for non-existent variety"""
        result = self.manager.get_dominant("unknown")
        self.assertIsNone(result)

    def test_generate_contract_codes_shfe(self):
        """Test generating contract codes for SHFE exchanges (lowercase, 4 digits)"""
        codes = self.manager.generate_contract_codes("rb", exchange="SHFE")
        self.assertEqual(len(codes), 6)
        # Verify format: rb + YYMM (e.g., rb2503)
        for code in codes:
            self.assertTrue(code.startswith("rb"))
            self.assertEqual(len(code), 6)  # rb + 4 digits

    def test_generate_contract_codes_czce(self):
        """Test generating contract codes for CZCE exchange (uppercase, 3 digits)"""
        codes = self.manager.generate_contract_codes("SR", exchange="CZCE")
        self.assertEqual(len(codes), 6)
        # Verify format: SR + YMM (e.g., SR503)
        for code in codes:
            self.assertTrue(code.startswith("SR"))
            self.assertEqual(len(code), 5)  # SR + 3 digits

    def test_save_and_load_config(self):
        """Test saving and reloading configuration"""
        # Modify and save
        self.manager.config["rb"] = "rb2506"
        self.manager.save_config()

        # Create new manager to reload
        new_manager = DominantContractManager(self.temp_config)
        self.assertEqual(new_manager.get_dominant("rb"), "rb2506")


if __name__ == '__main__':
    unittest.main()
