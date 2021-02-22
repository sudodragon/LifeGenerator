def sort_data(data, number_of_toys):
    # sort by uniq_id
    filtered_data = sorter(data, 'uniq_id')

    # sort by number_of_reviews from most to least
    filtered_data = sorter(data, 'number_of_reviews')[::-1]

    # top X*10
    filtered_data = filtered_data[:number_of_toys*10]

    # sort the top X*10 by uniq_id
    filtered_data = sorter(filtered_data, 'uniq_id')

    # sort the top X*10 by average_review_rating from highest to lowest
    filtered_data = sorter(filtered_data, 'average_review_rating')[::-1]

    return filtered_data[:number_of_toys] # top X toys sorted


def sorter(data, filter_by):
    return sorted(data, key=lambda i: i[filter_by])
