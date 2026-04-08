from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.archive_spec import ArchiveConfig, archive
from scripts.select_context import format_catalog_listing, select_context


