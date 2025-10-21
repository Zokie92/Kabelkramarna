
# Hej Johan! här kommmer min uppgift.
# Jag måste erkänna att denna uppgift var svår och jag är inte 100% med att alla begrepp ännu, men jag fortsätter jobba på det dagligen.
# // Mattias Englund //

# Introduktion.
print("Good day\nMy name is Mattias\nI'm here to calculate everything by two, try me!!! ")
print("Type 'end' or 'exit' to stop the program.\n")

# En while-loop som körs för alltid tills vi använder 'break' som avslutar loopen (nämns även nedan)
while True:
    # Tar in text (input) från användaren, alltså det användaren skriver in.
    user = input("Enter a number:  ")

    # En if som kollar om användaren vill avsluta programmet med 'end' eller 'exit'. 
    if user.lower() in ["end", "exit"]:
        print("Goodbye And thank you for playing with me, see you later!")
        break  # Avslutar loopen 

    # Try: används för att fånga upp fel.
    try:
        # omvandla tal med decimaler.
        number = float(user)

        # En for loop som körs 1 gång
        for i in range(1):
            # Multiplicerar användarens tal med 2
            result = number * 2
            # Skriver ut resultatet med hjälp av en f-sträng
            print(f"Your number {number} multiplied by 2 is {result}\n")

    # Om användaren skrev något som inte går att göra till ett tal
    except ValueError:
        print("Enter a valid number, please!")

    # Else körs bara om allt i try-blocket lyckades (dvs. ingen ValueError uppstod)
    else:
        print("That worked just fine!")

