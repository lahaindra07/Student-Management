from pydantic import BaseModel,Field,EmailStr

# pydantic model 
class student(BaseModel):
    name:str
    age:int
    marks:int

s=student(name="indra",age=21,marks=98)
# print(s.age,s.name,s.marks)



# pydantic model with FIELD RULES
class ruleStudent(BaseModel):
    name:str=Field(...,min_length=3,max_length=25)
    age:int=Field(...,gt=0,lt=100)
    marks:int=Field(...,gt=0,lt=100)
    course:str="Data Science"
    phone:str  | None=None
    email:EmailStr

new_s=ruleStudent(name="nil",age=20,marks=11,email="nil@hotmail.com")
# print(new_s.name,new_s.marks,new_s.age,new_s.phone,new_s.course,new_s.email)


# FIELD VALIDATORS








