from profanity_check import predict, predict_prob

# Check if a word or sentence contains profanity
words = ["hello", "エロ", "this is explicit", "nice day"]

# Returns a list of 0 (not profane) or 1 (profane)
profanity_results = predict(words)

# Returns a list of probabilities for being profane
profanity_probabilities = predict_prob(words)

# Output results
for word, result, probability in zip(words, profanity_results, profanity_probabilities):
    print(f"'{word}' -> Profane: {bool(result)}, Probability: {probability:.2f}")
