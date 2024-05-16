import os
from openai import OpenAI 

client = OpenAI(api_key='Here is where the API KEY goes')

class User:
    def __init__(self, age, sex, height, weight, bulking, cutting):
        self.age = age
        self.sex = sex
        self.height = height
        self.weight = weight
        self.bulking = bulking
        self.cutting = cutting

    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

class AI_Nutritionist:
    def __init__(self, user, language):
        self.user = user
        self.language = language
        
    def recommend_diet(self):
        bmi = self.user.calculate_bmi()
        if self.language == "en":
            message = f"The user's BMI is {bmi}. His Age - {self.user.age}, Sex - {self.user.sex}, Height - {self.user.height}, Weight - {self.user.weight}, Bulking - {self.user.bulking}, Cutting - {self.user.cutting}. Please provide a detailed diet plan for each day of the week with specific meals and their caloric content, Give a Breakfast, a Snack, a Lunch, another snack, and Dinner. Add the total calories per day."
        else:
            message = f"El IMC del usuario es {bmi}. Su Edad - {self.user.age}, Sexo - {self.user.sex}, Altura - {self.user.height}, Peso - {self.user.weight}, Volumen - {self.user.bulking}, Definición - {self.user.cutting}. Por favor, proporciona un plan de dieta detallado para cada día de la semana con comidas específicas y su contenido calórico. Proporciona un Desayuno, un Snack, una comida, otro snack, y Cena. Agrega las calorias totales por día."
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
        )      
        diet_recommendation = None
        if chat_completion.choices:
            diet_recommendation = chat_completion.choices[0].message.content
        return diet_recommendation
    def recommend_workout(self):
        if self.language == "en":
            message = f"The user, with age {self.user.age}, sex {self.user.sex}, height {self.user.height}m, weight {self.user.weight}kg, is currently {'bulking' if self.user.bulking else 'cutting'}. They are looking for a detailed weekly gym routine. Could you provide a suitable workout plan?"
        else:
            message = f"El usuario, con edad {self.user.age}, sexo {self.user.sex}, altura {self.user.height}m, peso {self.user.weight}kg, actualmente está {'en volumen' if self.user.bulking else 'en definición'}. Está buscando una rutina de gimnasio semanal detallada. ¿Podrías proporcionar un plan de entrenamiento adecuado?"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        model="gpt-3.5-turbo",
        )          
        workout_recommendation = None
        if chat_completion.choices:
            workout_recommendation = chat_completion.choices[0].message.content
        return workout_recommendation

translations = {
    "en": {
        "enter_age": "Please enter your age: ",
        "enter_sex": "Please enter your sex (Masculine/Femenine): ",
        "enter_height": "Please enter your height in meters: ",
        "enter_weight": "Please enter your weight in kg: ",
        "bulking": "Are you bulking? (true/false): ",
        "cutting": "Are you cutting? (true/false): ",
        "workout_routine": "Do you want a weekly gym routine? (true/false): "
    },
    "es": {
        "enter_age": "Por favor, introduce tu edad: ",
        "enter_sex": "Por favor, introduce tu sexo (Masculino/Femenino): ",
        "enter_height": "Por favor, introduce tu altura en metros: ",
        "enter_weight": "Por favor, introduce tu peso en kg: ",
        "bulking": "¿Estás en volumen? (verdadero/falso): ",
        "cutting": "¿Estás en definición? (verdadero/falso): ",
        "workout_routine": "¿Quieres una rutina de gimnasio semanal? (verdadero/falso): "
    }
}

# Ask the user which language they prefer
language = input("Please enter your preferred language (en/es): ")

def get_boolean_input(prompt):
    while True:
        response = input(prompt).lower()
        if response in ['true', 'verdadero']:
            return True
        elif response in ['false', 'falso']:
            return False
        else:
            print("Invalid input. Please enter 'true'/'verdadero' or 'false'/'falso'.")

# Ask the user for their information
age = int(input(translations[language]["enter_age"]))
sex = input(translations[language]["enter_sex"])
height = float(input(translations[language]["enter_height"]))
weight = float(input(translations[language]["enter_weight"]))
bulking= input(translations[language]["bulking"])
cutting = input(translations[language]["cutting"])

# Create a user with the provided information
user = User(age=age, sex=sex, height=height, weight=weight, bulking=bulking, cutting=cutting)

# Print the diet recommendation
ai_nutritionist = AI_Nutritionist(user, language)
print(ai_nutritionist.recommend_diet())

workout_routine_response = get_boolean_input(translations[language]["workout_routine"])
if workout_routine_response:
    print(ai_nutritionist.recommend_workout())