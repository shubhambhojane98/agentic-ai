import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text="Hey There!My name is Shubham"
tokens =  enc.encode(text)

# Tokens [25216, 3274, 0, 5444, 1308, 382, 1955, 431, 6595]
print("Tokens", tokens)

decode = enc.decode([25216, 3274, 0, 5444, 1308, 382, 1955, 431, 6595])

print("DeToken",decode)