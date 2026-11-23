from pydantic import BaseModel,Field,EmailStr,field_validator,computed_field

# FIELD VALIDATORS --------> Final BaseModel
class dataStudent(BaseModel):
    id:str=Field(...,examples="S001")
    name:str=Field(...,min_length=3,max_length=25)
    age:int=Field(...,gt=0,lt=100)
    marks:int=Field(...,gt=0,lt=100)
    course:str=Field(...,max_length=30)
    email:EmailStr
    phone:str |None=None

    @field_validator("name")
    @classmethod
    def name_check(cls,value):
        if not value.replace(" ","").isalpha():
            raise ValueError("Name must be in alphabate character")
        return value.title()

    # computed field using pydantic
    @computed_field(return_type=str)
    @property
    def student_marks(self)->str:
        if self.marks >=90:
            return "A+"
        elif self.marks >=80:
            return "A"

s_data=dataStudent(id="S001",name="indranil laha",age=20,marks=88,course="Data Science",email="nil@hotmail.com")
# model dump ....covert object to dict
data=s_data.model_dump()
print(data)







