from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class Length(str, Enum):
    mm = "millimeter"
    cm = "centimeter"
    m = "meter"
    km = "kilometer"
    inch = "inch"
    ft = "foot"
    yd = "yard"

class Weight(str, Enum):
    mg = "milligram"
    gm = "gram"
    kg = "kilogram"
    oz = "ounce"
    pound = "pound"

class Temperature(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"
    kelvin = "kelvin"

LENGTH_FACTORS: dict = {
    Length.mm : 1,
    Length.cm : 10,
    Length.m : 1000,
    Length.km : 1000000,
    Length.inch : 25.4,
    Length.ft : 304.8,
    Length.yd : 914.4
}

WEIGHT_FACTORS: dict = {
    Weight.mg : 1,
    Weight.gm : 1000,
    Weight.kg : 1000000,
    Weight.oz : 28349.523125,
    Weight.pound : 453592.37
}

def convert_to_kelvin(temp: float, unit: Temperature) -> float:
    if unit == Temperature.celsius:
        return temp + 273.15
    if unit == Temperature.fahrenheit:
        return (temp - 32) * 5/9 + 273.15
    return temp

def convert_from_kelvin(temp: float, unit:Temperature) -> float:
    if unit == Temperature.celsius:
        return temp - 273.15
    if unit == Temperature.fahrenheit:
        return (temp - 273.15) * 9/5 + 32
    return temp

@app.get("/length/")
async def convert_length(value: float, convert_from: Length, convert_to: Length) -> dict:

    if convert_from.value == convert_to.value:
        return {
            convert_to.value: str(value)
        }
    
    base_value: float = value * LENGTH_FACTORS[convert_from]
    result: float = base_value / LENGTH_FACTORS[convert_to]
    
    return {
        convert_from.value: str(value),
        convert_to.value: str(result)
    }

@app.get("/weight")
async def convert_weight(value: float, convert_from: Weight, convert_to: Weight) -> dict:

    if convert_from.value == convert_to.value:
        return {
            convert_to.value: str(value)
        }
    
    base_value: float = value * WEIGHT_FACTORS[convert_from]
    result: float = base_value / WEIGHT_FACTORS[convert_to]
    
    return {
        convert_from.value: str(value),
        convert_to.value: str(result)
    }

@app.get("/temperature/")
async def convert_temperature(value: float, convert_from: Temperature, convert_to: Temperature) -> dict:

    if convert_from.value == convert_to.value:
        return {
            convert_to.value: str(value)
        }
    
    kelvin_value = convert_to_kelvin(value, convert_from)
    result = convert_from_kelvin(kelvin_value, convert_to)
    
    return {
        convert_from.value: str(value),
        convert_to.value: str(result)
    }