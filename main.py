#!/usr/bin/env python3
import argparse
import datetime
import random
import os
import sys
from typing import List, Dict, Optional
import shutil

class GitHubHistoryGenerator:
    def __init__(self):
        self.DAYS_IN_WEEK = 7
        self.WEEKS_IN_YEAR = 53
        self.MAX_TEXT_LENGTH = 15
        self.VALID_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()_+-={}[]:\";\\'<>,./?\\| ")
        self.REPO_NAME = "my-history"
        self.TEXT_MODE_COMMITS = 5  # Fixed commits for text mode only
        
        # Character matrices for text display (5x7 grid for each character)
        self.CHAR_MATRICES = {
            'A': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1]
            ],
            'B': [
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,0]
            ],
            'C': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            'D': [
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,0]
            ],
            'E': [
                [1,1,1,1,1],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,1,1,1,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,1,1,1,1]
            ],
            'F': [
                [1,1,1,1,1],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,1,1,1,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0]
            ],
            'G': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,0],
                [1,0,1,1,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            'H': [
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1]
            ],
            'I': [
                [1,1,1,1,1],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [1,1,1,1,1]
            ],
            'J': [
                [1,1,1,1,1],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [1,0,1,0,0],
                [0,1,0,0,0]
            ],
            'K': [
                [1,0,0,0,1],
                [1,0,0,1,0],
                [1,0,1,0,0],
                [1,1,0,0,0],
                [1,0,1,0,0],
                [1,0,0,1,0],
                [1,0,0,0,1]
            ],
            'L': [
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,1,1,1,1]
            ],
            'M': [
                [1,0,0,0,1],
                [1,1,0,1,1],
                [1,0,1,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1]
            ],
            'N': [
                [1,0,0,0,1],
                [1,1,0,0,1],
                [1,0,1,0,1],
                [1,0,0,1,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1]
            ],
            'O': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            'P': [
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0]
            ],
            'Q': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,1,0,1],
                [1,0,0,1,0],
                [0,1,1,0,1]
            ],
            'R': [
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,1,1,1,0],
                [1,0,1,0,0],
                [1,0,0,1,0],
                [1,0,0,0,1]
            ],
            'S': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,0],
                [0,1,1,1,0],
                [0,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            'T': [
                [1,1,1,1,1],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0]
            ],
            'U': [
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            'V': [
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,0,1,0],
                [0,0,1,0,0]
            ],
            'W': [
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [1,0,1,0,1],
                [1,1,0,1,1],
                [1,0,0,0,1]
            ],
            'X': [
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,0,1,0],
                [0,0,1,0,0],
                [0,1,0,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1]
            ],
            'Y': [
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,0,1,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0]
            ],
            'Z': [
                [1,1,1,1,1],
                [0,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [1,0,0,0,0],
                [1,1,1,1,1]
            ],
            '0': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,1,1],
                [1,0,1,0,1],
                [1,1,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '1': [
                [0,0,1,0,0],
                [0,1,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,1,1,1,0]
            ],
            '2': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [0,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [1,1,1,1,1]
            ],
            '3': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [0,0,0,0,1],
                [0,0,1,1,0],
                [0,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '4': [
                [0,0,0,1,0],
                [0,0,1,1,0],
                [0,1,0,1,0],
                [1,0,0,1,0],
                [1,1,1,1,1],
                [0,0,0,1,0],
                [0,0,0,1,0]
            ],
            '5': [
                [1,1,1,1,1],
                [1,0,0,0,0],
                [1,1,1,1,0],
                [0,0,0,0,1],
                [0,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '6': [
                [0,1,1,1,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '7': [
                [1,1,1,1,1],
                [0,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [0,1,0,0,0],
                [0,1,0,0,0]
            ],
            '8': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            '9': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,1],
                [0,0,0,0,1],
                [1,0,0,0,1],
                [0,1,1,1,0]
            ],
            ' ': [
                [0,0,0],
                [0,0,0],
                [0,0,0],
                [0,0,0],
                [0,0,0],
                [0,0,0],
                [0,0,0]
            ],
            '!': [
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0]
            ],
            '@': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [1,0,1,1,1],
                [1,0,1,0,1],
                [1,0,1,1,1],
                [1,0,0,0,0],
                [0,1,1,1,0]
            ],
            '#': [
                [0,1,0,1,0],
                [0,1,0,1,0],
                [1,1,1,1,1],
                [0,1,0,1,0],
                [1,1,1,1,1],
                [0,1,0,1,0],
                [0,1,0,1,0]
            ],
            '$': [
                [0,0,1,0,0],
                [0,1,1,1,1],
                [1,0,1,0,0],
                [0,1,1,1,0],
                [0,0,1,0,1],
                [1,1,1,1,0],
                [0,0,1,0,0]
            ],
            '%': [
                [1,1,0,0,1],
                [1,1,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [1,0,0,1,1],
                [1,0,0,1,1]
            ],
            '^': [
                [0,0,1,0,0],
                [0,1,0,1,0],
                [1,0,0,0,1],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]
            ],
            '&': [
                [0,1,1,0,0],
                [1,0,0,1,0],
                [1,0,1,0,0],
                [0,1,0,0,0],
                [1,0,1,0,1],
                [1,0,0,1,0],
                [0,1,1,0,1]
            ],
            '*': [
                [0,0,1,0,0],
                [1,0,1,0,1],
                [0,1,1,1,0],
                [0,0,1,0,0],
                [0,1,1,1,0],
                [1,0,1,0,1],
                [0,0,1,0,0]
            ],
            '(': [
                [0,0,1,0,0],
                [0,1,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [0,1,0,0,0],
                [0,0,1,0,0]
            ],
            ')': [
                [0,0,1,0,0],
                [0,0,0,1,0],
                [0,0,0,0,1],
                [0,0,0,0,1],
                [0,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0]
            ],
            '_': [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [1,1,1,1,1]
            ],
            '+': [
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [1,1,1,1,1],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0]
            ],
            '-': [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [1,1,1,1,1],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]
            ],
            '=': [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [1,1,1,1,1],
                [0,0,0,0,0],
                [1,1,1,1,1],
                [0,0,0,0,0],
                [0,0,0,0,0]
            ],
            '{': [
                [0,0,1,1,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,1,0]
            ],
            '}': [
                [0,1,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,1,1,0,0]
            ],
            '[': [
                [0,1,1,1,0],
                [0,1,0,0,0],
                [0,1,0,0,0],
                [0,1,0,0,0],
                [0,1,0,0,0],
                [0,1,0,0,0],
                [0,1,1,1,0]
            ],
            ']': [
                [0,1,1,1,0],
                [0,0,0,1,0],
                [0,0,0,1,0],
                [0,0,0,1,0],
                [0,0,0,1,0],
                [0,0,0,1,0],
                [0,1,1,1,0]
            ],
            ':': [
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0]
            ],
            '"': [
                [0,1,0,1,0],
                [0,1,0,1,0],
                [0,1,0,1,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]
            ],
            ';': [
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,1,0,0,0]
            ],
            '\'': [
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]
            ],
            '<': [
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [1,0,0,0,0],
                [0,1,0,0,0],
                [0,0,1,0,0],
                [0,0,0,1,0]
            ],
            '>': [
                [0,1,0,0,0],
                [0,0,1,0,0],
                [0,0,0,1,0],
                [0,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0]
            ],
            ',': [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,1,0,0,0]
            ],
            '.': [
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0]
            ],
            '/': [
                [0,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,1,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0],
                [1,0,0,0,0]
            ],
            '?': [
                [0,1,1,1,0],
                [1,0,0,0,1],
                [0,0,0,1,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,0,0,0],
                [0,0,1,0,0]
            ],
            '\\': [
                [1,0,0,0,0],
                [1,0,0,0,0],
                [0,1,0,0,0],
                [0,0,1,0,0],
                [0,0,0,1,0],
                [0,0,0,1,0],
                [0,0,0,0,1]
            ],
            '|': [
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0],
                [0,0,1,0,0]
            ],
            '~': [
                [0,1,0,1,0],
                [1,0,1,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]
            ],
        }
        
        self.INTENSITY_LEVELS = {
            0: 0,  # No commits
            1: 1,  # Light
            2: 2,  # Medium
            3: 3,  # Dark
            4: 4   # Darkest
        }

    def validate_text(self, text: str) -> bool:
        """Validate if the text can be displayed in the GitHub contribution graph."""
        if not text:
            print("Error: Text cannot be empty")
            return False
            
        if len(text) > self.MAX_TEXT_LENGTH:
            print(f"Error: Text must be {self.MAX_TEXT_LENGTH} characters or less")
            return False
            
        text = text.upper()
        invalid_chars = set(text) - self.VALID_CHARS
        if invalid_chars:
            print(f"Error: Invalid characters found: {invalid_chars}")
            return False
            
        return True

    def generate_commits(
        self,
        commits_per_day: float = 0.3,
        workdays_only: bool = False,
        start_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None,
        text: Optional[str] = None,
        year: Optional[int] = None
    ) -> Dict[str, int]:
        """Generate commit pattern based on mode."""
        if text and year:
            return self.create_text_pattern(text, year)
        else:
            return self.create_random_pattern(
                commits_per_day,
                workdays_only,
                start_date,
                end_date
            )

    def create_random_pattern(
        self,
        commits_per_day: float,
        workdays_only: bool,
        start_date: Optional[datetime.date],
        end_date: Optional[datetime.date]
    ) -> Dict[str, int]:
        """Generate random commit pattern."""
        if not end_date:
            end_date = datetime.date.today()
        if not start_date:
            start_date = end_date - datetime.timedelta(days=365)

        commit_pattern = {}
        current_date = start_date

        while current_date <= end_date:
            if workdays_only and current_date.weekday() >= 5:
                current_date += datetime.timedelta(days=1)
                continue

            if commits_per_day <= 1:
                num_commits = 1 if random.random() < commits_per_day else 0
            else:
                num_commits = random.randint(0, int(commits_per_day))

            if num_commits > 0:
                commit_pattern[current_date.isoformat()] = num_commits

            current_date += datetime.timedelta(days=1)

        return commit_pattern

    def create_text_pattern(self, text: str, year: int) -> Dict[str, int]:
        """Create commit pattern for text display with fixed commits."""
        text = text.upper()
        if not self.validate_text(text):
            raise ValueError(f"Invalid text. Must be {self.MAX_TEXT_LENGTH} characters or less.")

        commit_pattern = {}
        start_date = datetime.date(year, 1, 1)
        
        # Calculate the offset needed to start from the first Sunday
        days_until_sunday = (6 - start_date.weekday()) % 7  # 6 is Sunday in Python's weekday()
        start_date = start_date + datetime.timedelta(days=days_until_sunday)
        
        text_width = sum(6 if char != ' ' else 3 for char in text)
        start_week = max(1, (self.WEEKS_IN_YEAR - text_width) // 2)
        current_week = start_week

        for char in text:
            if char == ' ':
                current_week += 3
                continue

            if char in self.CHAR_MATRICES:
                matrix = self.CHAR_MATRICES[char]
                for row in range(7):
                    for col in range(5):
                        if matrix[row][col] == 1:
                            week = current_week + col
                            if 0 <= week < self.WEEKS_IN_YEAR:
                                commit_date = start_date + datetime.timedelta(weeks=week, days=row)
                                if commit_date.year == year:
                                    commit_pattern[commit_date.isoformat()] = self.TEXT_MODE_COMMITS

            current_week += 6

        return commit_pattern

    def init_repository(self) -> str:
        """Initialize a new Git repository."""
        repo_path = os.path.abspath(self.REPO_NAME)
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        os.makedirs(repo_path)
        
        original_dir = os.getcwd()
        os.chdir(repo_path)
        
        try:
            os.system('git init -b main')
            os.system('git config user.name "GitHub History Generator"')
            os.system('git config user.email "history-generator@example.com"')
            
            with open('README.md', 'w') as f:
                f.write('# GitHub History Generator\n\nThis repository was created using the GitHub History Generator.')
            
            os.system('git add README.md')
            os.system('git commit -m "Initial commit"')
            
            return repo_path
        finally:
            os.chdir(original_dir)

    def create_commits(self, commit_pattern: Dict[str, int], git_name: str, git_email: str):
        """Create Git commits based on pattern using a single file."""
        repo_path = self.init_repository()
        original_dir = os.getcwd()
        os.chdir(repo_path)

        try:
            os.system(f'git config user.name "{git_name}"')
            os.system(f'git config user.email "{git_email}"')
            
            sorted_dates = sorted(commit_pattern.items())
            total_commits = sum(num_commits for _, num_commits in sorted_dates)
            current_commit = 0
            
            # Create a single file to track commits
            commit_file = 'commit_history.txt'
            
            for date, num_commits in sorted_dates:
                for i in range(num_commits):
                    current_commit += 1
                    
                    if num_commits == self.TEXT_MODE_COMMITS:
                        hour = 9 + (i * 2)
                        minute = (i * 13) % 60
                    else:
                        hour = random.randint(9, 18)
                        minute = random.randint(0, 59)
                    
                    # Update the single file with the new commit information
                    with open(commit_file, 'a') as f:
                        f.write(f'Commit {current_commit} of {total_commits} on {date}\n')
                    
                    commit_date = f'{date}T{hour:02d}:{minute:02d}:00'
                    
                    os.system(f'git add {commit_file}')
                    os.system(
                        f'git -c user.name="{git_name}" '
                        f'-c user.email="{git_email}" '
                        f'commit --date="{commit_date}" '
                        f'-m "Commit {current_commit}" '
                    )

            print(f"\nCreated {total_commits} commits successfully!")
            print("\nNext steps:")
            print("1. cd my-history")
            print("2. git remote add origin <your-repository-url>")
            print(f'3. git -c user.name="{git_name}" -c user.email="{git_email}" push -f origin main')
            
        except Exception as e:
            print(f"Error creating commits: {e}", file=sys.stderr)
            raise
        finally:
            os.chdir(original_dir)

def main():
    parser = argparse.ArgumentParser(description='Generate GitHub commit history')
    parser.add_argument('--commitsPerDay', type=float, default=0.3,
                      help='Average number of commits per day (default: 0.3)')
    parser.add_argument('--workdaysOnly', action='store_true',
                      help='Only create commits on workdays')
    parser.add_argument('--startDate', type=str,
                      help='Start date (YYYY-MM-DD)')
    parser.add_argument('--endDate', type=str,
                      help='End date (YYYY-MM-DD)')
    parser.add_argument('--text', type=str,
                      help='Text to display in commit history')
    parser.add_argument('--year', type=int,
                      help='Year for text display')
    parser.add_argument('--gitName', type=str, required=True,
                      help='Git user name')
    parser.add_argument('--gitEmail', type=str, required=True,
                      help='Git user email')

    args = parser.parse_args()

    try:
        generator = GitHubHistoryGenerator()
        
        start_date = datetime.datetime.strptime(args.startDate, '%Y-%m-%d').date() if args.startDate else None
        end_date = datetime.datetime.strptime(args.endDate, '%Y-%m-%d').date() if args.endDate else None

        commit_pattern = generator.generate_commits(
            commits_per_day=args.commitsPerDay,
            workdays_only=args.workdaysOnly,
            start_date=start_date,
            end_date=end_date,
            text=args.text,
            year=args.year
        )
        
        generator.create_commits(commit_pattern, args.gitName, args.gitEmail)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()