def combineScores(CFScore,SAScore):
    # Combine the scores of the two algorithms
    # Input: CFScore: a dictionary of book and its score from CF algorithm
    #        SAScore: a dictionary of book and its score from SA algorithm
    # Output: a dictionary of book and its score from the combined algorithm
    bookScore={}

    for book in CFScore.keys():
        bookScore[book]=(CFScore[book]+SAScore[book]*10)
    return bookScore