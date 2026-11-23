from fastapi import FastAPI
import json
from fastapi import HTTPException,Path,Query
app=FastAPI()


# json data load function
def get_data():
    with open("student.json","r") as file:
        return json.load(file)


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
    


