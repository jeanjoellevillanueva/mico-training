# Must not be empty
# Must be at least 8 characters
# Must include at least 1 uppercase
# Must include at least 1 lowercase
# Must not be same as the email
# Must not contain any spaces
# Must start and end with a letter or digit

email = "mico.agapito28@gmail.com"
password = "Agapito222"
email = email.strip()
password = password.strip()

if email == "" and password == "":
    print("Email and Password must not empty")
# Must not be at least 8 characters
elif not (len(email) >= 8 and len(password) >= 8):
    print("Email and Password must be at least 8 characters")
# Must include at least 1 uppercase
elif not any(char.isupper() for char in email and password):
    print("Must include at least 1 uppercase")
 # Must include at least 1 lowercase
elif not any(char.islower() for char in email and password):
    print("Must include at least 1 lowercase")
# Must not be asame as the email
elif not (email != password):
    print("Must not be asame as the email")
# Must not contain any spaces
elif any(char.isspace() for char in email):
    print("Must not contain any spaces")
# Must start and end with a letter or digit
elif not (email[0].isalnum() and email[-1].isalnum()):
    print("Email must start and end with a letter or digit")

elif not (password[0].isalnum() and password[-1].isalnum()):
    print("Password must start and end with a letter or digit")  

else:
    print("Email and Password is accepted")