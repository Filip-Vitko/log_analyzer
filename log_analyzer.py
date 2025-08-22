import re
import os
import datetime
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
from dataclasses import dataclass, field
import time
from typing import List, Dict, Tuple, Optional
import sys

SCRIPT_DIR = Path(__file__).parent.resolve()

# TODO:
    # make flag python log_analyzer.py --base-dir /path/to/app
    # add fail saves like if "Desktop" in str(APP_ROOT) or APP_ROOT == Path("/")

@dataclass
class LogStatus:
    log_levels: Dict[str, int] = field(default_factory=dict)
    logs_per_day: Dict[str, int] = field(default_factory=dict)
    time_range: Tuple[datetime, datetime] = field(default_factory=lambda: (None, None))
    total_duration: timedelta = field(init=False)

    def __post_init__(self):
        start, end = self.time_range
        if not start or not end:
            print("No valid timestamps found.", file=sys.stderr)
            sys.exit(2)
        self.total_duration = (end - start) if start and end else timedelta(0)

class Analyzer():
    def __init__(self):
        self.date_patterns: list = [
            r"\b\d{4}[-/]\d{2}[-/]\d{2}\b",                                                         # 2025-08-09
            r"\b\d{2}[-/]\d{2}[-/]\d{4}\b",                                                         # 09-08-2025
            r"\b\d{2}[-/]\d{2}[-/]\d{2}\b",                                                         # 09-08-25
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b",   # Aug 9 2025
            r"\b\d{4}\d{2}\d{2}\b",                                                                 # 20250809
        ]
        self.time_patterns: list = [
            r"\b\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b",                              # 14:32:15.123+02:00
        ]
        
        self.date_regex = re.compile("|".join(self.date_patterns), re.IGNORECASE)
        self.time_regex = re.compile("|".join(self.time_patterns), re.IGNORECASE)
        self.full_timestamp_regex = re.compile(
            rf"(?:{self.date_regex.pattern})\s+(?:{self.time_regex.pattern})",
            re.IGNORECASE
        )

        self.level_regex = re.compile(r"\b(?:DEBUG|INFO|WARNING|ERROR|CRITICAL)\b")

        self._dt_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%d-%m-%y %H:%M:%S",
        ]

    def _iter_lines(self):
        path = SCRIPT_DIR / "example.log"
        with path.open(mode='r', encoding='utf-8') as file:
            for line in file:
                yield line
    
    def _cache_logs(self) -> list[str]:
        if not hasattr(self, '_cached_logs'):
            self._cached_logs = list(self._iter_lines())
        return self._cached_logs

    def get_data(self) -> LogStatus:
        return LogStatus(
                log_levels=self.get_log_levels(),
                logs_per_day=self.get_logs_per_day(),
                time_range=self.get_time()
            )

    def get_log_levels(self) -> Dict[str, int]:
        counter = Counter()
        log_lines = self._cache_logs()
        for log_line in log_lines:
            match = self.level_regex.search(log_line)
            if match:
                counter[match.group()] += 1

        return dict(counter)

    def get_logs_per_day(self) -> dict:
        counter = Counter()
        log_lines = self._cache_logs()
        for log_line in log_lines:
            match = self.date_regex.search(log_line)
            if match:
                counter[match.group()] += 1
        
        return dict(counter)

    def get_time(self) -> Tuple:
        fmt = "%Y-%m-%d %H:%M:%S"
        log_lines = self._cache_logs()
        def parse(line):
            m = self.full_timestamp_regex.search(line)
            return datetime.strptime(m.group(), fmt) if m else None
        start = next((dt for dt in (parse(l) for l in log_lines) if dt), None)
        end  = next((dt for dt in (parse(l) for l in reversed(log_lines)) if dt), None)
        return (start, end)
    
    # TODO: add helpper functions
    # ---------- helpers ----------

    def _normalize_datetime_string(self, s: str) -> str:
        pass

    def _extract_first_timestamp(self, line: str) -> Optional[datetime]:
        pass

    def _normalize_date_only(self, s: str) -> Optional[str]:
        pass

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def json_output():
    pass

def output(analyzer):
    clear()
    log_status = analyzer.get_data()
    start, end = log_status.time_range

    print("📊 Log Summary Report")
    print("=" * 50, end="\n\n")
    print("🔹 Log Levels:")
    print(f"INFO    : {log_status.log_levels.get('INFO', 0)}")
    print(f"WARNING : {log_status.log_levels.get('WARNING', 0)}")
    print(f"ERROR   : {log_status.log_levels.get('ERROR', 0)}")
    print(f"DEBUG   : {log_status.log_levels.get('DEBUG', 0)}")
    print(f"CRITICAL: {log_status.log_levels.get('CRITICAL', 0)}", end="\n\n")
    print("🔹 Logs Per Day:")
    for key, val in log_status.logs_per_day.items():
        print(f"{key}: {val} entries")
    print()
    print("🔹 Time Range:")
    print(f"From: {start}")
    print(f"To:   {end}")
    print(f"Total Duration: {log_status.total_duration}")

def main():
    clear()
    analyzer = Analyzer()
    output(analyzer)

main()