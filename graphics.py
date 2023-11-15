HighScore = open("HighScore", "w")
score = 14
HighScore.write(str(score))
HighScore.close()
HighScore = open("HighScore", "r")
print(HighScore.read())
HighScore.close()