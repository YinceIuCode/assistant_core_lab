# responder.py
import os
import csv
import json
import time
import random
from typing import Protocol, runtime_checkable

BASE = os.path.dirname(os.path.abspath(__file__))

@runtime_checkable
class Responder(Protocol):
    def generate_response(self, query: str) -> str:
        ...

class TemplateResponder:
    def __init__(self, rate=450000, retake_rate=1.5):
        self.rate = rate
        self.retake_rate = retake_rate
        self.offices = {}
        self._load_offices()

    def _load_offices(self):
        try:
            path = os.path.join(BASE, "data", "offices.csv")
            with open(path, mode="r", encoding="utf-8") as f:
                r = csv.reader(f)
                next(r, None)
                for row in r:
                    if row:
                        self.offices[row[0].lower()] = row
        except Exception:
            pass

    def generate_response(self, query: str) -> str:
        m = query.lower().strip()
        if m in ["hi", "hello", "hey", "xin chao"]:
            return "Hello! I can help with offices, fees and rules."
        
        # Xử lý hỏi học phí (fee/tuition)
        if "fee" in m or "tuition" in m:
            words = m.replace("?", " ").split()
            credits = 0
            retake = 0
            for i in range(len(words)):
                if words[i].isdigit():
                    if i + 1 < len(words) and words[i + 1].startswith("retake"):
                        retake = int(words[i])
                    elif credits == 0:
                        credits = int(words[i])
            if credits == 0:
                return "How many credits?"
            if credits > 30:
                return "too many credits"
            total = credits * self.rate + retake * self.rate * self.retake_rate
            return "Your tuition is " + str(int(total)) + " VND"

        # Xử lý hỏi văn phòng (office)
        for k in self.offices:
            if k in m:
                o = self.offices[k]
                return o[0] + ": room " + o[1] + ", open " + o[2]
        
        return "Sorry I dont know"

class StubLLMResponder:
    def __init__(self, model="gpt-small", api_key="sk-test-2b7c1d9e4f0a", debug=False):
        self.model = model
        self.api_key = api_key
        self.debug = debug
        self.handbook = []
        self._load_handbook()

    def _load_handbook(self):
        try:
            path = os.path.join(BASE, "data", "handbook.json")
            with open(path, mode="r", encoding="utf-8") as f:
                self.handbook = json.load(f)
        except Exception:
            pass

    def _mock_llm(self, prompt: str) -> str:
        if self.debug:
            print(f"[debug] calling {self.model} with key {self.api_key} prompt: {prompt[:60]}")
        time.sleep(0.1)
        if random.random() < 0.05:
            raise Exception("LLM timeout")
        return "Here is what I found: " + prompt[-120:]

    def generate_response(self, query: str) -> str:
        m = query.lower().strip()
        best = None
        best_score = 0
        for rule in self.handbook:
            score = 0
            for w in m.split():
                if len(w) > 3 and w in rule["text"].lower():
                    score += 1
            if score > best_score:
                best_score = score
                best = rule

        if best is not None and best_score >= 1:
            try:
                ans = self._mock_llm("Answer using this rule: " + best["text"] + " Question: " + query)
                return ans + " (source: " + best["id"] + ")"
            except Exception:
                return best["text"] + " (source: " + best["id"] + ")"
        return "Sorry I dont know"