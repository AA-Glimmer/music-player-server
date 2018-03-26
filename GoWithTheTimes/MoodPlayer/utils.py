import math


def find_standard_error(vector):
    mean = sum(vector) / len(vector)
    result = math.sqrt(sum([(e - mean) ** 2 for e in vector]) / len(vector))
    return result


def find_consine_distance(vector_l, vector_r):
    if len(vector_l) != len(vector_r):
        print("vector_l and vector_r should have same dimension")
        raise Exception
    numerator = sum([vector_l[i] * vector_r[i] for i in range(len(vector_l))])
    denominator = math.sqrt(sum([e ** 2 for e in vector_l])) * math.sqrt(sum([e ** 2 for e in vector_r]))
    result = numerator / denominator
    # Opps! forget I could
    # from scipy import spatial
    # result = 1 - spatial.distance.cosine(vector_l, vector_r)
    return result
