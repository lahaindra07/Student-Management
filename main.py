from fastapi import FastAPI
import json
from fastapi import HTTPException,Path,Query
from pydantic import BaseModel,Field,EmailStr,field_validator,computed_field
app=FastAPI()


# json data load function
def get_data():
    with open("student.json","r") as file:
        return json.load(file)


# to update data in db 
def save_data(data):
    with open("student.json","w") as file:
        json.dump(data,file,indent=4)


# to show all student data
@app.get('/student')
def myData():
    data = get_data()
    return data

# students data display using customized PATH parameters
@app.get('/student/{id}')
def display_usingPath(id:str = Path(...,description="The student id is nessasry",example="S001")):
    data=get_data()
    if id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student not found in this id {id}"

        )
    return data[id] 

# students data display using customized Query parameters
@app.get('/students')
def display_usingQuery(course:str=Query(None,description="Show students data only in this course",example="Python")):
    data=get_data()
    if course is None:
        return data
    filtered={}
    for student_id , info in data.items():
        if info["course"].lower()==course.lower():
            filtered[student_id]=info
    return filtered

SORT_FEILD=['age','marks','name']
SORT_ORDER=['asc','dsc']

@app.get('/sort')
def sort(sort_by:str=Query(None),order:str=Query("asc")):
    if sort_by not in SORT_FEILD:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid sort_by {sort_by} ,choose from {SORT_FEILD}"
        )

    if order not in SORT_ORDER:
        raise HTTPException(
                status_code=404,
                detail=f"Invalid order {order} ,choose from {SORT_ORDER}"
        )

    data = get_data()
    student=[]
    for student_id,info in data.items():
        info["id"]=student_id
        student.append(info)

    reverse=(order=="dsc") 
    sorted_student=sorted(student,key =lambda s:s[sort_by],reverse=reverse)
    return sorted_student
    


# POST route
class dataStudent(BaseModel):
        id:str=Field(...,examples="S001")
        name:str=Field(...,min_length=3,max_length=25)
        age:int=Field(...,gt=0,lt=100)
        course:str=Field(...,max_length=30)
        marks:int=Field(...,gt=0,lt=100)
        email:EmailStr
        

        @field_validator("name")
        @classmethod
        def name_check(cls,value):
            if not value.replace(" ","").isalpha():
                raise ValueError("Name must be in alphabate character")
            return value.title()

    # computed field using pydantic
        @computed_field()
        @property
        def student_marks(self)->str:
            if self.marks >=90:
                return "A+"
            elif self.marks >=80:
                return "A"
            elif self.marks >=70:
                return "B+"
            elif self.marks >=60:
                return "B"

@app.post('/create',status_code=201)
def create_data(student:dataStudent):
    data=get_data()
    data[student.id]=student.model_dump(exclude={"id","student_marks"})
    save_data(data)
    return {
        'message':'created',
        'student':student
    }


# PUT route
class StudentUpdate(BaseModel):
    id:str|None=Field(...,examples="S001")
    name:str|None=Field(...,min_length=3,max_length=25)
    age:int|None=Field(...,gt=0,lt=100)
    course:str|None=Field(...,max_length=30)
    marks:int|None=Field(...,gt=0,lt=100)
    email:EmailStr|None=None



@app.put('/update/{stu_id}')
def data_update(studentupdate:StudentUpdate,stu_id:str=Path(...,description="THE ID OF THE STUDENT",example="S001")):
    data=get_data()
    if stu_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"student with {id} does not exists in data"
        )
    exisiting=data[stu_id]
    update=studentupdate.model_dump()
    for key,values in update.items():
        exisiting[key]=values
    student=dataStudent(id=stu_id,**exisiting)
    data[stu_id]=student.model_dump(exclude={"id","student_marks"})
    save_data(data)
    return {
        'message':'data update successfuly..',
        'student':student
    }