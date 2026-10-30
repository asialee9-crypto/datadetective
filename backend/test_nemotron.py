from services.nemotron import ask_nemotron

print("Connecting to NVIDIA Nemotron...")

response = ask_nemotron(
    "Hello! I'm building DataDetective, "
    "an AI data science application. "
    "Explain in two sentences how you can "
    "help analyze datasets."
)

print("\nNVIDIA Nemotron Response:")
print(response)

print("\n------------------------------")
print("TEST 2: Classification vs Regression")
print("------------------------------")

result = ask_nemotron(
    "Explain the difference between classification and regression."
)

print(result)