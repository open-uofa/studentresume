from copy import deepcopy
from json import loads

import pytest

from ..resume import *

"""
    Test each function that retrives information to confirm that the list returned the correct data and format.
    Create mock objects to check the exceptions in the function.
"""
        
def test_process_education():
    # read in data from sample.resume.json
    resume = Resume(False)
    resume.get_default_theme()
    with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
    resume_json = loads(data)
    # check the output of the function to make sure it returns the correct value
    assert resume.process_education(resume_json) == ['<b>University of Oklahoma</b>', '<b>Bachelor</b> Information Technology', '<b>Dates: </b>June, 2011 - January, 2014', '<b>GPA:</b> 4.0']
    assert resume.process_education(resume_json) != ""
    
    # check the exception raised to make sure it raises the correct error
    
def test_process_skills():
    resume = Resume(False)
    resume.get_default_theme()
    with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
    resume_json = loads(data) 
    assert(resume.process_skills(resume_json)) == ['<b>Web Development</b>: HTML, CSS, Javascript', '<b>Compression</b>: Mpeg, MP4, GIF']
    assert resume.process_skills(resume_json) != ""
        
def test_process_projects():
    resume = Resume(False)
    resume.get_default_theme()
    with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
    resume_json = loads(data)
    
    assert(resume.process_projects(resume_json)) == ['<b>Miss Direction</b>: A mapping engine that misguides you - <b>August, 2016</b><br/><a href=http://missdirection.example.com>http://missdirection.example.com</a><br/><b>Techonology Used</b>: GoogleMaps, Chrome Extension, Javascript<br/><b>Highlights: </b><br/>- Won award at AIHacks 2016<br/>- Built by all women team of newbie programmers<br/>- Using modern technologies such as GoogleMaps, Chrome Extension and Javascript']
    assert resume.process_projects(resume_json) != ""

def test_process_work_experience():
    with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
    resume_json = loads(data)
    resume = Resume(False)
    resume.get_default_theme()
    assert(resume.process_work_experience(resume_json)) == ['<b>Pied Piper</b>: - Palo Alto, CA<br/><b>CEO/President</b>: December, 2013 - December, 2014<br/>Pied Piper is a multi-platform technology based on a proprietary universal compression algorithm that has consistently fielded high Weisman Scores™ that are not merely competitive, but approach the theoretical limit of lossless compression.<br/><b>Highlights: </b><br/>- Build an algorithm for artist to detect if their music was violating copy right infringement laws<br/>- Successfully won Techcrunch Disrupt<br/>- Optimized an algorithm that holds the current world record for Weisman Scores']
    assert resume.process_work_experience(resume_json) != ""

def test_process_vol_experience():
    with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
    resume_json = loads(data)
    resume = Resume(False)
    resume.get_default_theme()
    assert(resume.process_vol_experience(resume_json)) == ["<b>CoderDojo</b> January, 2012 - January, 2013<br/>Global movement of free coding clubs for young people.<br/><b>Highlights: </b><br/>- Awarded 'Teacher of the Month'"]
    assert resume.process_vol_experience(resume_json) != ""
    
def test_process_awards():
    with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
    resume_json = loads(data)
    resume = Resume(False)
    resume.get_default_theme()
    assert(resume.process_awards(resume_json)) == ['<b>Digital Compression Pioneer Award</b><br/>Awarded by: Techcrunch - November, 2014<br/>There is no spoon.']
    assert resume.process_awards(resume_json) != ""

def test_process_publications():
    with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
    resume_json = loads(data)
    resume = Resume(False)
    resume.get_default_theme()
    assert(resume.process_publications(resume_json)) == ['<b>Video compression for 3d media</b><br/>Hooli - October, 2014<br/><a href=http://en.wikipedia.org/wiki/Silicon_Valley_(TV_series)>http://en.wikipedia.org/wiki/Silicon_Valley_(TV_series)</a><br/>Innovative middle-out compression algorithm that changes the way we store data.']
    assert resume.process_publications(resume_json) != ""
      

def test_required_fields_basics():
  with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["basics"]["name"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["basics"]["name"] = "Richard Hendricks"
  bad["basics"]["email"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["basics"]["email"] = "richard.hendriks@mail.com"
  bad["basics"]["phone"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["basics"]["phone"] = "(912) 555-4321"
  bad["basics"]["summary"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["basics"]["summary"] = "Richard hails from Tulsa. He has earned degrees from the University of Oklahoma and Stanford. (Go Sooners and Cardinal!) Before starting Pied Piper, he worked for Hooli as a part time software developer. While his work focuses on applied information theory, mostly optimizing lossless compression schema of both the length-limited and adaptive variants, his non-work interests range widely, everything from quantum computing to chaos theory. He could tell you about it, but THAT would NOT be a “length-limited” conversation!"
  bad["basics"]["location"]["region"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["basics"]["location"]["region"] = "California"
  bad["basics"]["location"]["city"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["basics"]["location"]["city"] = "San Francisco"
  bad["basics"]["location"]["countryCode"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  
def test_required_fields_empty():
  with open("sample.resume.json", encoding="utf8") as f:
        data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["education"] = []
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["education"] = resume_json["education"]
  bad["skills"] = []
  with pytest.raises(Exception):
        resume.required_fields(bad)
        
def test_required_fields_skills():
  with open("sample.resume.json", encoding="utf8") as f:
      data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["skills"][0]["keywords"] = []
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["skills"][0]["keywords"] = resume_json["skills"][0]["keywords"]
  bad["skills"][0]["level"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["skills"][0]["level"] = resume_json["skills"][0]["level"]
  bad["skills"][0]["name"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["skills"][0]["name"] = resume_json["skills"][0]["name"]
  bad["education"][0]["institution"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
        
def test_required_fields_education():
  with open("sample.resume.json", encoding="utf8") as f:
      data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["education"][0]["institution"] = resume_json["education"][0]["institution"]
  bad["education"][0]["area"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["education"][0]["area"] = resume_json["education"][0]["area"]
  bad["education"][0]["studyType"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["education"][0]["studyType"] = resume_json["education"][0]["studyType"]
  bad["education"][0]["startDate"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["education"][0]["startDate"] = resume_json["education"][0]["startDate"]
  bad["education"][0]["endDate"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)

def test_required_fields_work():
  with open("sample.resume.json", encoding="utf8") as f:
      data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["work"][0]["name"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["work"][0]["name"] = resume_json["work"][0]["name"]
  bad["work"][0]["position"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["work"][0]["position"] = resume_json["work"][0]["position"]
  bad["work"][0]["startDate"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["work"][0]["startDate"] = resume_json["work"][0]["startDate"]
  bad["work"][0]["endDate"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["work"][0]["endDate"] = resume_json["work"][0]["endDate"]
  bad["work"][0]["summary"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["work"][0]["summary"] = resume_json["work"][0]["summary"]
  bad["work"][0]["highlights"] = []
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["work"][0]["highlights"] = resume_json["work"][0]["highlights"]
  bad["work"][0]["location"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  
def test_required_fields_projects():
  with open("sample.resume.json", encoding="utf8") as f:
      data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["projects"][0]["name"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["projects"][0]["name"] = resume_json["projects"][0]["name"]
  bad["projects"][0]["description"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["projects"][0]["description"] = resume_json["projects"][0]["description"]
  bad["projects"][0]["highlights"] = []
  with pytest.raises(Exception):
        resume.required_fields(bad)
  
def test_required_fields_awards():
  with open("sample.resume.json", encoding="utf8") as f:
      data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["awards"][0]["title"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["awards"][0]["title"] = resume_json["awards"][0]["title"]
  bad["awards"][0]["date"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["awards"][0]["date"] = resume_json["awards"][0]["date"]
  bad["awards"][0]["awarder"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["awards"][0]["awarder"] = resume_json["awards"][0]["awarder"]
  bad["awards"][0]["summary"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  
def test_required_fields_publications():
  with open("sample.resume.json", encoding="utf8") as f:
      data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["publications"][0]["name"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["publications"][0]["name"] = resume_json["publications"][0]["name"]
  bad["publications"][0]["publisher"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["publications"][0]["publisher"] = resume_json["publications"][0]["publisher"]
  bad["publications"][0]["releaseDate"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["publications"][0]["releaseDate"] = resume_json["publications"][0]["releaseDate"]
  bad["publications"][0]["url"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["publications"][0]["url"] = resume_json["publications"][0]["url"]
  bad["publications"][0]["summary"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)

def test_required_fields_volunteer():
  with open("sample.resume.json", encoding="utf8") as f:
      data = f.read()
  resume_json = loads(data)
  resume = Resume(False)
  resume.get_default_theme()
  assert resume.required_fields(resume_json) == True
  bad = deepcopy(resume_json)
  bad["volunteer"][0]["organization"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["volunteer"][0]["organization"] = resume_json["volunteer"][0]["organization"]
  bad["volunteer"][0]["startDate"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["volunteer"][0]["startDate"] = resume_json["volunteer"][0]["startDate"]
  bad["volunteer"][0]["endDate"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["volunteer"][0]["endDate"] = resume_json["volunteer"][0]["endDate"]
  bad["volunteer"][0]["summary"] = ""
  with pytest.raises(Exception):
        resume.required_fields(bad)
  bad["volunteer"][0]["summary"] = resume_json["volunteer"][0]["summary"]
  bad["volunteer"][0]["highlights"] = []
  with pytest.raises(Exception):
        resume.required_fields(bad)