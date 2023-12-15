from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize

from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, RadioField, DateField, SelectField
from wtforms.validators import DataRequired, length, equal_to


class AddProductForm(FlaskForm):
    name = StringField("პროდუქტის სახელი", validators=[DataRequired(message="სახელის ველი სავალდებულოა")])
    price = IntegerField("ფასი", validators=[DataRequired()])
    img = FileField("სურათი",
                    validators=[
                        FileRequired(),
                        FileSize(max_size=1024 * 1024 * 20),
                        FileAllowed(["jpg", "png", "jpeg"], message="დაშვებულია მხოლოდ jpg, png და jpeg ფაილები")
                    ])

    submit = SubmitField("დამატება")


class RegisterForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი")
    password = PasswordField("შეიყვანეთ პაროლი", validators=[
        length(min=8, max=64)
    ])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[equal_to("password", message="პაროლები არ ემთხვევა")])
    gender = RadioField("მონიშნეთ სქესი", choices=["ქალი", "კაცი"])
    birthday = DateField("დაბადების თარიღი")
    country = SelectField("მონიშნეთ ქვეყანა", choices=["მონიშნეთ ქვეყანა", "საქართველო", "გერმანია", "ბრიტანეთი"])

    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired(), length(min=8, max=64)])
    submit = SubmitField("ავტორიზაცია")