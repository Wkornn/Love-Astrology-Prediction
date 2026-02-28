"""Core Python Data Structures for Love Debugging Lab v2.0"""

from dataclasses import dataclass
from typing import List, Literal, Optional
from enum import Enum

class ZodiacSign(Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

class PlanetName(Enum):
    SUN = "Sun"
    MOON = "Moon"
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"

class AspectType(Enum):
    CONJUNCTION = "Conjunction"
    OPPOSITION = "Opposition"
    TRINE = "Trine"
    SQUARE = "Square"
    SEXTILE = "Sextile"

@dataclass
class Planet:
    name: PlanetName
    sign: ZodiacSign
    degree: float
    house: int

@dataclass
class Aspect:
    planetA: PlanetName
    planetB: PlanetName
    type: AspectType
    orb: float
    angle: float

@dataclass
class BirthChart:
    planets: List[Planet]
    aspects: List[Aspect]
    ascendant: Optional[ZodiacSign] = None

@dataclass
class BirthData:
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: str

BugSeverity = Literal["CRITICAL", "WARNING", "INFO"]

@dataclass
class LoveBug:
    severity: BugSeverity
    code: str
    message: str
    stack_trace: Optional[str] = None

@dataclass
class CompatibilityScores:
    emotional: float
    physical: float
    stability: float
    drama: float
    overall: float

@dataclass
class CompatibilityResult:
    archetype: str
    scores: CompatibilityScores
    bugs: List[LoveBug]
    emotional_risk_index: float
    forecast: List[str]
    debug_summary: str
