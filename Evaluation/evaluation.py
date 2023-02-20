import numpy as np


def get_evaluation_data(predictions: list):
    predictions = [(1, 2.3), (2, 3.6), (3, 3.4), (5, 4.5),
                   (7, 4.9), (10, 4.3)]  # (item, prediction)
    # get min and max predictions
    min_pred = min(predictions, key=lambda x: x[1])[1]
    max_pred = max(predictions, key=lambda x: x[1])[1]
    targets = []
    for i in predictions:
        targets.append((i[0], np.random.randint(min_pred, max_pred)))

    # targets =[(1,4),(2,2), (3,3),(5,5),(7,2),(10,4)]# (item, target)
    relevant_threshold = 3  # items with target >= relevant_threshold are considered relevant
    recommended_count = 3

    # sort the predictions by prediction descending
    # this is the recommended list
    predictions.sort(key=lambda x: x[1], reverse=True)

    recommended = [item for item,
                   prediction in predictions[:recommended_count]]
    relevant = [item for item,
                target in targets if target >= relevant_threshold]
    relavant_count = len(relevant)
    return recommended, relevant, relavant_count, recommended_count, predictions

#print("relevant:", relevant)
#print("relavant_count:", relavant_count)
#print("recommended:", recommended)

# calculate the precision at k


def precision_at_k(recommended, relevant, k):
    if len(recommended) > k:
        recommended = recommended[:k]

    precision = 0
    for i in range(len(recommended)):
        if recommended[i] in relevant:
            precision += 1
    precision /= len(recommended)
    return precision
# precision = precision_at_k(recommended, relevant, recommended_count)
# print("precision:", precision)


# calculate the recall at k
def recall_at_k(recommended, relevant, k):
    if len(recommended) > k:
        recommended = recommended[:k]

    recall = 0
    for i in range(len(recommended)):
        if recommended[i] in relevant:
            recall += 1
    recall /= len(relevant)
    return recall
# recall = recall_at_k(recommended, relevant, recommended_count)
# print("recall:", recall)


# calculate the F1 score
def f1_metric(precision, recall):
    return 2 * precision * recall / (precision + recall)

# calculate the average precision @ k
# average precision is the average of the precision at each relevant item


def apk(recommended, relevant, k, predictions):
    recommended = [item for item, prediction in predictions]
    if len(recommended) > k:
        recommended = recommended[:k]
    score = 0.0
    num_hits = 0.0
    for i, p in enumerate(recommended):
        if p in relevant and p not in recommended[:i]:
            num_hits += 1.0  # if the item is relevant and not already counted
            score += num_hits / (i+1.0)  # this is the precision at k
            #print("score:", score, "num_hits:", num_hits, "i:", i)
    if not relevant:
        return 0.0
    return score / min(len(relevant), k)


# #print("recommended:", recommended)
# print("average precision:", apk(recommended, relevant, recommended_count))

# mapk takes a list of recommended lists and a list of relevant lists

def mapk(recommended, relevant, k):
    return np.mean([apk(r, rel, k) for r, rel in zip(recommended, relevant)])

# print("mapk:", mapk([recommended], [relevant], recommended_count))

# calcualate the mean reciprocal rank
# the reciprocal rank of a recommended item is the rank of the first relevant item in the recommended list
# the mean reciprocal rank is the average of the reciprocal rank of all the relevant items


def MRR(recommended, relevant):
    reciprocal_ranks = []
    for i in range(len(recommended)):
        if recommended[i] in relevant:
            reciprocal_ranks.append(1/(i+1))
            break
    return np.mean(reciprocal_ranks)


# MRR = MRR(recommended, relevant)
# print("MRR:", MRR)

# calculate MRR for all the users
# recommended is a list of lists of recommended items
# relevant is a list of lists of relevant items


def MRR_all(recommended, relevant):
    reciprocal_ranks = []
    for i in range(len(recommended)):
        for j in range(len(recommended[i])):
            if recommended[i][j] in relevant[i]:
                reciprocal_ranks.append(1/(j+1))
                break
    return np.mean(reciprocal_ranks)


def get_metrics(recommended, relevant, relavant_count, recommended_count, predictions):
    precision = precision_at_k(recommended, relevant, recommended_count)
    recall = recall_at_k(recommended, relevant, recommended_count)
    f1 = f1_metric(precision, recall)
    average_precision = apk(recommended, relevant,
                            recommended_count, predictions)
    mrr = MRR(recommended, relevant)
    return precision, recall, f1, average_precision, mrr
