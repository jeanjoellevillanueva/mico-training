# Email must not be empty (line 11,12)
# Email must contain a '.' and '@' (line 15 to 17)
# Email must contain exactly one '@' symbol
# Email must end with '.com', '.org' or '.net'
# Email must not longer than 254 characters
# Email must start and end with a letter or digit

email = "micoagapito28@gmail.com"
# Clean the String
# we use strip() - removes leadnig and trailing whitespaces from a string
email = email.strip()
# Email must not be empty
if email == "":
    print("Email cannot be empty.")
# Email must contain a '.' and '@'
elif not('.' in email and '@' in email):
    print("Email must contain '.' and '@'")
# Email must contain exactly one '@' symbol
elif  email.count('@') != 1:
    print("Email must contain exactly one @.")
# Email must end with '.com', '.org' or '.net'
elif not email.endswith(('.org', '.com', '.net')):
    print('Email must end with .com, .org or .net')
# Email must not longer than 254 characters
elif len(email) > 254:
    print("Email must not longer than 254 characters")
# Email must start and end with a letter or digit
elif not (email[0].isalnum() and email[-1].isalnum()):
    print("Email must start and end with a letter or digit")
else:
    print("Email is valid.")