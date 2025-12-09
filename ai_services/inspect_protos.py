import google.generativeai as genai

print("Available attributes in genai.protos:")
for attr in dir(genai.protos):
    if "Search" in attr:
        print(attr)
