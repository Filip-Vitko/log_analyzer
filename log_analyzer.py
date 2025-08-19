import re
import os
import datetime
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple

SCRIPT_DIR = Path(__file__).parent.resolve()

# TODO:
    # make flag python log_analyzer.py --base-dir /path/to/app
    # add fail saves like if "Desktop" in str(APP_ROOT) or APP_ROOT == Path("/")

@dataclass
class LogStatus:
    log_levels: Dict[str, int]
    logs_per_day: Dict[str, int]
    time_range: Tuple[datetime, datetime]
    total_duration: timedelta

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
    
    def _generator(self):
        path = SCRIPT_DIR / "example.log"
        with path.open(mode='r', encoding='utf-8') as file:
            for log_line in file:
                yield log_line
    
    def _cache_logs(self):
        if not hasattr(self, '_cached_logs'):
            self._cached_logs = list(self._generator())
        return self._cached_logs

    def get_data(self):
        counter_levels: Counter = Counter()
        counter_dates: Counter = Counter()
        log_lines = self._cache_logs()
        for log_line in log_lines:
            match_levels = self.level_regex.search(log_line)
            match_date = self.date_regex.search(log_line)
            match_time = self.time_regex.search(log_line)
            match_full_timestamp = self.full_timestamp_regex.search(log_line)
            if match_levels:
                counter_levels[match_levels.group()] += 1
            if match_full_timestamp:
                counter_dates[match_date.group()] += 1
                print(match_full_timestamp.group())

        log_levels: dict = dict(counter_levels)
        logs_per_day: dict = dict(counter_dates)   
        return LogStatus(
                log_levels=log_levels,
                logs_per_day=logs_per_day,
                time_range=(datetime.now(), datetime.now()),
                total_duration=timedelta(seconds=0)
            )

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