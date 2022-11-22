from io import BytesIO
from json import loads

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfdoc
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Frame, PageTemplate
from reportlab.platypus.flowables import Spacer

import os.path

class Resume:
    
    # Set the page height and width
    height = 0 #11 * inch
    width = 8.5 * inch
    resume_json = {}
    theme = {}
    web = True
    required = None
    page = None
    # Set our styles
    styles = None 
                                

    def register_fonts(self):
        # register fonts to be used throughout the document.
        registerFont(TTFont(self.theme["fonts"]["fontName"], os.path.join(os.path.dirname(__file__), self.theme["fonts"]["font"])))
        registerFont(TTFont(self.theme["fonts"]["fontBoldName"], os.path.join(os.path.dirname(__file__), self.theme["fonts"]["fontBold"])))
        registerFontFamily(self.theme["fonts"]["fontName"], normal= self.theme["fonts"]["fontName"] , bold=self.theme["fonts"]["fontBoldName"])
        
    def generate_pdf(self, data, contact):
        pdfname = 'resume.pdf'
        buffer = BytesIO() if self.web else None
        doc = SimpleDocTemplate(
            buffer if self.web else pdfname,
            pagesize = letter,
            bottomMargin = self.theme["page"]["margin"][0] * inch,
            topMargin= self.theme["page"]["margin"][1] * inch,
            rightMargin= self.theme["page"]["margin"][2] * inch,
            leftMargin= self.theme["page"]["margin"][3] * inch)  # set the doc template
        style = self.styles[self.theme["page"]["styles"]]  # set the style to normal
        if self.theme["multiCol"]:
            frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
            frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')
            doc.addPageTemplates([PageTemplate(id='TwoCol', onPage=self.myPageWrapper(contact), frames=[frame1,frame2])]) 
        story = []  # create a blank story to tell
        contentTable = Table(
             data,
             colWidths=[
                 self.theme["tableStyles"]["colWidths"][0] * inch,
                 self.theme["tableStyles"]["colWidths"][1] * inch])
        tblStyle = TableStyle([ # sents font and colours used within the table (left side is titles right side is content)
              ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor(self.theme["fonts"]["fontColor"])),
              ('FONT', (0, 0), (-1, -1), self.theme["fonts"]["fontName"]),
              ('FONTSIZE', (0, 0), (-1, -1), self.theme["fonts"]["fontSize"]),
              ('VALIGN', (0, 0), (-1, -1), self.theme["tableStyles"]["valign"]),
              ('ALIGN', (0, 0), (-1, -1), self.theme["tableStyles"]["align"])])
        contentTable.setStyle(tblStyle)
        story.append(contentTable)
        doc.build(
            story,
            onFirstPage=self.myPageWrapper(
                contact),
            )
        if self.web:
            pdf = buffer.getvalue()
            buffer.close()
        return pdf if self.web else pdfname

    """
        Draw the framework for the first page,
        pass in contact info as a dictionary
    """
    def myPageWrapper(self, contact):
        # template for static, non-flowables, on the first page
        # draws all of the contact information at the top of the page
        #myPage changes depending on the theme, The font also changes depending on theme, most of the setfonts evaluate to None
        def myPage(canvas, doc):
            canvas.saveState()  # save the current state
            canvas.setFont(self.theme["fonts"]["fontName"], self.theme["fonts"]["fontSize"])
            canvas.setFont(self.theme["fonts"]["fontBoldName"], self.theme["fonts"]["titleFontSize"])  if self.theme["headTitle"]["leftTop"] else None
            canvas.drawString(
                self.theme["headAln"]["leftTop"][0] * inch,
                self.height - (self.theme["headAln"]["leftTop"][1] * inch),
                contact[self.theme["head"]["leftTop"]])  if self.theme["head"]["leftTop"]  else None
            canvas.setFont(self.theme["fonts"]["fontName"], self.theme["fonts"]["fontSize"]) if self.theme["headTitle"]["leftTop"] else None 
            canvas.setFont(self.theme["fonts"]["fontBoldName"], self.theme["fonts"]["titleFontSize"])  if self.theme["headTitle"]["rightTop"] else None
            canvas.drawRightString(
                self.width - (self.theme["headAln"]["rightTop"][0] * inch),
                self.height - (self.theme["headAln"]["rightTop"][1] * inch),
                contact[self.theme["head"]["rightTop"]]) if self.theme["head"]["rightTop"] else None  
            canvas.setFont(self.theme["fonts"]["fontName"], self.theme["fonts"]["fontSize"]) if self.theme["headTitle"]["rightTop"] else None 
            canvas.line(self.theme["headLine"][0] * inch, self.height - (self.theme["headLine"][1] * inch), 
                self.width - (self.theme["headLine"][2] * inch), self.height - (self.theme["headLine"][3] * inch))
            canvas.setFont(self.theme["fonts"]["fontBoldName"], self.theme["fonts"]["titleFontSize"])  if self.theme["headTitle"]["leftBot"] else None
            canvas.drawString(
                self.theme["headAln"]["leftBot"][0] * inch,
                self.height - (self.theme["headAln"]["leftBot"][1] * inch),
                contact[self.theme["head"]["leftBot"]]) if self.theme["head"]["leftBot"] else None
            canvas.setFont(self.theme["fonts"]["fontName"], self.theme["fonts"]["fontSize"]) if self.theme["headTitle"]["leftBot"] else None 
            canvas.setFont(self.theme["fonts"]["fontBoldName"], self.theme["fonts"]["titleFontSize"])  if self.theme["headTitle"]["centerBot"] else None 
            canvas.drawCentredString(
                self.width / self.theme["headAln"]["centerBot"][0],
                self.height - (self.theme["headAln"]["centerBot"][1] * inch),
                contact[self.theme["head"]["centerBot"]]) if self.theme["head"]["centerBot"] else None
            canvas.setFont(self.theme["fonts"]["fontName"], self.theme["fonts"]["fontSize"]) if self.theme["headTitle"]["centerBot"] else None 
            canvas.setFont(self.theme["fonts"]["fontBoldName"], self.theme["fonts"]["titleFontSize"])  if self.theme["headTitle"]["rightBot"] else None 
            canvas.drawRightString(
                self.width - (self.theme["headAln"]["rightBot"][0] * inch),
                self.height - (self.theme["headAln"]["rightBot"][1] * inch),
                contact[self.theme["head"]["rightBot"]]) if self.theme["head"]["rightBot"] else None
            canvas.setFont(self.theme["fonts"]["fontName"], self.theme["fonts"]["fontSize"]) if self.theme["headTitle"]["rightBot"] else None 
            
            canvas.setFont(self.theme["fonts"]["fontBoldName"], self.theme["fonts"]["titleFontSize"])  if self.theme["headTitle"]["centerTop"] else None 
            canvas.drawCentredString(
                self.width / self.theme["headAln"]["centerTop"][0],
                self.height - (self.theme["headAln"]["centerTop"][1] * inch),
                contact[self.theme["head"]["centerTop"]]) if self.theme["head"]["centerTop"] else None
            canvas.setFont(self.theme["fonts"]["fontName"], self.theme["fonts"]["fontSize"]) if self.theme["headTitle"]["centerTop"] else None 
            # restore the state to what it was when saved
            canvas.restoreState()
        return myPage
        

    def process_education(self, resume_json):
        """Summary: Process the education section of the resume json

        Args:
            resume_json (json): The resume json

        Returns:
            list: A list of education objects
        """
        education_list = []    
        for item in resume_json["education"]:
            education_list.append("<b>"+item["institution"]+"</b>")
            education_list.append("<b>" + item["studyType"]+"</b> "+item["area"])
            education_list.append("<b>Dates: </b>" + item["startDate"] + " through " + item["endDate"])
            
            if "score" in item.keys() and item["score"] != "": #or check if empty string
                education_list.append("<b>GPA:</b> "+item["score"])
                
        return education_list

    def process_skills(self, resume_json):
        """Summary: Process the skills section of the resume json

        Args:
            resume_json (json): the resume json

        Returns:
            list: A list of skills objects
        """
        skill_list = []
        for item in resume_json["skills"]: 
            skill_list.append("<b>"+item["name"]+"</b>"+": "+", ".join(item["keywords"]))
            
        return skill_list

    def process_projects(self, resume_json):
        """Summary: Process the projects section of the resume json

        Args:
            resume_json (json): the resume json

        Returns:
            list: A list of projects objects
        """
        projects_list = []
        for item in resume_json["projects"]: 
            projects = []
            projects.append("<b>"+item["name"]+"</b>"+": "+item["description"]+ " - "+"<b>"+item["endDate"]+"</b>")
            projects.append(item["url"])  
            projects.append("<b>"+"Techonology Used"+"</b>"+": "+", ".join(item["keywords"]))
            projects.append("<b>Highlights: </b><br/>- "+"<br/>- ".join(item["highlights"]))
            
            projects_list.append("<br/>".join(projects))
            
        return projects_list

    def process_work_experience(self, resume_json):
        """Summary: Process the work experience section of the resume json

        Args:
            resume_json (json): the resume json

        Returns:
            list: A list of work experience objects
        """
        experience_list = []
        for item in resume_json["work"]: 
            work = []
            work.append("<b>"+item["name"]+"</b>"+":" + " - "+item["location"])
            work.append("<b>"+item["position"]+"</b>"+": "+item["startDate"]+" through "+item["endDate"])
            work.append(item["summary"])
            if item["highlights"] != [""]:
                work.append("<b>Highlights: </b><br/>- "+"<br/>- ".join(item["highlights"]))
            experience_list.append("<br/>".join(work))           
        return experience_list
    
    def process_vol_experience(self, resume_json):
        """Summary: Process the volunteer experience section of the resume json

        Args:
            resume_json (json): the resume json

        Returns:
            list: A list of volunteer experience objects
        """
        experience_list = []
        for item in resume_json["volunteer"]: 
            vol = []
            vol.append("<b>"+item["organization"]+"</b> "+item["startDate"]+" through "+item["endDate"])
            vol.append(item["summary"])
            if item["highlights"] != [""]:
                vol.append("<b>Highlights: </b><br/>- "+"<br/>- ".join(item["highlights"]))
            experience_list.append("<br/>".join(vol))           
        return experience_list

    def process_awards(self, resume_json):
        """summary: Process the awards section of the resume json

        Args:
            resume_json (json): the resume json

        Returns:
            list: A list of awards objects
        """
        awards_list = []
        for item in resume_json["awards"]:
            award = [] 
            award.append("<b>"+item["title"]+"</b>")
            award.append("Awarded by: "+item["awarder"]+" - "+item["date"])
            award.append(item["summary"])
            awards_list.append("<br/>".join(award))
        return awards_list
    
    def process_publications(self, resume_json):
        """summary: Process the publications section of the resume json

        Args:
            resume_json (json): the resume json

        Returns:
            list: A list of publications objects
        """
        publications_list = []
        for item in resume_json["publications"]:
            publication = [] 
            publication.append("<b>"+item["name"]+"</b>")
            publication.append(item["publisher"]+" - "+item["releaseDate"])
            publication.append(item["url"])
            publication.append(item["summary"])
            publications_list.append("<br/>".join(publication))
        return publications_list
    
    # THIS ISNT MUCH BETTER
    # NESTED MESS
    def required_fields(self, resume_json):
        if not self.required_fields_worker(resume_json):
            raise Exception("Required fields cannot be empty! Please check the resume.json file and fix")
        return True
    
    def required_fields_worker(self, resume_json) -> bool:
        """summary: Check if the required fields are empty

        Args:
            resume_json (json): the resume json

        Returns:
            bool: True if all required fields are not empty, False otherwise
        """
        for field in self.required.keys():
            if self.required[field]["required"] == "True" and field not in resume_json.keys():
                return False
            if field not in resume_json.keys(): # if the field is not in the resume json and is not required we skip it
                continue
            if self.required[field]["required"] == "True" or len(resume_json[field]) > 0:
                if type(resume_json[field]) == list and len(resume_json[field]) == 0:
                    return False
                elif type(resume_json[field]) == dict:
                    for item in self.required[field]["fields"]:
                        if item not in resume_json[field].keys():
                            continue
                        if type(resume_json[field][item]) == dict:
                            for subitem in self.required[field][item]['fields']: #loop for subfields like profiles
                                if resume_json[field][item][subitem] == "":
                                    return False
                        elif resume_json[field][item] == "":
                            return False
                elif type(resume_json[field]) == list:
                    for i in range(len(resume_json[field])):
                        for item in self.required[field]["fields"]:
                            if type(resume_json[field][i][item]) == list and len(resume_json[field][i][item]) == 0:
                                return False
                            elif resume_json[field][i][item] == "":
                                return False
        return True
    
    def one_page(self, resume_json):
        if len(resume_json["basics"]["summary"]) > 650:
            raise Exception("Summary is too long! Please shorten it to make it fit on one page")
        if len(resume_json["education"]) > 2:
            raise Exception("Too many education entries! Please shorten it to 2 or less to make it fit on one page")
        if len(resume_json["skills"]) > 2:
            raise Exception("You have more than two skills entries! Please remove all but two to make it fit on one page")
        if len(resume_json["work"]) > 2:
            raise Exception("You have more than two work entries! Please remove all but two to make it fit on one page")
        else:
            if len(resume_json["work"]) <= 2:
                for i in range(len(resume_json["work"])):
                    if len(resume_json["work"][i]["summary"]) > 250:
                        raise Exception("Work summary is too long! Please shorten it to make it fit on one page")
                    if len(resume_json["work"][i]["highlights"]) > 2:
                        raise Exception("You have more than two work highlights! Please remove all but two to make it fit on one page")
                    else:
                        if len(resume_json["work"][i]["highlights"]) <= 2:
                            for j in range(len(resume_json["work"][i]["highlights"])):
                                if len(resume_json["work"][i]["highlights"][j]) > 100:
                                    raise Exception("Work highlight is too long! Please shorten it to make it fit on one page")
        if len(resume_json["projects"]) > 2:
            raise Exception("You have more than two projects entries! Please remove all but two to make it fit on one page")
        else:
            if len(resume_json["projects"]) <= 2:
                for i in range(len(resume_json["projects"])):
                    if len(resume_json["projects"][i]["description"]) > 90:
                        raise Exception("Project description is too long! Please shorten it to make it fit on one page")
                    if len(resume_json["projects"][i]["highlights"]) > 2:
                        raise Exception("You have more than two project highlights! Please remove all but two to make it fit on one page")
                    else:
                        if len(resume_json["projects"][i]["highlights"]) <= 2:
                            for j in range(len(resume_json["projects"][i]["highlights"])):
                                if len(resume_json["projects"][i]["highlights"][j]) > 100:
                                    raise Exception("Project highlight is too long! Please shorten it to make it fit on one page")
        if len(resume_json["volunteer"]) > 1:
            raise Exception("You have more than one volunteer entries! Please remove all but one to make it fit on one page")
        else:
            for i in range(len(resume_json["volunteer"])):
                if len(resume_json["volunteer"][i]["summary"]) > 100:
                    raise Exception("Volunteer summary is too long! Please shorten it to make it fit on one page")
        if len(resume_json["awards"]) > 1:
            raise Exception("You have more than one awards entries! Please remove all but one to make it fit on one page")
        else:
            for i in range(len(resume_json["awards"])):
                if len(resume_json["awards"][i]["summary"]) > 100:
                    raise Exception("Awards summary is too long! Please shorten it to make it fit on one page")   
        if len(resume_json["publications"]) > 1:
            raise Exception("You have more than one publications entries! Please remove all but one to make it fit on one page")
        else:
            for i in range(len(resume_json["publications"])): 
                if len(resume_json["publications"][i]["summary"]) > 100:
                    raise Exception("Publications summary is too long! Please shorten it to make it fit on one page")
        return True
    def two_page(self, resume_json):
        if len(resume_json["basics"]["summary"]) > 1300:
            raise Exception("Summary is too long! Please shorten it to make it fit on two page")
        if len(resume_json["education"]) > 3:
            raise Exception("Too many education entries! Please shorten it to 2 or less to make it fit on two page")
        if len(resume_json["skills"]) > 3:
            raise Exception("You have more than two skills entries! Please remove all but two to make it fit on two page")
        if len(resume_json["work"]) > 3:
            raise Exception("You have more than two work entries! Please remove all but two to make it fit on two page")
        else:
            if len(resume_json["work"]) <= 3:
                for i in range(len(resume_json["work"])):
                    if len(resume_json["work"][i]["summary"]) > 250:
                        raise Exception("Work summary is too long! Please shorten it to make it fit on two page")
                    if len(resume_json["work"][i]["highlights"]) > 4:
                        raise Exception("You have more than four work highlights! Please remove all but four to make it fit on two page")
                    else:
                        if len(resume_json["work"][i]["highlights"]) <= 4:
                            for j in range(len(resume_json["work"][i]["highlights"])):
                                if len(resume_json["work"][i]["highlights"][j]) > 100:
                                    raise Exception("Work highlight is too long! Please shorten it to make it fit on two page")
        if len(resume_json["projects"]) > 4:
            raise Exception("You have more than two projects entries! Please remove all but two to make it fit on two page")
        else:
            if len(resume_json["projects"]) <= 4:
                for i in range(len(resume_json["projects"])):
                    if len(resume_json["projects"][i]["description"]) > 90:
                        raise Exception("Project summary is too long! Please shorten it to make it fit on two page")
                    if len(resume_json["projects"][i]["highlights"]) > 4:
                        raise Exception("You have more than four project highlights! Please remove all but four to make it fit on two page")
                    else:
                        if len(resume_json["projects"][i]["highlights"]) <= 4:
                            for j in range(len(resume_json["projects"][i]["highlights"])):
                                if len(resume_json["projects"][i]["highlights"][j]) > 100:
                                    raise Exception("Project highlight is too long! Please shorten it to make it fit on two page")
        if len(resume_json["volunteer"]) > 2:
            raise Exception("You have more than two volunteer entries! Please remove all but two to make it fit on two page")
        else:
            for i in range(len(resume_json["volunteer"])):
                if len(resume_json["volunteer"][i]["summary"]) > 100:
                    raise Exception("Volunteer summary is too long! Please shorten it to make it fit on two page")
        if len(resume_json["awards"]) > 2:
            raise Exception("You have more than two awards entries! Please remove all but two to make it fit on two page")
        else:
            for i in range(len(resume_json["awards"])):
                if len(resume_json["awards"][i]["summary"]) > 100:
                    raise Exception("Awards summary is too long! Please shorten it to make it fit on two page")
        if len(resume_json["publications"]) > 2:
            raise Exception("You have more than two publications entries! Please remove all but two to make it fit on two page")
        else:
            for i in range(len(resume_json["publications"])): 
                if len(resume_json["publications"][i]["summary"]) > 100:
                    raise Exception("Publications summary is too long! Please shorten it to make it fit on two page")
        return True
          
    def generate_resume(self, resume_json):
        self.required_fields(resume_json)
        self.one_page(resume_json) if self.page == 1 else None
        self.two_page(resume_json) if self.page == 2 else None
        order = {}
        contact = {
            'name': resume_json["basics"]["name"],
            'website': resume_json["basics"]["url"], #what assumtions do we want to make a but website? 
            'email': resume_json["basics"]["email"],
            'phone': resume_json["basics"]["phone"]
            }
        contact['address'] = resume_json["basics"]["location"]['city']  + " " + resume_json["basics"]["location"]['region']+", " + resume_json["basics"]["location"]['countryCode']
        contact['information'] = [contact['email'], contact['address'], contact['phone'], contact['website']]
        contact["information"].pop() if contact["website"] == "" else contact["information"]
        contact["information"] = "   -   ".join(contact["information"])
        if contact["website"] == "":
            key = [k for k, v in self.theme["head"].items() if v == 'website'][0]
            self.theme["head"][key] = False
        data = {
            'summary': resume_json["basics"]["summary"]}
        #adds item into data
        data['education'] = '<br/>'.join(self.process_education(resume_json)) 
        data['skills'] = '<br/>'.join(self.process_skills(resume_json)) if "skills" in resume_json.keys() else None
        data['projects'] = self.process_projects(resume_json) if "projects" in resume_json.keys() else None
        data['experience'] = self.process_work_experience(resume_json) if "work" in resume_json.keys() else None
        data['volunteer'] = self.process_vol_experience(resume_json) if "volunteer" in resume_json.keys() else None
        data['awards'] = self.process_awards(resume_json) if "awards" in resume_json.keys() else None
        data['publications'] = self.process_publications(resume_json) if "publications" in resume_json.keys() else None
        #creates table for generatepdf to use to create the pdf
        order["summary"] = ['SUMMARY', Paragraph(data['summary'], self.styles['Content'])] 
        order["education"] = ['EDUCATION', Paragraph(data['education'], self.styles['Content'])] 
        order["skills"] = ['SKILLS', Paragraph(data['skills'], self.styles['Content'])] if "skills" in resume_json.keys() else None
        order["experience"] = ['EXPERIENCE', [Paragraph(x, self.styles['Content']) for x in data['experience']]] if "work" in resume_json.keys() else None
        order["projects"] = ['PROJECTS', [Paragraph(x, self.styles['Content']) for x in data['projects']]] if "projects" in resume_json.keys() else None
        order["volunteer"] = ['VOLUNTEER', [Paragraph(x, self.styles['Content']) for x in data['volunteer']]] if "volunteer" in resume_json.keys() else None
        order["awards"] = ['AWARDS', [Paragraph(x, self.styles['Content']) for x in data['awards']]] if "awards" in resume_json.keys() else None
        order["publications"] = ['PUBLICATIONS', [Paragraph(x, self.styles['Content']) for x in data['publications']]] if "publications" in resume_json.keys() else None
        #orders table based on order in theme.json
        tblData = [order[x] for x in self.theme["ordering"]["body"] if order[x] != None]
        return self.generate_pdf(tblData, contact)

    def apply_theme(self, theme_json):
        #sets up paragraph styles
        self.theme = theme_json
        self.register_fonts()
        self.height = theme_json["page"]["height"] * inch
        self.width = theme_json["page"]["width"] * inch
        self.styles.add(ParagraphStyle(name='Content',
                            fontFamily=self.theme["fonts"]["fontFamily"],
                            fontSize=self.theme["fonts"]["fontSize"],
                            spaceAfter=self.theme["paragraph"]["spaceAfter"]*inch,
                            leftIndent=0,
                            rightIndent=0))

    
    #this is mostly for testing purposes
    def get_default_theme(self):
        dir_name = os.path.join(os.path.dirname(__file__), 'themes')
        file = os.path.join(dir_name, 'default.json')
        with open(file, encoding="utf8") as f:
            data = f.read()
        self.theme = loads(data)
    
    def load_required(self):
        #loads required fields from required.json to be used by required_fields_worker method
        file = "requiredFields.json"
        file = os.path.join(os.path.dirname(__file__), file)
        with open(file, encoding="utf8") as f:
            data = f.read()
        self.required = loads(data)
    
    def set_page(self, num):
        self.page = num
        
    def __init__(self, web=True) -> None:
        self.height = 11 * inch
        self.width = 8.5 * inch
        self.styles = getSampleStyleSheet()
        self.web = web
        self.load_required()
