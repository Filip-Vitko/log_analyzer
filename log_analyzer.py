import re
import os
import datetime
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
from dataclasses import dataclass, field
import time
from typing import List, Dict, Tuple, Optional

SCRIPT_DIR = Path(__file__).parent.resolve()

# TODO:
    # make flag python log_analyzer.py --base-dir /path/to/app
    # add fail saves like if "Desktop" in str(APP_ROOT) or APP_ROOT == Path("/")

@dataclass
class LogStatus:
    log_levels: Dict[str, int] = field(default_factory=dict)
    logs_per_day: Dict[str, int] = field(default_factory=dict)
    time_range: Tuple[datetime, datetime] = field(default_factory=lambda: (None, None))
    total_duration: timedelta = field(default_factory=timedelta)

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
    
    def _iter_lines(self):
        path = SCRIPT_DIR / "example.log"
        with path.open(mode='r', encoding='utf-8') as file:
            for line in file:
                yield line.rsplit("\n")
    
    def _cache_logs(self) -> list[str]:
        if not hasattr(self, '_cached_logs'):
            self._cached_logs = list(self._iter_lines())
        return self._cached_logs

    def get_data(self) -> LogStatus:
        log_lines = self._cache_logs()

        return LogStatus(
                log_levels=self.get_log_levels(),
                logs_per_day=self.get_logs_per_day(),
                time_range=self.get_time(),
                total_duration=timedelta(seconds=0)
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
        first = datetime.strptime(self.full_timestamp_regex.search(log_lines[0]).group(), fmt)
        last  = datetime.strptime(self.full_timestamp_regex.search(log_lines[-1]).group(), fmt)
        print(last - first)
        return (first, last)
    
    # TODO: add helppers
    # ---------- helpers ----------

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def json_output():
    pass

def output():
    clear()
    print("📊 Log Summary Report")
    print("=" * 50, end="\n\n")
    print("🔹 Log Levels:")
    print("INFO   : 2")
    print("WARNING: 1")
    print("ERROR  : 1")
    print("DEBUG  : 1", end="\n\n")
    print("🔹 Logs Per Day:")
    print("{Date(1)}: {count} entries")
    print("{Date(n)}: {count} entries", end="\n\n")
    print("🔹 Time Range:")
    print("From: {start_time}")
    print("To:   {end_time}")
    print("Total Duration: {end_time - start_time}")

def main():
    clear()
    analyzer = Analyzer()
    log_status = analyzer.get_data()
    print(log_status.log_levels)
    print(log_status.logs_per_day)
    print(log_status.time_range)
    print(log_status.total_duration)

main()